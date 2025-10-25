"""
Punto de entrada del microservicio de predicción de reservas.
Expone los endpoints definidos y configura la documentación Swagger y ReDoc.
"""

from fastapi import FastAPI
from app.api.routes_health import router as health_router
from app.api.routes_sync import router as sync_router
from app.core.config import settings
from app.core.database import init_db

def create_app() -> FastAPI:
    """
    Crea y configura la instancia principal de la aplicación FastAPI.
    """
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=(
            "Microservicio encargado de la predicción de reservas. "
            "Proporciona endpoints para monitorear el estado, obtener predicciones "
            "y realizar análisis sobre el uso de recursos."
        ),   
        license_info={
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT",
        },
    )

    # Inicializa base y tablas al inicio
    @app.on_event("startup")
    def startup_event():
        print("Initializing database connection")
        init_db()

    # Registrar rutas
    app.include_router(health_router, prefix="/api/v1")
    app.include_router(sync_router, prefix="/api/v1")

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)