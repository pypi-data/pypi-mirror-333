//! Handle NDScope style scope views
//! These views take an arbitrary number of channels and functions on those channels as a ViewSet
//! And also a ViewSpan, a time span, and continuously and asynchronously produce time domain results
//! across that time span for the ViewSet

mod pipeline_graph;

use std::collections::HashMap;

use gps_pip::{PipInstant, PipDuration};

use crate::analysis::graph::view_graph_to_pipeline::view_graph_to_pipeline;
use crate::analysis::result::ResultsReceiver;
use crate::data_source::{DataBlockReceiver, DataBlockSender, DataSourceRef};
use crate::errors::DTTError;
use crate::params::channel_params::Channel;
use crate::run_context::RunContext;
use crate::scope_view::pipeline_graph::create_pipeline_graph;
use tokio_util::{
    sync::{
        CancellationToken,
        DropGuard,
    },
};
#[cfg(not(feature = "python"))]
use dtt_macros::staticmethod;

#[cfg(feature = "python")]
use pyo3::{
  pyclass, pymethods
};
use crate::analysis::scope::inline_fft::InlineFFT;
use crate::user::ResponseToUser::ScopeViewResult;

#[derive(Clone)]
#[cfg_attr(feature = "python", pyclass)]
pub (crate) enum SetMember {
    Channel(Channel),
    /// The set has a name but no other channel information
    /// the channel name needs to be resolved into a Channel()
    /// before pipelines can be created. 
    UnresolvedChannelName(String),
    //Function(String, Vec<isize>),
}

#[derive(Clone)]
#[cfg_attr(feature = "python", pyclass)]
pub struct ViewSet {
    members: Vec<SetMember>,
}

impl From<ViewSet> for Vec<Channel> {
    fn from(value: ViewSet) -> Self {
        let mut cvec = Vec::new();
        for m in value.members {
            if let SetMember::Channel(c) =  m {
                cvec.push(c)
            }
        }
        cvec
    }
}


impl From<Vec<Channel>> for ViewSet {
    fn from(value: Vec<Channel>) -> Self {
        Self {
            members: value.into_iter().map(|c| { SetMember::Channel(c) }).collect()
        }
    }
}


impl From<Vec<String>> for ViewSet {
    fn from(value: Vec<String>) -> Self {
        Self {
            members: value.into_iter().map(|c| { SetMember::UnresolvedChannelName(c) }).collect()
        }
    }
}

#[cfg_attr(feature = "python", pymethods)]
impl ViewSet {

    /// convenience function
    /// for turning a simple list of channels into a ViewSet
    #[staticmethod]
    pub fn from_channels(channels: Vec<Channel>) -> Self {
        channels.into()
    }

    /// convenience function
    /// for turning a simple list of channel names into a ViewSet with
    /// unresolved channel names
    #[staticmethod]
    pub fn from_channel_names(channel_names: Vec<String>) -> Self { channel_names.into() }
    
    
    pub fn has_unresolved_channels(&self) -> bool {
        self.members.iter().any(|m|
            matches!(m, SetMember::UnresolvedChannelName(_))
        )
    }

    /// Return the names of any channels in the set
    pub fn to_channel_names(&self) -> Vec<String> {
        let mut names = Vec::new();
        for member in self.members.iter() {
            match member {
                SetMember::UnresolvedChannelName(c) => names.push(c.clone()),
                SetMember::Channel(c) => names.push(c.channel_name.clone()),
            };
        }
        names
    }
}

impl ViewSet {
    /// Change any unresolved channel names to resolved channels.
    async fn resolve_channels(&mut self, mut block_rx: DataBlockReceiver) -> Result<DataBlockReceiver, DTTError> {
        let (new_tx, new_rx) = tokio::sync::mpsc::channel(1);

        // hash the set
        let set_hash: HashMap<String, usize> = self.members.iter().enumerate().map(|(i, m)| {
            (match m {
                SetMember::UnresolvedChannelName(n) => n.clone(),
                SetMember::Channel(c) => c.channel_name.clone(),
            }
                , i
            )
        }).collect();

        if let Some(block) = block_rx.recv().await {
            for channel in block.keys() {
                if let Some(i) = set_hash.get(channel.channel_name.as_str()) {
                    if matches!(self.members[*i], SetMember::UnresolvedChannelName(_)) {
                        self.members[*i] = SetMember::Channel(channel.clone());
                    }
                }
            }

            new_tx.send(block).await?;

            // link up to the new block channel
            tokio::spawn(async move {
                while let Some(block) = block_rx.recv().await {
                    if new_tx.send(block).await.is_err() {
                        break;
                    }
                }
            });
        };

        if self.has_unresolved_channels() {
            Err(DTTError::MissingDataStreamError("Couldn't resolve all channel names from data stream".into()))
        } else {
            Ok(new_rx)
        }
    }
}

#[derive(Clone)]
pub (crate) enum SpanStart{
    Online,
    Offline(PipInstant),
}

/// When the span is online, the start is just a beginning marker taken
/// from the current time.
#[derive(Clone)]
pub (crate) struct ViewSpan {
    pub online: bool,
    pub start_pip: PipInstant,
    pub span_pip: PipDuration,
}

impl ViewSpan {
    pub (crate) fn optional_end_pip(&self) -> Option<PipInstant> {
        if self.online {
            None
        } else {
            Some(self.end_pip())
        }
    }

    pub (crate) fn end_pip(&self) -> PipInstant {
        self.start_pip + self.span_pip
    }
}

pub struct ScopeView {
    pub (crate) id: u64,
    pub (crate) set: ViewSet,
    pub (crate) span: ViewSpan,

    /// When dropped, this token will cause the results task to quit
    cancel_token: DropGuard,
    pub (crate) data_source: DataSourceRef,

    /// Once created, this value can be used to
    /// Update the scope window
    pub (crate) block_tx: Option<DataBlockSender>,
    
    /// Used to cancel the data task if the view is updated
    pub (crate) data_task_cancel_token: Option<CancellationToken>,
    
    /// Used to update a span of unordered live request in place
    pub (crate) span_update_tx: Option<tokio::sync::watch::Sender<PipDuration>>,

    /// Used to update frequency domain configuration for on-the-fly
    /// frequency domain results
    pub (crate) fft_config_tx: tokio::sync::watch::Sender<InlineFFT>,
}


impl ScopeView {
    pub (crate) fn new(id: u64, set: ViewSet, span: ViewSpan, data_source: DataSourceRef) -> Self {
        let (fft_config_tx, _) = tokio::sync::watch::channel(InlineFFT::default());
        Self {
            id,
            set,
            span,
            cancel_token: CancellationToken::new().drop_guard(),
            data_source,
            block_tx: None,
            data_task_cancel_token: None,
            span_update_tx: None,
            fft_config_tx,
        }
    }

    async fn setup_analysis(& mut self, rc: &Box<RunContext>,
                                        block_rx: DataBlockReceiver)
                                        -> Result<ResultsReceiver, DTTError>
    {

        let mut ag = create_pipeline_graph(self)?;
        view_graph_to_pipeline(rc, self, &mut ag,  block_rx).await
    }

    async fn start_new_analysis(&mut self, rc: &Box<RunContext>) -> Result<(), DTTError> {
        let block_rx = self.resolve_data_source(rc.clone()).await?;
        let rr = self.setup_analysis(rc, block_rx).await?;
        self.start_results_loop(rc, rr).await;
        Ok(())
    }

    /// get a DataBlockReceiver for a data source
    /// if any members of the ViewSet are just channel names, these
    /// need to be resolved into actual channel structs
    async fn resolve_data_source(&mut self, rc: Box<RunContext>) -> Result<DataBlockReceiver, DTTError> {
        let mut block_rx = self.data_source.clone().start_scope_data(rc, self)?;

        if self.set.has_unresolved_channels() {
            block_rx = self.set.resolve_channels(block_rx).await?
        }

        Ok(block_rx)
    }

    async fn start_results_loop(&mut self, rc: &Box<RunContext>, rr: ResultsReceiver) {

        let ct = CancellationToken::new();
        let ct2 = ct.clone();
        self.cancel_token = ct.drop_guard();
        tokio::spawn( ScopeView::results_loop(rc.clone(), self.id, rr, ct2) );
    }

    async fn results_loop(rc: Box<RunContext>, id: u64, mut rr: ResultsReceiver, cancel_token: CancellationToken)  {
        loop {
            tokio::select! {
                _ = cancel_token.cancelled() => {
                    break
                },
                r = rr.recv() => {
                    match r {
                        Some(m) => if rc.output_handle.send(rc.clone(), ScopeViewResult{id, result: m}).is_err() {
                                   break;
                        },
                        None => {
                            break;
                        }
                    }
                },
            }
        }
    }

    fn set_span(&mut self, rc: &Box<RunContext>, span: ViewSpan) -> Result<(), DTTError> {
        self.span = span;

        self.data_source.clone().update_scope_data(rc.clone(), self)
    }
}


pub (crate) struct ScopeViewRegistry {
    registry: HashMap<u64, ScopeView>,
}

/// Register any number of views
impl ScopeViewRegistry {
    pub (crate) fn new() -> ScopeViewRegistry {
        ScopeViewRegistry {
            registry: HashMap::new(),
        }
    }

    /// Create a new view.  Any view so created should be closed with close_view()
    async fn new_view(&mut self, rc: &Box<RunContext>, source: DataSourceRef, id: u64, set: ViewSet, span: ViewSpan) {
        if self.registry.contains_key(&id) {
            self.close_view(rc, id);
        }
        let mut view = ScopeView::new(id, set, span, source.clone());
        if let Err(e) = view.start_new_analysis(rc).await {
            rc.user_messages.error(format!("Error creating view: {}", e));
        } else {
            self.registry.insert(id, view);
        }
    }

    /// When done with a view, close it by passing a handle to this function
    /// otherwise resources used by the view will be leaked.
    pub (crate) fn close_view(&mut self, rc: &Box<RunContext>, id: u64) {
        if self.registry.contains_key(&id) {
            let view = self.registry.get(&id).unwrap();
            if let Some(c) = &view.data_task_cancel_token {
                c.cancel();
            }
            self.registry.remove(&id);
        } else {
            rc.user_messages.error(format!("Closing View: No view with id {} found", id));
        }
    }

    /// Update an existing view with a new span
    /// We make the spans mutable so we don't
    /// have to rebuild analyses every time the span changes
    fn set_span(&mut self, rc: &Box<RunContext>, id: u64, span: ViewSpan) {
        let view = match self.registry.get_mut(&id) {
            Some(v) => v,
            None => {
                rc.user_messages.error(format!("No view with id {} found", id));
                return;
            },
        };

        match view.set_span(rc, span) {
            Ok(()) => (),
            Err(e) => {
                rc.user_messages.error(format!("Error setting span: {}", e));
            }
        };

    }

    fn fixed_span(start_pip: PipInstant, end_pip: PipInstant) -> ViewSpan {
        ViewSpan{
            online: false,
            start_pip,
            span_pip: end_pip - start_pip,
        }
    }

    /// create a fixed-width view
    pub (crate) async fn new_fixed_view(&mut self, rc: &Box<RunContext>, source: DataSourceRef, id: u64,
                                  start_pip: PipInstant, end_pip: PipInstant,
                                  set: ViewSet) {
        let span = Self::fixed_span(start_pip, end_pip);

        self.new_view(rc, source, id, set, span).await;
    }

    /// Set a new span on the view, but don't change the analysis
    /// Might be needed for speed
    pub (crate) async fn set_fixed_view(&mut self, rc: &Box<RunContext>, id: u64,
                                  start_pip: PipInstant, end_pip: PipInstant)
    {
        let span = Self::fixed_span(start_pip, end_pip);

        self.set_span(rc, id, span);
    }

    fn online_span(data_source: DataSourceRef, span: PipDuration) -> ViewSpan {

        let start_pip = data_source.now() - span;

        ViewSpan {
            online: true,
            start_pip,
            span_pip: span,
        }

    }

    /// create a fixed-width view
    pub (crate) async fn new_online_view(&mut self, rc: &Box<RunContext>, source: DataSourceRef,  id: u64, span_pip: PipDuration,
                                   set: ViewSet)
    {
        let span = Self::online_span(source.clone(), span_pip);

        self.new_view(rc, source, id, set, span).await;
    }

    /// Set a new span on the view, but don't change the analysis
    /// Might be needed for speed
    pub (crate) async fn set_online_view(&mut self, rc: &Box<RunContext>, id: u64,
                                   span_pip: PipDuration)
    {
        let view =
            match self.registry.get(&id) {
                Some(v) => v,
                None => {
                    rc.user_messages.error(format!("No view with id {} found", id));
                    return;
                }
            };

        let span = Self::online_span(view.data_source.clone(), span_pip);

        self.set_span(rc, id, span);
    }



}

//# Public interface
