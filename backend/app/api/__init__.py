"""
API routes package.
"""
from fastapi import APIRouter
from app.api import upload, status, results, health

# Create main router
router = APIRouter()

# Include sub-routers
router.include_router(health.router, tags=["health"])
router.include_router(upload.router, tags=["upload"])
router.include_router(status.router, tags=["status"])
router.include_router(results.router, tags=["results"])
