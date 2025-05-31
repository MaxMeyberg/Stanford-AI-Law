
mod pdf_to_json;
use anyhow::{Context, Result};
use serde_json;

fn main() -> Result<()> {

    
    let pdf_path = "pdfs/WW Guide 3-25-1.pdf";
    let json_output = pdf_to_json::pdf_to_json_converter(pdf_path).context("Pdf coulsnt convert to Json")?;

    let pretty_json = serde_json::to_string_pretty(&json_output).context("oof")?;
    // Testing for json unwrapping

    println!("{}", pretty_json);
    Ok(())
 
}