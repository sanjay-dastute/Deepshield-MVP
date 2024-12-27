from typing import Dict, Any, Optional
import json
from fastapi import WebSocket

from .base import NotificationService

class WebSocketNotificationService(NotificationService):
    """Service for sending real-time notifications via WebSocket."""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, user_id: str, websocket: WebSocket):
        """Connect a user's WebSocket."""
        await websocket.accept()
        self.active_connections[user_id] = websocket
    
    async def disconnect(self, user_id: str):
        """Disconnect a user's WebSocket."""
        if user_id in self.active_connections:
            del self.active_connections[user_id]
    
    async def send_notification(
        self,
        user_id: str,
        notification_type: str,
        content: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Send a notification to a connected user via WebSocket."""
        try:
            if user_id in self.active_connections:
                websocket = self.active_connections[user_id]
                notification = {
                    "type": notification_type,
                    "content": content,
                    "metadata": metadata or {}
                }
                await websocket.send_text(json.dumps(notification))
                return True
            return False
        except Exception as e:
            print(f"Failed to send WebSocket notification: {str(e)}")
            return False
