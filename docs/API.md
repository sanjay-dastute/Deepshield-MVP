# DeepShield API Documentation

## Authentication

### Register User
```http
POST /api/v1/users/register
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "securepassword",
    "username": "username"
}
```

### Login
```http
POST /api/v1/users/login
Content-Type: application/json

{
    "username": "username",
    "password": "securepassword"
}
```

Response:
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer"
}
```

## Content Analysis

### Analyze Media for Deepfakes
```http
POST /api/v1/ai/analyze/deepfake
Content-Type: multipart/form-data
Authorization: Bearer <token>

file: <media_file>
```

Response:
```json
{
    "is_deepfake": boolean,
    "confidence": float,
    "analysis_details": {
        "facial_inconsistencies": [],
        "manipulation_score": float
    }
}
```

### Content Moderation
```http
POST /api/v1/ai/analyze/content
Content-Type: multipart/form-data
Authorization: Bearer <token>

file: <media_file>
type: "image" | "video" | "text"
content: string (optional, for text analysis)
```

Response:
```json
{
    "explicit_content": boolean,
    "abusive_content": boolean,
    "confidence_scores": {
        "nsfw": float,
        "hate_speech": float
    },
    "detected_violations": []
}
```

### Face Verification
```http
POST /api/v1/ai/verify/face
Content-Type: multipart/form-data
Authorization: Bearer <token>

reference_image: <file>
verification_image: <file>
```

Response:
```json
{
    "match": boolean,
    "confidence": float,
    "verification_details": {
        "facial_landmarks_match": float,
        "similarity_score": float
    }
}
```

## Instagram Integration

### Webhook Verification
```http
GET /api/v1/instagram/webhook
```

### Media Processing Webhook
```http
POST /api/v1/instagram/webhook
Content-Type: application/json
X-Hub-Signature-256: sha256=...

{
    "entry": [{
        "changes": [{
            "field": "media",
            "value": {
                "media_id": "..."
            }
        }]
    }]
}
```

### Profile Verification
```http
POST /api/v1/instagram/verify-profile
Content-Type: application/json
Authorization: Bearer <token>

{
    "username": "instagram_username"
}
```

## Notifications

### Get User Notifications
```http
GET /api/v1/notifications
Authorization: Bearer <token>
```

### Update Notification Settings
```http
PUT /api/v1/notifications/settings
Content-Type: application/json
Authorization: Bearer <token>

{
    "email_notifications": boolean,
    "sms_notifications": boolean,
    "notification_types": ["content_violation", "account_security"]
}
```

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
    "detail": "Invalid request parameters"
}
```

### 401 Unauthorized
```json
{
    "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
    "detail": "Not enough privileges"
}
```

### 404 Not Found
```json
{
    "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
    "detail": "Internal server error"
}
```
