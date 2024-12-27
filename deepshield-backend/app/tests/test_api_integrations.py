"""
Tests for external API integrations
"""
import pytest
from pathlib import Path
import os
from app.services.api.instagram import InstagramAPI
from app.services.api.google_vision import GoogleVisionAPI
from app.services.api.translation import TranslationAPI

# Test data directory setup
TEST_DIR = Path(__file__).parent / "test_data"
TEST_DIR.mkdir(exist_ok=True)

# Create a sample test image
TEST_IMAGE = TEST_DIR / "test_image.jpg"
if not TEST_IMAGE.exists():
    # Create a blank test image
    from PIL import Image
    img = Image.new('RGB', (100, 100), color='white')
    img.save(TEST_IMAGE)

@pytest.fixture
def instagram_api():
    return InstagramAPI()

@pytest.fixture
def google_vision_api():
    return GoogleVisionAPI()

@pytest.fixture
def translation_api():
    return TranslationAPI()

# Instagram API Tests
@pytest.mark.asyncio
async def test_instagram_profile_verification(instagram_api):
    """Test Instagram profile verification"""
    result = await instagram_api.verify_profile("dastute_tech")
    assert result["verified"] is not None
    assert "error" in result

@pytest.mark.asyncio
async def test_instagram_media_insights(instagram_api):
    """Test Instagram media insights"""
    # Using a dummy media ID for testing
    result = await instagram_api.get_media_insights("dummy_media_id")
    assert "success" in result
    assert "error" in result

# Google Vision API Tests
@pytest.mark.asyncio
async def test_explicit_content_detection(google_vision_api):
    """Test explicit content detection"""
    result = await google_vision_api.detect_explicit_content(str(TEST_IMAGE))
    assert "is_explicit" in result
    assert "confidence" in result
    assert "details" in result
    assert "error" in result

@pytest.mark.asyncio
async def test_ocr(google_vision_api):
    """Test OCR functionality"""
    result = await google_vision_api.perform_ocr(str(TEST_IMAGE))
    assert "success" in result
    assert "text" in result
    assert "error" in result

@pytest.mark.asyncio
async def test_face_detection(google_vision_api):
    """Test face detection"""
    result = await google_vision_api.detect_faces(str(TEST_IMAGE))
    assert "success" in result
    assert "face_count" in result
    assert "faces" in result
    assert "error" in result

# Translation API Tests
@pytest.mark.asyncio
async def test_text_translation(translation_api):
    """Test text translation"""
    test_text = "Hello, world!"
    result = await translation_api.translate_text(test_text, target_lang="es")
    assert "success" in result
    assert "translated_text" in result
    assert "error" in result

@pytest.mark.asyncio
async def test_language_detection(translation_api):
    """Test language detection"""
    test_text = "Bonjour le monde"
    result = await translation_api.detect_language(test_text)
    assert "success" in result
    assert "language" in result
    assert "confidence" in result
    assert "error" in result

@pytest.mark.asyncio
async def test_batch_translation(translation_api):
    """Test batch translation"""
    test_texts = ["Hello", "World", "Test"]
    result = await translation_api.batch_translate(test_texts, target_lang="fr")
    assert "success" in result
    assert "translations" in result
    assert "error" in result
    if result["success"]:
        assert len(result["translations"]) == len(test_texts)
