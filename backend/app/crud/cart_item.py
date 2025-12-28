from sqlalchemy.orm import Session
from typing import Optional
from app.models import CartItem, Cart, Product
from app.schemas import CartItemCreate, CartItemUpdate


# ✅ Add item to cart
def add_item_to_cart(db: Session, cart_id: int, item:  CartItemCreate) -> Optional[CartItem]: 
    # Check if product exists and is active
    product = db.query(Product).filter(
        Product.id == item.product_id,
        Product.is_active == 1
    ).first()
    if not product:
        return None
    
    # Check if item already exists in cart
    existing_item = db.query(CartItem).filter(
        CartItem.cart_id == cart_id,
        CartItem.product_id == item.product_id
    ).first()
    
    if existing_item:
        # Update quantity if item exists
        existing_item.quantity += item.quantity
        db.commit()
        db.refresh(existing_item)
        return existing_item
    
    # Create new cart item
    db_item = CartItem(
        cart_id=cart_id,
        product_id=item.product_id,
        quantity=item.quantity,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# ✅ Get cart item by ID
def get_cart_item_by_id(db: Session, item_id: int) -> Optional[CartItem]:
    return db.query(CartItem).filter(CartItem.id == item_id).first()


# ✅ Get cart item by cart and product
def get_cart_item_by_product(db: Session, cart_id: int, product_id:  int) -> Optional[CartItem]:
    return db.query(CartItem).filter(
        CartItem.cart_id == cart_id,
        CartItem.product_id == product_id
    ).first()


# ✅ Get all items in cart
def get_cart_items(db:  Session, cart_id: int) -> list[CartItem]: 
    return db.query(CartItem).filter(CartItem.cart_id == cart_id).all()


# ✅ Update cart item quantity
def update_cart_item(db: Session, item_id: int, item_data: CartItemUpdate) -> Optional[CartItem]: 
    db_item = get_cart_item_by_id(db, item_id)
    if not db_item:
        return None
    
    db_item.quantity = item_data.quantity
    db.commit()
    db.refresh(db_item)
    return db_item


# ✅ Update cart item quantity by cart and product
def update_cart_item_by_product(db:  Session, cart_id: int, product_id: int, quantity: int) -> Optional[CartItem]: 
    db_item = get_cart_item_by_product(db, cart_id, product_id)
    if not db_item:
        return None
    
    db_item.quantity = quantity
    db.commit()
    db.refresh(db_item)
    return db_item


# ✅ Remove item from cart
def remove_cart_item(db:  Session, item_id: int) -> bool:
    db_item = get_cart_item_by_id(db, item_id)
    if not db_item:
        return False
    
    db.delete(db_item)
    db.commit()
    return True


# ✅ Remove item from cart by product
def remove_cart_item_by_product(db: Session, cart_id:  int, product_id: int) -> bool:
    db_item = get_cart_item_by_product(db, cart_id, product_id)
    if not db_item: 
        return False
    
    db.delete(db_item)
    db.commit()
    return True


# ✅ Increase item quantity
def increase_quantity(db: Session, item_id: int, amount: int = 1) -> Optional[CartItem]: 
    db_item = get_cart_item_by_id(db, item_id)
    if not db_item: 
        return None
    
    db_item.quantity += amount
    db.commit()
    db.refresh(db_item)
    return db_item


# ✅ Decrease item quantity (remove if 0)
def decrease_quantity(db: Session, item_id: int, amount: int = 1) -> Optional[CartItem]:
    db_item = get_cart_item_by_id(db, item_id)
    if not db_item:
        return None
    
    db_item.quantity -= amount
    
    if db_item.quantity <= 0:
        db.delete(db_item)
        db.commit()
        return None
    
    db.commit()
    db.refresh(db_item)
    return db_item