"""Content notification service module."""
from typing import Dict, Any
from ..notifications.email import EmailNotificationService
from ..notifications.sms import SMSNotificationService
from ..notifications.websocket import WebSocketNotificationService

# Initialize notification services
email_service = EmailNotificationService()
sms_service = SMSNotificationService()
websocket_service = WebSocketNotificationService()

async def notify_content_flagged(user_id: str, content: Dict[str, Any]) -> Dict[str, bool]:
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
    
    return {
        "email": email_sent,
        "sms": sms_sent,
        "websocket": websocket_sent
    }
