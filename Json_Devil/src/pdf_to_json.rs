use serde_json::{json, Value};
use std::path::Path;
use anyhow::Result;

pub fn pdf_to_json_converter<P: AsRef<Path>>(pdf_path: P) -> Result<Value> {
    let path_ref = pdf_path.as_ref();
    let bytes = std::fs::read(path_ref)?;
    let out = pdf_extract::extract_text_from_mem(&bytes)?;

    let filename = path_ref
        .file_name()
        .unwrap_or_default()
        .to_string_lossy()
        .into_owned();

    let json_output = json!({
        "filename": filename,
        "extracted_text": out
    });

    Ok(json_output)
}