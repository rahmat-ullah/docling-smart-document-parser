"""
Health check endpoints.
"""
from fastapi import APIRouter
from app.models.schemas import HealthResponse
from app.core.config import settings

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns the current health status of the application.
    """
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        environment=settings.environment,
    )


@router.get("/health/ready")
async def readiness_check():
    """
    Readiness check endpoint.
    
    Returns whether the application is ready to serve requests.
    """
    # Add any readiness checks here (database connections, model loading, etc.)
    return {
        "success": True,
        "status": "ready",
        "checks": {
            "docling_model": "ready",  # This would be checked in real implementation
            "file_system": "ready",
        }
    }


@router.get("/health/live")
async def liveness_check():
    """
    Liveness check endpoint.
    
    Returns whether the application is alive and running.
    """
    return {
        "success": True,
        "status": "alive",
        "timestamp": "2024-01-01T00:00:00Z",  # Would use actual timestamp
    }
