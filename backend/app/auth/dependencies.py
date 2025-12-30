from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.auth.jwt import verify_token, TokenData


# ✅ OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# ✅ Get current user from token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    print("Token Received:", token)
    token_data = verify_token(token)
    print("Token Data:", token_data)
    if token_data is None:
        raise credentials_exception

    print(f"Querying user: User.id == {token_data.user_id!r} (type: {type(token_data.user_id)})")
    user = db.query(User).filter(User.id == token_data.user_id).first()
    print("Queried User:", user)
    if user is None:
        raise credentials_exception

    return user


# ✅ Optional: Get current user or None (for public routes)
def get_current_user_optional(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Optional[User]:
    try:
        return get_current_user(token, db)
    except HTTPException:
        return None
