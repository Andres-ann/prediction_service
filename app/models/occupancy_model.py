from pydantic import BaseModel, Field


class Occupancy(BaseModel):
    room: str = Field(..., example="room_name", description="Name of the room to be analyzed")
    date_hour_start: str = Field(
        ..., example="2025-10-18T00:00:00", description="Start date and time"
    )
    date_hour_end: str = Field(
        ..., example="2025-10-18T23:59:59", description="End date and time"
    )

    class Config:
        schema_extra = {
            "example": {
                "room": "room_name",
                "date_hour_start": "2025-10-18T00:00:00",
                "date_hour_end": "2025-10-18T23:59:59",
            }
        }