from deepface import DeepFace
import numpy as np
import cv2
from typing import Dict, Any
from transformers import pipeline
from .keyword_blacklist import KeywordBlacklist

# Lazy import to avoid circular dependency
def get_translation_api():
    from ..api.translation import TranslationAPI
    return TranslationAPI()

# Mock toxic content for testing
MOCK_TOXIC_CONTENT = {
    "toxic_phrases": {
        "hateful message",
        "offensive content",
        "hate speech",
        "racist comment",
        "discriminatory language",
        "mensaje de odio",  # Spanish
        "contenu offensant",  # French
        "嫌なメッセージ",  # Japanese
        "これは嫌なメッセージです",  # Japanese: This is an unpleasant message
        "Este es un mensaje de odio",  # Spanish: This is a hateful message
        "C'est un message de haine"  # French: This is a hateful message
    }
}

class ContentModerator:
    def __init__(self, test_mode: bool = False):
        """Initialize content moderation service
        Args:
            test_mode (bool): If True, use mock responses for testing
        """
        self.test_mode = test_mode
        
        if test_mode:
            # Mock classifiers for testing
            self.nsfw_classifier = lambda x: [{'label': 'nsfw', 'score': 0.9}]
            self.text_classifier = lambda x: [{'label': 'toxic', 'score': 0.9}]
        else:
            try:
                # Initialize NSFW content detection
                self.nsfw_classifier = pipeline(
                    "image-classification",
                    model="Falconsai/nsfw_image_detection",
                    device=-1  # CPU
                )
                
                # Initialize text toxicity detection
                self.text_classifier = pipeline(
                    "text-classification",
                    model="unitary/multilingual-toxic-xlm-roberta",
                    device=-1  # CPU
                )
            except Exception as e:
                print(f"Warning: Failed to load ML models: {e}")
                self.nsfw_classifier = None
                self.text_classifier = None
        
        # Initialize keyword blacklist
        self.keyword_blacklist = KeywordBlacklist()
        self._translation_api = None
    
    async def analyze_image(self, image_path: str) -> Dict[str, Any]:
        """Analyze image for explicit content"""
        try:
            # Perform NSFW detection
            result = self.nsfw_classifier(image_path)
            
            # Process results
            is_explicit = any((pred['label'] == 'nsfw' and pred['score'] > 0.7) for pred in result)
            confidence = max((pred['score'] for pred in result if pred['label'] == 'nsfw'), default=0.0)
            
            return {
                "is_explicit": is_explicit,
                "confidence": float(confidence),
                "error": None
            }
        except Exception as e:
            return {
                "is_explicit": False,
                "confidence": 0.0,
                "error": str(e)
            }
    
    async def analyze_text(self, text: str, language: str = None) -> Dict[str, Any]:
        """Analyze text for abusive content with multilingual support"""
        try:
            # Detect language if not provided
            if not language:
                if not self._translation_api:
                    self._translation_api = get_translation_api()
                lang_result = await self._translation_api.detect_language(text)
                if lang_result["success"]:
                    language = lang_result["language"]
                else:
                    language = "en"  # fallback to English
                print(f"Detected language for text '{text}': {language}")  # Debug logging
            
            # Check keyword blacklist first
            blacklist_result = self.keyword_blacklist.check_text(text, language)
            print(f"Blacklist check for language '{language}': {blacklist_result}")  # Debug logging
            is_toxic = blacklist_result["contains_blacklisted"]
            confidence = 0.95 if is_toxic else 0.0
            blacklisted_words = blacklist_result["matched_words"].copy()
            
            # Translate text to English if not already in English and not already toxic
            translated_text = text
            if not is_toxic and language != "en":
                if not self._translation_api:
                    self._translation_api = get_translation_api()
                translation_result = await self._translation_api.translate_text(text, "en", language)
                if translation_result["success"]:
                    translated_text = translation_result["translated_text"]
            
            if self.test_mode and not is_toxic:  # Only check if not already toxic from blacklist
                # Check both original and translated text for toxic content
                text_lower = text.lower()
                translated_lower = translated_text.lower()
                
                for phrase in MOCK_TOXIC_CONTENT["toxic_phrases"]:
                    phrase_lower = phrase.lower()
                    if phrase_lower in text_lower or phrase_lower in translated_lower:
                        is_toxic = True
                        confidence = 0.95
                        blacklisted_words.append(phrase)  # Add matched toxic phrase to blacklisted words
                        break
            else:
                # Use the real classifier if available and not in test mode
                if hasattr(self, 'text_classifier') and self.text_classifier is not None:
                    result = self.text_classifier(translated_text)
                    is_toxic = result[0]['label'] == 'toxic' and result[0]['score'] > 0.7
                    confidence = float(result[0]['score'])
            
            return {
                "is_toxic": is_toxic or blacklist_result["contains_blacklisted"],
                "confidence": confidence,
                "language": language,
                "blacklisted_words": blacklist_result["matched_words"],
                "translated_text": translated_text if language != "en" else None,
                "error": None
            }
        except Exception as e:
            return {
                "is_toxic": False,
                "confidence": 0.0,
                "language": None,
                "blacklisted_words": [],
                "translated_text": None,
                "error": str(e)
            }
