from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    price:  Decimal = Field(... , ge=0, decimal_places=2)
    stock:  int = Field(default=0, ge=0)
    sku: Optional[str] = Field(None, max_length=100)
    category_id: Optional[int] = None


class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    stock: Optional[int] = Field(None, ge=0)
    sku: Optional[str] = Field(None, max_length=100)
    category_id: Optional[int] = None
    is_active: Optional[int] = Field(None, ge=0, le=1)

class ProductResponse(ProductBase):
    id: int
    is_active: int
    created_at: datetime
    updated_at: datetime

    class Config: 
        from_attributes = True


class ProductWithCategory(ProductResponse):
    category: Optional["CategoryBasic"] = None


# ✅ Basic category info (to avoid circular import)
class CategoryBasic(BaseModel):
    id: int
    name: str

    class Config: 
        from_attributes = True


# Fix forward reference
ProductWithCategory.model_rebuild()