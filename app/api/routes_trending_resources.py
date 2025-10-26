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
    summary="Analyze the usage trend of items (resources) in the reserves",
    responses={
        200: {
            "description": "TTrends successfully detected.",
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
        404: {"description": "There is not enough historical data."},
        500: {
            "description": "Internal Server Error.",
            "content": {"application/json": {"example": {"detail": "Error message"}}},
        },
    },
)
def get_trending_resources(db: Session = Depends(get_db)):
    """
    Returns item usage trends from reservation history.
    If data is limited, use a simple comparison between the first and last records.
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