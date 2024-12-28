from typing import Dict, Any
from .mock_deepfake import MockDeepfakeDetector

class DeepfakeDetector(MockDeepfakeDetector):
    """Deepfake detection using mock implementation for testing."""
    def __init__(self):
        super().__init__()
        self.model = "mock_deepfake_model"
        self.face_detection = "mock_face_detector"

    async def analyze_video(self, video_path: str) -> Dict[str, Any]:
        result = await super().analyze_video(video_path)
        frame_analysis = [
            {"frame": i, "is_deepfake": False, "confidence": 0.95}
            for i in range(result["frames_analyzed"])
        ]
        result.update({
            "frame_analysis": frame_analysis,
            "temporal_consistency": 0.98,
            "is_deepfake": False,
            "confidence": 0.95,
            "facial_inconsistencies": []
        })
        return result

    async def analyze_image(self, image_path: str) -> Dict[str, Any]:
        """Analyze an image for potential deepfake manipulation."""
        return {
            "is_deepfake": False,
            "confidence": 0.95,
            "error": None,
            "facial_inconsistencies": [],
            "manipulation_score": 0.05  # Low score indicates likely authentic image
        }
