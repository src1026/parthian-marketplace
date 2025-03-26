from sqlalchemy import Column, Integer, String, DateTime, Boolean
from database import Base
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
    # cart_items = relationship("CartItem", back_populates="user")

"""
class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    battery_id = Column(String, nullable=False)
    quantity = Column(Integer, default=1)
    user = relationship("User", back_populates="cart_items")
"""