"""
Rutas relacionadas con el estado del servicio.
Incluye un endpoint de verificación de salud (/health).
"""

from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()

@router.get(
    "/health",
    tags=["Sistema"],
    summary="Verifica el estado del microservicio",
    description="Devuelve información básica sobre el estado, la versión y el entorno del microservicio.",
    responses={
        200: {
            "description": "El servicio está activo y funcionando correctamente",
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
    Endpoint de verificación de salud del sistema.

    **Retorna:**
    - `status`: Estado del servicio (`ok` si responde correctamente)
    - `app_name`: Nombre del microservicio
    - `version`: Versión actual del sistema
    - `environment`: Entorno de ejecución (dev, staging, prod)
    """
    return {
        "status": "ok",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.env,
    }