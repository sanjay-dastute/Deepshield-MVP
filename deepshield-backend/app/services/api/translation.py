"""
Translation API integration for multilingual support
"""
from typing import Dict, Any, List
import requests
from app.config import settings

# Mock translations for testing
MOCK_TRANSLATIONS = {
    "ja": {
        "これは嫌なメッセージです": "This is an unpleasant message",
    },
    "es": {
        "Este es un mensaje de odio": "This is a hateful message",
    },
    "fr": {
        "C'est un message de haine": "This is a hateful message",
    }
}

# Mock language detection
MOCK_LANGUAGE_DETECTION = {
    "これは嫌なメッセージです": "ja",
    "Este es un mensaje de odio": "es",
    "C'est un message de haine": "fr",
    "Hello, how are you?": "en",
    "This is a hateful message": "en",
    "¿Hola, cómo estás?": "es",
    "Bonjour, comment allez-vous?": "fr",
    "こんにちは、元気ですか？": "ja",
    "Buenos días, ¿cómo estás?": "es",
    "Este contenido es ofensivo": "es",  # Add test case
    "Ce contenu est offensant": "fr",  # Add French test case
    "안녕하세요": "ko"  # Korean for testing unsupported language
}

class TranslationAPI:
    def __init__(self):
        self.api_key = settings.TRANSLATION_API_KEY
        self.base_url = "https://translation.googleapis.com/language/translate/v2"
    
    async def translate_text(self, text: str, target_lang: str = "en", source_lang: str = None) -> Dict[str, Any]:
        """Translate text to target language"""
        try:
            # Use mock translations if API key is not available
            if not self.api_key:
                # Detect source language from mock data if not provided
                if not source_lang and text in MOCK_LANGUAGE_DETECTION:
                    source_lang = MOCK_LANGUAGE_DETECTION[text]
                
                # Check if we have a mock translation
                if source_lang in MOCK_TRANSLATIONS and text in MOCK_TRANSLATIONS[source_lang]:
                    return {
                        "success": True,
                        "translated_text": MOCK_TRANSLATIONS[source_lang][text],
                        "detected_language": source_lang,
                        "error": None
                    }
                
                # Return original text if it's already in English
                if source_lang == "en" or text in MOCK_LANGUAGE_DETECTION and MOCK_LANGUAGE_DETECTION[text] == "en":
                    return {
                        "success": True,
                        "translated_text": text,
                        "detected_language": "en",
                        "error": None
                    }
            
            # Use API if key is available
            if self.api_key:
                params = {
                    "q": text,
                    "target": target_lang,
                    "key": self.api_key
                }
                
                if source_lang:
                    params["source"] = source_lang
                
                response = requests.post(self.base_url, params=params)
                response.raise_for_status()
                
                data = response.json()
                translation = data["data"]["translations"][0]
                
                return {
                    "success": True,
                    "translated_text": translation["translatedText"],
                    "detected_language": translation.get("detectedSourceLanguage"),
                    "error": None
                }
            
            return {
                "success": False,
                "translated_text": "",
                "detected_language": None,
                "error": "API key not available and text not in mock data"
            }
        except Exception as e:
            return {
                "success": False,
                "translated_text": "",
                "detected_language": None,
                "error": str(e)
            }
    
    async def detect_language(self, text: str) -> Dict[str, Any]:
        """Detect the language of input text"""
        try:
            # Use mock detection if API key is not available
            if not self.api_key and text in MOCK_LANGUAGE_DETECTION:
                return {
                    "success": True,
                    "language": MOCK_LANGUAGE_DETECTION[text],
                    "confidence": 1.0,
                    "error": None
                }
            
            # Use API if key is available
            if self.api_key:
                params = {
                    "q": text,
                    "key": self.api_key
                }
                
                response = requests.post(f"{self.base_url}/detect", params=params)
                response.raise_for_status()
                
                data = response.json()
                detection = data["data"]["detections"][0][0]
                
                return {
                    "success": True,
                    "language": detection["language"],
                    "confidence": detection["confidence"],
                    "error": None
                }
            
            return {
                "success": False,
                "language": None,
                "confidence": 0.0,
                "error": "API key not available and text not in mock data"
            }
        except Exception as e:
            return {
                "success": False,
                "language": None,
                "confidence": 0.0,
                "error": str(e)
            }
    
    async def batch_translate(self, texts: List[str], target_lang: str = "en") -> Dict[str, Any]:
        """Translate multiple texts in a single request"""
        try:
            params = {
                "q": texts,
                "target": target_lang,
                "key": self.api_key
            }
            
            response = requests.post(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            translations = data["data"]["translations"]
            
            return {
                "success": True,
                "translations": [
                    {
                        "translated_text": t["translatedText"],
                        "detected_language": t.get("detectedSourceLanguage")
                    }
                    for t in translations
                ],
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "translations": [],
                "error": str(e)
            }
