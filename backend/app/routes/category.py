from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import os
from uuid import uuid4
from app.database import get_db
from app.models import User
from app.schemas import CategoryCreate, CategoryUpdate, CategoryResponse, CategoryWithCount
from app.crud import (
    create_category,
    get_category_by_id,
    get_category_by_name,
    get_all_categories,
    update_category,
    delete_category,
    get_category_with_products_count,
)
from app.auth import get_current_user


router = APIRouter()


# ✅ Get all categories
@router.get("/", response_model=List[CategoryResponse])
def list_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    categories = get_all_categories(db, skip=skip, limit=limit)
    return categories

# ✅ Get single category
@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = get_category_by_id(db, category_id)
    if not category: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category


# ✅ Get category with products count
@router.get("/{category_id}/count")
def get_category_count(category_id: int, db: Session = Depends(get_db)):
    result = get_category_with_products_count(db, category_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return result


# ✅ Create category (protected)
@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def add_category(
    name: str = Form(...),
    description: str = Form(""),
    image: UploadFile = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing = get_category_by_name(db, name)
    if existing: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category name already exists"
        )

    image_url = None
    if image:
        ext = os.path.splitext(image.filename)[-1]
        filename = f"{uuid4().hex}{ext}"
        upload_folder = os.path.join("static", "categories")
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        with open(file_path, "wb") as f:
            f.write(await image.read())
        image_url = f"/static/categories/{filename}"

    category_in = CategoryCreate(
        name=name,
        description=description,
        image_url=image_url
    )
    new_category = create_category(db, category_in)
    return new_category


# ✅ Update category (protected)
@router.put("/{category_id}", response_model=CategoryResponse)
async def edit_category(
    category_id: int,
    name: str = Form(None),
    description: str = Form(None),
    image: UploadFile = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    category_data = {}
    if name is not None:
        category_data["name"] = name
    if description is not None:
        category_data["description"] = description

    image_url = None
    if image:
        ext = os.path.splitext(image.filename)[-1]
        filename = f"{uuid4().hex}{ext}"
        upload_folder = os.path.join("static", "categories")
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        with open(file_path, "wb") as f:
            f.write(await image.read())
        image_url = f"/static/categories/{filename}"
        category_data["image_url"] = image_url

    updated = update_category(db, category_id, CategoryUpdate(**category_data))
    if not updated: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return updated

# ✅ Delete category (protected)
@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_category(
    category_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    deleted = delete_category(db, category_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return None