from sqlalchemy.orm import Session
from typing import Optional
from passlib.context import CryptContext
from app.models import User
from app.schemas import UserCreate, UserUpdate


# ✅ Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plain password"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)


# ✅ Create user
def create_user(db: Session, user: UserCreate) -> User:
    hashed_pwd = hash_password(user.password)
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=hashed_pwd,
        phone=user.phone,
        address=user.address,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, user_id: int) -> Optional[User]: 
    return db.query(User).filter(User.id == user_id).first()


# ✅ Get user by email
def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


# ✅ Get all users
def get_all_users(db:  Session, skip: int = 0, limit: int = 100) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()


# ✅ Update user
def update_user(db: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
    db_user = get_user_by_id(db, user_id)
    if not db_user: 
        return None
    
    update_data = user_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


# ✅ Delete user
def delete_user(db: Session, user_id: int) -> bool:
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True


# ✅ Authenticate user (for login)
def authenticate_user(db: Session, email:  str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user