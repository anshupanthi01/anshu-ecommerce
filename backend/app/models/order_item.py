from sqlalchemy import Column, Integer, ForeignKey, DateTime, Numeric 
from sqlalchemy.orm import relationship
from sqlalchemy. sql import func
from app.database import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    
    unit_price = Column(Numeric(10, 2), nullable=False)  # Price at time of order
    subtotal = Column(Numeric(10, 2), nullable=False)    # quantity * unit_price

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func. now(), onupdate=func.now(), nullable=False)

    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")