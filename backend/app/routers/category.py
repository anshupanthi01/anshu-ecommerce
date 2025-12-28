from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
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
def add_category(
    category: CategoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if category name exists
    existing = get_category_by_name(db, category.name)
    if existing: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category name already exists"
        )
    
    new_category = create_category(db, category)
    return new_category


# ✅ Update category (protected)
@router.put("/{category_id}", response_model=CategoryResponse)
def edit_category(
    category_id: int,
    category_data: CategoryUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated = update_category(db, category_id, category_data)
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