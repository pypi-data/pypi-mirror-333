use pyo3::{prelude::*, types::PyList};

mod edit_distance;

#[derive(Debug)]
enum EditDistanceItem {
    String(String),
    Int(i64),
    Float(f64),
    Bool(bool),
    Object(Py<PyAny>),
}

impl PartialEq for EditDistanceItem {
    fn eq(&self, other: &Self) -> bool {
        match (self, other) {
            (EditDistanceItem::String(a), EditDistanceItem::String(b)) => a == b,
            (EditDistanceItem::Int(a), EditDistanceItem::Int(b)) => a == b,
            (EditDistanceItem::Float(a), EditDistanceItem::Float(b)) => a == b,
            (EditDistanceItem::Bool(a), EditDistanceItem::Bool(b)) => a == b,
            (EditDistanceItem::Object(a), EditDistanceItem::Object(b)) => {
                // Use Python's __eq__ by acquiring the GIL
                Python::with_gil(|py| {
                    // Bind the Py<PyAny> to this thread-local context
                    let a_bound = a.bind(py);
                    let b_bound = b.bind(py);

                    // Call eq method between the two objects
                    match a_bound.eq(&b_bound) {
                        Ok(val) => val,
                        Err(_) => false, // If there's an error, consider them not equal
                    }
                })
            }
            // If types don't match, they're not equal
            _ => false,
        }
    }
}

impl<'source> FromPyObject<'source> for EditDistanceItem {
    fn extract_bound(obj: &Bound<'source, PyAny>) -> PyResult<Self> {
        // Try to extract each supported type in order
        if let Ok(val) = obj.extract::<String>() {
            return Ok(EditDistanceItem::String(val));
        } else if let Ok(val) = obj.extract::<i64>() {
            return Ok(EditDistanceItem::Int(val));
        } else if let Ok(val) = obj.extract::<f64>() {
            return Ok(EditDistanceItem::Float(val));
        } else if let Ok(val) = obj.extract::<bool>() {
            return Ok(EditDistanceItem::Bool(val));
        } else {
            // For any other type, store the Python object for later comparison
            let py_obj = obj.clone().unbind();
            return Ok(EditDistanceItem::Object(py_obj));
        }
    }
}

#[pyfunction(name = "word_error_rate")]
fn word_error_rate_py(predictions: Vec<String>, references: Vec<String>) -> PyResult<Vec<f64>> {
    let left_vec: Vec<&str> = predictions.iter().map(|x| x.as_str()).collect();
    let right_vec: Vec<&str> = references.iter().map(|x| x.as_str()).collect();
    let result = edit_distance::word_error_rate(&left_vec, &right_vec);
    Ok(result)
}

#[pyfunction(name = "word_edit_distance")]
fn word_edit_distance_py(
    predictions: Vec<String>,
    references: Vec<String>,
) -> PyResult<Vec<usize>> {
    let left_vec: Vec<&str> = predictions.iter().map(|x| x.as_str()).collect();
    let right_vec: Vec<&str> = references.iter().map(|x| x.as_str()).collect();
    let result = edit_distance::word_edit_distance(&left_vec, &right_vec);
    Ok(result)
}

#[pyfunction(name = "word_mean_error_rate")]
fn word_mean_error_rate_py(predictions: Vec<String>, references: Vec<String>) -> PyResult<f64> {
    let left_vec: Vec<&str> = predictions.iter().map(|x| x.as_str()).collect();
    let right_vec: Vec<&str> = references.iter().map(|x| x.as_str()).collect();
    let result = edit_distance::word_mean_error_rate(&left_vec, &right_vec);
    Ok(result)
}

#[pyfunction(name = "character_error_rate")]
fn character_error_rate_py(
    predictions: Vec<String>,
    references: Vec<String>,
) -> PyResult<Vec<f64>> {
    let left_vec: Vec<&str> = predictions.iter().map(|x| x.as_str()).collect();
    let right_vec: Vec<&str> = references.iter().map(|x| x.as_str()).collect();
    let result = edit_distance::character_error_rate(&left_vec, &right_vec);
    Ok(result)
}

#[pyfunction(name = "character_edit_distance")]
fn character_edit_distance_py(
    predictions: Vec<String>,
    references: Vec<String>,
) -> PyResult<Vec<usize>> {
    let left_vec: Vec<&str> = predictions.iter().map(|x| x.as_str()).collect();
    let right_vec: Vec<&str> = references.iter().map(|x| x.as_str()).collect();
    let result = edit_distance::character_edit_distance(&left_vec, &right_vec);
    Ok(result)
}

#[pyfunction(name = "character_mean_error_rate")]
fn character_mean_error_rate_py(
    predictions: Vec<String>,
    references: Vec<String>,
) -> PyResult<f64> {
    let left_vec: Vec<&str> = predictions.iter().map(|x| x.as_str()).collect();
    let right_vec: Vec<&str> = references.iter().map(|x| x.as_str()).collect();
    let result = edit_distance::character_mean_error_rate(&left_vec, &right_vec);
    Ok(result)
}

#[pyfunction(name = "universal_error_rate")]
fn universal_error_rate_py(
    predictions: &Bound<PyList>,
    references: &Bound<PyList>,
) -> PyResult<Vec<f64>> {
    // Create vectors to store the converted data
    let pred_vecs: Vec<Vec<EditDistanceItem>> = convert_to_edit_distance_item_vec(predictions)?;
    let ref_vecs: Vec<Vec<EditDistanceItem>> = convert_to_edit_distance_item_vec(references)?;

    // Create the vectors of references to vectors that the edit_distance function expects
    let pred_vec_refs: Vec<&Vec<EditDistanceItem>> = pred_vecs.iter().collect();
    let ref_vec_refs: Vec<&Vec<EditDistanceItem>> = ref_vecs.iter().collect();

    // Call a modified edit_distance implementation that works with EditDistanceItem
    let result = edit_distance::universal_error_rate(&pred_vec_refs, &ref_vec_refs);

    Ok(result)
}

#[pyfunction(name = "universal_edit_distance")]
fn universal_edit_distance_py(
    predictions: &Bound<PyList>,
    references: &Bound<PyList>,
) -> PyResult<Vec<usize>> {
    // Create vectors to store the converted data
    let pred_vecs: Vec<Vec<EditDistanceItem>> = convert_to_edit_distance_item_vec(predictions)?;
    let ref_vecs: Vec<Vec<EditDistanceItem>> = convert_to_edit_distance_item_vec(references)?;

    // Create the vectors of references to vectors that the edit_distance function expects
    let pred_vec_refs: Vec<&Vec<EditDistanceItem>> = pred_vecs.iter().collect();
    let ref_vec_refs: Vec<&Vec<EditDistanceItem>> = ref_vecs.iter().collect();

    // Call a modified edit_distance implementation that works with EditDistanceItem
    let result = edit_distance::universal_edit_distance(&pred_vec_refs, &ref_vec_refs);

    Ok(result)
}

fn convert_to_edit_distance_item_vec(
    pylist: &Bound<PyList>,
) -> PyResult<Vec<Vec<EditDistanceItem>>> {
    // Create vectors to store the converted data
    let mut vecs: Vec<Vec<EditDistanceItem>> = Vec::with_capacity(pylist.len());

    // Extract the data from Python
    for i in 0..pylist.len() {
        let item = pylist.get_item(i)?;
        let list = item.downcast::<PyList>()?;

        let mut inner: Vec<EditDistanceItem> = Vec::with_capacity(list.len());

        // Extract items from the inner lists, converting to EditDistanceItem
        for j in 0..list.len() {
            inner.push(list.get_item(j)?.extract::<EditDistanceItem>()?);
        }

        vecs.push(inner);
    }

    // Create the vectors of references to vectors that the edit_distance function expects
    return Ok(vecs);
}

/// A Python module implemented in Rust.
#[pymodule]
fn universal_edit_distance(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(word_error_rate_py, m)?)?;
    m.add_function(wrap_pyfunction!(character_error_rate_py, m)?)?;
    m.add_function(wrap_pyfunction!(universal_error_rate_py, m)?)?;
    m.add_function(wrap_pyfunction!(word_edit_distance_py, m)?)?;
    m.add_function(wrap_pyfunction!(character_edit_distance_py, m)?)?;
    m.add_function(wrap_pyfunction!(word_mean_error_rate_py, m)?)?;
    m.add_function(wrap_pyfunction!(character_mean_error_rate_py, m)?)?;
    m.add_function(wrap_pyfunction!(universal_edit_distance_py, m)?)?;
    Ok(())
}
