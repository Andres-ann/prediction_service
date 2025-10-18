"""
Módulo de configuración general.
Lee las variables de entorno necesarias para inicializar el microservicio.
"""

import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Clase de configuración de la aplicación."""
    app_name: str = os.getenv("APP_NAME", "PredictionService")
    app_version: str = os.getenv("APP_VERSION", "1.0.0")
    database_url: str = os.getenv("DATABASE_URL", "")
    env: str = os.getenv("ENV", "development")

settings = Settings()