use std::{collections::BTreeMap, sync::Arc};

use axum::async_trait;
use futures::FutureExt;
use pyo3::{
    exceptions::PyException,
    pyclass, pymethods,
    types::{IntoPyDict, PyAnyMethods, PyList, PyString, PyTuple},
    Bound, IntoPyObjectExt, Py, PyAny, PyResult, Python,
};
use pythonize::pythonize;

use crate::{
    base::{schema, value},
    builder::plan,
    py::IntoPyResult,
};
use anyhow::Result;

use super::sdk::{
    ExecutorFuture, FlowInstanceContext, SimpleFunctionExecutor, SimpleFunctionFactory,
};

fn basic_value_to_py_object<'py>(
    py: Python<'py>,
    v: &value::BasicValue,
) -> PyResult<Bound<'py, PyAny>> {
    let result = match v {
        value::BasicValue::Bytes(v) => v.into_bound_py_any(py)?,
        value::BasicValue::Str(v) => v.into_bound_py_any(py)?,
        value::BasicValue::Bool(v) => v.into_bound_py_any(py)?,
        value::BasicValue::Int64(v) => v.into_bound_py_any(py)?,
        value::BasicValue::Float32(v) => v.into_bound_py_any(py)?,
        value::BasicValue::Float64(v) => v.into_bound_py_any(py)?,
        value::BasicValue::Vector(v) => v
            .iter()
            .map(|v| basic_value_to_py_object(py, v))
            .collect::<PyResult<Vec<_>>>()?
            .into_bound_py_any(py)?,
        _ => {
            return Err(PyException::new_err(format!(
                "unsupported value type: {}",
                v.kind()
            )))
        }
    };
    Ok(result)
}

fn field_values_to_py_object<'py, 'a>(
    py: Python<'py>,
    values: impl Iterator<Item = &'a value::Value>,
) -> PyResult<Bound<'py, PyAny>> {
    let fields = values
        .map(|v| value_to_py_object(py, v))
        .collect::<PyResult<Vec<_>>>()?;
    Ok(PyTuple::new(py, fields)?.into_any())
}

fn value_to_py_object<'py>(py: Python<'py>, v: &value::Value) -> PyResult<Bound<'py, PyAny>> {
    let result = match v {
        value::Value::Null => py.None().into_bound(py),
        value::Value::Basic(v) => basic_value_to_py_object(py, v)?,
        value::Value::Struct(v) => field_values_to_py_object(py, v.fields.iter())?,
        value::Value::Collection(v) | value::Value::List(v) => {
            let rows = v
                .iter()
                .map(|v| field_values_to_py_object(py, v.0.fields.iter()))
                .collect::<PyResult<Vec<_>>>()?;
            PyList::new(py, rows)?.into_any()
        }
        value::Value::Table(v) => {
            let rows = v
                .iter()
                .map(|(k, v)| {
                    field_values_to_py_object(
                        py,
                        std::iter::once(&value::Value::from(k.clone())).chain(v.0.fields.iter()),
                    )
                })
                .collect::<PyResult<Vec<_>>>()?;
            PyList::new(py, rows)?.into_any()
        }
    };
    Ok(result)
}

fn basic_value_from_py_object<'py>(
    typ: &schema::BasicValueType,
    v: &Bound<'py, PyAny>,
) -> PyResult<value::BasicValue> {
    let result = match typ {
        schema::BasicValueType::Bytes => {
            value::BasicValue::Bytes(Arc::from(v.extract::<Vec<u8>>()?))
        }
        schema::BasicValueType::Str => value::BasicValue::Str(Arc::from(v.extract::<String>()?)),
        schema::BasicValueType::Bool => value::BasicValue::Bool(v.extract::<bool>()?),
        schema::BasicValueType::Int64 => value::BasicValue::Int64(v.extract::<i64>()?),
        schema::BasicValueType::Float32 => value::BasicValue::Float32(v.extract::<f32>()?),
        schema::BasicValueType::Float64 => value::BasicValue::Float64(v.extract::<f64>()?),
        schema::BasicValueType::Vector(elem) => value::BasicValue::Vector(Arc::from(
            v.extract::<Vec<Bound<'py, PyAny>>>()?
                .into_iter()
                .map(|v| basic_value_from_py_object(&elem.element_type, &v))
                .collect::<PyResult<Vec<_>>>()?,
        )),
        _ => {
            return Err(PyException::new_err(format!(
                "unsupported value type: {}",
                typ
            )))
        }
    };
    Ok(result)
}

fn field_values_from_py_object<'py>(
    schema: &schema::StructSchema,
    v: &Bound<'py, PyAny>,
) -> PyResult<value::FieldValues> {
    let list = v.extract::<Vec<Bound<'py, PyAny>>>()?;
    if list.len() != schema.fields.len() {
        return Err(PyException::new_err(format!(
            "struct field number mismatch, expected {}, got {}",
            schema.fields.len(),
            list.len()
        )));
    }
    Ok(value::FieldValues {
        fields: schema
            .fields
            .iter()
            .zip(list.into_iter())
            .map(|(f, v)| value_from_py_object(&f.value_type.typ, &v))
            .collect::<PyResult<Vec<_>>>()?,
    })
}

fn value_from_py_object<'py>(
    typ: &schema::ValueType,
    v: &Bound<'py, PyAny>,
) -> PyResult<value::Value> {
    let result = if v.is_none() {
        value::Value::Null
    } else {
        match typ {
            schema::ValueType::Basic(typ) => {
                value::Value::Basic(basic_value_from_py_object(typ, v)?)
            }
            schema::ValueType::Struct(schema) => {
                value::Value::Struct(field_values_from_py_object(schema, v)?)
            }
            schema::ValueType::Collection(schema) => {
                let list = v.extract::<Vec<Bound<'py, PyAny>>>()?;
                let values = list
                    .into_iter()
                    .map(|v| field_values_from_py_object(&schema.row, &v))
                    .collect::<PyResult<Vec<_>>>()?;
                match schema.kind {
                    schema::CollectionKind::Collection => {
                        value::Value::Collection(values.into_iter().map(|v| v.into()).collect())
                    }
                    schema::CollectionKind::List => {
                        value::Value::List(values.into_iter().map(|v| v.into()).collect())
                    }
                    schema::CollectionKind::Table => value::Value::Table(
                        values
                            .into_iter()
                            .map(|v| {
                                let mut iter = v.fields.into_iter();
                                let key = iter.next().unwrap().to_key().into_py_result()?;
                                Ok((
                                    key,
                                    value::ScopeValue(value::FieldValues {
                                        fields: iter.collect::<Vec<_>>(),
                                    }),
                                ))
                            })
                            .collect::<PyResult<BTreeMap<_, _>>>()?,
                    ),
                }
            }
        }
    };
    Ok(result)
}

#[pyclass(name = "OpArgSchema")]
pub struct PyOpArgSchema {
    value_type: crate::py::Pythonized<schema::EnrichedValueType>,
    analyzed_value: crate::py::Pythonized<plan::AnalyzedValueMapping>,
}

#[pymethods]
impl PyOpArgSchema {
    #[getter]
    fn value_type(&self) -> &crate::py::Pythonized<schema::EnrichedValueType> {
        &self.value_type
    }

    #[getter]
    fn analyzed_value(&self) -> &crate::py::Pythonized<plan::AnalyzedValueMapping> {
        &self.analyzed_value
    }
}

struct PyFunctionExecutor {
    py_function_executor: Py<PyAny>,
    num_positional_args: usize,
    kw_args_names: Vec<Py<PyString>>,
    result_type: schema::EnrichedValueType,

    enable_cache: bool,
    behavior_version: Option<u32>,
}

#[async_trait]
impl SimpleFunctionExecutor for Arc<PyFunctionExecutor> {
    async fn evaluate(&self, input: Vec<value::Value>) -> Result<value::Value> {
        let self = self.clone();
        let result = tokio::task::spawn_blocking(move || {
            Python::with_gil(|py| -> Result<_> {
                let mut args = Vec::with_capacity(self.num_positional_args);
                for v in input[0..self.num_positional_args].iter() {
                    args.push(value_to_py_object(py, v)?);
                }

                let kwargs = if self.kw_args_names.is_empty() {
                    None
                } else {
                    let mut kwargs = Vec::with_capacity(self.kw_args_names.len());
                    for (name, v) in self
                        .kw_args_names
                        .iter()
                        .zip(input[self.num_positional_args..].iter())
                    {
                        kwargs.push((name.bind(py), value_to_py_object(py, v)?));
                    }
                    Some(kwargs)
                };

                let result = self.py_function_executor.call(
                    py,
                    PyTuple::new(py, args.into_iter())?,
                    kwargs
                        .map(|kwargs| -> Result<_> { Ok(kwargs.into_py_dict(py)?) })
                        .transpose()?
                        .as_ref(),
                )?;

                Ok(value_from_py_object(
                    &self.result_type.typ,
                    result.bind(py),
                )?)
            })
        })
        .await??;
        Ok(result)
    }

    fn enable_cache(&self) -> bool {
        self.enable_cache
    }

    fn behavior_version(&self) -> Option<u32> {
        self.behavior_version
    }
}

pub(crate) struct PyFunctionFactory {
    pub py_function_factory: Py<PyAny>,
}

impl SimpleFunctionFactory for PyFunctionFactory {
    fn build(
        self: Arc<Self>,
        spec: serde_json::Value,
        input_schema: Vec<schema::OpArgSchema>,
        _context: Arc<FlowInstanceContext>,
    ) -> Result<(
        schema::EnrichedValueType,
        ExecutorFuture<'static, Box<dyn SimpleFunctionExecutor>>,
    )> {
        let (result_type, executor, kw_args_names, num_positional_args) =
            Python::with_gil(|py| -> anyhow::Result<_> {
                let mut args = vec![pythonize(py, &spec)?];
                let mut kwargs = vec![];
                let mut num_positional_args = 0;
                for arg in input_schema.into_iter() {
                    let py_arg_schema = PyOpArgSchema {
                        value_type: crate::py::Pythonized(arg.value_type.clone()),
                        analyzed_value: crate::py::Pythonized(arg.analyzed_value.clone()),
                    };
                    match arg.name.0 {
                        Some(name) => {
                            kwargs.push((name.clone(), py_arg_schema));
                        }
                        None => {
                            args.push(py_arg_schema.into_bound_py_any(py)?);
                            num_positional_args += 1;
                        }
                    }
                }

                let kw_args_names = kwargs
                    .iter()
                    .map(|(name, _)| PyString::new(py, name).unbind())
                    .collect::<Vec<_>>();
                let result = self.py_function_factory.call(
                    py,
                    PyTuple::new(py, args.into_iter())?,
                    Some(&kwargs.into_py_dict(py)?),
                )?;
                let (result_type, executor) = result
                    .extract::<(crate::py::Pythonized<schema::EnrichedValueType>, Py<PyAny>)>(py)?;
                Ok((
                    result_type.into_inner(),
                    executor,
                    kw_args_names,
                    num_positional_args,
                ))
            })?;

        let executor_fut = {
            let result_type = result_type.clone();
            async move {
                let executor = tokio::task::spawn_blocking(move || -> Result<_> {
                    let (enable_cache, behavior_version) =
                        Python::with_gil(|py| -> anyhow::Result<_> {
                            executor.call_method(py, "prepare", (), None)?;
                            let enable_cache = executor
                                .call_method(py, "enable_cache", (), None)?
                                .extract::<bool>(py)?;
                            let behavior_version = executor
                                .call_method(py, "behavior_version", (), None)?
                                .extract::<Option<u32>>(py)?;
                            Ok((enable_cache, behavior_version))
                        })?;
                    Ok(Box::new(Arc::new(PyFunctionExecutor {
                        py_function_executor: executor,
                        num_positional_args,
                        kw_args_names,
                        result_type,
                        enable_cache,
                        behavior_version,
                    })) as Box<dyn SimpleFunctionExecutor>)
                })
                .await??;
                Ok(executor)
            }
        };

        Ok((result_type, executor_fut.boxed()))
    }
}
