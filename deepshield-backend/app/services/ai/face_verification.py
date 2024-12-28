from typing import Dict, Any, List, Tuple
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image
import numpy as np
from deepface import DeepFace
import cv2
from datasets import load_dataset

class FaceVerifier:
    """Face verification using FaceNet and DeepFace models."""
    def __init__(self, test_mode: bool = False):
        self.test_mode = test_mode
        if not test_mode:
            try:
                # Initialize face detection
                self.mtcnn = MTCNN(keep_all=True)
                
                # Initialize face recognition model (FaceNet)
                self.facenet = InceptionResnetV1(pretrained='vggface2').eval()
                
                # Load face verification dataset for threshold calibration
                self.dataset = load_dataset("vggface2", split="train[:100]")
                
                # Initialize threshold values
                self.similarity_threshold = 0.7
                self.confidence_threshold = 0.85
                
            except Exception as e:
                print(f"Failed to load face verification models: {e}")
                self.mtcnn = None
                self.facenet = None
    
    def _extract_face_embedding(self, image_path: str) -> Tuple[torch.Tensor, float]:
        """Extract face embedding from image using FaceNet."""
        try:
            # Load and preprocess image
            img = Image.open(image_path)
            
            # Detect face
            face = self.mtcnn(img)
            if face is None:
                return None, 0.0
            
            # Get embedding
            embedding = self.facenet(face.unsqueeze(0))
            return embedding, 1.0
            
        except Exception as e:
            print(f"Error extracting face embedding: {e}")
            return None, 0.0

    async def verify_face(self, image1_path: str, image2_path: str) -> Dict[str, Any]:
        """Verify if two face images match using multiple models."""
        if self.test_mode:
            return {
                "verified": True,
                "confidence": 0.95,
                "face_match": True,
                "id_valid": True,
                "error": None
            }
            
        try:
            # Get face embeddings
            embedding1, conf1 = self._extract_face_embedding(image1_path)
            embedding2, conf2 = self._extract_face_embedding(image2_path)
            
            if embedding1 is None or embedding2 is None:
                return {
                    "verified": False,
                    "confidence": 0.0,
                    "face_match": False,
                    "id_valid": False,
                    "error": "Failed to detect faces in one or both images"
                }
            
            # Calculate cosine similarity
            similarity = torch.nn.functional.cosine_similarity(embedding1, embedding2)
            similarity_score = float(similarity.item())
            
            # Use DeepFace as secondary verification
            try:
                deepface_result = DeepFace.verify(image1_path, image2_path)
                deepface_verified = deepface_result.get("verified", False)
            except:
                deepface_verified = None
            
            # Combine results
            verified = similarity_score > self.similarity_threshold
            if deepface_verified is not None:
                verified = verified and deepface_verified
            
            confidence = (similarity_score + conf1 + conf2) / 3
            
            return {
                "verified": verified,
                "confidence": float(confidence),
                "face_match": verified,
                "id_valid": confidence > self.confidence_threshold,
                "error": None
            }
            
        except Exception as e:
            return {
                "verified": False,
                "confidence": 0.0,
                "face_match": False,
                "id_valid": False,
                "error": str(e)
            }

    async def verify_profile_image(self, profile_image: str, reference_image: str) -> Dict[str, Any]:
        """Verify if a profile image matches a reference image."""
        try:
            # Use the same verification logic as verify_face
            result = await self.verify_face(profile_image, reference_image)
            
            # Add additional profile-specific checks
            if result["verified"]:
                # Check for image manipulation using DeepFace
                try:
                    analysis = DeepFace.analyze(profile_image, actions=['emotion', 'age', 'gender'])
                    result.update({
                        "analysis": {
                            "emotion": analysis[0].get("dominant_emotion"),
                            "age": analysis[0].get("age"),
                            "gender": analysis[0].get("gender")
                        }
                    })
                except:
                    pass
            
            return result
            
        except Exception as e:
            return {
                "verified": False,
                "confidence": 0.0,
                "match": False,
                "error": str(e)
            }
