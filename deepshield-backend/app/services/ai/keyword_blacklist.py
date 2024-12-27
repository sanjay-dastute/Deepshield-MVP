"""
Multilingual keyword blacklist system for content moderation
"""
from typing import Dict, List, Set
import json
import os

class KeywordBlacklist:
    def __init__(self):
        self.blacklists: Dict[str, Set[str]] = {
            "en": set([
                "abuse", "hate", "violence", "explicit",
                # Add more English keywords
            ]),
            "es": set([
                "abuso", "odio", "violencia", "explícito",
                # Add more Spanish keywords
            ]),
            "fr": set([
                "abus", "haine", "violence", "explicite",
                # Add more French keywords
            ]),
            # Add more languages as needed
        }
    
    def load_blacklist(self, file_path: str):
        """Load blacklist from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for lang, words in data.items():
                    self.blacklists[lang] = set(words)
        except Exception as e:
            print(f"Error loading blacklist: {e}")
    
    def check_text(self, text: str, language: str) -> Dict[str, any]:
        """Check if text contains blacklisted keywords"""
        print(f"Checking text '{text}' for language '{language}'")  # Debug logging
        print(f"Available blacklists: {self.blacklists.keys()}")  # Debug logging
        if language not in self.blacklists:
            print(f"Language {language} not supported")  # Debug logging
            return {
                "contains_blacklisted": False,
                "matched_words": [],
                "error": f"Language {language} not supported"
            }
        
        # Case-insensitive substring matching
        text_lower = text.lower()
        matched_words = []
        
        # Check each blacklisted word
        for word in self.blacklists[language]:
            word_lower = word.lower()
            if word_lower in text_lower:
                matched_words.append(word)  # Add original word form to matches
        
        return {
            "contains_blacklisted": len(matched_words) > 0,
            "matched_words": matched_words,
            "error": None
        }
    
    def add_keywords(self, language: str, keywords: List[str]):
        """Add keywords to blacklist"""
        if language not in self.blacklists:
            self.blacklists[language] = set()
        self.blacklists[language].update(keywords)
    
    def remove_keywords(self, language: str, keywords: List[str]):
        """Remove keywords from blacklist"""
        if language in self.blacklists:
            self.blacklists[language].difference_update(keywords)
