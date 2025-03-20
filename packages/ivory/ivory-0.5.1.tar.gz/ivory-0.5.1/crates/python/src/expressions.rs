use ivory_core::optimize;
use polars::prelude::*;
use pyo3_polars::derive::polars_expr;

fn linear_fit_output(_: &[Field]) -> PolarsResult<Field> {
    let fields = vec![
        Field::new("slope".into(), DataType::Float64),
        Field::new("intercept".into(), DataType::Float64),
    ];
    Ok(Field::new("linear_fit".into(), DataType::Struct(fields)))
}

#[polars_expr(output_type_func = linear_fit_output)]
fn linear_fit(inputs: &[Series]) -> PolarsResult<Series> {
    if inputs.len() != 2 {
        polars_bail!(ComputeError: "linear_fit expects 2 input series, got {}", inputs.len())
    }

    let x = inputs[0].f64()?;
    let y = inputs[1].f64()?;

    let (slope, intercept) = optimize::linear_fit(x, y)?;

    let slope = Series::new("slope".into(), &[slope]);
    let intercept = Series::new("intercept".into(), &[intercept]);

    Ok(
        StructChunked::from_series("linear_fit".into(), 1, [slope, intercept].iter())?
            .into_series(),
    )
}
