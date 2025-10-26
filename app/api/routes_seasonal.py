from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from app.core.database import SessionLocal
from app.services.predict.seasonal_patterns_service import SeasonalPatternsService

router = APIRouter()


# Dependencia de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get(
    "/seasonal-patterns",
    tags=["Predictions"],
    summary="Analyze seasonal patterns of room usage",
    responses={
        200: {
            "description": "Seasonal patterns successfully detected.",
            "content": {
                "application/json": {
                    "example": {
                        "sala1": {"peak_day": "tuesday", "low_day": "friday"},
                        "sala2": {"peak_day": "monday", "low_day": "thursday"}
                    }
                }
            },
        },
        401: {"description": "Unauthorized."},
        404: {"description": "There is not enough historical data."},
        500: {
            "description": "Inernal Server Error.",
            "content": {"application/json": {"example": {"detail": "Error message"}}},
        },
    },
)
def get_seasonal_patterns(db: Session = Depends(get_db)):
    """
    Detect recurring occupancy patterns (days of the week with the most and least reservations)
    for each room.

    """
    try:
        service = SeasonalPatternsService(db)
        result = service.analyze_patterns()
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