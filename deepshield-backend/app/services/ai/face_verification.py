import insightface
import numpy as np
import cv2
from typing import Dict, Any, Tuple
from pathlib import Path

class FaceVerifier:
    def __init__(self):
        # Initialize InsightFace model
        self.model = insightface.app.FaceAnalysis()
        self.model.prepare(ctx_id=-1)  # Use CPU
        
        # Set verification threshold
        self.similarity_threshold = 0.6
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """Preprocess image for face detection"""
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image
    
    def extract_face_embedding(self, image: np.ndarray) -> Tuple[np.ndarray, Dict]:
        """Extract face embedding from image"""
        faces = self.model.get(image)
        if not faces:
            raise ValueError("No face detected in image")
        
        # Get the largest face in the image
        face = max(faces, key=lambda x: x.bbox[2] * x.bbox[3])
        return face.embedding, {
            "bbox": face.bbox.tolist(),
            "landmarks": face.landmark_2d_106.tolist() if hasattr(face, 'landmark_2d_106') else None
        }
    
    def calculate_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Calculate cosine similarity between two face embeddings"""
        return float(np.dot(embedding1, embedding2) / 
                    (np.linalg.norm(embedding1) * np.linalg.norm(embedding2)))
    
    async def verify_face(self, image1_path: str, image2_path: str) -> Dict[str, Any]:
        """Verify if two face images belong to the same person"""
        try:
            # Process both images
            img1 = self.preprocess_image(image1_path)
            img2 = self.preprocess_image(image2_path)
            
            # Extract face embeddings
            embedding1, face_data1 = self.extract_face_embedding(img1)
            embedding2, face_data2 = self.extract_face_embedding(img2)
            
            # Calculate similarity
            similarity = self.calculate_similarity(embedding1, embedding2)
            
            return {
                "match": similarity > self.similarity_threshold,
                "similarity": similarity,
                "face_data": {
                    "image1": face_data1,
                    "image2": face_data2
                },
                "error": None
            }
        except Exception as e:
            return {
                "match": False,
                "similarity": 0.0,
                "face_data": None,
                "error": str(e)
            }
    
    async def extract_face_data(self, image_path: str) -> Dict[str, Any]:
        """Extract face data from a single image"""
        try:
            img = self.preprocess_image(image_path)
            embedding, face_data = self.extract_face_embedding(img)
            
            return {
                "success": True,
                "face_data": face_data,
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "face_data": None,
                "error": str(e)
            }
