"""
Main API router
"""
from fastapi import APIRouter

from app.api.endpoints.health import router as health_router
from app.api.endpoints.auth import router as auth_router


api_router = APIRouter(prefix="/api")

# Health endpoint
api_router.include_router(health_router, tags=["health"])

# Auth endpoints
api_router.include_router(auth_router, tags=["auth"])


