from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from app.core.database import SessionLocal
from app.services.predict.occupancy_ranking_service import OccupancyRankingService
from app.schemas.occupancy_ranking_schema import OccupancyRankingResponse

router = APIRouter()


# Dependencia de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get(
    "/occupancy-ranking",
    tags=["Predictions"],
    summary="Predictive ranking of room occupancy by weekday",
    response_model=OccupancyRankingResponse,
    responses={
        200: {"description": "OK. Predicted occupancy ranking generated successfully."},
        401: {"description": "Unauthorized."},
        404: {"description": "No historical data found."},
        422: {"description": "Invalid data format."},
        500: {
            "description": "Internal Server Error.",
            "content": {
                "application/json": {"example": {"detail": "Database or computation error"}}
            },
        },
    },
)
def get_occupancy_ranking(db: Session = Depends(get_db)):
    """
    Generates a predictive ranking of room occupancy for the week (Monday to Friday).
    Uses historical reservation data to estimate expected occupancy.
    """
    service = OccupancyRankingService(db)

    try:
        result = service.predict_weekly_occupancy()
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection error.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error: {str(e)}",
        )

    if result is None:
        raise HTTPException(
            status_code=404, detail="No historical reservation data available."
        )

    return result