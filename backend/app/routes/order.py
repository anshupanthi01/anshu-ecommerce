from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import User
from app.schemas import OrderResponse, OrderUpdate, OrderDetail
from app.crud import (
    create_order_from_cart,
    get_order_by_id_and_user,
    get_user_orders,
    get_order_with_items,
    cancel_order,
)
from app.auth import get_current_user


router = APIRouter()


# ✅ Get all orders for current user
@router.get("/", response_model=List[OrderDetail])
def list_orders(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    orders = get_user_orders(db, current_user.id, skip=skip, limit=limit)
    return orders


# ✅ Get single order
@router.get("/{order_id}")
def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = get_order_with_items(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Verify order belongs to user
    if order["user_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    return order


# ✅ Create order from cart (checkout)
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_order(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = create_order_from_cart(db, current_user.id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty or not found"
        )
    
    return {
        "message": "Order created successfully",
        "order_id": order.id,
        "total_amount": order.total_amount,
    }


# ✅ Cancel order
@router.put("/{order_id}/cancel")
def cancel_user_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = cancel_order(db, order_id, current_user.id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order not found or cannot be cancelled"
        )
    
    return {"message": "Order cancelled successfully"}