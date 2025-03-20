//! Downsample a time-domain trace to
//! a fixed number of points, the easier to draw with

use std::collections::VecDeque;
use std::sync::Arc;
use futures::future::FutureExt;
use gps_pip::{PipDuration, PipInstant};
use pipeline_macros::box_async;
use pipelines::{PipeDataPrimitive, PipeResult, PipelineSubscriber};
use pipelines::pipe::Pipe1;
use user_messages::UserMsgProvider;
use crate::AccumulationStats;
use crate::analysis::types::time_domain_array::TimeDomainArray;

#[derive(Clone, Default)]
pub (crate) struct DownsampleCache<T>
where
    T: PipeDataPrimitive + Copy + PartialOrd
{
    min: VecDeque<T>,
    max: VecDeque<T>,
    n: VecDeque<usize>,
    factor: usize,
    /// the decimator is given some flexibility.
    /// the cache is allowed to range to two times target_size
    /// and won't enlarge unless less than half target_size
    target_size: usize,
    start_pip: PipInstant,
    accumulation_stats: AccumulationStats,
    rate_hz: f64
}

impl <T>  DownsampleCache<T>
where
    T: PipeDataPrimitive + Copy + Default + PartialOrd
{
    fn new(target_size: usize) -> Self {
        Self {
            min: VecDeque::with_capacity(3*target_size),
            max: VecDeque::with_capacity(3*target_size),
            n: VecDeque::with_capacity(3*target_size),
            factor: 0,
            target_size,
            start_pip: PipInstant::gpst_epoch(),
            rate_hz: 0.0,
            accumulation_stats: AccumulationStats::default()
        }
    }

    fn len(&self) -> usize {
        self.min.len()
    }

    fn update(&mut self, input: &TimeDomainArray<T>) -> (TimeDomainArray<T>, TimeDomainArray<T>) {
        self.accumulation_stats = input.accumulation_stats;

        let suggested_factor = if input.len() < self.target_size {
            return (input.clone(), input.clone());
        } else if input.len() % self.target_size == 0 {
                input.len() / self.target_size
        } else {
            input.len() / self.target_size + 1
        };

        let input_period = PipDuration::freq_hz_to_period(input.rate_hz);
        let orig_dec_period = self.factor * input_period;

        // if the factor is changed by at least 2x, or if the new data doesn't intersect the cache
        // clear the cache
        if (self.factor == 0)
            || (! (self.factor / 2 + 1 .. self.factor * 2).contains(&suggested_factor) )
            || (self.start_pip > input.end_gps_pip())
            || (self.start_pip + self.len()*orig_dec_period < input.start_gps_pip)
        {
           self.factor = suggested_factor;
            self.min.clear();
            self.max.clear();
        }

        let dec_period = self.factor * input_period;

        self.rate_hz = input.rate_hz / self.factor as f64;


        {
            // Find out of there is any leading component of the input
            // that's not in the cache, and how much
            let (lead_end, mut block_start_pip) = if self.len() == 0 {
                // if the cache is empty, we have to do the whole thing
                (Some(input.len() - 1), None)
            } else if input.start_gps_pip.snap_down_to_step(&dec_period) < self.start_pip {
                let max_time = self.start_pip + (self.factor - 1) * input_period;
                let block_start_pip = max_time.snap_down_to_step(&dec_period);
                (Some(input.gps_pip_to_index(max_time).min(input.len() - 1)), Some(block_start_pip))
            } else {
                (None, None)
            };

            // if there is any leading component, then decimate it.
            if let Some(e) = lead_end {
                let mut new_min = None;
                let mut new_max = None;
                let mut new_n = 0;

                for inp_index in (0..=e).rev() {
                    let inp_pip = input.index_to_gps_pip(inp_index);
                    let new_block_start_pip = inp_pip.snap_down_to_step(&dec_period);

                    if let Some(t) = &block_start_pip {
                        if &new_block_start_pip != t {
                            let block_start_index = ((t - self.start_pip) / dec_period) as usize;
                            if let Some(min) = new_min {
                                self.min[block_start_index] = min;
                            }
                            if let Some(max) = new_max {
                                self.max[block_start_index] = max;
                            }
                            self.n[block_start_index] = new_n;

                            // fill in any zero size blocks that might have been pushed earlier
                            for i in block_start_index..self.min.len() {
                                if self.n[i] == 0 {
                                    self.min[i] = self.min[block_start_index];
                                    self.max[i] = self.max[block_start_index];
                                } else {
                                    break;
                                }
                            }

                            new_min = None;
                            new_max = None;
                            new_n = 0;
                        }
                    } else {
                        self.min.push_front(T::default());
                        self.max.push_front(T::default());
                        self.n.push_front(0);
                        self.start_pip = new_block_start_pip;
                    }

                    while new_block_start_pip < self.start_pip {
                        self.min.push_front(T::default());
                        self.max.push_front(T::default());
                        self.n.push_front(0);
                        self.start_pip -= dec_period;
                    }

                    block_start_pip = Some(new_block_start_pip);

                    new_min = match new_min {
                        None => Some(input.data[inp_index]),
                        Some(x) => if input.data[inp_index] < x { Some(input.data[inp_index]) } else { Some(x) }
                    };

                    new_max = match new_max {
                        None => Some(input.data[inp_index]),
                        Some(x) => if input.data[inp_index] > x { Some(input.data[inp_index]) } else { Some(x) }
                    };

                    new_n += 1;
                }

                // fill in the last block
                if new_n > 0 {
                    let block_start_index = ((block_start_pip.unwrap() - self.start_pip) / dec_period) as usize;
                    self.min[block_start_index] = new_min.unwrap();
                    self.max[block_start_index] = new_max.unwrap();
                    self.n[block_start_index] = new_n;
                }
            }
        }

        {
            // handle any extension of the nput past the cache end
            let inp_last = input.len() - 1;
            let inp_last_pip = input.index_to_gps_pip(inp_last);

            let mut block_start_pip = self.start_pip + (self.len() - 1) * dec_period;

            if inp_last_pip.snap_down_to_step(&dec_period) > block_start_pip {
                let mut new_min = None;
                let mut new_max = None;
                let mut new_n = 0;

                let inp_start_pip = input.gps_pip_to_index(block_start_pip).max(0);

                for inp_index in (inp_start_pip..=inp_last) {
                    let inp_pip = input.index_to_gps_pip(inp_index);
                    let new_block_start_pip = inp_pip.snap_down_to_step(&dec_period);


                    if new_block_start_pip != block_start_pip {
                        let block_start_index = ((block_start_pip - self.start_pip) / dec_period) as usize;
                        self.min[block_start_index] = if let Some(min) = new_min {
                            min
                        } else if block_start_index > 0 {
                            self.min[block_start_index - 1]
                        } else {
                            T::default()
                        };

                        self.max[block_start_index] = if let Some(max) = new_max {
                            max
                        } else if block_start_index > 0 {
                            self.max[block_start_index - 1]
                        } else {
                            T::default()
                        };

                        self.n[block_start_index] = new_n;

                        new_min = None;
                        new_max = None;
                        new_n = 0;
                    }


                    while new_block_start_pip >= self.start_pip + self.len() * dec_period {
                        self.min.push_back(T::default());
                        self.max.push_back(T::default());
                        self.n.push_back(0);
                    }

                    block_start_pip = new_block_start_pip;

                    new_min = match new_min {
                        None => Some(input.data[inp_index]),
                        Some(x) => if input.data[inp_index] < x { Some(input.data[inp_index]) } else { Some(x) }
                    };

                    new_max = match new_max {
                        None => Some(input.data[inp_index]),
                        Some(x) => if input.data[inp_index] > x { Some(input.data[inp_index]) } else { Some(x) }
                    };

                    new_n += 1;
                }

                if new_n > 0 {
                    let block_start_index = ((block_start_pip - self.start_pip) / dec_period) as usize;
                    self.min[block_start_index] = new_min.unwrap();
                    self.max[block_start_index] = new_max.unwrap();
                    self.n[block_start_index] = new_n;
                }
            }
        }

        // trim the cache to minimize its size

        let end_time = (input.end_gps_pip() - input_period).snap_down_to_step(&dec_period);
        let start_time = input.start_gps_pip.snap_down_to_step(&dec_period);

        let start_index = ((start_time - self.start_pip) / dec_period) as usize;
        let end_index = ((end_time - self.start_pip) / dec_period) as usize;

        if start_index > 0
        {
            self.min.drain(..start_index);
            self.max.drain(..start_index);
            self.n.drain(..start_index);
            self.start_pip += (start_index) * dec_period;
        }

        if end_index < self.min.len() - 1 {
            self.min.truncate(end_index+1);
            self.max.truncate(end_index+1);
            self.n.truncate(end_index+1);
        }

        //println!("downsampled from {} to {} points", input.len(), self.len());

        self.get_min_max()
    }

    fn get_min_max(&self) -> (TimeDomainArray<T>, TimeDomainArray<T>) {

        (
            TimeDomainArray {
                start_gps_pip: self.start_pip,
                rate_hz: self.rate_hz,
                data: self.min.clone().make_contiguous().to_vec(),
                accumulation_stats: self.accumulation_stats,
            }
            ,
            TimeDomainArray {
                start_gps_pip: self.start_pip,
                rate_hz: self.rate_hz,
                data: self.max.clone().make_contiguous().to_vec(),
                accumulation_stats: self.accumulation_stats,
            }
        )

    }

    #[box_async]
    pub (crate) fn generate(_rc: Box<dyn UserMsgProvider>, state: &mut Self,
                                  input: Arc<TimeDomainArray<T>>)
        -> PipeResult<(TimeDomainArray<T>, TimeDomainArray<T>)>
    {
        state.update(input.as_ref()).into()
    }


    pub (crate) async fn create(rc: Box<dyn UserMsgProvider>, name: impl Into<String>,
                                   input: &PipelineSubscriber<TimeDomainArray<T>>)
                                   -> PipelineSubscriber<(TimeDomainArray<T>, TimeDomainArray<T>)>
    {
        let state = Self::new(4096);

        Pipe1::create(rc, name.into(), Self::generate, state, None, None, input).await
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::analysis::types::time_domain_array::TimeDomainArray;

    #[test]
    fn test_add_lead() {
        let mut dc = DownsampleCache::<f64>::new(4);
        let rate_hz = 100.0;
        let step_pip = PipDuration::freq_hz_to_period(rate_hz);
        let offset = 10;

        let t1 = TimeDomainArray{
            start_gps_pip: PipInstant::gpst_epoch() + step_pip * (offset + 5),
            rate_hz,
            data: vec![1.0; 20],
            accumulation_stats: AccumulationStats::default()
        };

        let t2 = TimeDomainArray{
            start_gps_pip: PipInstant::gpst_epoch() + step_pip * (offset),
            rate_hz,
            data: vec![2.0; 27],
            accumulation_stats: AccumulationStats::default()
        };

        dc.update(&t1);

        assert_eq!(dc.factor, 5);
        assert_eq!(dc.min.len(), 4);


        dc.update(&t2);

        assert_eq!(dc.factor, 5);
        assert_eq!(dc.min.len(), 6);
        assert_eq!(dc.n[0], 5);
        assert_eq!(dc.min[0], 2.0);
        assert_eq!(dc.min[1], 2.0);
        assert_eq!(dc.max[1], 2.0);
    }
}



