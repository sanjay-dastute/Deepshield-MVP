import pytest
import asyncio
import time
from httpx import AsyncClient
from fastapi import FastAPI, WebSocket
from fastapi.testclient import TestClient
from ..main import app
from ..services.notifications.email import EmailNotificationService
from ..services.notifications.sms import SMSNotificationService
from ..services.notifications.websocket import WebSocketNotificationService
from asgi_lifespan import LifespanManager

@pytest.fixture
def test_client():
    return TestClient(app)

@pytest.fixture
async def async_client():
    async with AsyncClient(base_url="http://test") as client:
        yield client

@pytest.fixture
async def test_app():
    async with LifespanManager(app):
        yield app

@pytest.fixture
def email_service():
    return EmailNotificationService()

@pytest.fixture
def sms_service():
    return SMSNotificationService()

@pytest.fixture
def websocket_service():
    """Mock WebSocket notification service fixture"""
    from app.services.notifications.mock import MockNotificationService
    return MockNotificationService()

def test_notify_content_flagged(test_client):
    """Test content flagged notification endpoint"""
    response = test_client.post(
        "/api/v1/notifications/notify/content-flagged/test_user",
        json={
            "request": {
                "type": "image",
                "file_path": "test.jpg",
                "reason": "Test violation",
                "details": "Test details",
                "confidence": 0.95,
                "severity": "high"
            }
        }
    )
    if response.status_code != 200:
        print("Validation Error:", response.json())
    assert response.status_code == 200
    assert response.json()["success"] is True

def test_notify_media_misuse(test_client):
    """Test media misuse notification endpoint"""
    response = test_client.post(
        "/api/v1/notifications/notify/media-misuse/test_user",
        json={
            "request": {
                "type": "deepfake",
                "file_path": "test.jpg",
                "confidence": 0.95,
                "details": "Test details",
                "reason": "Detected deepfake manipulation",
                "severity": "high"
            }
        }
    )
    if response.status_code != 200:
        print("Validation Error:", response.json())
    assert response.status_code == 200
    assert response.json()["success"] is True

@pytest.mark.asyncio
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

@pytest.mark.asyncio
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

@pytest.mark.asyncio
async def test_websocket_notification(websocket_service):
    """Test WebSocket notification service using mock"""
    # Send a test notification using async method
    notification_sent = await websocket_service.send_notification(
        user_id="test_user",
        notification_type="flagged_content",
        content={
            "type": "image",
            "file_path": "test.jpg",
            "reason": "Test violation",
            "details": "Test details",
            "confidence": 0.95,
            "severity": "high"
        }
    )
    assert notification_sent is True
    
    # Verify notification was sent through mock service
    notifications = websocket_service.get_notifications()
    assert len(notifications) > 0
    notification = next(n for n in notifications if n["user_id"] == "test_user")
    assert notification["type"] == "flagged_content"
    assert "reason" in notification["content"]
