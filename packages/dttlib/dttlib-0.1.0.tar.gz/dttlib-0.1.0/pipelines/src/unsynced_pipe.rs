//! Thse pipelines do not take every input, but are allowed to drop some inputs
//! If the input stream stops, this pipeline will eventually take the final input
//! Useful for pipelines that take a lot of calculation and don't need to run on every input.
//! Prevents the rest of the pipeline structure from bogging down.
//! 
//! This pipe also takes an optional configuration watch channel to tweak the configuration
//! mid-analysis. 

use std::marker::PhantomData;
use futures::future::BoxFuture;
use tokio::sync::watch::error::RecvError;
use user_messages::UserMsgProvider;
use crate::{ConfigData, PipeData, PipeOut, PipeResult, PipelineBase, PipelineError, PipelineOutput, PipelineWatchReceiver, PipelineSender, PipelineSubscriber, StateData, PIPELINE_SIZE};
use crate::pipe::{PipeSetup, PipeTeardown};
use crate::publisher::{MaybeInitialized, Publisher, Subscriber};

pub trait UnsyncPipe1Generator<I: PipeData, A: PipeOut<I>, T: PipeData, S: StateData, C: ConfigData>: 'static + Sync + Send +
for<'a> Fn(Box<dyn UserMsgProvider>, &'a C,  &'a mut S, A) -> PipeResult<T> {}
impl<I: PipeData, A: PipeOut<I>, T: PipeData, S: StateData, C: ConfigData,
    Z: 'static + Sync + Send + for<'a> Fn(Box<dyn UserMsgProvider>,  &'a C, &'a mut S, A) -> PipeResult<T>>
UnsyncPipe1Generator<I, A, T, S, C> for Z  {}


async fn await_optional_watch<T>(watch: &mut Option<tokio::sync::watch::Receiver<T>>) -> Option<Result<T, RecvError>> 
where
    T: Clone + Send + Sync + 'static,
{
    match watch {
        None => None,
        Some(w) => {
           match w.changed().await {
               Ok(_) => {
                   Some(Ok(w.borrow().clone()))
               },
               Err(e) => Some(Err(e))
           }
        }
    }
}


pub struct UnsyncPipe1<I: PipeData, A: PipeOut<I>, T: PipeData, S: StateData, C: ConfigData, G> 
where
    G: UnsyncPipe1Generator<I, A, T, S, C>
{
    name: String,
    generate: G,
    setup_fn: Option<PipeSetup<S>>,
    teardown_fn: Option<PipeTeardown<S>>,
    config_watch: Option<tokio::sync::watch::Receiver<C>>,
    state: S,
    publisher: PipelineSender<T>,
    phantom_data: PhantomData<I>,
    phantom_data2: PhantomData<A>,
}

impl<I: PipeData, A: PipeOut<I>, T: PipeData, S: StateData, C: ConfigData, G> PipelineBase for UnsyncPipe1<I, A, T, S, C, G>
where
    G: UnsyncPipe1Generator<I, A, T, S, C>
{
    type Output = T;
    
    fn name(&self) -> &str {
        self.name.as_str()
    }
}

enum PipeInputReceived<I: PipeData> {
    Some(PipelineOutput<I>),
    None,
    Close,
}

impl<I: PipeData, A: PipeOut<I>, T: PipeData, S: StateData, C: ConfigData + Default, G>  UnsyncPipe1<I, A, T, S, C, G> 
where
    G: UnsyncPipe1Generator<I, A, T, S, C>
{
    
    async fn read_pipe_input(&mut self, mut config: &mut C, mut input_recv: PipelineWatchReceiver<I>) -> PipeInputReceived<I> {
        tokio::select! {
            c = input_recv.changed() => {
                match c {
                    Ok(_) => {
                        match input_recv.borrow().clone() {
                            MaybeInitialized::Initialized(i) => PipeInputReceived::Some(i),
                            MaybeInitialized::Uninitialized => {
                                PipeInputReceived::None
                            }
                        }
                    },
                    Err(_) => {PipeInputReceived::Close},
                }
            },
            Some(cr) = await_optional_watch(&mut self.config_watch) => {
                match cr {
                    Ok(c) => {
                        *config = c;
                        match input_recv.borrow().clone() {
                            MaybeInitialized::Initialized(i) => PipeInputReceived::Some(i),
                            MaybeInitialized::Uninitialized => {
                                PipeInputReceived::None
                            }
                        }
                    },
                    Err(_) => {
                        PipeInputReceived::Close
                    },
                }
            }
        }
    } 
    
    fn run(mut self, rc: Box<dyn UserMsgProvider>,  mut input_recv: PipelineWatchReceiver<I>) {
        
        let rt = tokio::runtime::Handle::current();
        let rt2 = rt.clone();
        rt2.spawn_blocking( move || {
            if let Err(e) = self.setup() {
                let msg = format!("Aborted unsynchronized pipeline '{}' during setup: {}", self.name(), e);
                rc.user_message_handle().error(msg);
                return;
            }
            let mut config = match &self.config_watch {
                None => C::default(),
                Some(w) => {
                    w.borrow().clone()
                }
            };
            'main: loop {
                
                let input = match rt.block_on(
                    self.read_pipe_input(&mut config, input_recv.clone()))
                {
                    PipeInputReceived::Some(i) => i,
                    PipeInputReceived::Close => break 'main,
                    PipeInputReceived::None => continue 'main,
                };

                #[allow(clippy::needless_borrow)]
                let out_vec = match (self.generate)(rc.ump_clone(), &config, & mut self.state, input.clone().into()) {
                    PipeResult::Output(x) => x,
                    PipeResult::Close => {break 'main},
                };

                for out in out_vec.into_iter() {
                    // handle good input
                    if rt.block_on(self.publisher.send(out)).is_err() {
                        // no more receivers, quit
                        break 'main;
                    }
                }
            }
            self.teardown();
        });
    }


    /// # setup
    /// create a 1-input pipeline
    /// given a generator function, a setup function and teardown function
    pub async fn create (rc: Box< dyn UserMsgProvider>, name: impl Into<String>, generate: G,
                         config_watch: Option<tokio::sync::watch::Receiver<C>>,
                         state: S, setup_fn: Option<PipeSetup<S>>,
                         teardown_fn: Option<PipeTeardown<S>>,
                         input_sub: &PipelineSubscriber<I>) -> Subscriber<PipelineOutput<T>>
    {
        let (publisher, subscriber) = Publisher::create(PIPELINE_SIZE);
        let p = Self {
            name: name.into(),
            generate,
            setup_fn,
            teardown_fn,
            state,
            publisher,
            config_watch,
            phantom_data: PhantomData,
            phantom_data2: PhantomData,
        };
        p.run(rc.ump_clone(), input_sub.unsync_subscribe_or_die(rc).await);
        subscriber
    }

    fn setup(&mut self) -> Result<(), PipelineError> {
        if let Some(setup) =  &self.setup_fn {
            setup(& mut self.state)
        }
        else {
            Ok(())
        }
    }

    fn teardown(&mut self) {
        if let Some(teardown) = &self.teardown_fn {
            teardown(& mut self.state);
        }
    }
}