from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., ge=1)
    unit_price: Decimal = Field(..., ge=0, decimal_places=2)
    subtotal: Decimal = Field(..., ge=0, decimal_places=2)


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., ge=1)


class OrderItemUpdate(BaseModel):
    quantity: Optional[int] = Field(None, ge=1)

class OrderItemResponse(OrderItemBase):
    id: int
    order_id: int
    created_at: datetime
    updated_at:  datetime

    class Config: 
        from_attributes = True


class OrderItemWithProduct(OrderItemResponse):
    product: Optional["ProductInfo"] = None


class ProductInfo(BaseModel):
    id: int
    name: str
    price:  Decimal
    sku: Optional[str] = None
    image_url: Optional[str] = None 

    class Config: 
        from_attributes = True


# Fix forward reference
OrderItemWithProduct.model_rebuild()