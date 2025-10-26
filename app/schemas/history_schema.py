from sqlalchemy import Column, Integer, String, DateTime, Text
from app.core.database import Base

class ReservationHistory(Base):
    __tablename__ = "reservation_history"

    id = Column(Integer, primary_key=True, index=True)
    reservation_id = Column(Integer, nullable=False)
    room = Column(String(100), nullable=False)         
    people_name = Column(String(150), nullable=False)  
    articles = Column(Text)
    date_hour_start = Column(DateTime, nullable=False)
    date_hour_end = Column(DateTime, nullable=False)
    fetched_at = Column(DateTime, nullable=False)