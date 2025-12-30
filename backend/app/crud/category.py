from sqlalchemy.orm import Session
from typing import Optional
from app.models import Category
from app.schemas import CategoryCreate, CategoryUpdate


# ✅ Create category
def create_category(db: Session, category: CategoryCreate) -> Category:
    db_category = Category(
        name=category.name,
        description=category.description,
        image_url=category.image_url
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


# ✅ Get category by ID
def get_category_by_id(db: Session, category_id: int) -> Optional[Category]: 
    return db.query(Category).filter(Category.id == category_id).first()


# ✅ Get category by name
def get_category_by_name(db: Session, name: str) -> Optional[Category]: 
    return db.query(Category).filter(Category.name == name).first()


# ✅ Get all categories
def get_all_categories(db: Session, skip: int = 0, limit: int = 100) -> list[Category]: 
    return db.query(Category).offset(skip).limit(limit).all()


# ✅ Update category
def update_category(db: Session, category_id:  int, category_data: CategoryUpdate) -> Optional[Category]: 
    db_category = get_category_by_id(db, category_id)
    if not db_category: 
        return None
    
    update_data = category_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_category, key, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category


# ✅ Delete category
def delete_category(db: Session, category_id: int) -> bool:
    db_category = get_category_by_id(db, category_id)
    if not db_category: 
        return False
    
    db.delete(db_category)
    db.commit()
    return True


# ✅ Get category with products count
def get_category_with_products_count(db: Session, category_id: int) -> Optional[dict]:
    db_category = get_category_by_id(db, category_id)
    if not db_category: 
        return None
    
    return {
        "id": db_category.id,
        "name": db_category.name,
        "description": db_category.description,
        "created_at": db_category.created_at,
        "updated_at": db_category.updated_at,
        "products_count": len(db_category.products),
    }