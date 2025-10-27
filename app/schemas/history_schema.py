from sqlalchemy import Column, Integer, String, DateTime, Text
from app.core.database import Base

class ReservationHistory(Base):
    __tablename__ = "reservation_history"

    id = Column(Integer, primary_key=True, index=True)
    reservation_id = Column(Integer, nullable=False)
    
    # Room
    room_id = Column(Integer, nullable=False)
    room_name = Column(String(100), nullable=False)
    room_capacity = Column(Integer, nullable=False)

    # Person
    people_id = Column(Integer, nullable=False)
    people_name = Column(String(150), nullable=False)
    people_email = Column(String(150), nullable=False)

    # Otros campos
    expected_people = Column(Integer, nullable=False, default=0)
    articles = Column(Text)  # podés guardar el JSON serializado como string
    date_hour_start = Column(DateTime, nullable=False)
    date_hour_end = Column(DateTime, nullable=False)
    fetched_at = Column(DateTime, nullable=False)