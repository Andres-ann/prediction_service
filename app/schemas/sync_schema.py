from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
import json

class ReservationCreate(BaseModel):
    reservation_id: int
    room_name: str = Field(..., example="Sala 1", description="Name of the room")
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

    model_config = {
        "json_encoders": {datetime: lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S")}
    }

def map_reservation_json(data: bytes) -> Optional[ReservationCreate]:
    """Recibe bytes JSON y los mapea al esquema ReservationCreate"""
    try:
        json_data = json.loads(data)
        reservation = ReservationCreate(**json_data)
        print("\n" + "="*50)
        print("📨 MENSAJE RESERVA RECIBIDO (TIPADO)")
        print("="*50)
        print(reservation.model_dump_json(indent=4))
        print("="*50)
        return reservation
    except json.JSONDecodeError as e:
        print(f"❌ Error decodificando JSON: {e}")
        return None
    except Exception as e:
        print(f"❌ Error mapeando al esquema: {e}")
        return None
