from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schemas.history_schema import ReservationHistory


class DataCollectorService:
    def __init__(self, db: Session):
        self.db = db

    def store_data(self, data: ReservationHistory):
        if not data:
            raise HTTPException(status_code=400, detail="No reservation data was received.")

        rid = data.reservation_id

        # Verificar si ya existe esa reserva
        existing = self.db.query(ReservationHistory).filter_by(reservation_id=rid).first()
        if existing:
            raise HTTPException(status_code=409, detail=f"The reserve already exists.")

        try:
            record = ReservationHistory(
                reservation_id=data.reservation_id,
                room_name=data.room_name,
                people_email=data.people_email,
                articles=",".join(data.articles) if data.articles else None,
                date_hour_start=data.date_hour_start,
                date_hour_end=data.date_hour_end,
                fetched_at=datetime.now(),
            )

            self.db.add(record)
            self.db.commit()
            self.db.refresh(record)

            return {
                "status": "OK",
                "reservation_id": record.reservation_id,
                "message": f"Reservation successfully stored."
            }

        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Error saving reservation: {e}")