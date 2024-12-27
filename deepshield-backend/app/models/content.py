from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ContentBase(BaseModel):
    user_id: str
    content_type: str  # "image", "video", "text"
    content_url: Optional[str] = None
    content_text: Optional[str] = None
    
class ContentCreate(ContentBase):
    pass

class ContentInDB(ContentBase):
    id: str
    created_at: datetime
    analysis_results: dict
    moderation_status: str = "pending"
    blockchain_hash: Optional[str] = None
    
class Content(ContentBase):
    id: str
    created_at: datetime
    moderation_status: str
    is_flagged: bool = False
