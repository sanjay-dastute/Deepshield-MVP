from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from typing import Dict, Any, Optional
import aiofiles
import os
from datetime import datetime
from ...services.ai.deepfake_detection import DeepfakeDetector
from ...services.ai.content_moderation import ContentModerator
from ...services.ai.face_verification import FaceVerifier
from ..deps import get_current_user
from .notifications import notify_content_flagged, notify_media_misuse

router = APIRouter()

# Initialize AI services
deepfake_detector = DeepfakeDetector()
content_moderator = ContentModerator()
face_verifier = FaceVerifier()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_upload_file(upload_file: UploadFile) -> str:
    """Save uploaded file and return the file path"""
    timestamp = datetime.utcnow().timestamp()
    file_path = os.path.join(UPLOAD_DIR, f"{timestamp}_{upload_file.filename}")
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await upload_file.read()
        await out_file.write(content)
    return file_path

from .notifications import notify_media_misuse

@router.post("/analyze/deepfake")
async def analyze_deepfake(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """Analyze image for potential deepfake"""
    try:
        file_path = await save_upload_file(file)
        result = await deepfake_detector.analyze_image(file_path)
        
        # If deepfake is detected, notify the user
        if result.get("is_deepfake", False):
            await notify_media_misuse(
                user_id=str(current_user["_id"]),
                content={
                    "type": "deepfake",
                    "file_path": file_path,
                    "confidence": result.get("confidence", 0),
                    "details": "Potential deepfake detected in your media."
                }
            )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/analyze/content")
async def analyze_content(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = None,
    language: Optional[str] = "en",
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """Analyze content (image or text) for explicit/abusive content"""
    try:
        if file:
            file_path = await save_upload_file(file)
            result = await content_moderator.analyze_image(file_path)
            
            # If content is flagged, notify the user
            if result.get("is_flagged", False):
                await notify_content_flagged(
                    user_id=str(current_user["_id"]),
                    content={
                        "type": "image",
                        "file_path": file_path,
                        "reason": result.get("reason", "Content policy violation"),
                        "details": result.get("details", "Your content has been flagged for review.")
                    }
                )
        elif text:
            result = await content_moderator.analyze_text(text, language)
            
            # If text content is flagged, notify the user
            if result.get("is_flagged", False):
                await notify_content_flagged(
                    user_id=str(current_user["_id"]),
                    content={
                        "type": "text",
                        "text": text,
                        "reason": result.get("reason", "Content policy violation"),
                        "details": result.get("details", "Your content has been flagged for review.")
                    }
                )
        else:
            raise HTTPException(
                status_code=400,
                detail="Either file or text must be provided"
            )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/verify/face")
async def verify_face(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """Verify if two face images match"""
    try:
        file1_path = await save_upload_file(file1)
        file2_path = await save_upload_file(file2)
        result = await face_verifier.verify_face(file1_path, file2_path)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/extract/face")
async def extract_face(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """Extract face data from image"""
    try:
        file_path = await save_upload_file(file)
        result = await face_verifier.extract_face_data(file_path)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
