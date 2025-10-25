"""
Rutas para sincronizar datos desde la API de reservas hacia la base local.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.data_collector_service import DataCollectorService
from app.core.database import SessionLocal

router = APIRouter()


# Dependencia para obtener una sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/sync",
    tags=["Sync"],
    summary="Sincronizar datos desde la API de reservas",
    description="Obtiene los datos de reservas desde el microservicio de reservas y los almacena localmente en la base para análisis.",
    responses={
        200: {
            "description": "Datos sincronizados correctamente",
            "content": {
                "application/json": {
                    "example": {"status": "ok", "records_imported": 100}
                }
            },
        },
        204: {"description": "No hay datos nuevos para sincronizar"},
        401: {"description": "Unauthorized"},
        500: {"description": "Error: Internal Server Error",
              "content": {
                "application/json": {
                    "example": {"detail":"Error message"}
                }
            },},
    },
)
async def sync_data(db: Session = Depends(get_db)):
    """
    Obtiene los datos de reservas desde el microservicio de reservas
    y los almacena localmente en la base para análisis.
    """
    collector = DataCollectorService(db)
    return await collector.collect_data()