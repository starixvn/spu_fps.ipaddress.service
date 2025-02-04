from sqlalchemy import Column, DateTime, Integer, String, Float, Boolean, JSON
from datetime import datetime, timezone
from .base import Base

class IPInfo(Base):
    __tablename__ = 'ip_info'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ip_address = Column(String(45), unique=True, nullable=False)
    asn = Column(String(50))
    ip_range = Column(String(50))
    provider = Column(String(255))
    organisation = Column(String(255))
    continent = Column(String(50))
    continent_code = Column(String(10))
    country = Column(String(100))
    iso_code = Column(String(10))
    region = Column(String(100))
    region_code = Column(String(10))
    timezone = Column(String(100))
    city = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    currency = Column(JSON)
    devices = Column(JSON)
    proxy = Column(String(50))
    ip_type = Column(String(50))
    checked_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))