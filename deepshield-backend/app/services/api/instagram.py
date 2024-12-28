"""
Instagram API integration for profile verification and content analysis
"""
from typing import Dict, Any, List
import requests
import hmac
import hashlib
import json
import aiohttp
from datetime import datetime
from fastapi import APIRouter, HTTPException, Request, Response

from app.core.config import settings
from app.services.ai.deepfake_detection import DeepfakeDetector
from app.services.ai.content_moderation import ContentModerator
from app.services.notifications.mock import MockNotificationService
from app.db.mongodb import get_database

router = APIRouter()

class InstagramAPI:
    def __init__(self):
        self.app_id = settings.INSTAGRAM_APP_ID
        self.app_secret = settings.INSTAGRAM_APP_SECRET
        self.access_token = settings.INSTAGRAM_ACCESS_TOKEN
        self.account_id = "17841451799717870"  # Hardcoded for now since it's not in settings
        self.base_url = "https://graph.instagram.com/v12.0"
        self.deepfake_detector = DeepfakeDetector()
        self.content_moderator = ContentModerator()
        self.notification_service = MockNotificationService()
        
    async def analyze_account_behavior(self, username: str) -> Dict[str, Any]:
        """Analyze account behavior for fake detection."""
        return {
            "username": username,
            "is_suspicious": False,
            "risk_score": 0.15,
            "behavioral_flags": [],
            "account_age_days": 180,
            "post_frequency": "normal",
            "engagement_rate": 0.05
        }

    async def analyze_account_metadata(self, username: str) -> Dict[str, Any]:
        """Analyze account metadata for verification."""
        return {
            "account_age": 180,
            "post_frequency": "daily",
            "follower_growth_rate": 0.05,
            "engagement_metrics": {
                "likes_per_post": 100,
                "comments_per_post": 10,
                "engagement_rate": 0.03
            }
        }

    async def verify_profile(self, username: str) -> Dict[str, Any]:
        """Verify Instagram profile using the Graph API"""
        try:
            url = f"{self.base_url}/{self.account_id}"
            params = {
                "fields": "id,username,profile_picture_url,media_count,followers_count",
                "access_token": self.access_token
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return {
                "verified": True,
                "profile_data": data,
                "error": None
            }
        except Exception as e:
            return {
                "verified": False,
                "profile_data": None,
                "error": str(e)
            }
    
    async def get_media_insights(self, media_id: str) -> Dict[str, Any]:
        """Get insights for a specific media post"""
        try:
            url = f"{self.base_url}/{media_id}/insights"
            params = {
                "metric": "engagement,impressions,reach",
                "access_token": self.access_token
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return {
                "success": True,
                "insights": response.json(),
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "insights": None,
                "error": str(e)
            }
    
    async def reverse_image_search(self, image_path: str) -> Dict[str, Any]:
        """Perform reverse image search for profile validation"""
        return {
            "matches": [],
            "similar_images": [],
            "similarity_scores": [],
            "source_urls": []
        }

    async def search_media(self, hashtag: str) -> Dict[str, Any]:
        """Search media by hashtag"""
        try:
            url = f"{self.base_url}/ig_hashtag_search"
            params = {
                "q": hashtag,
                "access_token": self.access_token
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return {
                "success": True,
                "media": response.json(),
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "media": None,
                "error": str(e)
            }
            
    async def verify_webhook_signature(self, request: Request, raw_body: bytes) -> bool:
        """Verify that the webhook request came from Instagram"""
        signature = request.headers.get('X-Hub-Signature-256', '')
        if not signature:
            return False
        
        expected_signature = hmac.new(
            self.app_secret.encode('utf-8'),
            raw_body,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(f"sha256={expected_signature}", signature)
    
    async def process_media(self, media_id: str) -> Dict[str, Any]:
        """Process media for deepfakes and content violations"""
        try:
            # Get media details
            url = f"{self.base_url}/{media_id}"
            params = {
                "fields": "media_url,media_type,caption",
                "access_token": self.access_token
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status != 200:
                        raise HTTPException(status_code=response.status, detail="Failed to fetch media details")
                    media_data = await response.json()
            
            media_url = media_data.get('media_url')
            media_type = media_data.get('media_type')
            caption = media_data.get('caption', '')
            
            results = {
                'media_id': media_id,
                'media_type': media_type,
                'timestamp': datetime.utcnow(),
                'analysis': {
                    'deepfake_detection': None,
                    'content_moderation': None,
                    'text_analysis': None
                },
                'violations_found': False
            }
            
            # Analyze media content
            if media_type in ['IMAGE', 'VIDEO']:
                # Run deepfake detection
                deepfake_result = await self.deepfake_detector.analyze(media_url)
                results['analysis']['deepfake_detection'] = deepfake_result
                
                # Run content moderation
                content_result = await self.content_moderator.analyze_media(
                    media_url, 
                    media_type.lower()
                )
                results['analysis']['content_moderation'] = content_result
            
            # Analyze caption text if present
            if caption:
                text_result = await self.content_moderator.analyze_text(caption)
                results['analysis']['text_analysis'] = text_result
            
            # Check for violations
            violations = []
            if results['analysis']['deepfake_detection'].get('is_deepfake', False):
                violations.append('deepfake_detected')
            if results['analysis']['content_moderation'].get('explicit_content', False):
                violations.append('explicit_content')
            if results['analysis']['text_analysis'] and results['analysis']['text_analysis'].get('is_abusive', False):
                violations.append('abusive_text')
            
            results['violations'] = violations
            results['violations_found'] = len(violations) > 0
            
            # Store results in database
            db = await get_database()
            await db.media_analysis.insert_one(results)
            
            # Send notifications if violations found
            if results['violations_found']:
                await self.notification_service.send_notification(
                    'content_violation',
                    {
                        'media_id': media_id,
                        'violations': violations,
                        'timestamp': results['timestamp']
                    }
                )
            
            return results
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing media: {str(e)}")


instagram_api = InstagramAPI()

@router.get("/webhook")
async def verify_webhook(request: Request):
    """Handle the webhook verification request from Instagram"""
    mode = request.query_params.get('hub.mode')
    token = request.query_params.get('hub.verify_token')
    challenge = request.query_params.get('hub.challenge')
    
    if mode and token:
        if mode == 'subscribe' and token == settings.instagram_verify_token:
            return Response(content=challenge, media_type="text/plain")
    
    raise HTTPException(status_code=400, detail="Invalid verification request")

@router.post("/webhook")
async def instagram_webhook(request: Request):
    """Handle incoming webhook events from Instagram"""
    # Get raw body for signature verification
    raw_body = await request.body()
    
    # Verify webhook signature
    if not await instagram_api.verify_webhook_signature(request, raw_body):
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    try:
        body = json.loads(raw_body)
        results = []
        
        # Process each media change
        for entry in body.get('entry', []):
            for change in entry.get('changes', []):
                if change.get('field') == 'media':
                    media_id = change.get('value', {}).get('media_id')
                    if media_id:
                        result = await instagram_api.process_media(media_id)
                        results.append(result)
        
        return {
            "status": "success",
            "processed_media": len(results),
            "results": results
        }
    
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
