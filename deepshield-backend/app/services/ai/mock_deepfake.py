from typing import Dict, Any
import numpy as np

class MockDeepfakeDetector:
    """Mock implementation of DeepfakeDetector for testing."""
    
    def __init__(self):
        self.model = "mock_deepfake_model"
        self.face_detection = "mock_face_detector"
        self.mock_responses = {
            'REAL': {
                'is_deepfake': False,
                'confidence': 0.95,
                'facial_inconsistencies': [],
                'manipulation_score': 0.05,
                'error': None
            },
            'FAKE': {
                'is_deepfake': True,
                'confidence': 0.85,
                'facial_inconsistencies': ['eye_alignment', 'texture_mismatch'],
                'manipulation_score': 0.92,
                'error': None
            },
            'NO_FACE': {
                'is_deepfake': False,
                'confidence': 0.0,
                'facial_inconsistencies': [],
                'manipulation_score': 0.0,
                'error': "No faces detected in image"
            }
        }
    
    async def analyze_image(self, image_path: str) -> Dict[str, Any]:
        """Mock deepfake detection."""
        # For testing purposes, detect fake images based on filename
        if 'fake' in image_path.lower():
            return self.mock_responses['FAKE']
        elif 'noface' in image_path.lower():
            return self.mock_responses['NO_FACE']
        return self.mock_responses['REAL']
    
    async def analyze_video(self, video_path: str) -> Dict[str, Any]:
        """Mock video analysis."""
        return {
            'is_deepfake': False,
            'confidence': 0.95,
            'frame_analysis': [
                {
                    'frame_number': i,
                    'is_deepfake': False,
                    'confidence': 0.95,
                    'facial_inconsistencies': [],
                    'manipulation_score': 0.05
                } for i in range(30)
            ],
            'temporal_consistency': 0.98,
            'error': None
        }
