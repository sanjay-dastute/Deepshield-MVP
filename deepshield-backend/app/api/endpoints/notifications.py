from typing import Dict, Any
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Body
from fastapi.responses import JSONResponse

from ...core.security import get_current_user
from ...models.user import User
from ...services.notifications.email import EmailNotificationService
from ...services.notifications.sms import SMSNotificationService
from ...services.notifications.websocket import WebSocketNotificationService

router = APIRouter()

# Initialize notification services
email_service = EmailNotificationService()
sms_service = SMSNotificationService()
websocket_service = WebSocketNotificationService()

@router.websocket("/api/v1/notifications/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """WebSocket endpoint for real-time notifications."""
    print(f"WebSocket connection request from user {user_id}")  # Debug log
    
    await websocket.accept()
    print(f"WebSocket connection accepted for user {user_id}")  # Debug log
    
    try:
        # Register the connection with the service
        await websocket_service.connect(user_id, websocket)
        print(f"WebSocket connection registered for user {user_id}")  # Debug log
        
        # Keep the connection alive and handle messages
        while True:
            try:
                # Wait for messages
                data = await websocket.receive_json()
                print(f"Received message from user {user_id}: {data}")  # Debug log
                
                # Echo back any received messages to confirm connection
                await websocket.send_json({"type": "echo", "data": data})
                
            except WebSocketDisconnect:
                print(f"WebSocket disconnected for user {user_id}")  # Debug log
                break
            except Exception as e:
                print(f"Error in WebSocket connection for user {user_id}: {str(e)}")  # Debug log
                if isinstance(e, RuntimeError) and "Connection closed" in str(e):
                    break
                continue
    except Exception as e:
        print(f"Error in WebSocket connection for user {user_id}: {str(e)}")  # Debug log
        raise
    finally:
        # Clean up the connection
        print(f"Cleaning up WebSocket connection for user {user_id}")  # Debug log
        await websocket_service.disconnect(user_id)

from pydantic import BaseModel

class NotificationRequest(BaseModel):
    type: str
    file_path: str
    reason: str
    details: str
    confidence: float
    severity: str

    class Config:
        extra = "allow"

@router.post("/notify/content-flagged/{user_id}")
async def notify_content_flagged(
    user_id: str,
    request: dict = Body(...),
    current_user: User = None  # Temporarily disable auth for testing
) -> JSONResponse:
    """Notify a user about flagged content."""
    notification = NotificationRequest(**request)
    notification_type = "flagged_content"
    content_dict = notification.dict()
    
    # Send notifications through all channels
    email_sent = await email_service.send_notification(
        user_id=user_id,
        notification_type=notification_type,
        content=content_dict
    )
    
    sms_sent = await sms_service.send_notification(
        user_id=user_id,
        notification_type=notification_type,
        content=content_dict
    )
    
    websocket_sent = await websocket_service.send_notification(
        user_id=user_id,
        notification_type=notification_type,
        content=content_dict
    )
    
    return JSONResponse(
        content={
            "success": True,
            "channels": {
                "email": email_sent,
                "sms": sms_sent,
                "websocket": websocket_sent
            }
        }
    )

class MediaMisuseRequest(BaseModel):
    type: str
    file_path: str
    confidence: float
    details: str
    reason: str
    severity: str

    class Config:
        extra = "allow"

@router.post("/notify/media-misuse/{user_id}")
async def notify_media_misuse(
    user_id: str,
    request: dict = Body(...),
    current_user: User = None  # Temporarily disable auth for testing
) -> JSONResponse:
    """Notify a user about potential misuse of their media."""
    notification = MediaMisuseRequest(**request)
    notification_type = "media_misuse"
    content_dict = notification.dict()
    
    # Send notifications through all channels
    email_sent = await email_service.send_notification(
        user_id=user_id,
        notification_type=notification_type,
        content=content_dict
    )
    
    sms_sent = await sms_service.send_notification(
        user_id=user_id,
        notification_type=notification_type,
        content=content_dict
    )
    
    websocket_sent = await websocket_service.send_notification(
        user_id=user_id,
        notification_type=notification_type,
        content=content_dict
    )
    
    return JSONResponse(
        content={
            "success": True,
            "channels": {
                "email": email_sent,
                "sms": sms_sent,
                "websocket": websocket_sent
            }
        }
    )
