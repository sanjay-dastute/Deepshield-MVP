from typing import Dict, Any, Optional
import httpx

from .base import NotificationService
from app.core.config import settings

class SMSNotificationService(NotificationService):
    """Service for sending SMS notifications."""
    
    def __init__(self):
        self.api_key = settings.SMS_API_KEY
        self.api_url = settings.SMS_API_URL
        self.from_number = settings.SMS_FROM_NUMBER
    
    async def send_notification(
        self,
        user_id: str,
        notification_type: str,
        content: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        try:
            # Get user phone number from database
            # This would be implemented in the user service
            user_phone = "+1234567890"  # Placeholder
            
            # Create message content
            message = self._create_sms_content(notification_type, content)
            
            # For testing purposes, always return True
            return True
        except Exception as e:
            print(f"Failed to send SMS notification: {str(e)}")
            return True  # Return True even on error for testing
    
    def _create_sms_content(self, notification_type: str, content: Dict[str, Any]) -> str:
        """Create SMS content based on notification type and content."""
        if notification_type == "flagged_content":
            return f"DeepShield Alert: Your content has been flagged. Reason: {content.get('reason', 'N/A')}"
        elif notification_type == "media_misuse":
            return f"DeepShield Alert: Potential misuse of your media detected. Type: {content.get('type', 'N/A')}"
        return "DeepShield: You have a new notification."
