from typing import Dict, Any, List, Optional
import numpy as np

class MockFaceVerifier:
    """Mock implementation of FaceVerifier for testing."""
    
    def __init__(self):
        self.model = "mock_face_model"
        self.face_detection = "mock_face_detector"
        self.mock_responses = {
            'MATCH': {
                'match': True,
                'similarity': 0.95,
                'verified': True,
                'confidence': 0.95,
                'face_match': True,
                'id_valid': True,
                'face_data': {
                    'image1': {'bbox': [0, 0, 100, 100], 'landmarks': {'left_eye': [30, 30]}},
                    'image2': {'bbox': [0, 0, 100, 100], 'landmarks': {'left_eye': [30, 30]}}
                },
                'error': None
            },
            'NO_MATCH': {
                'match': False,
                'similarity': 0.15,
                'face_data': {
                    'image1': {'bbox': [0, 0, 100, 100], 'landmarks': {'left_eye': [30, 30]}},
                    'image2': {'bbox': [0, 0, 100, 100], 'landmarks': {'left_eye': [40, 40]}}
                },
                'error': None
            },
            'NO_FACE': {
                'match': False,
                'similarity': 0.0,
                'face_data': None,
                'error': "No face detected in image"
            }
        }
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """Mock image preprocessing."""
        return np.zeros((224, 224, 3))
    
    async def verify_face(self, image1_path: str, image2_path: str) -> Dict[str, Any]:
        """Mock face verification."""
        if 'noface' in image1_path.lower() or 'noface' in image2_path.lower():
            return self.mock_responses['NO_FACE']
        elif 'match' in image1_path.lower() and 'match' in image2_path.lower():
            return self.mock_responses['MATCH']
        return self.mock_responses['NO_MATCH']
    
    async def extract_face_data(self, image_path: str) -> Dict[str, Any]:
        """Mock face data extraction."""
        if 'noface' in image_path.lower():
            return {
                'success': False,
                'face_data': None,
                'error': "No face detected in image"
            }
        return {
            'success': True,
            'face_data': {
                'bbox': [0, 0, 100, 100],
                'landmarks': {'left_eye': [30, 30]}
            },
            'error': None
        }
        
    async def verify_profile_image(self, profile_image: str, reference_image: str) -> Dict[str, Any]:
        """Mock profile image verification."""
        result = await self.verify_face(profile_image, reference_image)
        return {
            **result,
            "verified": result["match"],
            "profile_image": profile_image,
            "reference_image": reference_image
        }
