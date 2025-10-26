from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sqlalchemy.orm import Session
from app.schemas.history_schema import ReservationHistory

# Valor por defecto para normalizar la probabilidad cuando no se conoce la capacidad real
DEFAULT_ROOM_CAPACITY = 10

class OccupancyPredictionService:
    """
    Servicio encargado de predecir la ocupación de salas
    usando datos históricos de la tabla reservation_history.
    """

    def __init__(self, db: Session):
        self.db = db

    def predict_occupancy(self, room: str, date_hour_start: str, date_hour_end: str):
        """Predicts the probability of occupancy for a specific room."""

        # Convertir fechas a objetos datetime
        try:
            start_date = datetime.fromisoformat(date_hour_start)
            end_date = datetime.fromisoformat(date_hour_end)
        except ValueError:
            raise ValueError("Invalid date format.. Use YYYY-MM-DD o YYYY-MM-DDTHH:MM:SS")

        # Obtener los registros históricos de la sala
        records = (
            self.db.query(ReservationHistory)
            .filter(ReservationHistory.room == room)
            .order_by(ReservationHistory.date_hour_start.asc())
            .all()
        )

        if not records:
            return None

        # Convertir los registros a un DataFrame
        df = pd.DataFrame([{
            "date": r.date_hour_start.date()
        } for r in records])

        # Agrupar por día (conteo de reservas por fecha)
        df_grouped = df.groupby("date").size().reset_index(name="reservas")
        df_grouped = df_grouped.sort_values("date")
        df_grouped["t"] = np.arange(len(df_grouped))

        # series de valores históricos
        y = df_grouped["reservas"].astype(float)

        # Si hay pocos puntos históricos, evitar entrenamiento de modelo
        if len(df_grouped) < 2:
            # usar la media histórica como predicción simple
            mean_pred = float(y.mean())
        else:
            # Entrenar modelo de regresión lineal
            X = df_grouped[["t"]]
            model = LinearRegression()
            model.fit(X, y)

            # Calcular predicciones para el rango futuro
            dias_pred = (end_date - start_date).days + 1
            t_future = np.arange(len(df_grouped), len(df_grouped) + dias_pred).reshape(-1, 1)
            preds = model.predict(t_future)

            # Evitar predicciones negativas
            preds = np.clip(preds, 0, None)
            mean_pred = float(np.mean(preds))

        # Normalización: usa el máximo histórico o un valor por defecto de capacidad
        percentile_90 = float(np.percentile(y, 90)) if len(y) > 0 else 0.0
        denom = max(percentile_90, float(y.max()), DEFAULT_ROOM_CAPACITY, 1.0)

        probability = min(mean_pred / denom, 1.0)

        # Determinar tendencia y recomendación
        if probability > 0.7:
            trend = "alta"
            recommendation = "¡Cuidado! Salas casi llenas. Intenta otro horario."
        elif probability > 0.4:
            trend = "media"            
            recommendation = "Disponibilidad Baja. Reserva pronto o considera otra fecha."
        else:
            trend = "baja"
            recommendation = "¡Buena disponibilidad! Reserva tu sala ahora."

        return {
            "room": room,
            "occupation_probability": round(probability,2),
            "trend": trend,
            "recommendation": recommendation,
        }