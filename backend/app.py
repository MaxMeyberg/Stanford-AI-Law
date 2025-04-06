import os
import json
import uuid
from flask_cors import CORS
from flask import Flask, request, jsonify, send_from_directory, render_template, url_for
import PyPDF2

from API_services.gpt import GPT_Process_PDFs
from API_services.cloud_convert import process_file_for_gpt

# Create Flask app
app = Flask(__name__, 
            static_folder='../frontend/static',
            template_folder='../frontend/templates')

# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*"}})

# Create a directory to store uploaded PDFs
UPLOAD_FOLDER = os.path.join('..', 'frontend', 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_text(pdf_file):
    """Extract text from a PDF file"""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

@app.route('/')
def index():
    """Serve the frontend interface"""
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/api/process-documents', methods=['POST'])
def process_documents():
    """Process documents using CloudConvert and GPT"""
    # Get files from request
    files = request.files.getlist('files')
    
    # Error handling
    if not files or all(not file.filename for file in files):
        return jsonify({'error': 'No files provided'}), 400
    
    # Process files one at a time
    results = []
    for file in files:
        try:
            # Convert to PDF and process with GPT in one step
            file_results = process_file_for_gpt(file, GPT_Process_PDFs)
            
            # Add results to the list
            if file_results and len(file_results) > 0:
                result = file_results[0]
                
                # If we have a PDF path from the conversion
                if 'pdf_path' in result and os.path.exists(result['pdf_path']):
                    # Create a unique filename for the PDF
                    pdf_filename = f"{uuid.uuid4().hex}.pdf"
                    pdf_destination = os.path.join(UPLOAD_FOLDER, pdf_filename)
                    
                    # Copy the PDF to the static folder
                    os.rename(result['pdf_path'], pdf_destination)
                    
                    # Add PDF URL to the result
                    result['pdf_url'] = url_for('uploaded_file', filename=pdf_filename)
                
                results.append(result)
                
        except Exception as e:
            # Log the error but continue processing other files
            print(f"Error processing file {file.filename}: {str(e)}")
            # Add error to results
            results.append({
                "filename": file.filename,
                "error": str(e),
                "marked_content": f"<p>Error processing file: {str(e)}</p>"
            })
    
    return jsonify(results)

if __name__ == '__main__':
    # Create directories if they don't exist
    os.makedirs('../frontend/templates', exist_ok=True)
    os.makedirs('../frontend/static', exist_ok=True)
    
    # Create a basic index.html if it doesn't exist
    if not os.path.exists('../frontend/templates/index.html'):
        with open('../frontend/templates/index.html', 'w') as f:
            f.write('''<!DOCTYPE html>
<html>
<head>
    <title>Document Analysis Tool</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .upload-container { border: 2px dashed #ccc; padding: 20px; text-align: center; }
        .results { margin-top: 20px; }
        .document-container { margin-bottom: 40px; border: 1px solid #ddd; padding: 15px; border-radius: 5px; }
        .pdf-viewer { width: 100%; height: 600px; border: 1px solid #ccc; margin-bottom: 20px; }
        .highlighted-text { margin-top: 20px; border: 1px solid #ccc; padding: 10px; }
        mark.low { background-color: yellow; }
        mark.medium { background-color: orange; }
        mark.high { background-color: red; }
        .legend { margin-top: 10px; font-size: 14px; }
        .legend-item { display: inline-block; margin-right: 20px; }
        .legend-color { display: inline-block; width: 20px; height: 14px; margin-right: 5px; vertical-align: middle; }
        .low-color { background-color: yellow; }
        .medium-color { background-color: orange; }
        .high-color { background-color: red; }
    </style>
</head>
<body>
    <h1>Document Analysis Tool</h1>
    
    <div class="upload-container">
        <h2>Upload Documents</h2>
        <form id="uploadForm" enctype="multipart/form-data">
            <input type="file" id="fileInput" name="files" multiple accept=".pdf,.docx,.xlsx">
            <button type="submit">Analyze Documents</button>
        </form>
    </div>
    
    <div class="results" id="results"></div>

    <script>
        document.getElementById('uploadForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData();
            const fileInput = document.getElementById('fileInput');
            
            for (let i = 0; i < fileInput.files.length; i++) {
                formData.append('files', fileInput.files[i]);
            }
            
            document.getElementById('results').innerHTML = '<p>Processing documents... This may take a while.</p>';
            
            try {
                const response = await fetch('/api/process-documents', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                let resultsHTML = '<h2>Analysis Results</h2>';
                
                if (data.length === 0) {
                    resultsHTML += '<p>No results returned.</p>';
                } else {
                    // Add legend
                    resultsHTML += `
                        <div class="legend">
                            <p><strong>Sensitivity Legend:</strong></p>
                            <div class="legend-item"><span class="legend-color low-color"></span> Low Sensitivity</div>
                            <div class="legend-item"><span class="legend-color medium-color"></span> Medium Sensitivity</div>
                            <div class="legend-item"><span class="legend-color high-color"></span> High Sensitivity</div>
                        </div>
                    `;
                    
                    data.forEach(result => {
                        resultsHTML += `<div class="document-container">`;
                        resultsHTML += `<h3>Results for ${result.filename}</h3>`;
                        
                        if (result.error) {
                            resultsHTML += `<p>Error: ${result.error}</p>`;
                        } else {
                            // Display PDF if available
                            if (result.pdf_url) {
                                resultsHTML += `
                                    <h4>Original Document</h4>
                                    <iframe class="pdf-viewer" src="${result.pdf_url}"></iframe>
                                `;
                            }
                            
                            // Display highlighted text
                            resultsHTML += `
                                <h4>Document with Highlighted Sensitive Information</h4>
                                <div class="highlighted-text">${result.marked_content}</div>
                            `;
                        }
                        
                        resultsHTML += `</div>`;
                    });
                }
                
                document.getElementById('results').innerHTML = resultsHTML;
                
            } catch (error) {
                document.getElementById('results').innerHTML = `<p>Error: ${error.message}</p>`;
            }
        });
    </script>
</body>
</html>''')
    
    app.run(debug=True, port=5001)
