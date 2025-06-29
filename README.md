Finlive Right AI PDF Generator

Overview

This is a production-ready FastAPI application that generates professional financial documents for Finlive Right, a data-driven financial services company. Users input a keyword, number of pages, and corporate details (company, title, author, subject) to create a PDF powered by OpenAI’s gpt-3.5-turbo model, tailored to financial services and Indian market needs.

Features





AI Model: Generates content using OpenAI’s gpt-3.5-turbo, aligned with Finlive Right’s mission of data-driven financial guidance.



PDF Generation: Creates multi-page PDFs with corporate styling (headers, footers, metadata) using reportlab, supporting Unicode for Indian languages.



Frontend: A responsive HTML/CSS/JS interface with inputs for keyword, pages, and corporate details, plus a live loader (Collecting Information, Generating PDF, Downloading, Ready).



Workflow Automation: Automates input processing, content generation, and PDF creation.



API: RESTful API with input validation using Pydantic.



Testing: Includes unit tests for reliability.



Deployment: Configured for Render hosting.

Installation





Clone the repository:

git clone <repository-url>
cd ai_pdf_generator



Create a virtual environment and install dependencies:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt



Run the application locally:

uvicorn app.main:app --host 0.0.0.0 --port 8000

Usage

Via Frontend





Open a browser and navigate to http://localhost:8000/static/index.html.



Enter:





A single keyword (e.g., "Investment").



Number of pages (1-5).



Company name (e.g., "Finlive Right").



Document title, author, and subject.



Click Generate PDF to download a professional PDF.



A loader will display stages: "Collecting Information", "Generating PDF", "Downloading", "Ready".



Errors (e.g., invalid input) will appear below the form.

Via API





Send a POST request to /api/v1/generate-pdf/ with a JSON payload:

{
    "word": "Investment",
    "pages": 2,
    "company": "Finlive Right",
    "title": "Investment Strategies",
    "author": "John Doe",
    "subject": "Financial Planning"
}

Example using curl:

curl -X POST http://localhost:8000/api/v1/generate-pdf/ -H "Content-Type: application/json" -d '{"word": "Investment", "pages": 2, "company": "Finlive Right", "title": "Investment Strategies", "author": "John Doe", "subject": "Financial Planning"}' --output generated_Investment.pdf

API Documentation

Access interactive API documentation at /docs (e.g., http://localhost:8000/docs).

Testing

Run unit tests:

pytest app/tests/

Deployment on Render





Create a Render account at render.com.



Create a new Web Service and connect your Git repository.



Use the provided Dockerfile and render.yaml.



Set PYTHON_VERSION to 3.9 in Render’s dashboard.



Deploy and access the API at the Render URL (e.g., https://ai-pdf-generator.onrender.com).



Access the frontend at <render-url>/static/index.html.

Indian Market Considerations





Supports Unicode for Indian languages in PDFs.



OpenAI prompts are tailored for Finlive Right’s financial services, focusing on data-driven insights.



Frontend is responsive for diverse devices.

Demo

Weekly video walkthroughs will demonstrate updates and functionality. Contact the developer for access.

Security Notes





The OpenAI API key is hardcoded in content_model.py (not recommended for production). Consider using environment variables for security.



Adjust CORS settings in main.py to restrict origins in production.

Future Improvements





Add PDF preview functionality in the frontend.



Implement caching for OpenAI API responses.



Enhance corporate styling with custom fonts or logos.

License

MIT License