"""
Punto de entrada del microservicio de predicción de reservas.
Expone los endpoints definidos y configura la documentación Swagger y ReDoc.
"""

from fastapi import FastAPI
from app.api.routes_health import router as health_router
from app.api.routes_predict import router as predict_router
from app.api.routes_predict_ranking import router as ranking_router
from app.api.routes_trending_resources import router as trending_router
from app.api.routes_seasonal import router as seasonal_router
from app.core.config import settings
from app.core.database import init_db
from app.core.rabbitMq import start_rabbitmq_consumer

def create_app() -> FastAPI:
    """
    Crea y configura la instancia principal de la aplicación FastAPI.
    """
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=(
            "Microservice responsible for reservation prediction."
            "Provides endpoints for monitoring status, obtaining predictions,"
            "and performing analysis on resource usage."
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
        start_rabbitmq_consumer()
        init_db()

    # Registrar rutas
    app.include_router(health_router, prefix="/api/v1")
    app.include_router(predict_router, prefix="/api/v1")
    app.include_router(ranking_router, prefix="/api/v1")
    app.include_router(trending_router, prefix="/api/v1")
    app.include_router(seasonal_router, prefix="/api/v1")

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)