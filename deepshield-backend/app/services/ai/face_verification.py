from typing import Dict, Any
from .mock_face import MockFaceVerifier

class FaceVerifier(MockFaceVerifier):
    """Face verification using mock implementation for testing."""
    def __init__(self):
        super().__init__()
        self.model = "mock_face_model"

    async def verify_face(self, image1_path: str, image2_path: str) -> Dict[str, Any]:
        result = await super().verify_face(image1_path, image2_path)
        result.update({
            "verified": result["match"],
            "confidence": 0.95 if result["match"] else 0.15,
            "face_match": True,
            "id_valid": True
        })
        return result

    async def verify_profile_image(self, profile_image: str, reference_image: str) -> Dict[str, Any]:
        result = await super().verify_profile_image(profile_image, reference_image)
        result["confidence"] = 0.95 if result["match"] else 0.15
        return result
