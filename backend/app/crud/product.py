from sqlalchemy.orm import Session
from typing import Optional
from app.models import Product
from app.schemas import ProductCreate, ProductUpdate


def create_product(db: Session, product:  ProductCreate) -> Product:
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


# ✅ Get product by ID
def get_product_by_id(db: Session, product_id: int) -> Optional[Product]: 
    return db.query(Product).filter(Product.id == product_id).first()


# ✅ Get product by SKU
def get_product_by_sku(db: Session, sku: str) -> Optional[Product]:
    return db.query(Product).filter(Product.sku == sku).first()


# ✅ Get all products (with pagination)
def get_all_products(db: Session, skip:  int = 0, limit: int = 100) -> list[Product]:
    return db.query(Product).filter(Product.is_active == 1).offset(skip).limit(limit).all()


# ✅ Get products by category
def get_products_by_category(db: Session, category_id:  int, skip: int = 0, limit: int = 100) -> list[Product]:
    return db.query(Product).filter(
        Product.category_id == category_id,
        Product.is_active == 1
    ).offset(skip).limit(limit).all()


# ✅ Search products by name
def search_products(db: Session, search:  str, skip: int = 0, limit: int = 100) -> list[Product]: 
    return db.query(Product).filter(
        Product.name.ilike(f"%{search}%"),
        Product.is_active == 1
    ).offset(skip).limit(limit).all()


# ✅ Update product
def update_product(db: Session, product_id:  int, product_data: ProductUpdate) -> Optional[Product]: 
    db_product = get_product_by_id(db, product_id)
    if not db_product:
        return None
    
    update_data = product_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product


# ✅ Delete product (soft delete - set is_active to 0)
def delete_product(db:  Session, product_id: int) -> bool:
    db_product = get_product_by_id(db, product_id)
    if not db_product: 
        return False
    
    db_product.is_active = 0
    db.commit()
    return True


# ✅ Hard delete product (permanently remove)
def hard_delete_product(db:  Session, product_id: int) -> bool:
    db_product = get_product_by_id(db, product_id)
    if not db_product: 
        return False
    
    db.delete(db_product)
    db.commit()
    return True


# ✅ Update product stock
def update_stock(db: Session, product_id: int, quantity: int) -> Optional[Product]: 
    db_product = get_product_by_id(db, product_id)
    if not db_product:
        return None
    
    db_product.stock += quantity  # Use negative value to decrease
    db.commit()
    db.refresh(db_product)
    return db_product


# ✅ Check if product is in stock
def is_in_stock(db:  Session, product_id: int, quantity: int = 1) -> bool:
    db_product = get_product_by_id(db, product_id)
    if not db_product:
        return False
    return db_product.stock >= quantity and db_product.is_active == 1