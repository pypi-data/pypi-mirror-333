use pyo3::prelude::*;

#[pyfunction]
fn pi() -> String {
    "3.141592653589793238462643383279...".to_string()
}

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn _core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(pi, m)?)?;
    Ok(())
}
