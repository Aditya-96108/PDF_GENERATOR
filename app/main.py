# main.py: Entry point for the FastAPI application.
# Purpose: Initializes the FastAPI app, sets up middleware for CORS, serves static files,
# and includes API routes. The static file serving enables the frontend to be accessed.
# Dependencies: FastAPI for the web framework, CORSMiddleware for cross-origin requests,
# StaticFiles for serving the frontend.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.routes import router

# Initialize FastAPI application
app = FastAPI(
    title="AI PDF Generator API",
    description="A production-ready API for generating content using OpenAI and creating PDFs from single-word inputs, with a simple frontend.",
    version="1.0.0"
)

# Add CORS middleware to allow cross-origin requests (useful for frontend integration)
# Purpose: Enables the API to be accessed from different domains, which is common in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production to specific domains for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static directory to serve frontend files
# Purpose: Serves HTML, CSS, and JS files from the 'static' directory at the root URL.
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include API routes from the routes module
# Purpose: Keeps the main file clean by delegating route definitions to a separate module.
app.include_router(router, prefix="/api/v1")