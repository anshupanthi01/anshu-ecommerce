from sqlalchemy.orm import Session
from typing import Optional
from decimal import Decimal
from app.models import OrderItem, Product
from app.schemas import OrderItemCreate


# ✅ Create order item
def create_order_item(db: Session, order_id: int, item: OrderItemCreate) -> Optional[OrderItem]:
    product = db.query(Product).filter(Product.id == item. product_id).first()
    if not product:
        return None
    
    subtotal = product.price * item.quantity
    
    db_item = OrderItem(
        order_id=order_id,
        product_id=item.product_id,
        quantity=item.quantity,
        unit_price=product.price,
        subtotal=subtotal,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# ✅ Get order item by ID
def get_order_item_by_id(db: Session, item_id: int) -> Optional[OrderItem]: 
    return db.query(OrderItem).filter(OrderItem.id == item_id).first()


# ✅ Get all items for order
def get_order_items(db: Session, order_id: int) -> list[OrderItem]: 
    return db.query(OrderItem).filter(OrderItem.order_id == order_id).all()


# ✅ Get order item with product details
def get_order_item_with_product(db: Session, item_id: int) -> Optional[dict]:
    db_item = get_order_item_by_id(db, item_id)
    if not db_item:
        return None
    
    return {
        "id": db_item.id,
        "order_id": db_item.order_id,
        "product_id": db_item.product_id,
        "quantity": db_item.quantity,
        "unit_price": db_item.unit_price,
        "subtotal": db_item.subtotal,
        "product": {
            "id": db_item.product.id,
            "name": db_item.product.name,
            "price": db_item.product.price,
            "sku": db_item.product.sku,
        },
    }


# ✅ Get all order items with product details
def get_order_items_with_products(db: Session, order_id: int) -> list[dict]:
    items = get_order_items(db, order_id)
    
    result = []
    for item in items: 
        result.append({
            "id": item.id,
            "order_id": item.order_id,
            "product_id": item.product_id,
            "quantity": item.quantity,
            "unit_price": item.unit_price,
            "subtotal": item.subtotal,
            "product": {
                "id": item.product.id,
                "name": item.product.name,
                "price": item.product.price,
                "sku": item.product.sku,
            },
        })
    
    return result


# ✅ Calculate order total from items
def calculate_order_total(db: Session, order_id: int) -> Decimal:
    items = get_order_items(db, order_id)
    total = Decimal("0.00")
    for item in items: 
        total += item.subtotal
    return total