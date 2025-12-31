from sqlalchemy.orm import Session, joinedload
from typing import Optional
from decimal import Decimal
from app.models import Cart, CartItem, Product


# ✅ Create cart for user
def create_cart(db: Session, user_id: int) -> Cart:
    db_cart = Cart(user_id=user_id)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart


# ✅ Get cart by ID
def get_cart_by_id(db: Session, cart_id: int) -> Optional[Cart]: 
    return db.query(Cart).filter(Cart.id == cart_id).first()


# ✅ Get cart by user ID
def get_cart_by_user_id(db: Session, user_id: int) -> Optional[Cart]: 
    return db.query(Cart).filter(Cart.user_id == user_id).first()


# ✅ Get or create cart for user
def get_or_create_cart(db: Session, user_id: int) -> Cart:
    db_cart = get_cart_by_user_id(db, user_id)
    if not db_cart: 
        db_cart = create_cart(db, user_id)
    return db_cart


# ✅ Get cart with items
def get_cart_with_items(db: Session, user_id: int) -> dict:
    cart = db.query(Cart)\
        .options(joinedload(Cart.items).joinedload(CartItem.product))\
        .filter(Cart.user_id == user_id)\
        .first()
    if not cart:
        return None

    items = []
    total_amount = 0
    for item in cart.items:
        product = item.product
        item_total = float(item.quantity) * float(product.price)
        items.append({
            "id": item.id,
            "product_id": item.product_id,
            "quantity": item.quantity,
            "cart_id": item.cart_id,
            "item_total": item_total,
            "product": {
                "id": product.id,
                "name": product.name,
                "price": float(product.price),
                "stock": product.stock,
                "is_active": product.is_active,
                "image_url": product.image_url,   # <-- Ensures image_url included
            }
        })
        total_amount += item_total

    return {
        "id": cart.id,
        "user_id": cart.user_id,
        "items": items,
        "total_items": len(items),
        "total_amount": total_amount,
    }

# ✅ Get cart summary (for navbar)
def get_cart_summary(db: Session, user_id: int) -> dict:
    db_cart = get_cart_by_user_id(db, user_id)
    if not db_cart:
        return {
            "id": None,
            "total_items": 0,
            "total_amount": Decimal("0.00"),
        }
    
    total_items = 0
    total_amount = Decimal("0.00")
    
    for item in db_cart.items:
        total_items += item.quantity
        total_amount += item.product.price * item.quantity
    
    return {
        "id": db_cart.id,
        "total_items": total_items,
        "total_amount": total_amount,
    }


# ✅ Clear cart (remove all items)
def clear_cart(db: Session, user_id: int) -> bool:
    db_cart = get_cart_by_user_id(db, user_id)
    if not db_cart:
        return False
    
    db.query(CartItem).filter(CartItem.cart_id == db_cart.id).delete()
    db.commit()
    return True


# ✅ Delete cart
def delete_cart(db: Session, user_id: int) -> bool:
    db_cart = get_cart_by_user_id(db, user_id)
    if not db_cart: 
        return False
    
    db.delete(db_cart)
    db.commit()
    return True