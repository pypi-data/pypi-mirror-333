use std::cmp::Ordering;
use std::hash::{Hash, Hasher};
use std::vec::IntoIter;
use nds2_client_rs::{ChannelType, DataType};
use nds_cache_rs::buffer::{Buffer};
use num_traits::{FromPrimitive};
use pipelines::complex::{c128, c64};
use pipelines::{PipeDataPrimitive, PipelineSubscriber};
use user_messages::UserMsgProvider;
use crate::analysis::conditioning::
    {setup_conditioning_pipeline_complex, setup_conditioning_pipeline_heterodyned_real,
     setup_conditioning_pipeline_non_heterodyned_real, StandardPipeOutput};
use crate::analysis::conditioning::convert::{start_pipe_converter, ConvertTo};
use crate::data_source::data_source_pipeline::DataSourcePipeline;
use crate::errors::DTTError;
use crate::gds_sigp::decimate::{DecimationFilter, firphase};
use crate::run_context::RunContext;
use gps_pip::{PipDuration};
#[cfg(feature = "python")]
use pyo3::{
    pyclass,
    pymethods,
};
#[cfg(not(feature = "python"))]
use dtt_macros::{
    new, getter
};

use crate::analysis::types::time_domain_array::TimeDomainArray;
use crate::timeline::Timeline;

/// These values are taken from the NDS2 client
/// With a hoped-for extension for 
/// Complex128
/// Note the names for complex take the total size of the number
/// Not the size of real or imaginary components as the actual NDS2 client does.
/// 
/// So an NDS2 Client type Complex32 is an NDSDataType::Complex64
#[cfg_attr(feature = "python",pyclass(eq))]
#[derive(Clone, Debug, PartialEq, Hash, Default)]
pub enum NDSDataType {
    Int16,
    Int32,
    Int64,
    #[default]
    Float32,
    Float64,
    Complex64,
    UInt32,
    
    /// not yet implemented in NDS or Arrakis
    Complex128,
    UInt64,
    UInt16,
    Int8,
    UInt8,
    //String,
}

impl FromPrimitive for NDSDataType {
    fn from_i64(n: i64) -> Option<Self> {
        Self::from_u64(u64::from_i64(n)?)
    }

    fn from_u64(n: u64) -> Option<Self> {
        match n {
            1 => Some(NDSDataType::Int16),
            2 => Some(NDSDataType::Int32),
            3 => Some(NDSDataType::Int64),
            4 => Some(NDSDataType::Float32),
            5 => Some(NDSDataType::Float64),
            6 => Some(NDSDataType::Complex64),
            7 => Some(NDSDataType::UInt32),
            8 => Some(NDSDataType::Complex128),
            _ => None,
        }
    }
}

impl Into<DataType> for NDSDataType {
    fn into(self) -> DataType {
        match self {
            NDSDataType::Int16 => {DataType::Int16},
            NDSDataType::Int32 => {DataType::Int32},
            NDSDataType::Int64 => {DataType::Int64},
            NDSDataType::Float32 => {DataType::Float32},
            NDSDataType::Float64 => {DataType::Float64}
            NDSDataType::Complex64 => {DataType::Complex32}
            NDSDataType::UInt32 => {DataType::UInt32},
            NDSDataType::Complex128 |
                NDSDataType::UInt64 |
                NDSDataType::UInt16 |
                NDSDataType::Int8   |
                NDSDataType::UInt8  => {DataType::Unknown},
                //NDSDataType::String 
        }
    }
}

impl Into<nds_cache_rs::buffer::DataType> for NDSDataType {
    fn into(self) -> nds_cache_rs::buffer::DataType {
        match self {
            NDSDataType::Int16 => {nds_cache_rs::buffer::DataType::Int16},
            NDSDataType::Int32 => {nds_cache_rs::buffer::DataType::Int32},
            NDSDataType::Int64 => {nds_cache_rs::buffer::DataType::Int64},
            NDSDataType::Float32 => {nds_cache_rs::buffer::DataType::Float32},
            NDSDataType::Float64 => {nds_cache_rs::buffer::DataType::Float64},
            NDSDataType::UInt32 => {nds_cache_rs::buffer::DataType::UInt32},
            NDSDataType::Complex64 => {nds_cache_rs::buffer::DataType::Complex32},
            NDSDataType::Complex128 |
            NDSDataType::UInt64 |
            NDSDataType::UInt16 |
            NDSDataType::Int8   |
            NDSDataType::UInt8  => {nds_cache_rs::buffer::DataType::Unknown},
            //NDSDataType::String  
        }
    }
}

impl From<nds_cache_rs::buffer::DataType> for NDSDataType {
    fn from(nds_type: nds_cache_rs::buffer::DataType) -> Self {
        match nds_type {
            nds_cache_rs::buffer::DataType::Int16 => {NDSDataType::Int16},
            nds_cache_rs::buffer::DataType::Int32 => {NDSDataType::Int32},
            nds_cache_rs::buffer::DataType::Int64 => {NDSDataType::Int64},
            nds_cache_rs::buffer::DataType::Float32 => {NDSDataType::Float32},
            nds_cache_rs::buffer::DataType::Float64 => {NDSDataType::Float64},
            nds_cache_rs::buffer::DataType::UInt32 => {NDSDataType::UInt32},
            nds_cache_rs::buffer::DataType::Complex32 => {NDSDataType::Complex64},
            nds_cache_rs::buffer::DataType::Unknown => {NDSDataType::UInt8},
        }
    }
}

impl NDSDataType {
    pub fn is_complex(&self) -> bool {
        match self {
            NDSDataType::Complex64 | NDSDataType::Complex128 => true,
            _ => false,
        }
    }
}

#[derive(Clone, Debug)]
pub struct ChannelCalibration {
    slope: f64,
    offset: f64,
}

#[cfg_attr(feature = "python", pyclass(get_all))]
#[derive(Clone, Debug, Default)]
pub struct Channel {
    pub channel_name: String,
    pub data_type: NDSDataType,
    pub rate_hz: f64,

    // decimation stage done on raw data
    // before it's heterodyned
    pub raw_decimation_params: DecimationParameters,

    // decimation stage done on data after it's heterodyned
    pub heterodyned_decimation_params: DecimationParameters,

    // when true, add in a heterodyne pipeline between decimations
    pub do_heterodyne: bool,

    pub decimation_delays: DecimationDelays,

    pub dcu_id: Option<i64>,
    pub channel_number: Option<i64>,
    pub calibration: Option<i64>,
    pub heterodyne_freq_hz: Option<f64>,
    pub gain: Option<f64>,
    pub slope: Option<f64>,
    pub offset: Option<f64>,
    pub use_active_time: bool,
    pub units: Option<String>,
}

impl Hash for Channel {
    fn hash<H: Hasher>(&self, state: &mut H) {
        // channel name
        self.channel_name.hash(state);

        // rate
        // get period in pips_per_sec
        let period_pips = PipDuration::freq_hz_to_period(self.rate_hz);
        period_pips.hash(state);

        // type
        self.data_type.hash(state);
    }
}

impl PartialEq<Self> for Channel {
    fn eq(&self, other: &Self) -> bool {
        (self.channel_name == other.channel_name)
            && (self.rate_hz == other.rate_hz)
            && (self.data_type == other.data_type)
    }
}

impl Eq for Channel {

}

impl Into<nds2_client_rs::Channel> for Channel {
    fn into(self) -> nds2_client_rs::Channel {
        nds2_client_rs::Channel {
            name: self.channel_name,
            channel_type: ChannelType::Raw,
            data_type: self.data_type.into(),
            sample_rate: self.rate_hz,
            gain: 1.0,
            slope: 1.0,
            offset: 0.0,
            units: "".to_string(),
        }
    }
}

impl Into<nds_cache_rs::buffer::Channel> for Channel {
    fn into(self) -> nds_cache_rs::buffer::Channel {
        nds_cache_rs::buffer::Channel::new(
            self.channel_name,
            nds_cache_rs::buffer::ChannelType::Raw,
            self.data_type.into(),
            self.gain.unwrap_or(1.0) as f32,
            self.slope.unwrap_or(1.0) as f32,
            self.offset.unwrap_or(0.0) as f32,
            self.units.unwrap_or(String::new()),
        )
    }
}

impl From<&Buffer> for Channel {
    fn from(buffer: &Buffer) -> Self {
        Channel {
            channel_name: buffer.channel().name().clone(),
            data_type: buffer.channel().data_type().clone().into(),
            rate_hz: buffer.period().period_to_freq_hz(),
            gain: Some(buffer.channel().gain() as f64),
            slope: Some(buffer.channel().slope() as f64),
            offset: Some(buffer.channel().offset() as f64),
            units: Some(buffer.channel().units().clone()),
            ..Self::default()
        }
    }
}

impl PartialOrd for Channel {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        if self.channel_name < other.channel_name {
            Some(Ordering::Less)
        }
        else if self.channel_name > other.channel_name {
            Some(Ordering::Greater)
        }
        else if self.rate_hz < other.rate_hz {
            Some(Ordering::Less)
        }
        else if self.rate_hz > other.rate_hz {
            Some(Ordering::Greater)
        }
        else if self.data_type == other.data_type {
            Some(Ordering::Equal)
        }
        else {
            None
        }
    }
}

impl Channel {
    
    /// Calculate decimation factors and delays
    /// heterodyned = true if the channel is heterodyned or is to be heterodyned
    /// sample_max_hz is the desired decimated rate before heterodyning (downconverting) or if not heterodyned
    /// heterodyned_sample_rate_hz is the desired decimated rate *after* heterodyning
    pub (crate) fn calc_decimation_factors(&mut self, remove_delay: bool,
                                   is_heterodyne: bool, sample_max_hz: f64, 
                                   heterodyned_sample_rate_hz: f64) -> Result<(), DTTError> {
        let is_complex = self.data_type.is_complex();
        
        if is_heterodyne {
            if is_complex {
                self.raw_decimation_params =
                    DecimationParameters::new(DecimationFilter::FirLS3, self.rate_hz,
                                              heterodyned_sample_rate_hz)?;

                self.heterodyned_decimation_params = DecimationParameters::default();

            } else {
                // real channels in a heterodyne test have to be heterodyned (downconverted).
                self.do_heterodyne = true;

                // decimation down to the raw sample rate first, but don't time shift.
                self.raw_decimation_params =
                    DecimationParameters::new(DecimationFilter::FirLS3,
                                              self.rate_hz, sample_max_hz)?;


                // decimation down to heterodyne rate after the heterodyne
                self.heterodyned_decimation_params =
                    DecimationParameters::new(DecimationFilter::FirLS3,
                                              sample_max_hz, heterodyned_sample_rate_hz)?;


            }
        } else {
            // not heterodyned
            self.raw_decimation_params =
                DecimationParameters::new(DecimationFilter::FirLS1, self.rate_hz, sample_max_hz)?;
            self.heterodyned_decimation_params = DecimationParameters::default();
        }

        // calculate the delays from the decimations
        let total_decs = self.heterodyned_decimation_params.num_decs
            + self.raw_decimation_params.num_decs;

        self.decimation_delays =
            DecimationDelays::new(remove_delay, self.rate_hz, total_decs,
                                  self.raw_decimation_params.filter);

        Ok(())
    }

    pub (crate) async fn create_data_source_pipeline(&self, rc: &Box<RunContext>,
                                             buffer_rx: tokio::sync::mpsc::Receiver<Buffer>) -> StandardPipeOutput
    {
        match self.data_type {
            NDSDataType::Int8 =>        StandardPipeOutput::Int8(self.create_data_source::<i8>(rc, buffer_rx).await),
            NDSDataType::Int16 =>       StandardPipeOutput::Int16(self.create_data_source::<i16>(rc, buffer_rx).await),
            NDSDataType::Int32 =>       StandardPipeOutput::Int32(self.create_data_source::<i32>(rc, buffer_rx).await),
            NDSDataType::Int64 =>       StandardPipeOutput::Int64(self.create_data_source::<i64>(rc, buffer_rx).await),
            //NDSDataType::Float32 =>     StandardPipeOutput::Float64(self.create_data_source_convert::<f32, f64>(rc, buffer_rx).await),
            NDSDataType::Float32 =>     StandardPipeOutput::Float64(self.create_data_source::<f64>(rc, buffer_rx).await),
            NDSDataType::Float64 =>     StandardPipeOutput::Float64(self.create_data_source::<f64>(rc, buffer_rx).await),
            NDSDataType::UInt8 =>       StandardPipeOutput::UInt8(self.create_data_source::<u8>(rc, buffer_rx).await),
            NDSDataType::UInt16 =>      StandardPipeOutput::UInt16(self.create_data_source::<u16>(rc, buffer_rx).await),
            NDSDataType::UInt32 =>      StandardPipeOutput::UInt32(self.create_data_source::<u32>(rc, buffer_rx).await),
            NDSDataType::UInt64 =>      StandardPipeOutput::UInt64(self.create_data_source::<u64>(rc, buffer_rx).await),
            NDSDataType::Complex64 =>   StandardPipeOutput::Complex128(self.create_data_source_convert::<c64, c128>(rc, buffer_rx).await),
            NDSDataType::Complex128 =>  StandardPipeOutput::Complex128(self.create_data_source::<c128>(rc, buffer_rx).await),
            //NDSDataType::String =>  StandardPipeOutput::String(self.create_data_source::<String>(rc, buffer_rx).await),
        }
    }

    /// Create a super pipeline that is a data source of TimeDomainArray<T>
    /// And converts to an output of TimeDomainArray<U>
    async fn create_data_source_convert<T, U>
        (&self, rc: &Box<RunContext>, buffer_rx: tokio::sync::mpsc::Receiver<Buffer>) -> PipelineSubscriber<TimeDomainArray<U>>
    where
        U: PipeDataPrimitive + Copy,
        T: PipeDataPrimitive + Copy + ConvertTo<U>,
        TimeDomainArray<T>: TryFrom<Buffer,Error=DTTError>
    {
        let ds = self.create_data_source::<T>(rc, buffer_rx).await;

        start_pipe_converter(rc.ump_clone(), self.channel_name.clone() + ":convert", &ds).await
    }

    /// Create a data source of TimeDomainArray<T>
    async fn create_data_source<T>
    (&self, rc: &Box<RunContext>, buffer_rx: tokio::sync::mpsc::Receiver<Buffer>) -> PipelineSubscriber<TimeDomainArray<T>>
    where
        T: PipeDataPrimitive,
        TimeDomainArray<T>: TryFrom<Buffer,Error=DTTError>
    {
        DataSourcePipeline::create::<T>(
            rc.ump_clone(),
            self.channel_name.clone() + ":source",
            buffer_rx
        )
    }

    pub (crate) async fn create_conditioning_pipeline(
        &self, rc: &Box<RunContext>, timeline: &Timeline,
        buffer_rx: tokio::sync::mpsc::Receiver<Buffer>) -> Result<StandardPipeOutput, DTTError> {
        let pipe_out = match self.data_type {
            NDSDataType::Int8 => self.create_conditioning_pipeline_generic_real::<i8>(rc, timeline, buffer_rx).await,
            NDSDataType::Int16 => self.create_conditioning_pipeline_generic_real::<i16>(rc, timeline, buffer_rx).await,
            NDSDataType::Int32 => self.create_conditioning_pipeline_generic_real::<i32>(rc, timeline, buffer_rx).await,
            NDSDataType::Int64 => self.create_conditioning_pipeline_generic_real::<i64>(rc, timeline, buffer_rx).await,
            NDSDataType::Float32 => self.create_conditioning_pipeline_generic_real::<f32>(rc, timeline, buffer_rx).await,
            NDSDataType::Float64 => self.create_conditioning_pipeline_generic_real::<f64>(rc, timeline, buffer_rx).await,
            NDSDataType::UInt64 => self.create_conditioning_pipeline_generic_real::<u64>(rc, timeline, buffer_rx).await,
            NDSDataType::UInt32 => self.create_conditioning_pipeline_generic_real::<u32>(rc, timeline, buffer_rx).await,
            NDSDataType::UInt16 => self.create_conditioning_pipeline_generic_real::<u16>(rc, timeline, buffer_rx).await,
            NDSDataType::UInt8 => self.create_conditioning_pipeline_generic_real::<u8>(rc, timeline, buffer_rx).await,
            NDSDataType::Complex64 => self.create_conditioning_pipeline_generic_complex::<c64>(rc, timeline, buffer_rx).await,
            NDSDataType::Complex128 => self.create_conditioning_pipeline_generic_complex::<c128>(rc, timeline, buffer_rx).await,
            //NDSDataType::String => return Err(DTTError::UnsupportedTypeError("String", "when creating conditioning pipeline")),
        };

        Ok(pipe_out)
    }

    async fn create_conditioning_pipeline_generic_real<T>
    (
        &self, rc: &Box<RunContext>, timeline: &Timeline,
        buffer_rx: tokio::sync::mpsc::Receiver<Buffer>) -> StandardPipeOutput
    where
        T: ConvertTo<f64> +  PipeDataPrimitive + Copy,
        TimeDomainArray<T>: TryFrom<Buffer,Error=DTTError>
    {
        let ds =
            DataSourcePipeline::create::<T>(
                rc.clone(),
                self.channel_name.clone() + ":source",
                buffer_rx
            );

        if self.do_heterodyne {
            setup_conditioning_pipeline_heterodyned_real(rc.ump_clone(), self, timeline, &ds).await
        }
        else {
            setup_conditioning_pipeline_non_heterodyned_real(rc.ump_clone(), self, timeline, &ds).await
        }
    }

    async fn create_conditioning_pipeline_generic_complex<T>
    (
        &self, rc: &Box<RunContext>, timeline: &Timeline,
        buffer_rx: tokio::sync::mpsc::Receiver<Buffer>) -> StandardPipeOutput
    where
        T: ConvertTo<c128> + PipeDataPrimitive + Copy,
        TimeDomainArray<T>: TryFrom<Buffer,Error=DTTError>
    {
        let ds =
            DataSourcePipeline::create::<T>(
                rc.clone(),
                self.channel_name.clone() + ":source",
                buffer_rx
            );


        setup_conditioning_pipeline_complex(rc.ump_clone(), self, timeline, &ds).await
    }

}

#[cfg_attr(feature = "python", pymethods)]
impl Channel {
    #[new]
    pub fn new(channel_name: String, data_type: NDSDataType, rate_hz: f64) -> Self {
        Channel {
            channel_name,
            data_type,
            rate_hz,
            ..Self::default()
        }
    }

    #[getter]
    pub fn channel_name(&self) -> &String {
        &self.channel_name
    }

    #[getter]
    pub fn data_type(&self) -> NDSDataType {
        self.data_type.clone()
    }

    #[getter]
    pub fn rate_hz(&self) -> f64 {
        self.rate_hz
    }
}

pub trait Activate {
    fn is_active(&self) -> bool;
}

#[cfg_attr(feature = "python", pyclass(get_all))]
#[derive(Clone, Debug)]
pub struct ChannelParams {
    pub active: bool,
    pub channel: Channel,
}

impl Activate for ChannelParams {
    fn is_active(&self) -> bool {
        self.active
    }
}

pub trait ActiveList<T> {
    fn active_iter(&self) -> IntoIter<&T>;
}

impl <T> ActiveList<T> for Vec<T>
    where T: Activate {
    fn active_iter(&self) -> IntoIter<&T> {
        self.into_iter()
            .filter(|s|{(*s).is_active()})
            .collect::<Vec<&T>>().into_iter()
    }
}

/// collects the delays associated with the total decimation on the channel
#[cfg_attr(feature = "python", pyclass)]
#[derive(Default, Clone, Debug)]
pub struct DecimationDelays {
    /// seconds of delay for the decimation
    pub decimation_delay_s: f64,

    /// the number of points to shift data up for alignment
    pub delay_taps: i32,

    /// the time to shift down the start of a segment
    pub delayshift_pip: PipDuration,

    /// Time shift for start of heterodyne calculation
    pub heterodyne_delay_pip: PipDuration,
}

impl DecimationDelays {
    fn new(remove_delay: bool, input_rate_hz: f64, num_decs: i32, filter: DecimationFilter) -> Self {
        let dec_factor = 1 << num_decs;
        let y = firphase(filter, dec_factor);
        let decimation_delay_s = y / input_rate_hz;

        if remove_delay {

            // this is the number of shift steps needed to correct the input
            let sDelay = i32::from_f64(y.round()).unwrap_or(0);
            let dec_factor = 1 << num_decs;

            // get sDelay rounded up to the nearest multiple of the decimation factor
            // this is number of shift steps on the output, but in units of input steps
            let tDelay = dec_factor * ((sDelay + dec_factor - 1) / dec_factor);

            // difference between output and input steps
            // data will be shifted later by this many points on input to get the timestamp
            // right on output
            let delay_taps = tDelay - sDelay;

            let dt = 1.0 / input_rate_hz;

            let delayshift_pip = PipDuration::from_seconds(f64::from(tDelay) * dt);

            let heterodyne_delay_pip = PipDuration::from_seconds((y + f64::from(delay_taps)) * dt);


                Self {
                    decimation_delay_s,
                    delay_taps,
                    delayshift_pip,
                    heterodyne_delay_pip,
                }
        }
        else {
                Self{
                    decimation_delay_s,
                    delay_taps: 0,
                    delayshift_pip: PipDuration::default(),
                    heterodyne_delay_pip: PipDuration::default(),
                }
        }
    }
}


/// Values used to generate a decimation pipeline for single stage of decimation
#[cfg_attr(feature = "python", pyclass(get_all))]
#[derive(Default, Clone, Debug)]
pub struct DecimationParameters {

    /// anti-aliasing filter
    pub filter: DecimationFilter,

    /// number of x2 decimations
    pub num_decs: i32,
}

impl DecimationParameters {
    /// Calculation of delay correction values
    ///
    /// remove delay is false, the number of decimations and the real delay is calculated
    /// but all the correction factors are set to zero.
    ///
    /// ### References
    ///
    /// 1. cds/software/dtt dataChannel::preprocessing::preprocessing
    ///    https://git.ligo.org/cds/software/dtt/-/blob/4.1.1/src/dtt/storage/channelinput.cc#L303
    fn new(filter: DecimationFilter, input_rate_hz: f64, output_rate_hz: f64)
        -> Result<Self, DTTError> {
        let dec_factor = if let Some(df) = i32::from_f64(input_rate_hz / output_rate_hz) {
            df
        } else {
            return Err(DTTError::BadArgument("DecimationParameters::new", "input_rate_hz",
                                             "should be output_rate_hz xN, where N is a multiple of two."))
        };

        let num_decs = num_decs_from_dec_factor(dec_factor)?;

        Ok(
            DecimationParameters {
                filter,
                num_decs,
            })
    }
}


/// calculate the number of x2 decimations that are needed to reach the
/// given decimation factor.
/// Only exact values are permitted, i.e. powers of two.  Everything else
/// returns an Err(BadArgument)
fn num_decs_from_dec_factor(dec_factor: i32) -> Result<i32, DTTError> {
    let num_decs = match i32::from_f64(f64::from(dec_factor).log2().ceil()) {
        Some(x) => x,
        None => { return Err(DTTError::BadArgument("num_decs_from_dec_factor","dec_factor",
        "could not take log2() of the value"));}
    };
    if (1<<num_decs) != dec_factor {
        return Err(DTTError::BadArgument("num_decS_from_dec_factor", "dec_factor",
                                         "was not an exact power of two"));
    }
    Ok(num_decs)
}