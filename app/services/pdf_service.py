# pdf_service.py: Handles PDF generation for Finlive Right’s corporate documents.
# Purpose: Creates professional, multi-page PDFs with three paragraphs (~8 lines each) per page,
# with optimized margins and spacing to minimize empty space. Supports Unicode for Indian languages.
# Dependencies: reportlab for PDF creation.

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import PageTemplate, Frame
import os

def create_pdf(word: str, content: str, output_path: str, pages: int, company: str, title: str, author: str, subject: str) -> str:
    """
    Creates a multi-page PDF with corporate styling for Finlive Right.
    Purpose: Generates a PDF with three paragraphs (~80-100 words, ~8 lines) per page,
    with reduced margins and optimized spacing to minimize empty space.
    Input:
        - word: The keyword used in the document.
        - content: The generated content from OpenAI.
        - output_path: File path to save the PDF.
        - pages: Number of pages requested (1-5).
        - company, title, author, subject: Corporate metadata.
    Output: The path to the generated PDF file.
    """
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        title=title,
        author=author,
        subject=subject,
        creator=company,
        topMargin=0.5 * inch,  # Reduced to increase content space
        bottomMargin=0.5 * inch,  # Reduced
        leftMargin=0.5 * inch,  # Reduced
        rightMargin=0.5 * inch  # Reduced
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        name='Title',
        fontSize=16,
        leading=20,
        spaceAfter=10,  # Reduced spacing
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        name='Body',
        fontSize=11,  # Slightly reduced to fit ~8 lines per paragraph
        leading=13,  # Adjusted for ~8 lines per paragraph
        spaceAfter=8,  # Reduced spacing
        fontName='Helvetica'
    )

    def add_header_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica-Bold', 9)  # Slightly smaller font
        canvas.drawString(0.5 * inch, A4[1] - 0.3 * inch, f"{company} - {title}")
        canvas.setFont('Helvetica', 7)  # Smaller footer font
        canvas.drawString(0.5 * inch, 0.3 * inch, f"Page {canvas.getPageNumber()} | Author: {author}")
        canvas.restoreState()

    # Create a frame with increased height to use more page space
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height - 0.6 * inch, id='normal')
    template = PageTemplate(id='main', frames=[frame], onPage=add_header_footer)
    doc.addPageTemplates([template])

    paragraphs = content.strip().split('\n\n')
    flowables = []

    # Title only on the first page
    flowables.append(Paragraph(f"{word.capitalize()}", title_style))
    flowables.append(Spacer(1, 10))  # Reduced spacing

    # Add exactly 3 paragraphs per page
    for page in range(pages):
        start = page * 3
        end = start + 3
        block = []

        # Use only available paragraphs or pad with empty ones if needed
        page_paragraphs = paragraphs[start:end]
        while len(page_paragraphs) < 3:  # Ensure 3 paragraphs per page
            page_paragraphs.append("Placeholder paragraph: Content generation incomplete. Please try again.")

        for para in page_paragraphs:
            block.append(Paragraph(para.strip(), body_style))
            block.append(Spacer(1, 8))  # Reduced spacing

        flowables.append(KeepTogether(block))

        if page < pages - 1:
            flowables.append(PageBreak())

    doc.build(flowables)
    return output_path