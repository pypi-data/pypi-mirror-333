use pyo3::prelude::*;
use std::sync::Arc;
use std::path::PathBuf;
use anyhow::{anyhow};

mod db;

#[pyclass]
struct PyPathEntry {
    #[pyo3(get)]
    path: String,
    #[pyo3(get)]
    flags: u32
}

#[pyclass]
pub struct Db {
    db: Arc<db::Db>
}

#[pyfunction]
fn flags_to_string(input: u32) -> anyhow::Result<String> {
    let flags = db::Flags::from_bits_retain(input);
    Ok(flags.to_string())
}

#[pyfunction]
fn load_db(path: PathBuf) -> anyhow::Result<Db> {
    let db = match db::db_read(&path) {
        Err(_) => return Err(anyhow!("failed to load database")),
        Ok(e) => e
    };

    Ok(Db { db: Arc::new(db) })
}

#[pymethods]
impl Db {
    fn path_children(slf: PyRef<'_, Self>, path: &str) -> PyResult<Vec<PyPathEntry>> {
        let mut children: Vec<PyPathEntry> = Vec::new();
        for entry in slf.db.path_children(path, true) {

            log::trace!("{}", entry.flags.as_u32());

            children.push( {
                PyPathEntry {
                    path: entry.path.clone(),
                    flags: entry.flags.as_u32()
                }
            });
        }

        Ok(children)
    }

    fn common_prefix_path(slf: PyRef<'_, Self>) -> PyResult<String> {
        Ok(slf.db.common_prefix_path())
    }

    fn is_annotated(slf: PyRef<'_, Self>) -> PyResult<bool> {
        Ok(slf.db.is_annotated())
    }

    fn path_count(slf: PyRef<'_, Self>) -> PyResult<u64> {
        Ok(slf.db.meta.pathcount)
    }

    fn path_filter(slf: PyRef<'_, Self>, filter: &str) -> anyhow::Result<Db> {
        let filtered_db = match slf.db.filter(&filter) {
            Err(_) => return Err(anyhow!("failed to filter paths")),
            Ok(e) => e
        };

        Ok(Db { db: Arc::new(filtered_db) })
    }

    fn calculate_permissions(slf: PyRef<'_, Self>, user: &str) -> anyhow::Result<Db> {
        let new_db = match slf.db.calculate_permissions(&user) {
            Err(_) => return Err(anyhow!("failed to calculate permissions")),
            Ok(e) => e
        };
        Ok(Db { db: Arc::new(new_db) })
    }
}

#[pymodule]
fn _lib(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(load_db, m)?)?;
    m.add_function(wrap_pyfunction!(flags_to_string, m)?)?;
    Ok(())
}
