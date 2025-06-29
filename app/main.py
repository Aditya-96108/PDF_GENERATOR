# main.py: Entry point for the FastAPI application
# Purpose: Initializes the FastAPI app, mounts static files, and defines routes for Finlive Right AI PDF Generator.
# Includes a root route to redirect to the frontend and CORS middleware for cross-origin requests.
# Dependencies: FastAPI, uvicorn, StaticFiles, CORSMiddleware.

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router

app = FastAPI(
    title="Finlive Right AI PDF Generator",
    description="A production-ready API to generate professional financial PDFs for Finlive Right using OpenAI.",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# Root route to redirect to frontend
@app.get("/")
async def root():
    """
    Redirects requests to the root URL to the frontend.
    Purpose: Prevents 404 errors when accessing the root URL and directs users to the UI.
    """
    return RedirectResponse(url="/static/index.html")