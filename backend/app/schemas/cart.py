from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal


class CartBase(BaseModel):
    user_id:  int

class CartCreate(CartBase):
    pass

class CartResponse(CartBase):
    id: int

    class Config: 
        from_attributes = True


class CartItemBasic(BaseModel):
    id: int
    product_id: int
    quantity: int

    class Config: 
        from_attributes = True

class CartItemWithProduct(CartItemBasic):
    product: Optional["ProductInfo"] = None
    item_total: Optional[Decimal] = None  # quantity * product. price

# ✅ Product info for cart
class ProductInfo(BaseModel):
    id: int
    name: str
    price: Decimal
    stock: int
    is_active: int

    class Config:  
        from_attributes = True


class CartWithItems(CartResponse):
    items: List[CartItemBasic] = []


class CartDetail(CartResponse):
    items: List[CartItemWithProduct] = []
    total_items: int = 0
    total_amount: Decimal = Decimal("0.00")


class CartSummary(BaseModel):
    id: int
    total_items: int = 0
    total_amount: Decimal = Decimal("0.00")

    class Config: 
        from_attributes = True

# Fix forward reference
CartItemWithProduct.model_rebuild()