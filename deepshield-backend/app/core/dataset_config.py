"""Dataset configuration and management for DeepShield."""
from pathlib import Path
import os

# Base directory for datasets (using /tmp for Render deployment)
DATASET_DIR = Path("/tmp/datasets")

# Dataset configurations
DATASETS = {
    "faceforensics": {
        "path": DATASET_DIR / "faceforensics",
        "url": "https://github.com/ondyari/FaceForensics",
        "description": "Dataset for deepfake detection",
        "required_files": ["real_vs_fake_data.h5"]
    },
    "nudenet": {
        "path": DATASET_DIR / "nudenet",
        "url": "https://github.com/notAI-tech/NudeNet",
        "description": "Dataset for NSFW content detection",
        "required_files": ["classifier_model.h5"]
    },
    "hatexplain": {
        "path": DATASET_DIR / "hatexplain",
        "url": "https://github.com/hate-alert/HateXplain",
        "description": "Dataset for hate speech detection",
        "required_files": ["dataset.json"]
    }
}

def ensure_dataset_dirs():
    """Ensure all dataset directories exist."""
    for dataset in DATASETS.values():
        os.makedirs(dataset["path"], exist_ok=True)

def get_dataset_path(name: str) -> Path:
    """Get the path for a specific dataset."""
    if name not in DATASETS:
        raise ValueError(f"Dataset {name} not found")
    return DATASETS[name]["path"]

def list_datasets():
    """List all available datasets."""
    return list(DATASETS.keys())

def verify_dataset_files():
    """Verify that required dataset files exist."""
    missing_files = []
    for name, config in DATASETS.items():
        for required_file in config["required_files"]:
            file_path = config["path"] / required_file
            if not file_path.exists():
                missing_files.append(f"{name}/{required_file}")
    return missing_files

# Initialize dataset directories
ensure_dataset_dirs()
