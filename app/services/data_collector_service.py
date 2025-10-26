"""
Servicio encargado de traer y almacenar datos históricos desde la API de reservas.
"""

import httpx
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, Response
from app.models.history_model import ReservationHistory
from app.core.config import settings

class DataCollectorService:
    """Sincroniza datos desde el microservicio de reservas."""

    def __init__(self, db: Session):
        self.db = db
        self.base_url = settings.external_api_url

    async def collect_data(self):
        """Obtiene los datos de la API externa y los guarda localmente."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/reservation", timeout=10.0)
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Error connecting to external API: {e}")

        # Manejo de error 401
        if response.status_code == 401:
            raise HTTPException(status_code=401, detail="Unauthorized")

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=500, detail=f"Error in external API response: {e}")

        try:
            data = response.json()
        except ValueError:
            raise HTTPException(status_code=500, detail="External API response is not valid JSON")

        # Si no hay datos o no es una lista, devolvemos 204 (no content)
        if not data or not isinstance(data, list):
            return Response(status_code=204)

        # Evitar insertar duplicados: obtener reservation_id ya existentes
        try:
            existing = {row[0] for row in self.db.query(ReservationHistory.reservation_id).all()}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error querying the database: {e}")

        imported = 0
        for item in data:
            rid = item.get("id")
            if rid in existing:
                continue
            try:
                record = ReservationHistory(
                    reservation_id=rid,
                    room=item.get("room", ""),
                    people_name=item.get("people_name", ""),
                    articles=", ".join(item.get("articles", [])) if item.get("articles") else None,
                    date_hour_start=datetime.fromisoformat(item.get("date_hour_start")),
                    date_hour_end=datetime.fromisoformat(item.get("date_hour_end")),
                    fetched_at=datetime.now(),
                )
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error processing registration {rid}: {e}")

            self.db.add(record)
            imported += 1

        if imported == 0:
            return Response(status_code=204)

        try:
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Error saving to database: {e}")

        return {"status": "ok", "records_imported": imported}