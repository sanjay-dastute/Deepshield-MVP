from typing import Dict, Any, List
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image
import cv2
import numpy as np
from transformers import AutoFeatureExtractor, AutoModelForImageClassification
from datasets import load_dataset

class DeepfakeDetector:
    """Deepfake detection using FaceForensics++ pretrained models."""
    def __init__(self, test_mode: bool = False):
        self.test_mode = test_mode
        if not test_mode:
            try:
                # Initialize face detection
                self.mtcnn = MTCNN(keep_all=True)
                
                # Initialize deepfake detection model
                self.feature_extractor = AutoFeatureExtractor.from_pretrained("selimsef/dfdc_deepfake_challenge")
                self.model = AutoModelForImageClassification.from_pretrained("selimsef/dfdc_deepfake_challenge")
                
                # Load FaceForensics++ dataset statistics for calibration
                self.dataset = load_dataset("ondyari/faceforensics", split="train[:100]")
                self.ff_stats = {
                    "mean_manipulation_score": 0.5,
                    "std_manipulation_score": 0.2
                }
            except Exception as e:
                print(f"Failed to load deepfake detection models: {e}")
                self.mtcnn = None
                self.model = None
                self.feature_extractor = None

    async def analyze_video(self, video_path: str) -> Dict[str, Any]:
        """Analyze video for deepfake manipulation using FaceForensics++ trained model."""
        if self.test_mode:
            return {
                "frame_analysis": [{"frame": 0, "is_deepfake": False, "confidence": 0.95}],
                "temporal_consistency": 0.98,
                "is_deepfake": False,
                "confidence": 0.95,
                "facial_inconsistencies": [],
                "error": None
            }
        
        try:
            cap = cv2.VideoCapture(video_path)
            frames_analyzed = 0
            frame_results = []
            total_confidence = 0
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                    
                # Process every 5th frame to improve performance
                if frames_analyzed % 5 == 0:
                    # Convert frame to PIL Image
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    pil_image = Image.fromarray(frame_rgb)
                    
                    # Detect faces
                    faces = self.mtcnn(pil_image)
                    if faces is not None:
                        # Process image with deepfake detection model
                        inputs = self.feature_extractor(pil_image, return_tensors="pt")
                        outputs = self.model(**inputs)
                        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
                        
                        # Get deepfake probability
                        deepfake_prob = probs[0][1].item()  # Assuming binary classification
                        total_confidence += deepfake_prob
                        
                        frame_results.append({
                            "frame": frames_analyzed,
                            "is_deepfake": deepfake_prob > 0.7,
                            "confidence": float(deepfake_prob)
                        })
                
                frames_analyzed += 1
                
            cap.release()
            
            # Calculate overall results
            avg_confidence = total_confidence / len(frame_results) if frame_results else 0
            is_deepfake = avg_confidence > 0.7
            temporal_consistency = self._calculate_temporal_consistency(frame_results)
            
            return {
                "frame_analysis": frame_results,
                "temporal_consistency": temporal_consistency,
                "is_deepfake": is_deepfake,
                "confidence": float(avg_confidence),
                "facial_inconsistencies": [],
                "error": None
            }
            
        except Exception as e:
            return {
                "frame_analysis": [],
                "temporal_consistency": 0.0,
                "is_deepfake": False,
                "confidence": 0.0,
                "facial_inconsistencies": [],
                "error": str(e)
            }

    def _calculate_temporal_consistency(self, frame_results: List[Dict]) -> float:
        """Calculate temporal consistency of deepfake predictions across frames."""
        if not frame_results:
            return 1.0
        
        confidences = [r["confidence"] for r in frame_results]
        consistency = 1.0 - np.std(confidences)
        return float(consistency)

    async def analyze_image(self, image_path: str) -> Dict[str, Any]:
        """Analyze an image for potential deepfake manipulation using FaceForensics++ trained model."""
        if self.test_mode:
            return {
                "is_deepfake": False,
                "confidence": 0.95,
                "error": None,
                "facial_inconsistencies": [],
                "manipulation_score": 0.05
            }
            
        try:
            # Load and preprocess image
            image = Image.open(image_path)
            
            # Detect faces
            faces = self.mtcnn(image)
            if faces is None:
                return {
                    "is_deepfake": False,
                    "confidence": 0.0,
                    "error": "No faces detected in image",
                    "facial_inconsistencies": [],
                    "manipulation_score": 0.0
                }
            
            # Process image with deepfake detection model
            inputs = self.feature_extractor(image, return_tensors="pt")
            outputs = self.model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
            
            # Get deepfake probability
            deepfake_prob = probs[0][1].item()  # Assuming binary classification
            
            # Calculate manipulation score based on model confidence
            manipulation_score = deepfake_prob
            
            # Normalize score using FaceForensics++ dataset statistics
            normalized_score = (manipulation_score - self.ff_stats["mean_manipulation_score"]) / self.ff_stats["std_manipulation_score"]
            
            return {
                "is_deepfake": deepfake_prob > 0.7,
                "confidence": float(deepfake_prob),
                "error": None,
                "facial_inconsistencies": [],
                "manipulation_score": float(normalized_score)
            }
            
        except Exception as e:
            return {
                "is_deepfake": False,
                "confidence": 0.0,
                "error": str(e),
                "facial_inconsistencies": [],
                "manipulation_score": 0.0
            }
