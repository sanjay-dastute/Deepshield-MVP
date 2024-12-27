import pytest
from fastapi.testclient import TestClient
from ..main import app
from ..services.notifications.email import EmailNotificationService
from ..services.notifications.sms import SMSNotificationService
from ..services.notifications.websocket import WebSocketNotificationService

client = TestClient(app)

@pytest.fixture
def email_service():
    return EmailNotificationService()

@pytest.fixture
def sms_service():
    return SMSNotificationService()

@pytest.fixture
def websocket_service():
    return WebSocketNotificationService()

def test_notify_content_flagged():
    """Test content flagged notification endpoint"""
    response = client.post(
        "/api/v1/notifications/notify/content-flagged/test_user",
        json={
            "type": "image",
            "file_path": "test.jpg",
            "reason": "Test violation",
            "details": "Test details"
        }
    )
    assert response.status_code == 200
    assert response.json()["success"] is True

def test_notify_media_misuse():
    """Test media misuse notification endpoint"""
    response = client.post(
        "/api/v1/notifications/notify/media-misuse/test_user",
        json={
            "type": "deepfake",
            "file_path": "test.jpg",
            "confidence": 0.95,
            "details": "Test details"
        }
    )
    assert response.status_code == 200
    assert response.json()["success"] is True

async def test_email_notification(email_service):
    """Test email notification service"""
    result = await email_service.send_notification(
        user_id="test_user",
        notification_type="flagged_content",
        content={
            "reason": "Test violation",
            "details": "Test details"
        }
    )
    assert result is True

async def test_sms_notification(sms_service):
    """Test SMS notification service"""
    result = await sms_service.send_notification(
        user_id="test_user",
        notification_type="media_misuse",
        content={
            "type": "deepfake",
            "details": "Test details"
        }
    )
    assert result is True

async def test_websocket_notification(websocket_service):
    """Test WebSocket notification service"""
    # Test connection
    async with client.websocket_connect("/api/v1/notifications/ws/test_user") as websocket:
        # Send a test notification
        result = await websocket_service.send_notification(
            user_id="test_user",
            notification_type="flagged_content",
            content={
                "reason": "Test violation",
                "details": "Test details"
            }
        )
        assert result is True
        
        # Receive the notification
        data = await websocket.receive_json()
        assert data["type"] == "flagged_content"
        assert "reason" in data["content"]
