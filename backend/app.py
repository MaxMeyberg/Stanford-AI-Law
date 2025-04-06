import os
import json
from flask_cors import CORS #allows you to call the flask functions
from flask import Flask, request, jsonify
import PyPDF2

from API_services.gpt import GPT_Process_PDFs



app = Flask(__name__)
CORS(app)

def extract_text(pdf_file):
    """Extract text from a PDF file"""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

@app.route('/api/process-documents', methods=['POST'])
def process_documents():
    # Get files from request
    files = request.files.getlist('files')
    
    # Error handling
    if not files or all(not file.filename for file in files):
        return jsonify({'error': 'No files provided'}), 400
    
    # Process PDFs one at a time
    results = []
    for index, file in enumerate(files):
        if file.filename.lower().endswith('.pdf'):
            # Extract text from PDF
            pdf_text = extract_text(file)
            
            # Process single PDF with GPT
            pdf_results = GPT_Process_PDFs([pdf_text])
            
            # Add file name to the result
            if pdf_results and len(pdf_results) > 0:
                pdf_results[0]["filename"] = file.filename
                results.append(pdf_results[0])
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
