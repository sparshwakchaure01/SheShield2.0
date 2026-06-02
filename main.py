"""
SheShield AI - Women Safety Route Assistant
FastAPI Backend Application

This application provides route planning with safety assessment for women travelers.
It uses Mapbox Directions API to fetch routes and applies safety scoring based on
various factors including time of day, distance, and route complexity.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.route_api import router
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI application
app = FastAPI(
    title="SheShield AI - Women Safety Route Assistant",
    description="Backend API for safe route planning with real-time safety assessment",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS (Cross-Origin Resource Sharing)
# This allows the frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """
    Root endpoint - Health check

    Returns a simple message to confirm the backend is running
    """
    return {
        "message": "Backend is running",
        "service": "SheShield AI - Women Safety Route Assistant",
        "version": "1.0.0",
        "status": "active"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint

    Returns the health status of the application and its dependencies
    """
    mapbox_key = os.getenv("MAPBOX_API_KEY", "YOUR_API_KEY")

    return {
        "status": "healthy",
        "services": {
            "api": "running",
            "mapbox": "configured" if mapbox_key != "YOUR_API_KEY" else "not configured"
        }
    }


# Include route handlers
app.include_router(
    router,
    tags=["Routes"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"}
    }
)


if __name__ == "__main__":
    """
    Run the application using uvicorn server

    To start the server, run:
        python main.py

    Or use uvicorn directly:
        uvicorn main:app --reload --host 0.0.0.0 --port 8000
    """
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))

    print(f"Starting SheShield AI Backend...")
    print(f"Server will be available at: http://{host}:{port}")
    print(f"API Documentation: http://{host}:{port}/docs")
    print(f"Alternative Docs: http://{host}:{port}/redoc")

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True  # Enable auto-reload during development
    )
