from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List
from app.models import Product
from app.schemas import ProductCreate, ProductUpdate


def create_product(db: Session, product: ProductCreate) -> Product:
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        sku=product.sku,
        category_id=product.category_id,
        image_url=product.image_url
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product_by_id(db: Session, product_id: int) -> Optional[Product]:
    return db.query(Product).filter(Product.id == product_id).first()


def get_product_by_sku(db: Session, sku: str) -> Optional[Product]:
    return db.query(Product).filter(Product.sku == sku).first()


def get_all_products(db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
    return db.query(Product).offset(skip).limit(limit).all()


def get_filtered_products(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
) -> List[Product]:
    query = db.query(Product)

    if category_id:
        query = query.filter(Product.category_id == category_id)

    if search:
        query = query.filter(
            or_(
                Product.name.ilike(f"%{search}%"),
                Product.description.ilike(f"%{search}%"),
            )
        )

    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    return query.offset(skip).limit(limit).all()


def get_products_by_category(db: Session, category_id: int, skip: int = 0, limit: int = 100) -> List[Product]:
    return db.query(Product).filter(Product.category_id == category_id).offset(skip).limit(limit).all()


def search_products(db: Session, query_str: str, skip: int = 0, limit: int = 100) -> List[Product]:
    return db.query(Product).filter(
        or_(
            Product.name.ilike(f"%{query_str}%"),
            Product.description.ilike(f"%{query_str}%")
        )
    ).offset(skip).limit(limit).all()


def update_product(db: Session, product_id: int, product_update: ProductUpdate) -> Optional[Product]:
    db_product = get_product_by_id(db, product_id)
    if not db_product:
        return None
    
    update_data = product_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int) -> bool:
    # Soft delete if is_active exists, else hard delete or just return false
    # Assuming soft delete based on previous code snippet
    db_product = get_product_by_id(db, product_id)
    if not db_product:
        return False
    
    # Check if is_active exists on model, otherwise hard delete
    if hasattr(db_product, 'is_active'):
        db_product.is_active = 0
        db.commit()
    else:
        db.delete(db_product)
        db.commit()
        
    return True


def hard_delete_product(db: Session, product_id: int) -> bool:
    db_product = get_product_by_id(db, product_id)
    if not db_product:
        return False
    
    db.delete(db_product)
    db.commit()
    return True


def update_stock(db: Session, product_id: int, quantity: int) -> Optional[Product]:
    db_product = get_product_by_id(db, product_id)
    if not db_product:
        return None
    
    db_product.stock += quantity
    db.commit()
    db.refresh(db_product)
    return db_product


def is_in_stock(db: Session, product_id: int, quantity: int = 1) -> bool:
    db_product = get_product_by_id(db, product_id)
    if not db_product:
        return False
    # Check is_active if it exists
    is_active = getattr(db_product, 'is_active', 1)
    return db_product.stock >= quantity and is_active == 1