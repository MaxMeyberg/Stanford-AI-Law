import os
import json
import requests
import glob

def test_fox_case_files():
    # Get list of files in Fox Case directory
    fox_case_files = glob.glob("Fox Case/*")
    
    # Set API endpoint (change port if needed)
    api_url = "http://localhost:5001/api/process-documents"
    
    # Process each file and collect results
    all_results = []
    
    for file_path in fox_case_files:
        filename = os.path.basename(file_path)
        print(f"Processing {filename}...")
        
        # Open file and send to API
        with open(file_path, 'rb') as file:
            files = {'files': (filename, file)}
            response = requests.post(api_url, files=files)
        
        # Check if request was successful
        if response.status_code == 200:
            # Get JSON results
            results = response.json()
            
            # Add results to collection
            all_results.append({
                "filename": filename,
                "results": results
            })
            
            print(f"Successfully processed {filename}")
        else:
            print(f"Error processing {filename}: {response.status_code}")
            print(response.text)
    
    # Save all results to test.txt
    with open("test.txt", "w") as output_file:
        # Write each result
        for result in all_results:
            output_file.write(f"File: {result['filename']}\n")
            output_file.write("-" * 80 + "\n\n")
            
            # Write results in a readable format
            for doc_result in result['results']:
                output_file.write(f"Document: {doc_result.get('filename', 'Unknown')}\n\n")
                
                # Extract and write the content (remove HTML tags for readability)
                content = doc_result.get('marked_content', '')
                # Simple HTML tag removal (not perfect but helps readability)
                import re
                content = re.sub(r'<.*?>', '', content)
                output_file.write(content + "\n\n")
                
                output_file.write("-" * 40 + "\n\n")
            
            output_file.write("=" * 80 + "\n\n")
    
    print(f"All results have been saved to test.txt")

if __name__ == "__main__":
    test_fox_case_files() 