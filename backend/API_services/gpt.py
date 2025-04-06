from dotenv import load_dotenv
from openai import OpenAI
import PyPDF2
from typing import List
import json
import os

load_dotenv("../.env")

def GPT_Process_PDFs(pdf_contents: List[str]):
    system_instructions = """You are a document review assistant. Analyze the document sentence by sentence and:

    1. Output each sentence on a new line
    2. For any content that potentially needs redaction (legal advice, PII, or sensitive corporate information), wrap it in <mark>highlighted text</mark> tags
    3. Preserve all paragraph breaks and document structure
    4. EXAMPLES of confidences:

    LOW:
    "The project will be completed by Q4."
    "John mentioned he would review the documents."
    "The team met with external consultants yesterday."
    "We expect positive market response."
    "The software update includes performance improvements."

    MED:
    "We project $2M in revenue for the next quarter."
    "The merger discussions are proceeding as planned."
    "Attorney Smith suggested we review the contract."
    "Contact Mike at extension 4567 for details."
    "The new algorithm improves accuracy by 45%."

    HIGH:
    "SSN: 123-45-6789"
    "Attorney-client privileged: Legal counsel advises against proceeding with the patent."
    "Project Neptune will launch on 3/15/24 with estimated revenue of $50M."
    "Login credentials: username: admin, password: Secure123!"
    "Sarah Jones (sarah.jones@company.com, 555-123-4567) will lead the confidential acquisition of XYZ Corp."

    
    Format example:
    This is a normal sentence.
    In this meeting, <mark probability_of_confidentiality=[(LOW='not very confident)]>Attorney Jane Smith advised against the merger</mark> due to concerns.
    Please contact <mark>john.doe@company.com</mark> for more information.
    The project timeline remains unchanged."""

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    results = []
    for index, content in enumerate(pdf_contents):
        response = client.chat.completions.create(
            model="o1",
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": content}
            ]
        )
        
        result = {
            "document_index": index,
            "marked_content": response.choices[0].message.content
        }
        results.append(result)
    
    return results
