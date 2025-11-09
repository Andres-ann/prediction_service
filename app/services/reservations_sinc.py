import json
from datetime import datetime
from sqlalchemy.orm import Session
from app.schemas.history_schema import ReservationHistory
from app.schemas.sync_schema import ReservationCreate

class DataCollectorService:

    @staticmethod
    def store_data(reservation: ReservationCreate, db: Session):
        """Crea o actualiza un registro de reserva en la DB"""
        try:
            # Buscar si ya existe por reservation_id
            db_reservation = db.query(ReservationHistory).filter_by(
                reservation_id=reservation.reservation_id
            ).first()

            if db_reservation:
                # Actualizar campos existentes
                db_reservation.room_name = reservation.room_name
                db_reservation.people_email = reservation.people_email
                db_reservation.articles = ",".join(reservation.articles) if reservation.articles else None
                db_reservation.date_hour_start = reservation.date_hour_start
                db_reservation.date_hour_end = reservation.date_hour_end
            else:
                # Crear nuevo registro
                db_reservation = ReservationHistory(
                    reservation_id=reservation.reservation_id,
                    room_name=reservation.room_name,
                    people_email=reservation.people_email,
                    articles= ",".join(reservation.articles) if reservation.articles else None,
                    date_hour_start=reservation.date_hour_start,
                    date_hour_end=reservation.date_hour_end,
                    fetched_at=datetime.utcnow()
                )
                db.add(db_reservation)

            db.commit()
            return {"reservation_id": reservation.reservation_id, "status": "success"}

        except Exception as e:
            db.rollback()
            return {"reservation_id": reservation.reservation_id, "status": "error", "error": str(e)}
