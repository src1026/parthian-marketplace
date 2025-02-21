from sqlalchemy import Column, Integer, String, DateTime, Boolean
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String)
    provider = Column(String)
    provider_id = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String, nullable=True)
