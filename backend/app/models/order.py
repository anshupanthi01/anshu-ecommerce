from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(50), default="pending", nullable=False)
    total_amount = Column(Numeric(10,2), nullable=False)

    # Timestamps
    order_date = Column(DateTime(timezone=True), server_default=func. now(), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func. now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func. now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")