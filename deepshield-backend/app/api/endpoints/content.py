from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import List
import aiofiles
import os
from datetime import datetime
from ...models.content import ContentCreate, Content
from ...db.mongodb import get_database
from ...core.blockchain import SimpleBlockchain
from ..deps import get_current_user

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

from .notifications import notify_content_flagged

@router.post("/upload", response_model=Content)
async def upload_content(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    # Save file
    file_path = os.path.join(UPLOAD_DIR, f"{datetime.utcnow().timestamp()}_{file.filename}")
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
    
    # Create content record
    content_data = {
        "user_id": str(current_user["_id"]),
        "content_type": file.content_type,
        "content_url": file_path,
        "created_at": datetime.utcnow(),
        "analysis_results": {},
        "moderation_status": "pending"
    }
    
    # Create blockchain hash
    content_hash = SimpleBlockchain.create_hash(content_data)
    content_data["blockchain_hash"] = content_hash
    
    db = await get_database()
    result = await db.content.insert_one(content_data)
    content_data["id"] = str(result.inserted_id)
    
    # Trigger content moderation and notification if needed
    if content_data.get("moderation_status") == "flagged":
        await notify_content_flagged(
            user_id=str(current_user["_id"]),
            content={
                "content_id": str(result.inserted_id),
                "reason": content_data.get("analysis_results", {}).get("reason", "Content policy violation"),
                "details": content_data.get("analysis_results", {}).get("details", "Your content has been flagged for review.")
            }
        )
    
    return Content(**content_data)

@router.get("/user/{user_id}", response_model=List[Content])
async def get_user_content(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    if str(current_user["_id"]) != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to view this content")
    
    db = await get_database()
    cursor = db.content.find({"user_id": user_id})
    contents = await cursor.to_list(length=100)
    return [Content(**content) for content in contents]
