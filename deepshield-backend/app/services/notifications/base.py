from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class NotificationService(ABC):
    """Base class for notification services."""
    
    @abstractmethod
    async def send_notification(
        self,
        user_id: str,
        notification_type: str,
        content: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Send a notification to a user.
        
        Args:
            user_id: The ID of the user to notify
            notification_type: Type of notification (e.g., 'flagged_content', 'media_misuse')
            content: The notification content
            metadata: Additional metadata for the notification
            
        Returns:
            bool: True if notification was sent successfully
        """
        pass
