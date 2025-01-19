"""AI service module initialization."""
import logging
import os
from pathlib import Path
from typing import Optional, Type

logger = logging.getLogger(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Ensure dataset directories exist
dataset_dir = Path("/tmp/datasets")
dataset_dir.mkdir(parents=True, exist_ok=True)

# Try to import real implementations
try:
    from .deepfake_detection import DeepfakeDetector
    from .content_moderation import ContentModerator
    from .face_verification import FaceVerifier
    
    __all__ = ['DeepfakeDetector', 'ContentModerator', 'FaceVerifier']
    
    logger.info("Successfully loaded AI model implementations")
except ImportError as e:
    logger.warning(f"Failed to load AI models: {e}")
    # Import mock implementations for testing/fallback
    from .mock_deepfake import MockDeepfakeDetector as DeepfakeDetector
    from .mock_face import MockFaceVerifier as FaceVerifier
    from .content_moderation import ContentModerator  # Try to import real content moderator
    
    logger.info("Using mock implementations for AI models")

def get_content_moderator(test_mode: bool = False) -> Optional[Type[ContentModerator]]:
    """Get content moderator implementation, returns None if not available."""
    if ContentModerator is None:
        logger.warning("Content moderation is not available")
        return None
    return ContentModerator

def is_using_mock_implementations() -> bool:
    """Check if using mock implementations."""
    return DeepfakeDetector.__name__.startswith('Mock')
