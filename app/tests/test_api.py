# Updated tests for OpenAI integration
# test_api.py: Contains unit tests for the API endpoints.
# Purpose: Ensures the API behaves correctly under various conditions, including
# valid and invalid inputs, and OpenAI API integration. Tests are designed to verify
# functionality, performance, and error handling, making the application production-ready.
# Dependencies: pytest for testing, FastAPI's TestClient for simulating HTTP requests,
# httpx for mocking OpenAI API calls.

import pytest
from fastapi.testclient import TestClient
from app.main import app
import httpx
from unittest.mock import AsyncMock, patch

client = TestClient(app)

@pytest.mark.asyncio
async def test_generate_pdf_valid_input():
    """
    Tests the /generate-pdf/ endpoint with a valid input and mocked OpenAI response.
    Purpose: Verifies that a valid single-word input generates a PDF response using OpenAI.
    """
    # Mock the OpenAI API response
    mock_response = {
        "choices": [{"message": {"content": "Mocked content about India"}}]
    }
    
    with patch("httpx.AsyncClient.post", new=AsyncMock(return_value=httpx.Response(200, json=mock_response))):
        response = client.post("/api/v1/generate-pdf/", json={"word": "India"})
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        assert "generated_India.pdf" in response.headers["content-disposition"]

def test_generate_pdf_invalid_input():
    """
    Tests the /generate-pdf/ endpoint with an invalid input (multi-word).
    Purpose: Ensures the API correctly rejects invalid inputs with appropriate error messages.
    """
    response = client.post("/api/v1/generate-pdf/", json={"word": "India Country"})
    assert response.status_code == 422  # Pydantic validation error
    assert "Input must be a single word" in response.text

def test_generate_pdf_empty_input():
    """
    Tests the /generate-pdf/ endpoint with an empty input.
    Purpose: Verifies that empty inputs are rejected with a clear error message.
    """
    response = client.post("/api/v1/generate-pdf/", json={"word": ""})
    assert response.status_code == 422
    assert "Input must be a single word" in response.text