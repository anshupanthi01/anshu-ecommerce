from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone:  Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=255)

class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name:  Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at:  datetime

    class Config: 
        from_attributes = True  # For Pydantic v2 (use orm_mode = True for Pydantic v1)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PasswordChange(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=6, max_length=255)