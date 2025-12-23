from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

class CategoryBase(BaseModel):
    name: str = Field(... , min_length=1, max_length=255)
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None


class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config: 
        from_attributes = True


class CategoryWithCount(CategoryResponse):
    products_count: int = 0


# ✅ For category with products list
class CategoryWithProducts(CategoryResponse):
    products: List["ProductBasic"] = []


# ✅ Basic product info (to avoid circular import)
class ProductBasic(BaseModel):
    id: int
    name: str
    price: "Decimal"
    stock: int
    is_active: int

    class Config: 
        from_attributes = True

# Fix forward reference
CategoryWithProducts.model_rebuild()