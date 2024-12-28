from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import datetime

from ...models.user import User, UserInDB
from ...models.content import ContentFlag
from ...core.security import get_current_admin_user
from ...db.mongodb import get_database

router = APIRouter()

@router.get("/users", response_model=List[UserInDB])
async def get_all_users(
    current_admin: User = Depends(get_current_admin_user),
    db = Depends(get_database)
):
    """Get all users (admin only)"""
    users = await db["users"].find().to_list(1000)
    return [UserInDB(**user) for user in users]

@router.post("/users/{user_id}/verify")
async def verify_user(
    user_id: str,
    current_admin: User = Depends(get_current_admin_user),
    db = Depends(get_database)
):
    """Verify a user (admin only)"""
    result = await db["users"].update_one(
        {"_id": user_id},
        {"$set": {"is_verified": True, "verified_at": datetime.utcnow()}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User verified successfully"}

@router.get("/flags", response_model=List[ContentFlag])
async def get_content_flags(
    current_admin: User = Depends(get_current_admin_user),
    db = Depends(get_database)
):
    """Get all content flags (admin only)"""
    flags = await db["content_flags"].find().to_list(1000)
    return [ContentFlag(**flag) for flag in flags]

@router.patch("/flags/{flag_id}")
async def update_flag_status(
    flag_id: str,
    status: str,
    current_admin: User = Depends(get_current_admin_user),
    db = Depends(get_database)
):
    """Update content flag status (admin only)"""
    valid_statuses = ["pending", "reviewing", "resolved", "dismissed"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )
    
    result = await db["content_flags"].update_one(
        {"_id": flag_id},
        {
            "$set": {
                "status": status,
                "updated_at": datetime.utcnow(),
                "updated_by": current_admin.id
            }
        }
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Flag not found")
    return {"message": "Flag status updated successfully"}

@router.get("/stats")
async def get_admin_stats(
    current_admin: User = Depends(get_current_admin_user),
    db = Depends(get_database)
):
    """Get admin dashboard statistics"""
    total_users = await db["users"].count_documents({})
    verified_users = await db["users"].count_documents({"is_verified": True})
    pending_flags = await db["content_flags"].count_documents({"status": "pending"})
    total_flags = await db["content_flags"].count_documents({})
    
    return {
        "total_users": total_users,
        "verified_users": verified_users,
        "pending_flags": pending_flags,
        "total_flags": total_flags
    }
