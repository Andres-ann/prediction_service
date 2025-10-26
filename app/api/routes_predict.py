from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from app.core.database import SessionLocal
from app.services.predict.occupancy_service import OccupancyPredictionService
from app.models.occupancy_model import Occupancy

router = APIRouter()


# Dependencia de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/occupancy",
    tags=["Predictions"],
    summary="Predicts the probability of a room being occupied",
    response_description="Prediction result",
    responses={
        200: {
            "description": "OK",
            "content": {
                "application/json": {
                    "example": {
                        "room": "sala1",
                        "occupation_probability": 0.3,
                        "trend": "baja",
                        "recommendation": "¡Buena disponibilidad! Reserva tu sala ahora.",
                    }
                }
            },
        },
        400: {"description": "Fields are missing in the request body."},
        404: {"description": "There is no historical data for the room."},
        422: {"description": "Invalid data format."},
        500: {"description": "Internal Server Error."},
    },
)
def predict_occupancy(request: Occupancy, db: Session = Depends(get_db)):
    """
    Predict the probability of a room being occupied between two dates
    using historical data from reservation_history.
    """
    service = OccupancyPredictionService(db)

    try:
        result = service.predict_occupancy(
            request.room, request.date_hour_start, request.date_hour_end
        )
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve)
        )
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error: {str(e)}",
        )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"There is no historical data for the room '{request.room}'",
        )

    return result