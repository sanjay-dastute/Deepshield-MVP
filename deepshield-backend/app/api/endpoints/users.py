from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any
from datetime import datetime, timedelta
from ...core.security import create_access_token, get_password_hash, verify_password
from ...models.user import UserCreate, User
from ...db.mongodb import get_database
from datetime import timedelta

router = APIRouter()

@router.post("/register", response_model=User)
async def register_user(user_in: UserCreate):
    db = await get_database()
    # Check for existing email or username
    existing_user = await db.users.find_one({
        "$or": [
            {"email": user_in.email},
            {"username": user_in.username}
        ]
    })
    if existing_user:
        if existing_user["email"] == user_in.email:
            raise HTTPException(status_code=400, detail="Email already registered")
        else:
            raise HTTPException(status_code=400, detail="Username already taken")
    
    user_dict = user_in.dict()
    user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
    user_dict["created_at"] = datetime.utcnow()
    user_dict["updated_at"] = user_dict["created_at"]
    user_dict["is_verified"] = False
    user_dict["verification_status"] = "pending"
    
    result = await db.users.insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)
    return User(**user_dict)

@router.post("/login")
async def login(email: str, password: str) -> Any:
    db = await get_database()
    user = await db.users.find_one({"email": email})
    if not user or not verify_password(password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user["_id"])}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
