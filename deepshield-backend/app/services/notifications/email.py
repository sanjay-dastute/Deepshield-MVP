import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Optional

from .base import NotificationService
from app.core.config import settings

class EmailNotificationService(NotificationService):
    """Service for sending email notifications."""
    
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = settings.FROM_EMAIL
    
    async def send_notification(
        self,
        user_id: str,
        notification_type: str,
        content: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        try:
            # Get user email from database
            # This would be implemented in the user service
            user_email = "user@example.com"  # Placeholder
            
            # Create message
            message = MIMEMultipart()
            message["From"] = self.from_email
            message["To"] = user_email
            message["Subject"] = self._get_subject(notification_type)
            
            # Create HTML body
            html = self._create_email_body(notification_type, content)
            message.attach(MIMEText(html, "html"))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(message)
            
            return True
        except Exception as e:
            print(f"Failed to send email notification: {str(e)}")
            return False
    
    def _get_subject(self, notification_type: str) -> str:
        """Get email subject based on notification type."""
        subjects = {
            "flagged_content": "Content Flagged - DeepShield Alert",
            "media_misuse": "Media Misuse Detected - DeepShield Alert",
        }
        return subjects.get(notification_type, "DeepShield Notification")
    
    def _create_email_body(self, notification_type: str, content: Dict[str, Any]) -> str:
        """Create HTML email body based on notification type and content."""
        if notification_type == "flagged_content":
            return f"""
            <html>
                <body>
                    <h2>Content Flagged</h2>
                    <p>Your content has been flagged for review:</p>
                    <p><strong>Reason:</strong> {content.get('reason', 'N/A')}</p>
                    <p><strong>Details:</strong> {content.get('details', 'N/A')}</p>
                </body>
            </html>
            """
        elif notification_type == "media_misuse":
            return f"""
            <html>
                <body>
                    <h2>Media Misuse Detected</h2>
                    <p>We detected potential misuse of your media:</p>
                    <p><strong>Type:</strong> {content.get('type', 'N/A')}</p>
                    <p><strong>Details:</strong> {content.get('details', 'N/A')}</p>
                </body>
            </html>
            """
        return """
        <html>
            <body>
                <h2>DeepShield Notification</h2>
                <p>You have a new notification from DeepShield.</p>
            </body>
        </html>
        """
