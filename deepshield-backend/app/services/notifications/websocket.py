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
        print(f"Connecting WebSocket for user {user_id}")  # Debug log
        try:
            # If there's an existing connection, close it
            if user_id in self.active_connections:
                try:
                    await self.active_connections[user_id].close()
                except Exception:
                    pass
            self.active_connections[user_id] = websocket
            print(f"Active connections: {list(self.active_connections.keys())}")  # Debug log
        except Exception as e:
            print(f"Error connecting WebSocket for user {user_id}: {str(e)}")
            raise
    
    async def disconnect(self, user_id: str):
        """Disconnect a user's WebSocket."""
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].close()
            except Exception:
                pass
            del self.active_connections[user_id]
            print(f"Disconnected WebSocket for user {user_id}")  # Debug log
    
    async def send_notification(
        self,
        user_id: str,
        notification_type: str,
        content: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Send a notification to a connected user via WebSocket."""
        try:
            print(f"Attempting to send notification to user {user_id}")  # Debug log
            print(f"Current active connections: {list(self.active_connections.keys())}")  # Debug log
            if user_id in self.active_connections:
                websocket = self.active_connections[user_id]
                notification = {
                    "type": notification_type,
                    "content": content,
                    "metadata": metadata or {}
                }
                await websocket.send_json(notification)  # Use send_json instead of send_text
                print(f"Successfully sent notification to user {user_id}")  # Debug log
                return True
            print(f"User {user_id} not found in active connections")  # Debug log
            return False
        except Exception as e:
            print(f"Failed to send WebSocket notification: {str(e)}")
            await self.disconnect(user_id)  # Clean up failed connection
            return False
