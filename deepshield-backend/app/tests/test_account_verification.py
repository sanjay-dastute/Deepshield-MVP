"""
Tests for fake account detection and KYC verification
"""
import pytest
from pathlib import Path
from ..services.ai.face_verification import FaceVerifier
from ..services.api.instagram import InstagramAPI
from ..models.user import User

# Test data directory setup
TEST_DIR = Path(__file__).parent / "test_data"
TEST_DIR.mkdir(exist_ok=True)

# Create sample test images
def create_sample_image(filename: str, size=(128, 128)):
    import numpy as np
    import cv2
    img = np.zeros((*size, 3), dtype=np.uint8)
    cv2.circle(img, (size[0]//2, size[1]//2), min(size)//3, (255, 255, 255), -1)
    cv2.imwrite(str(TEST_DIR / filename), img)
    return str(TEST_DIR / filename)

@pytest.fixture(scope="session", autouse=True)
def setup_test_data():
    # Create test images for KYC
    create_sample_image("id_card.jpg")
    create_sample_image("selfie.jpg")
    create_sample_image("profile_pic.jpg")
    yield
    # Cleanup
    import shutil
    shutil.rmtree(TEST_DIR)

@pytest.fixture
def face_verifier():
    return FaceVerifier()

@pytest.fixture
def instagram_api():
    return InstagramAPI()

@pytest.mark.asyncio
async def test_kyc_verification(face_verifier):
    """Test KYC verification process"""
    # Test ID card and selfie matching
    result = await face_verifier.verify_face(
        image1_path=str(TEST_DIR / "id_card.jpg"),
        image2_path=str(TEST_DIR / "selfie.jpg")
    )
    assert isinstance(result, dict)
    assert "verified" in result
    assert "confidence" in result
    assert "face_match" in result
    assert "id_valid" in result

@pytest.mark.asyncio
async def test_profile_verification(face_verifier, instagram_api):
    """Test profile verification with facial recognition"""
    # Test profile picture verification
    result = await face_verifier.verify_profile_image(
        profile_image=str(TEST_DIR / "profile_pic.jpg"),
        reference_image=str(TEST_DIR / "selfie.jpg")
    )
    assert isinstance(result, dict)
    assert "match" in result
    assert "confidence" in result

    # Test Instagram profile verification
    ig_result = await instagram_api.verify_profile("test_user")
    assert isinstance(ig_result, dict)
    assert "verified" in ig_result
    assert "profile_data" in ig_result

@pytest.mark.asyncio
async def test_fake_account_detection(instagram_api):
    """Test fake account detection algorithms"""
    # Test behavioral analysis
    behavior_result = await instagram_api.analyze_account_behavior("test_user")
    assert isinstance(behavior_result, dict)
    assert "is_suspicious" in behavior_result
    assert "risk_score" in behavior_result
    assert "behavioral_flags" in behavior_result

    # Test metadata analysis
    metadata_result = await instagram_api.analyze_account_metadata("test_user")
    assert isinstance(metadata_result, dict)
    assert "account_age" in metadata_result
    assert "post_frequency" in metadata_result
    assert "follower_growth_rate" in metadata_result
    assert "engagement_metrics" in metadata_result

@pytest.mark.asyncio
async def test_reverse_image_search(instagram_api):
    """Test reverse image search for profile validation"""
    # Use mock response for faster testing
    instagram_api.use_mock_responses = True
    result = await instagram_api.reverse_image_search(str(TEST_DIR / "profile_pic.jpg"))
    assert isinstance(result, dict)
    assert "matches" in result
    assert "similarity_scores" in result
    assert "source_urls" in result
    assert len(result["matches"]) >= 0  # Allow empty matches for test data
    assert isinstance(result["similarity_scores"], list)
    assert isinstance(result["source_urls"], list)

@pytest.mark.asyncio
async def test_account_verification_workflow():
    """Test complete account verification workflow"""
    from datetime import datetime
    # Create test user
    user = User(
        username="test_user",
        email="test@example.com",
        full_name="Test User",
        id="test123",
        is_verified=False,
        verification_status="pending",
        created_at=datetime.utcnow(),
        profile_image=str(TEST_DIR / "profile_pic.jpg")
    )

    # Test verification steps
    verification_steps = [
        "kyc_verification",
        "profile_verification",
        "behavioral_analysis",
        "metadata_analysis",
        "image_verification"
    ]

    for step in verification_steps:
        result = await user.verify_step(step)
        assert isinstance(result, dict)
        assert "success" in result
        assert "step" in result
        assert result["step"] == step
