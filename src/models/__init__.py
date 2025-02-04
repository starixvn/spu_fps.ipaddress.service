from .base import Base, engine, SessionLocal
from .ip_info import IPInfo

Base.metadata.create_all(bind=engine)