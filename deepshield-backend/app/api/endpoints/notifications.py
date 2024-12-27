from typing import Dict, Any
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
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

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """WebSocket endpoint for real-time notifications."""
    await websocket_service.connect(user_id, websocket)
    try:
        while True:
            # Keep the connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        await websocket_service.disconnect(user_id)

@router.post("/notify/content-flagged/{user_id}")
async def notify_content_flagged(
    user_id: str,
    content: Dict[str, Any],
    current_user: User = Depends(get_current_user)
) -> JSONResponse:
    """Notify a user about flagged content."""
    notification_type = "flagged_content"
    
    # Send notifications through all channels
    email_sent = await email_service.send_notification(
        user_id=user_id,
        notification_type=notification_type,
        content=content
    )
    
    sms_sent = await sms_service.send_notification(
        user_id=user_id,
        notification_type=notification_type,
        content=content
    )
    
    websocket_sent = await websocket_service.send_notification(
        user_id=user_id,
        notification_type=notification_type,
        content=content
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

@router.post("/notify/media-misuse/{user_id}")
async def notify_media_misuse(
    user_id: str,
    content: Dict[str, Any],
    current_user: User = Depends(get_current_user)
) -> JSONResponse:
    """Notify a user about potential misuse of their media."""
    notification_type = "media_misuse"
    
    # Send notifications through all channels
    email_sent = await email_service.send_notification(
        user_id=user_id,
        notification_type=notification_type,
        content=content
    )
    
    sms_sent = await sms_service.send_notification(
        user_id=user_id,
        notification_type=notification_type,
        content=content
    )
    
    websocket_sent = await websocket_service.send_notification(
        user_id=user_id,
        notification_type=notification_type,
        content=content
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
