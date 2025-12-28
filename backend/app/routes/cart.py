from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import CartItemCreate, CartItemUpdate
from app.crud import (
    get_or_create_cart,
    get_cart_with_items,
    get_cart_summary,
    clear_cart,
    add_item_to_cart,
    get_cart_item_by_id,
    update_cart_item,
    remove_cart_item,
)
from app.auth import get_current_user


router = APIRouter()


# ✅ Get cart
@router.get("/")
def get_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cart = get_cart_with_items(db, current_user.id)
    if not cart:
        # Return empty cart
        return {
            "id": None,
            "user_id": current_user.id,
            "items": [],
            "total_items": 0,
            "total_amount": 0,
        }
    return cart


# ✅ Get cart summary (for navbar)
@router.get("/summary")
def cart_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    summary = get_cart_summary(db, current_user.id)
    return summary


# ✅ Add item to cart
@router.post("/items", status_code=status.HTTP_201_CREATED)
def add_to_cart(
    item: CartItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get or create cart
    cart = get_or_create_cart(db, current_user.id)
    
    # Add item
    cart_item = add_item_to_cart(db, cart.id, item)
    if not cart_item: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product not found or not available"
        )
    
    return {"message": "Item added to cart", "item_id": cart_item.id}


# ✅ Update cart item quantity
@router.put("/items/{item_id}")
def update_cart_item_quantity(
    item_id: int,
    item_data: CartItemUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify item belongs to user's cart
    cart_item = get_cart_item_by_id(db, item_id)
    if not cart_item: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    
    if cart_item.cart.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    updated = update_cart_item(db, item_id, item_data)
    return {"message": "Cart item updated"}


# ✅ Remove item from cart
@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_cart(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify item belongs to user's cart
    cart_item = get_cart_item_by_id(db, item_id)
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    
    if cart_item.cart.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    remove_cart_item(db, item_id)
    return None


# ✅ Clear cart
@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def empty_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    clear_cart(db, current_user.id)
    return None