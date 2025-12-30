from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import UploadFile, File, Form
import os
from uuid import uuid4
from app.database import get_db
from app.models import User
from app.schemas import ProductCreate, ProductUpdate, ProductResponse, ProductWithCategory
from app.crud import (
    create_product,
    get_product_by_id,
    get_product_by_sku,
    get_all_products,
    get_products_by_category,
    search_products,
    update_product,
    delete_product,
)
from app.auth import get_current_user


router = APIRouter()


# ✅ Get all products
@router.get("/", response_model=List[ProductResponse])
def list_products(
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    if search:
        products = search_products(db, search, skip=skip, limit=limit)
    elif category_id: 
        products = get_products_by_category(db, category_id, skip=skip, limit=limit)
    else: 
        products = get_all_products(db, skip=skip, limit=limit)
    
    return products


# ✅ Get single product
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product_by_id(db, product_id)
    if not product: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product


# ✅ Create product (protected)
@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
# def add_product(
#     product: ProductCreate,
#     current_user:User = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     # Check if SKU exists
#     if product.sku:
#         existing = get_product_by_sku(db, product.sku)
#         if existing: 
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Product SKU already exists"
#             )
    
#     new_product = create_product(db, product)
#     return new_product
async def add_product(
    name: str = Form(...),
    description: str = Form(""),
    price: float = Form(...),
    sku: str = Form(None),
    category_id: int = Form(...),
    stock: int = Form(...),
    image: UploadFile = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if SKU exists
    if sku:
        existing = get_product_by_sku(db, sku)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product SKU already exists"
            )

    image_url = None
    if image:
        ext = os.path.splitext(image.filename)[-1]
        filename = f"{uuid4().hex}{ext}"
        upload_folder = os.path.join("static", "products")
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        with open(file_path, "wb") as f:
            f.write(await image.read())
        image_url = f"/static/products/{filename}"

    # Build ProductCreate object as your current create_product expects
    product_in = ProductCreate(
        name=name,
        description=description,
        price=price,
        sku=sku,
        category_id=category_id,
        stock=stock,
        image_url=image_url
    )
    new_product = create_product(db, product_in)
    return new_product

# ✅ Update product (protected)
@router.put("/{product_id}", response_model=ProductResponse)
def edit_product(
    product_id: int,
    product_data: ProductUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated = update_product(db, product_id, product_data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return updated


# ✅ Delete product (protected)
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_product(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    deleted = delete_product(db, product_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return None