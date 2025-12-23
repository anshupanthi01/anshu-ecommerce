from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
# ✅ Order Status Enum (optional but recommended)
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class OrderBase(BaseModel):
    status: str = Field(default="pending", max_length=50)
    total_amount: Decimal = Field(... , ge=0, decimal_places=2)


class OrderCreate(BaseModel):
    # Usually order is created from cart, so minimal fields needed
    pass


class OrderUpdate(BaseModel):
    status: Optional[str] = Field(None, max_length=50)


class OrderItemBasic(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    subtotal: Decimal

    class Config: 
        from_attributes = True


class OrderItemWithProduct(OrderItemBasic):
    product: Optional["ProductBasic"] = None


class ProductBasic(BaseModel):
    id: int
    name: str
    price: Decimal

    class Config: 
        from_attributes = True


class OrderResponse(OrderBase):
    id: int
    user_id: int
    order_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config: 
        from_attributes = True


class OrderWithItems(OrderResponse):
    items: List[OrderItemBasic] = []


class OrderDetail(OrderResponse):
    items: List[OrderItemWithProduct] = []


class OrderSummary(BaseModel):
    id: int
    status: str
    total_amount: Decimal
    order_date: datetime
    items_count: int

    class Config: 
        from_attributes = True

# Fix forward references
OrderItemWithProduct.model_rebuild()