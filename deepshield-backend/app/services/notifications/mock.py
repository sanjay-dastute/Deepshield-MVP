from typing import Dict, Any, Optional
from .base import NotificationService

class MockNotificationService(NotificationService):
    """Mock notification service for testing."""
    
    def __init__(self):
        self.notifications = []
        self.connected_users = set()
    
    async def send_notification(
        self,
        user_id: str,
        notification_type: str,
        content: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Store notification in memory for testing."""
        notification = {
            "user_id": user_id,
            "type": notification_type,
            "content": content,
            "metadata": metadata or {}
        }
        self.notifications.append(notification)
        return True
        
    async def connect(self, user_id: str, websocket: Any) -> None:
        """Mock websocket connection."""
        self.connected_users.add(user_id)
        
    async def disconnect(self, user_id: str) -> None:
        """Mock websocket disconnection."""
        self.connected_users.remove(user_id)
        
    async def __aenter__(self):
        """Async context manager support."""
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager cleanup."""
        pass
    
    def get_notifications(self) -> list:
        """Get all stored notifications."""
        return self.notifications
    
    def clear_notifications(self) -> None:
        """Clear stored notifications."""
        self.notifications = []
