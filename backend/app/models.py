from sqlalchemy import Column, String, Float, Boolean, Integer, DateTime, Text
from sqlalchemy.sql import func
from .database import Base

class Event(Base):
    __tablename__ = "events"

    event_id = Column(String, primary_key=True)
    video_id = Column(String)
    event_type = Column(String)
    severity = Column(String)
    timestamp = Column(DateTime, default=func.now())
    frame_index = Column(Integer)
    frame_snapshot_path = Column(String, nullable=True)
    threat_score = Column(Float, default=0.0)
    genai_summary = Column(Text, nullable=True)
    acknowledged = Column(Boolean, default=False)
    acknowledged_by = Column(String, nullable=True)

class Video(Base):
    __tablename__ = "videos"

    video_id = Column(String, primary_key=True)
    filename = Column(String)
    status = Column(String, default="pending")
    uploaded_at = Column(DateTime, default=func.now())
    duration_seconds = Column(Float, nullable=True)
    total_events = Column(Integer, default=0)