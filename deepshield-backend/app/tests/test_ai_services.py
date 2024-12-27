import pytest
import os
import shutil
from pathlib import Path
from ..services.ai.deepfake_detection import DeepfakeDetector
from ..services.ai.content_moderation import ContentModerator
from ..services.ai.face_verification import FaceVerifier

# Create test data directory
TEST_DATA_DIR = Path("test_data")
TEST_DATA_DIR.mkdir(exist_ok=True)

# Create sample test images
def create_sample_image(filename: str, size=(128, 128)):
    import numpy as np
    import cv2
    # Create a simple test image
    img = np.zeros((*size, 3), dtype=np.uint8)
    cv2.circle(img, (size[0]//2, size[1]//2), min(size)//3, (255, 255, 255), -1)
    cv2.imwrite(str(TEST_DATA_DIR / filename), img)
    return str(TEST_DATA_DIR / filename)

@pytest.fixture(scope="session", autouse=True)
def setup_test_data():
    # Create test images
    create_sample_image("test_image1.jpg")
    create_sample_image("test_image2.jpg")
    yield
    # Cleanup after tests
    shutil.rmtree(TEST_DATA_DIR)

@pytest.fixture
def deepfake_detector():
    return DeepfakeDetector()

@pytest.fixture
def content_moderator():
    return ContentModerator()

@pytest.fixture
def face_verifier():
    return FaceVerifier()

@pytest.mark.asyncio
async def test_deepfake_detection(deepfake_detector):
    # Test initialization
    assert deepfake_detector is not None
    assert deepfake_detector.model is not None
    assert deepfake_detector.face_detection is not None
    
    # Test image analysis
    result = await deepfake_detector.analyze_image(str(TEST_DATA_DIR / "test_image1.jpg"))
    assert isinstance(result, dict)
    assert "is_deepfake" in result
    assert "confidence" in result
    assert "error" in result

@pytest.mark.asyncio
async def test_content_moderation(content_moderator):
    # Test text moderation
    result = await content_moderator.analyze_text("This is a normal text")
    assert result["is_toxic"] is False
    assert "confidence" in result
    assert result["error"] is None

    result = await content_moderator.analyze_text("You are stupid and I hate you")
    assert result["is_toxic"] is True
    assert result["confidence"] > 0.5
    
    # Test image moderation
    result = await content_moderator.analyze_image(str(TEST_DATA_DIR / "test_image1.jpg"))
    assert isinstance(result, dict)
    assert "is_explicit" in result
    assert "confidence" in result
    assert "error" in result

@pytest.mark.asyncio
async def test_face_verification(face_verifier):
    # Test initialization
    assert face_verifier is not None
    assert face_verifier.model is not None
    
    # Test face verification
    result = await face_verifier.verify_face(
        str(TEST_DATA_DIR / "test_image1.jpg"),
        str(TEST_DATA_DIR / "test_image2.jpg")
    )
    assert isinstance(result, dict)
    assert "match" in result
    assert "similarity" in result
    assert "face_data" in result
    assert "error" in result

def test_model_loading():
    # Test if all models can be loaded
    deepfake_detector = DeepfakeDetector()
    content_moderator = ContentModerator()
    face_verifier = FaceVerifier()
    
    assert deepfake_detector is not None
    assert content_moderator is not None
    assert face_verifier is not None
