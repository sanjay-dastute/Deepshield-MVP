"""
External API integrations for DeepShield
"""
from .instagram import InstagramAPI
from .google_vision import GoogleVisionAPI
from .translation import TranslationAPI

__all__ = ['InstagramAPI', 'GoogleVisionAPI', 'TranslationAPI']
