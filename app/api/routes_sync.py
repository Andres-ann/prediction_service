"""
Rutas para sincronizar datos de reservas hacia la base local.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.sync_service import DataCollectorService
from app.core.database import SessionLocal
from app.schemas.sync_schema import ReservationCreate
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/sync", 
    tags=["Sync"],
    summary="Store reservation data",
    description="Store a single reservation in the local database for analysis."
)
async def sync_data(
    data: ReservationCreate,
    db: Session = Depends(get_db)
):
    collector = DataCollectorService(db)
    return collector.store_data(data)
async def sync_data(
    data: List[ReservationCreate],
    db: Session = Depends(get_db)
):
    collector = DataCollectorService(db)
    return await collector.store_data([reservation.model_dump() for reservation in data])