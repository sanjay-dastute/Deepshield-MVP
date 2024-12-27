"""
Instagram API integration for profile verification and content analysis
"""
from typing import Dict, Any
import requests
from app.config import settings

class InstagramAPI:
    def __init__(self):
        self.app_id = settings.instagram_app_id
        self.app_secret = settings.instagram_app_secret
        self.access_token = settings.instagram_access_token
        self.account_id = settings.instagram_account_id
        self.base_url = "https://graph.instagram.com/v12.0"
        
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
