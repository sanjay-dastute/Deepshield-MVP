from typing import List, Dict, Any, Optional
from enum import Enum

class Likelihood(str, Enum):
    """Mock enum for likelihood values."""
    UNKNOWN = "UNKNOWN"
    VERY_UNLIKELY = "VERY_UNLIKELY"
    UNLIKELY = "UNLIKELY"
    POSSIBLE = "POSSIBLE"
    LIKELY = "LIKELY"
    VERY_LIKELY = "VERY_LIKELY"

class Image:
    """Mock Image class for testing."""
    def __init__(self, content: Optional[bytes] = None, source: Optional[str] = None):
        self.content = content
        self.source = source

class MockGoogleVisionAPI:
    """Mock implementation of Google Vision API for testing."""
    
    def __init__(self):
        self.responses = {
            'SAFE': {
                'adult': 'VERY_UNLIKELY',
                'violence': 'VERY_UNLIKELY',
                'racy': 'VERY_UNLIKELY'
            },
            'UNSAFE': {
                'adult': 'VERY_LIKELY',
                'violence': 'LIKELY',
                'racy': 'POSSIBLE'
            }
        }
    
    async def detect_safe_search(self, image_content: bytes) -> Dict[str, str]:
        """Mock safe search detection."""
        # For testing, assume all test images are safe
        return self.responses['SAFE']
    
    async def detect_labels(self, image_content: bytes) -> List[Dict[str, Any]]:
        """Mock label detection."""
        return [
            {'description': 'test_label', 'score': 0.95},
            {'description': 'mock_label', 'score': 0.85}
        ]
    
    async def detect_text(self, image_content: bytes) -> str:
        """Mock text detection."""
        return "Sample detected text for testing"
        
    async def detect_faces(self, image_content: bytes) -> List[Dict[str, Any]]:
        """Mock face detection."""
        return [{
            "detection_confidence": 0.95,
            "joy_likelihood": "LIKELY",
            "anger_likelihood": "VERY_UNLIKELY",
            "surprise_likelihood": "UNLIKELY",
            "headwear_likelihood": "VERY_UNLIKELY"
        }]
