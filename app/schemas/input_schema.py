# input_schema.py: Defines Pydantic schemas for input validation.
# Purpose: Ensures API inputs (word, pages, company, title, author, subject) are valid
# and conform to expected formats. Optimized for Finlive Right's corporate PDF requirements.
# Dependencies: Pydantic for data validation.

from pydantic import BaseModel, validator

class InputWord(BaseModel):
    """
    Pydantic schema for validating inputs for PDF generation.
    Purpose: Ensures all inputs are valid, with a single word, valid page count,
    and non-empty corporate details for professional PDF generation.
    """
    word: str
    pages: int
    company: str
    title: str
    author: str
    subject: str

    @validator("word")
    def validate_word(cls, value):
        """
        Validates that the keyword is a single, non-empty word.
        """
        if not value or len(value.split()) > 1:
            raise ValueError("Keyword must be a single word")
        return value.strip()

    @validator("pages")
    def validate_pages(cls, value):
        """
        Validates that the number of pages is between 1 and 5.
        """
        if value < 1 or value > 5:
            raise ValueError("Number of pages must be between 1 and 5")
        return value

    @validator("company", "title", "author", "subject")
    def validate_non_empty(cls, value):
        """
        Validates that corporate fields are non-empty.
        """
        if not value.strip():
            raise ValueError("Field cannot be empty")
        return value.strip()