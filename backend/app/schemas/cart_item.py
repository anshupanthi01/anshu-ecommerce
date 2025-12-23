from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class CartItemBase(BaseModel):
    product_id: int
    quantity: int = Field(... , ge=1)


class CartItemCreate(CartItemBase):
    pass


class CartItemUpdate(BaseModel):
    quantity: int = Field(..., ge=1)


class CartItemResponse(CartItemBase):
    id: int
    cart_id: int

    class Config:  
        from_attributes = True


class ProductInfo(BaseModel):
    id: int
    name: str
    price: Decimal
    stock: int
    is_active:  int

    class Config: 
        from_attributes = True


class CartItemDetail(CartItemResponse):
    product: Optional[ProductInfo] = None
    item_total: Decimal = Decimal("0.00")  # quantity * product. price