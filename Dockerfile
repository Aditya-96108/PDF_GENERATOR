# Updated for environment variables
# Dockerfile: Configures the Docker image for deploying the FastAPI application on Render.

# Purpose: Defines the environment and setup for running the application in a container.

# Uses a lightweight Python image and installs dependencies from requirements.txt.

# Exposes port 8000 for the FastAPI application.

# FROM python:3.9-slim

# Set working directory

# WORKDIR /app

# Copy requirements and install dependencies

# COPY requirements.txt . RUN pip install --no-cache-dir -r requirements.txt

# Copy application code

# COPY . .

# Expose port for FastAPI

# EXPOSE 8000

# Run the application with uvicorn

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]