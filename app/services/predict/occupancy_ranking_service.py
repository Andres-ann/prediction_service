from datetime import timedelta
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sqlalchemy.orm import Session
from app.schemas.history_schema import ReservationHistory

# Capacidad por defecto para normalizar cuando no conocemos la capacidad real de la sala
DEFAULT_ROOM_CAPACITY = 10


class OccupancyRankingService:
    """
    Genera un ranking predictivo de ocupación por sala para cada día de la semana (mon-fri).
    - Usa regresión lineal si hay suficiente histórico.
    - Si hay poco histórico, usa promedios por día de la semana.
    """

    def __init__(self, db: Session):
        self.db = db

    def predict_weekly_occupancy(self):
        # Obtener todos los registros históricos
        records = (
            self.db.query(ReservationHistory)
            .order_by(ReservationHistory.date_hour_start.asc())
            .all()
        )

        if not records:
            return None

        # DataFrame base
        df = pd.DataFrame(
            [
                {
                    "room": r.room,
                    "date": r.date_hour_start.date(),
                }
                for r in records
            ]
        )

        if df.empty:
            return None

        # Agrupar por sala y fecha -> cantidad de reservas diarias
        df_grouped = (
            df.groupby(["room", "date"])
            .size()
            .reset_index(name="reservas")
            .sort_values(["room", "date"])
        )

        # Nos interesa predecir el comportamiento por sala
        rooms_results = {}

        # Horizonte para predecir: próximos 14 días (nos permite agrupar por weekday)
        n_future_days = 14

        for room_name, room_data in df_grouped.groupby("room"):
            room_data = room_data.reset_index(drop=True)
            # serie temporal: fechas y conteos
            y = room_data["reservas"].astype(float).values
            dates = pd.to_datetime(room_data["date"])

            if len(room_data) == 0:
                continue

            # Estadísticas históricas para normalización
            percentile_90 = float(np.percentile(y, 90)) if len(y) > 0 else 0.0
            max_hist = float(y.max()) if len(y) > 0 else 0.0
            denom = max(percentile_90, max_hist, DEFAULT_ROOM_CAPACITY, 1.0)

            # Si hay pocos puntos históricos, usar promedio por weekday (fallback conservador)
            if len(room_data) < 3:
                # calcular promedio histórico por día de semana (0=lunes .. 6=domingo)
                hist = (
                    pd.DataFrame({"date": dates, "reservas": y})
                    .assign(weekday=lambda d: d["date"].dt.weekday)
                    .groupby("weekday")["reservas"]
                    .mean()
                )
                # construir preds para los próximos n_future_days usando esos promedios (fallback)
                start_date = dates.max().date()
                preds = []
                for i in range(1, n_future_days + 1):
                    d = start_date + timedelta(days=i)
                    wk = d.weekday()
                    preds.append(hist.get(wk, np.nan))
                preds = np.array([p if not pd.isna(p) else float(np.nanmean(y)) for p in preds])
                preds = np.clip(preds, 0, None)
            else:
                # Entrenar regresión lineal sobre t (fecha ordenada)
                room_data = room_data.sort_values("date").reset_index(drop=True)
                t = np.arange(len(room_data)).reshape(-1, 1)
                model = LinearRegression()
                model.fit(t, y)
                # predecir próximos n_future_days
                t_future = np.arange(len(room_data), len(room_data) + n_future_days).reshape(-1, 1)
                preds = model.predict(t_future)
                preds = np.clip(preds, 0, None)

            # Mapear predicciones a weekdays y obtener promedio por weekday (mon-fri)
            start_date = pd.to_datetime(room_data["date"].max()).date()
            weekday_preds = {i: [] for i in range(7)}  # 0..6
            for i in range(n_future_days):
                d = start_date + timedelta(days=i + 1)
                wk = d.weekday()
                weekday_preds[wk].append(float(preds[i]))

            # Calcular valor esperado por weekday (lunes=0 .. viernes=4)
            expected_by_weekday = {}
            for wk in range(0, 5):  # monday..friday
                vals = weekday_preds.get(wk, [])
                if len(vals) == 0:
                    expected = 0.0
                else:
                    expected = float(np.mean(vals))
                # normalizar
                expected_norm = min(round(expected / denom, 2), 1.0)
                expected_by_weekday[wk] = expected_norm

            # Guardar resultados (lunes..viernes)
            rooms_results[room_name] = expected_by_weekday

        # Armar ranking por día (human readable keys)
        days = ["monday", "tuesday", "wednesday", "thursday", "friday"]
        ranking = {day: [] for day in days}

        for i, day in enumerate(days):
            for room, wk_map in rooms_results.items():
                val = wk_map.get(i, 0.0)
                ranking[day].append({"room": room, "expected_occupancy": val})
            # ordenar por occupancy desc
            ranking[day] = sorted(ranking[day], key=lambda x: x["expected_occupancy"], reverse=True)

        return {"ranking": ranking}