# routes.py: Defines API endpoints for the application.
# Purpose: Handles HTTP requests, validates input, triggers the workflow, and returns responses.
# Updated to accept new input fields (word, pages, company, title, author, subject) for Finlive Right's
# corporate PDF generation. Uses FastAPI's APIRouter and Pydantic schemas for validation.
# Dependencies: FastAPI, Pydantic, and custom services.

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.schemas.input_schema import InputWord
from app.services.workflow import generate_content_and_pdf
import os

router = APIRouter()

@router.post("/generate-pdf/", response_class=FileResponse)
async def generate_pdf(input_data: InputWord):
    """
    Endpoint to generate a PDF based on user inputs.
    Purpose: Accepts a keyword, number of pages, and corporate details, processes them through the
    OpenAI model, generates a professional PDF, and returns it as a downloadable file.
    Input: JSON payload with fields: word, pages, company, title, author, subject.
    Output: A PDF file containing generated content.
    Error Handling: Returns a 400 error if the workflow fails.
    """
    try:
        # Call the workflow with all input fields
        pdf_path = await generate_content_and_pdf(
            word=input_data.word,
            pages=input_data.pages,
            company=input_data.company,
            title=input_data.title,
            author=input_data.author,
            subject=input_data.subject
        )
        
        # Check if PDF was created successfully
        if not os.path.exists(pdf_path):
            raise HTTPException(status_code=500, detail="Failed to generate PDF")
        
        # Return the PDF file as a response
        return FileResponse(
            path=pdf_path,
            filename=f"generated_{input_data.word}.pdf",
            media_type="application/pdf"
        )
    except Exception as e:
        # Handle any errors during processing
        raise HTTPException(status_code=400, detail=f"Error processing request: {str(e)}")