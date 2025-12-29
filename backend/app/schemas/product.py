from pydantic import BaseModel, Field, condecimal
from typing import Optional, Annotated
from datetime import datetime
from decimal import Decimal

Price = Annotated[Decimal, condecimal(ge=0, max_digits=12, decimal_places=2)]
# ✅ Base schema (shared fields)
class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    price: Price
    stock: int = Field(default=0, ge=0)
    sku: Optional[str] = Field(None, max_length=100)
    category_id: Optional[int] = None


# ✅ For creating product (request)
class ProductCreate(ProductBase):
    pass


# ✅ For updating product (request)
class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    price: Optional[Price] = None
    stock: Optional[int] = Field(None, ge=0)
    sku: Optional[str] = Field(None, max_length=100)
    category_id: Optional[int] = None
    is_active: Optional[int] = Field(None, ge=0, le=1)


# ✅ For product response
class ProductResponse(ProductBase):
    id: int
    is_active: int
    created_at: datetime
    updated_at: datetime

    class Config: 
        from_attributes = True


# ✅ For product response with category details
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