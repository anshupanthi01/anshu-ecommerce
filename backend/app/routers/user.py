from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserResponse, UserUpdate, PasswordChange
from app.crud import get_user_by_id, update_user, delete_user, hash_password, verify_password
from app.auth import get_current_user


router = APIRouter()


# ✅ Get current user profile
@router.get("/me", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user


# ✅ Update profile
@router.put("/me", response_model=UserResponse)
def update_profile(
    user_data:  UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated_user = update_user(db, current_user.id, user_data)
    return updated_user


# ✅ Change password
@router.put("/me/password")
def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify current password
    if not verify_password(password_data.current_password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Update password
    current_user.password = hash_password(password_data.new_password)
    db.commit()
    
    return {"message": "Password updated successfully"}


# ✅ Delete account
@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    delete_user(db, current_user.id)
    return None