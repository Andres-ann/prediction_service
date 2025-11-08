import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sqlalchemy.orm import Session
from app.schemas.history_schema import ReservationHistory 


class TrendingResourcesService:
    """
    Analiza la tendencia de uso de artículos en las reservas.
    Devuelve un listado con la variación esperada y un índice de confianza.
    """

    def __init__(self, db: Session):
        self.db = db

    def analyze_trending(self):
        records = (
            self.db.query(ReservationHistory)
            .order_by(ReservationHistory.date_hour_start.asc())
            .all()
        )

        if not records:
            return None

        rows = []
        for r in records:
            if not r.articles:
                continue

            # Separamos por comas
            articles = [a.strip() for a in r.articles.split(",") if a.strip()]

            for art in articles:
                rows.append({
                    "article": art,
                    "date": r.date_hour_start.date(),
                })

        if not rows:
            return None

        df = pd.DataFrame(rows)

        # Agrupar por fecha y artículo
        df_grouped = (
            df.groupby(["article", "date"])
            .size()
            .reset_index(name="count")
            .sort_values(["article", "date"])
        )

        results = []

        for article, art_data in df_grouped.groupby("article"):
            art_data = art_data.sort_values("date")
            y = art_data["count"].astype(float).values
            t = np.arange(len(art_data)).reshape(-1, 1)

            if len(y) < 2:
                continue

            # Tendencia: lineal si hay suficientes puntos
            if len(y) < 3:
                change_pct = ((y[-1] - y[0]) / max(y[0], 1)) * 100
                trust = 0.4  
            else:
                model = LinearRegression()
                model.fit(t, y)
                slope = model.coef_[0]
                change_pct = (slope / max(np.mean(y), 1)) * 100
                trust = min(0.3 + len(y) * 0.1, 0.95)

            trend_symbol = f"{'+' if change_pct >= 0 else ''}{round(change_pct, 2)}%"

            results.append({
                "article": article,
                "trend": trend_symbol,
                "trust": round(trust, 2)
            })

        # Ordenar por tendencia descendente
        results = sorted(results, key=lambda x: float(x["trend"].replace('%', '')), reverse=True)

        return results