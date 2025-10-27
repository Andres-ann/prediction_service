import pandas as pd
from sqlalchemy.orm import Session
from app.schemas.history_schema import ReservationHistory


class SeasonalPatternsService:
    """
    Analiza los patrones estacionales de uso de salas
    (día de la semana con mayor y menor ocupación).
    """

    def __init__(self, db: Session):
        self.db = db

    def analyze_patterns(self):
        records = (
            self.db.query(ReservationHistory)
            .order_by(ReservationHistory.date_hour_start.asc())
            .all()
        )

        if not records:
            return None

        # Transformar datos en DataFrame
        df = pd.DataFrame(
            [
                {
                    "room": r.room_name,
                    "weekday": r.date_hour_start.strftime("%A").lower(),  # día en texto
                }
                for r in records
                if r.date_hour_start is not None and r.room_name
            ]
        )

        if df.empty:
            return None

        # Agrupar por sala y día
        df_grouped = (
            df.groupby(["room", "weekday"])
            .size()
            .reset_index(name="count")
            .sort_values(["room", "weekday"])
        )

        # Calcular días pico y bajos
        results = {}
        for room_name, room_data in df_grouped.groupby("room"):
            if len(room_data) == 0:
                continue

            # Día con más y menos reservas
            peak_row = room_data.loc[room_data["count"].idxmax()]
            low_row = room_data.loc[room_data["count"].idxmin()]

            results[room_name] = {
                "peak_day": peak_row["weekday"],
                "low_day": low_row["weekday"],
            }

        return results