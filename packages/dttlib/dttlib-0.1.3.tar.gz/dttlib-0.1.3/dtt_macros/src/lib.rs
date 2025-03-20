extern crate proc_macro;
use proc_macro::TokenStream;

/// Does nothing
/// This macro is needed so that `#[staticmethod]` method attribute used by\ pyo3 still builds
/// when not using pyo3
///
/// There doesn't seem to be a way to make that attribute conditional
#[proc_macro_attribute]
pub fn staticmethod(_attr: TokenStream, input: TokenStream) -> TokenStream {
    input
}

/// Does nothing
/// This macro is needed so that `#[new]` method attribute use by pyo3 still builds
/// when not using pyo3
///
/// There doesn't seem to be a way to make that attribute conditional
#[proc_macro_attribute]
pub fn new(_attr: TokenStream, input: TokenStream) -> TokenStream {
    input
}

/// Does nothing
/// This macro is needed so that `#[getter]` method attribute use by pyo3 still builds
/// when not using pyo3
///
/// There doesn't seem to be a way to make that attribute conditional
#[proc_macro_attribute]
pub fn getter(_attr: TokenStream, input: TokenStream) -> TokenStream {
    input
}