from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    
class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: str
    hashed_password: str
    is_verified: bool = False
    verification_status: str = "pending"
    created_at: datetime
    updated_at: datetime
    
class User(UserBase):
    id: str
    is_verified: bool
    verification_status: str
    created_at: datetime
