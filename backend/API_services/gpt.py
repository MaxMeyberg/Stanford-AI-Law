from dotenv import load_dotenv
from openai import OpenAI
import PyPDF2
from typing import List
import json
import os

load_dotenv("../.env")

def GPT_Process_PDFs(pdf_contents: List[str]):
    system_instructions = """You are a document review assistant. Analyze the document sentence by sentence and:

        For each document:
    1. First, read and understand the entire document to grasp its overall purpose, structure, and context.
    2. Identify sections or passages that contain potentially sensitive information requiring redaction.
    3. Consider the relationship between different parts of the document - some information might be sensitive only in the context of other information.
    4. For any content that potentially needs redaction, wrap it in <mark class="[low|medium|high]">highlighted text</mark> tags.
    5. Determine classification levels based on:
       - HIGH: Legal advice, attorney-client communications, explicit trade secrets, strategic decisions, confidential financial projections, litigation strategy
       - MEDIUM: Business sensitive information, financial data not publicly disclosed, technical details, personnel information
       - LOW: General business information with minimal sensitivity, contact information, job titles

    Format example:
    <mark class="high">ATTORNEY-CLIENT PRIVILEGED AND CONFIDENTIAL</mark>
    <mark class="high">WORK PRODUCT PREPARED IN ANTICIPATION OF LITIGATION</mark>

    <mark class="high">MEMORANDUM</mark>

    DATE: September 15, 2024
    <mark class="high">TO: Board of Directors, Quantum Innovations, Inc.</mark>
    <mark class="high">FROM: Eleanor Richardson, General Counsel</mark>
    
    1. Output each sentence on a new line
    2. For any content that potentially needs redaction (legal advice, PII, or sensitive corporate information), wrap it in <mark, confidence>highlighted text</mark> tags
    3. Preserve all paragraph breaks and document structure
    4. If the document looks like an email from a lawyer, it has confidence = HIGH
    5. EXAMPLES of confidences:

    LOW:
    "The legal team will review this next week."
    "We should check with counsel before proceeding."
    "The project details are still being finalized."
    "Management is considering several options."
     "The new algorithm improves accuracy by 45%."

    MED:
    "We project $2M in revenue for the next quarter."
    "The merger discussions are proceeding as planned."
    "Contact Mike at extension 4567 for details."
    "This information should be kept internal."
    "Sarah Jones (sarah.jones@company.com, 555-123-4567) will lead the confidential acquisition of XYZ Corp."

    HIGH:
    "SSN: 123-45-6789"
    "Attorney-client privileged: Legal counsel advises against proceeding with the patent."
    "Attorney Jane Smith advises against proceeding with the merger due to antitrust concerns."
    "Our legal department confirms this falls under attorney-client privilege."
    "The confidential source code uses a proprietary algorithm that [technical details]."
    "Attorney Smith suggested we review the contract."
    "Legal analysis: The contract terms violate section 8.2 of the Sherman Act."
    "Internal memo: Project Phoenix will acquire CompanyX for $50M, pending board approval."
    "Login credentials: username: admin, password: Secure123!"

    
    Format example:
        CONFIDENTIAL INTERNAL MEMO
        Strategic Planning 2024-2025
        Date: June 12, 2024

        EXECUTIVE SUMMARY

        The following document outlines Acme Corporation's strategic initiatives for the upcoming fiscal year. All information contained herein is strictly confidential and for internal use only.

        MARKET ANALYSIS

        Our current market share stands at 23%, representing a 3% increase from the previous fiscal year. <mark probability="Medium">Recent consumer data indicates a significant shift toward cloud-based solutions in our target demographic.</mark> This trend aligns with our product development roadmap.

        <mark probability="High">Our competitive analysis reveals that RivalTech is planning to launch a competing service in Q4, potentially undercutting our pricing by 15-20%.</mark> Standard market fluctuations remain within expected parameters for Q2-Q3.

        LEGAL CONSIDERATIONS

        <mark probability="High">As per our meeting with outside counsel on May 30, we have been advised to proceed with caution regarding the Johnson patent acquisition due to potential antitrust scrutiny.</mark> The regulatory environment remains challenging but navigable.

        <mark probability="Medium">The pending litigation with EastCorp may impact our Q3 financial reporting if not resolved by August.</mark> Standard compliance measures have been implemented across all departments.

        <mark probability="Low">The legal department recommends reviewing all vendor contracts before renewal.</mark> All existing partnerships are currently in good standing.

        FINANCIAL PROJECTIONS

        Revenue projections for FY2024-2025 are as follows:
        - Q1: $42.3M
        - <mark probability="Medium">Q2: $56.7M (including $12M from Project Phoenix launch)</mark>
        - Q3: $61.2M
        - <mark probability="High">Q4: $78.5M (contingent on successful acquisition of MicroSystems Inc. for $145M, currently in final negotiation stages)</mark>

        <mark probability="High">Our CFO has prepared contingency budgets in the event the SEC inquiry into our accounting practices extends beyond July.</mark> These alternative projections are available upon request from the finance department.

        HUMAN RESOURCES

        The current headcount is 1,245 full-time employees across all divisions. <mark probability="Medium">We anticipate a 7% reduction in workforce following the automation initiative in the manufacturing division.</mark> Standard retention strategies remain in place.

        <mark probability="High">HR Director Maria Chen has proposed a confidential restructuring of the executive compensation package, reducing bonuses by 22% while increasing equity distributions, potentially saving $3.4M annually.</mark> Employee satisfaction surveys indicate stable morale across departments.

        TECHNOLOGY ROADMAP

        <mark probability="Medium">Our proprietary algorithm for customer prediction has achieved 89% accuracy in testing environments.</mark> The IT infrastructure upgrade is proceeding on schedule and within budget.

        <mark probability="High">CTO Ron Stevens recommends accelerating the acquisition of QuantumSoft to secure their machine learning patents before competitors can approach them.</mark> The development team is currently focused on security enhancements to our core platform.

        <mark probability="Low">We should review the AWS architecture for potential cost savings.</mark> All systems are currently operating at optimal efficiency.

        NEXT STEPS

        1. <mark probability="Medium">Finalize the terms of the MicroSystems acquisition by June 30</mark>
        2. Complete the quarterly compliance review
        3. <mark probability="High">Prepare documentation for potential DOJ inquiry as advised by legal counsel Sarah Johnson</mark>
        4. Update the board on Project Phoenix milestones

        Please direct any questions to <mark probability="Low">david.chen@acmecorp.com</mark> or ext. 4567.

        Prepared by:
        <mark probability="Low">Jennifer Williams, Chief Strategy Officer</mark>
    
    """

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    #TODO: Ask Yaroslav how to input pdfs
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
