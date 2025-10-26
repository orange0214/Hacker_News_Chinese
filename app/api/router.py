"""
Main API router
"""
from fastapi import APIRouter

from app.api.endpoints.health import router as health_router


api_router = APIRouter(prefix="/api")

# Health endpoint
api_router.include_router(health_router, tags=["health"])


