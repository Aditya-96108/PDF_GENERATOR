# workflow.py: Automates the workflow from input to PDF generation.
# Purpose: Orchestrates the process of taking user inputs (word, pages, company, title, author, subject),
# generating content using OpenAI, and creating a professional PDF for Finlive Right.
# Dependencies: content_model for OpenAI API, pdf_service for PDF creation.

import os
from app.models.content_model import generate_content
from app.services.pdf_service import create_pdf

async def generate_content_and_pdf(word: str, pages: int, company: str, title: str, author: str, subject: str) -> str:
    """
    Automates the workflow for generating content and creating a PDF.
    Purpose: Takes user inputs, generates content using OpenAI, creates a multi-page PDF,
    and returns the file path. Optimized for Finlive Right’s corporate needs.
    Input: Keyword, number of pages, company, title, author, subject.
    Output: The file path of the generated PDF.
    Error Handling: Raises exceptions for invalid inputs or processing errors.
    """
    # Validate input
    if not word or len(word.split()) > 1:
        raise ValueError("Input must be a single word")
    
    # Generate content using OpenAI
    content = await generate_content(word, pages, company, title, author, subject)
    
    # Define output PDF path
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, f"generated_{word}.pdf")
    
    # Create PDF
    pdf_path = create_pdf(word, content, pdf_path, pages, company, title, author, subject)
    
    return pdf_path