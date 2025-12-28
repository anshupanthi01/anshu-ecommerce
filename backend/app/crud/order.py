from sqlalchemy.orm import Session
from typing import Optional
from decimal import Decimal
from datetime import datetime
from app.models import Order, OrderItem, Cart, CartItem
from app.schemas import OrderStatus


# ✅ Create order from cart
def create_order_from_cart(db: Session, user_id: int) -> Optional[Order]:
    # Get user's cart
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart or not cart.items:
        return None
    
    # Calculate total amount
    total_amount = Decimal("0.00")
    for item in cart.items:
        total_amount += item.product.price * item.quantity
    
    # Create order
    db_order = Order(
        user_id=user_id,
        status="pending",
        total_amount=total_amount,
        order_date=datetime.utcnow(),
    )
    db.add(db_order)
    db.flush()  # Get order ID without committing
    
    # Create order items from cart items
    for cart_item in cart.items:
        order_item = OrderItem(
            order_id=db_order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            unit_price=cart_item.product.price,
            subtotal=cart_item.product.price * cart_item.quantity,
        )
        db.add(order_item)
        
        # Reduce product stock
        cart_item.product.stock -= cart_item.quantity
    
    # Clear cart
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    
    db.commit()
    db.refresh(db_order)
    return db_order


# ✅ Get order by ID
def get_order_by_id(db:  Session, order_id: int) -> Optional[Order]:
    return db.query(Order).filter(Order.id == order_id).first()


# ✅ Get order by ID with user check
def get_order_by_id_and_user(db:  Session, order_id: int, user_id: int) -> Optional[Order]: 
    return db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == user_id
    ).first()


# ✅ Get all orders for user
def get_user_orders(db:  Session, user_id: int, skip: int = 0, limit: int = 100) -> list[Order]:
    return db.query(Order).filter(
        Order.user_id == user_id
    ).order_by(Order.order_date.desc()).offset(skip).limit(limit).all()


# ✅ Get all orders (admin)
def get_all_orders(db:  Session, skip: int = 0, limit: int = 100) -> list[Order]: 
    return db.query(Order).order_by(Order.order_date.desc()).offset(skip).limit(limit).all()


# ✅ Get orders by status
def get_orders_by_status(db: Session, status: str, skip: int = 0, limit: int = 100) -> list[Order]: 
    return db.query(Order).filter(
        Order.status == status
    ).order_by(Order.order_date.desc()).offset(skip).limit(limit).all()


# ✅ Update order status
def update_order_status(db: Session, order_id: int, status: str) -> Optional[Order]:
    db_order = get_order_by_id(db, order_id)
    if not db_order: 
        return None
    
    db_order.status = status
    db.commit()
    db.refresh(db_order)
    return db_order


# ✅ Cancel order
def cancel_order(db: Session, order_id:  int, user_id: int) -> Optional[Order]: 
    db_order = get_order_by_id_and_user(db, order_id, user_id)
    if not db_order:
        return None
    
    # Only cancel if pending or confirmed
    if db_order.status not in ["pending", "confirmed"]:
        return None
    
    # Restore product stock
    for item in db_order.items:
        item.product.stock += item.quantity
    
    db_order.status = "cancelled"
    db.commit()
    db.refresh(db_order)
    return db_order


# ✅ Get order with items
def get_order_with_items(db: Session, order_id: int) -> Optional[dict]:
    db_order = get_order_by_id(db, order_id)
    if not db_order: 
        return None
    
    items = []
    for item in db_order.items:
        items.append({
            "id": item.id,
            "product_id": item.product_id,
            "quantity": item.quantity,
            "unit_price": item.unit_price,
            "subtotal": item.subtotal,
            "product": {
                "id": item.product.id,
                "name":  item.product.name,
                "price": item.product.price,
            },
        })
    
    return {
        "id":  db_order.id,
        "user_id": db_order.user_id,
        "status": db_order.status,
        "total_amount": db_order.total_amount,
        "order_date": db_order.order_date,
        "created_at": db_order.created_at,
        "updated_at": db_order.updated_at,
        "items": items,
    }


# ✅ Get order summary (list view)
def get_order_summary(db: Session, order_id: int) -> Optional[dict]:
    db_order = get_order_by_id(db, order_id)
    if not db_order:
        return None
    
    items_count = sum(item.quantity for item in db_order.items)
    
    return {
        "id": db_order.id,
        "status": db_order.status,
        "total_amount": db_order.total_amount,
        "order_date": db_order.order_date,
        "items_count": items_count,
    }


# ✅ Delete order (admin only)
def delete_order(db: Session, order_id: int) -> bool:
    db_order = get_order_by_id(db, order_id)
    if not db_order: 
        return False
    
    db.delete(db_order)
    db.commit()
    return True