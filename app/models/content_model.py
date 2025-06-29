# content_model.py: Implements content generation using the OpenAI API.
# Purpose: Generates professional financial content for Finlive Right with exactly three paragraphs
# (~80-100 words each, ~8 lines in PDF) per page, based on user inputs.
# The OpenAI API key is hardcoded as per user request (not recommended for production).
# Dependencies: httpx for async HTTP requests.

import httpx
import logging
import os


# Configure logging for debugging and monitoring
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenAI API configuration with hardcoded API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-3.5-turbo"

async def generate_content(word: str, pages: int, company: str, title: str, author: str, subject: str) -> str:
    """
    Generates content using OpenAI's API for Finlive Right’s corporate PDFs.
    Purpose: Creates a professional document with exactly three paragraphs (~80-100 words each, ~8 lines)
    per page, based on the keyword, tailored to Finlive Right’s financial services mission.
    Input: Keyword, number of pages (1-5), company, title, author, subject.
    Output: A string with exactly three paragraphs per page, separated by double newlines.
    Error Handling: Raises exceptions for API failures.
    """
    if not OPENAI_API_KEY:
        raise ValueError("OpenAI API key is not provided")

    # Craft a prompt for Finlive Right’s financial services
    prompt = (
        f"Generate a professional document for {company}, a data-driven financial services company "
        f"focused on helping clients make informed investment decisions through market trend analysis, "
        f"personalized financial guidance, and innovative solutions. The document should be about '{word}' "
        f"and align with the subject '{subject}'. It must reflect Finlive Right’s mission to provide "
        f"data-driven insights, personalized plans, and accurate forecasting. Create content for {pages} page(s), "
        f"with exactly three paragraphs per page. Each paragraph must be 200-300 words "
        f"and focus on distinct aspects of '{word}' (e.g., strategies, benefits, trends). Ensure the tone is professional, "
        f"engaging, and suitable for a corporate PDF titled '{title}' authored by '{author}'. "
        f"Separate each paragraph with exactly two newlines ('\n\n') and ensure exactly {3 * pages} paragraphs are generated, "
        f"with no additional text or headings outside the paragraphs."
    )

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "You are a professional assistant creating content for Finlive Right, a financial services company specializing in data-driven investment solutions."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 350 * pages,  # Increased to ensure 3 paragraphs of ~80-100 words each
        "temperature": 0.7
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(OPENAI_URL, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Extract the generated content
            result = response.json()
            content = result["choices"][0]["message"]["content"].strip()
            logger.info(f"Generated content for word '{word}': {content[:50]}...")
            return content
            
    except httpx.HTTPStatusError as e:
        logger.error(f"OpenAI API request failed: {str(e)}")
        raise Exception(f"Failed to generate content: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error during content generation: {str(e)}")
        raise Exception(f"Unexpected error: {str(e)}")