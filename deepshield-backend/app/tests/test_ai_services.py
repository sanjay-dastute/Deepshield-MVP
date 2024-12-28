import pytest
import os
import shutil
from pathlib import Path
from ..services.ai.mock_deepfake import MockDeepfakeDetector as DeepfakeDetector
from ..services.ai.mock_face import MockFaceVerifier as FaceVerifier
from ..services.ai.content_moderation import ContentModerator  # Already has test_mode support

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
    return ContentModerator(test_mode=True)

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
    assert "facial_inconsistencies" in result
    assert "manipulation_score" in result

@pytest.mark.asyncio
async def test_video_deepfake_detection(deepfake_detector):
    """Test video deepfake detection"""
    # Create a test video
    import cv2
    import numpy as np
    
    video_path = str(TEST_DATA_DIR / "test_video.mp4")
    fps = 30
    size = (128, 128)
    out = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
    
    # Create 30 frames (1 second)
    for _ in range(30):
        frame = np.zeros((size[1], size[0], 3), dtype=np.uint8)
        cv2.circle(frame, (size[0]//2, size[1]//2), min(size)//3, (255, 255, 255), -1)
        out.write(frame)
    out.release()
    
    # Test video analysis
    result = await deepfake_detector.analyze_video(video_path)
    assert isinstance(result, dict)
    assert "is_deepfake" in result
    assert "confidence" in result
    assert "frame_analysis" in result
    assert "temporal_consistency" in result
    assert "error" in result

@pytest.mark.asyncio
async def test_content_moderation(content_moderator):
    """Test content moderation functionality with multilingual support"""
    # Test safe text in English
    result = await content_moderator.analyze_text("This is a normal text")
    assert result["is_toxic"] is False
    assert result["confidence"] >= 0.0
    assert result["error"] is None
    assert result["language"] == "en"
    assert isinstance(result["blacklisted_words"], list)
    assert len(result["blacklisted_words"]) == 0

    # Test toxic text in English
    result = await content_moderator.analyze_text("You are stupid and I hate you")
    assert result["is_toxic"] is True
    assert result["confidence"] > 0.5
    assert result["language"] == "en"
    
    # Test multilingual toxic content
    result = await content_moderator.analyze_text("これは嫌なメッセージです")  # Japanese toxic message
    assert result["is_toxic"] is True
    assert result["confidence"] > 0.5
    assert result["language"] == "ja"
    assert result["translated_text"] is not None
    
    # Test image moderation
    result = await content_moderator.analyze_image(str(TEST_DATA_DIR / "test_image1.jpg"))
    assert isinstance(result, dict)
    assert "is_explicit" in result
    assert "confidence" in result
    assert result["error"] is None
    assert isinstance(result["confidence"], float)
    assert 0.0 <= result["confidence"] <= 1.0

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
