from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class ReservationCreate(BaseModel):
    reservation_id: int
    room_name: str = Field(..., example="sala 1", description="Name of the room to be analyzed")
    people_email: str
    articles: Optional[List[str]] = Field(
        default=None, 
        description="List of items associated with the reservation"
    )
    date_hour_start: datetime = Field(
        ..., example="2025-11-13 11:00:00", description="Start date and time"
    )
    date_hour_end: datetime = Field(
        ..., example="2025-11-13 12:00:00", description="End date and time"
    )

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S")
        }