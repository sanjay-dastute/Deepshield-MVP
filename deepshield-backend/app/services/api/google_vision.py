"""
Google Cloud Vision API integration for image analysis and OCR
"""
from typing import Dict, Any, List
import io
from google.cloud import vision
from app.config import settings

class GoogleVisionAPI:
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()
    
    async def detect_explicit_content(self, image_path: str) -> Dict[str, Any]:
        """Detect explicit content in an image using Google Vision API"""
        try: 
            with open(image_path, "rb") as image_file:
                content = image_file.read()
            
            image = vision.Image(content=content)
            response = self.client.safe_search_detection(image=image)
            safe_search = response.safe_search_annotation
            
            # Convert likelihood to confidence score (0-1)
            likelihood_scores = {
                vision.Likelihood.VERY_UNLIKELY: 0.0,
                vision.Likelihood.UNLIKELY: 0.25,
                vision.Likelihood.POSSIBLE: 0.5,
                vision.Likelihood.LIKELY: 0.75,
                vision.Likelihood.VERY_LIKELY: 1.0
            }
            
            details = {
                "adult": likelihood_scores.get(safe_search.adult, 0.0),
                "violence": likelihood_scores.get(safe_search.violence, 0.0),
                "racy": likelihood_scores.get(safe_search.racy, 0.0),
                "medical": likelihood_scores.get(safe_search.medical, 0.0)
            }
            
            max_score = max(details.values())
            
            return {
                "is_explicit": max_score > 0.5,
                "confidence": max_score,
                "details": details,
                "error": None
            }
        except Exception as e:
            return {
                "is_explicit": False,
                "confidence": 0.0,
                "details": None,
                "error": str(e)
            }
    
    async def perform_ocr(self, image_path: str) -> Dict[str, Any]:
        """Extract text from image using OCR"""
        try: 
            with open(image_path, "rb") as image_file:
                content = image_file.read()
            
            image = vision.Image(content=content)
            response = self.client.text_detection(image=image)
            texts = response.text_annotations
            
            return {
                "success": True,
                "text": texts[0].description if texts else "",
                "language": texts[0].locale if texts else None,
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "text": "",
                "language": None,
                "error": str(e)
            }
    
    async def detect_faces(self, image_path: str) -> Dict[str, Any]:
        """Detect faces in an image and analyze facial features"""
        try:
            with open(image_path, "rb") as image_file:
                content = image_file.read()
            
            image = vision.Image(content=content)
            response = self.client.face_detection(image=image)
            faces = response.face_annotations
            
            face_details = []
            for face in faces:
                face_details.append({
                    "confidence": face.detection_confidence,
                    "joy": face.joy_likelihood,
                    "anger": face.anger_likelihood,
                    "surprise": face.surprise_likelihood,
                    "headwear": face.headwear_likelihood
                })
            
            return {
                "success": True,
                "face_count": len(faces),
                "faces": face_details,
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "face_count": 0,
                "faces": [],
                "error": str(e)
            }
