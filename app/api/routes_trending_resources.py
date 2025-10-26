from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from app.core.database import SessionLocal
from app.services.predict.trending_resources_service import TrendingResourcesService

router = APIRouter()

# Dependencia de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get(
    "/trending-resources",
    tags=["Predictions"],
    summary="Analiza la tendencia de uso de artículos (recursos) en las reservas",
    responses={
        200: {
            "description": "Tendencias detectadas exitosamente.",
            "content": {
                "application/json": {
                    "example": [
                        {"article": "Proyector", "trend": "+12.5%", "trust": 0.85},
                        {"article": "Pizarra", "trend": "-5.3%", "trust": 0.68},
                    ]
                }
            },
        },
        401: {"description": "Unauthorized."},
        404: {"description": "No hay datos históricos suficientes."},
        500: {
            "description": "Error interno del servidor.",
            "content": {"application/json": {"example": {"detail": "Error message"}}},
        },
    },
)
def get_trending_resources(db: Session = Depends(get_db)):
    """
    Retorna las tendencias de uso de los artículos a partir del histórico de reservas.
    Si hay pocos datos, utiliza comparación simple entre primeros y últimos registros.
    """
    try:
        service = TrendingResourcesService(db)
        result = service.analyze_trending()
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection error."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

    if not result:
        raise HTTPException(status_code=404, detail="No historical data found.")

    return result