"""
Rutas relacionadas con el estado del servicio.
Incluye un endpoint de verificación de salud (/health).
"""

from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()

@router.get(
    "/health",
    tags=["System"],
    summary="Check the status of the microservice",
    description="Returns basic information about the microservice's status, version, and environment.",
    responses={
        200: {
            "description": "The service is active and working correctly.",
            "content": {
                "application/json": {
                    "example": {
                        "status": "ok",
                        "app_name": "PredictionService",
                        "version": "1.0.0",
                        "environment": "development"
                    }
                }
            }
        }
    },
)
def health_check():
    """
    System health check endpoint.
    Returns basic information about the microservice's status, version, and environment.

    """
    return {
        "status": "ok",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.env,
    }