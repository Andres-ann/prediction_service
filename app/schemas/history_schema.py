from sqlalchemy import Column, Integer, String, DateTime, Text
from app.core.database import Base

class ReservationHistory(Base):
    __tablename__ = "reservation_history"

    id = Column(Integer, primary_key=True, index=True)
    reservation_id = Column(Integer, nullable=False)
    
    # Room
    room_name = Column(String(100), nullable=False)
    expected_people = Column(Integer, nullable=False, default=0)

    # Person
    people_email = Column(String(150), nullable=False)

    # Otros campos
    articles = Column(Text)
    date_hour_start = Column(DateTime, nullable=False)
    date_hour_end = Column(DateTime, nullable=False)
    fetched_at = Column(DateTime, nullable=False) 