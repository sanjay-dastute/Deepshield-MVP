"""
Tests for multilingual content analysis
"""
import pytest
from ..services.ai.content_moderation import ContentModerator
from ..services.api.translation import TranslationAPI
from ..services.ai.keyword_blacklist import KeywordBlacklist

@pytest.fixture
def content_moderator():
    return ContentModerator(test_mode=True)

@pytest.fixture
def translation_api():
    return TranslationAPI()

@pytest.fixture
def keyword_blacklist():
    return KeywordBlacklist()

@pytest.mark.asyncio
async def test_multilingual_toxicity_detection(content_moderator):
    """Test toxicity detection in multiple languages"""
    # Test English text
    result_en = await content_moderator.analyze_text("This is a hateful message")
    assert result_en["is_toxic"]
    assert result_en["language"] == "en"
    
    # Test Spanish text
    result_es = await content_moderator.analyze_text("Este es un mensaje de odio")
    assert result_es["is_toxic"]
    assert result_es["language"] == "es"
    
    # Test French text
    result_fr = await content_moderator.analyze_text("C'est un message de haine")
    assert result_fr["is_toxic"]
    assert result_fr["language"] == "fr"

@pytest.mark.asyncio
async def test_language_detection(translation_api):
    """Test language detection"""
    # Test English
    result_en = await translation_api.detect_language("Hello, how are you?")
    assert result_en["language"] == "en"
    
    # Test Spanish
    result_es = await translation_api.detect_language("¿Hola, cómo estás?")
    assert result_es["language"] == "es"
    
    # Test French
    result_fr = await translation_api.detect_language("Bonjour, comment allez-vous?")
    assert result_fr["language"] == "fr"

@pytest.mark.asyncio
async def test_keyword_blacklist(content_moderator):
    """Test keyword blacklist in multiple languages"""
    # Add test keywords
    content_moderator.keyword_blacklist.add_keywords("en", ["offensive"])
    content_moderator.keyword_blacklist.add_keywords("es", ["ofensivo"])
    content_moderator.keyword_blacklist.add_keywords("fr", ["offensant"])

    # Test English blacklist
    result_en = await content_moderator.analyze_text("This is offensive content")
    assert result_en["is_toxic"]
    assert "offensive" in result_en["blacklisted_words"]

    # Test Spanish blacklist
    result_es = await content_moderator.analyze_text("Este contenido es ofensivo")
    assert result_es["is_toxic"]
    assert "ofensivo" in result_es["blacklisted_words"]

    # Test French blacklist
    result_fr = await content_moderator.analyze_text("Ce contenu est offensant")
    assert result_fr["is_toxic"]
    assert "offensant" in result_fr["blacklisted_words"]

    # Test non-toxic content
    result_safe = await content_moderator.analyze_text("This is safe content")
    assert not result_safe["is_toxic"]
    assert len(result_safe["blacklisted_words"]) == 0

@pytest.mark.asyncio
async def test_translation_fallback(content_moderator):
    """Test translation fallback for multiple languages"""
    # Test Japanese toxic content
    result_ja = await content_moderator.analyze_text("これは嫌なメッセージです")  # Japanese text
    assert result_ja["is_toxic"]
    assert result_ja["language"] == "ja"
    assert result_ja["translated_text"] is not None
    assert result_ja["confidence"] > 0.7

    # Test Spanish toxic content
    result_es = await content_moderator.analyze_text("Este es un mensaje de odio")  # Spanish text
    assert result_es["is_toxic"]
    assert result_es["language"] == "es"
    assert result_es["translated_text"] is not None
    assert result_es["confidence"] > 0.7

    # Test French toxic content
    result_fr = await content_moderator.analyze_text("C'est un message de haine")  # French text
    assert result_fr["is_toxic"]
    assert result_fr["language"] == "fr"
    assert result_fr["translated_text"] is not None
    assert result_fr["confidence"] > 0.7

    # Test safe content in different languages
    result_safe_ja = await content_moderator.analyze_text("こんにちは、元気ですか？")  # Japanese: Hello, how are you?
    assert not result_safe_ja["is_toxic"]
    assert result_safe_ja["language"] == "ja"
    assert result_safe_ja["translated_text"] is not None

    result_safe_es = await content_moderator.analyze_text("Buenos días, ¿cómo estás?")  # Spanish: Good morning, how are you?
    assert not result_safe_es["is_toxic"]
    assert result_safe_es["language"] == "es"
    assert result_safe_es["translated_text"] is not None

    # Test unsupported language fallback
    result_unknown = await content_moderator.analyze_text("안녕하세요")  # Korean text
    assert "translated_text" in result_unknown
    assert result_unknown["error"] is None  # Should handle gracefully
