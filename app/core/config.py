"""
Módulo de configuración general.
Lee las variables de entorno necesarias para inicializar el microservicio.
"""

import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Clase de configuración de la aplicación."""
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = os.getenv("APP_NAME", "PredictionService")
    app_version: str = os.getenv("APP_VERSION", "1.0.0")
    database_url: str = os.getenv("DATABASE_URL", "")
    admin_database_url: str = os.getenv("ADMIN_DATABASE_URL", "")
    env: str = os.getenv("ENV", "development")
    external_api_url: str = os.getenv("EXTERNAL_API_URL", "https://api-reservas-demo.com")

settings = Settings()