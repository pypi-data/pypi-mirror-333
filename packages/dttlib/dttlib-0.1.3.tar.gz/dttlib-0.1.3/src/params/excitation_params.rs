#[cfg(feature = "python")]
use pyo3::pyclass;
use super::channel_params::{Activate, Channel};

#[cfg_attr(feature = "python", pyclass(get_all))]
#[derive(Clone, Debug)]
pub struct Excitation {
    pub channel: Channel,
    pub read_back_channel: Option<Channel>,
}

impl Excitation {
    
    /// Return the read back channel
    pub fn get_read_back_channel(&self) -> Channel {
        match &self.read_back_channel {
            None => self.channel.clone(),
            Some(c) => c.clone(),
        }
    }
}

#[cfg_attr(feature = "python", pyclass(get_all))]
#[derive(Clone, Debug)]
pub struct ExcitationParams {
    pub active: bool,
    pub excitation: Excitation,
}

impl Activate for ExcitationParams {
    fn is_active(&self) -> bool {
        self.active
    }
}