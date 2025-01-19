# DeepShield Installation Guide

This guide provides comprehensive instructions for setting up DeepShield locally.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Directory Structure](#directory-structure)
3. [Local Installation](#local-installation)
4. [Dataset Installation](#dataset-installation)
5. [AI Model Setup](#ai-model-setup)
6. [Environment Configuration](#environment-configuration)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements
- CPU: 4+ cores recommended
- RAM: 8GB minimum, 16GB recommended
- Storage: 20GB+ free space for datasets and models
- GPU: Optional but recommended for faster inference

### Software Requirements
- Python 3.12+
- Node.js 20+
- MongoDB 7.0+
- Git

## Directory Structure

```
deepshield/
├── deepshield-frontend/     # React.js frontend
│   ├── src/
│   ├── public/
│   └── node_modules/
├── deepshield-backend/      # Python FastAPI backend
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   └── services/
│   ├── datasets/           # AI datasets
│   │   ├── faceforensics/
│   │   ├── nudenet/
│   │   └── hatexplain/
│   └── model_cache/        # AI model cache
│       ├── transformers/
│       ├── torch/
│       └── nsfw/
└── docs/                   # Documentation
```

## Local Installation

### 1. Clone the Repository
```bash
git clone https://github.com/sanjay-dastute/Deepshield-MVP.git
cd Deepshield-MVP
```

### 2. Backend Setup
```bash
# Create and activate virtual environment
cd deepshield-backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p app/model_cache/{transformers,torch,nsfw}
mkdir -p app/datasets/{faceforensics,nudenet,hatexplain}

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

### 3. Frontend Setup
```bash
cd ../deepshield-frontend
pnpm install  # or npm install
cp .env.example .env
# Edit .env with your configuration
```

## Dataset Installation

### 1. FaceForensics++ Dataset
```bash
cd deepshield-backend/app/datasets
curl -L https://github.com/ondyari/FaceForensics/raw/master/dataset/FaceForensics++ -o faceforensics.zip
unzip faceforensics.zip -d faceforensics
rm faceforensics.zip
```

### 2. NudeNet Dataset
```bash
cd deepshield-backend/app/datasets
curl -L https://github.com/notAI-tech/NudeNet/raw/v2/dataset/nude.zip -o nudenet.zip
unzip nudenet.zip -d nudenet
rm nudenet.zip
```

### 3. HateXplain Dataset
```bash
cd deepshield-backend/app/datasets
curl -L https://huggingface.co/datasets/hatexplain/raw/main/dataset.zip -o hatexplain.zip
unzip hatexplain.zip -d hatexplain
rm hatexplain.zip
```

## AI Model Setup

### 1. NSFWJS Model
```bash
cd deepshield-backend/app/model_cache
curl -L https://github.com/infinitered/nsfwjs/raw/master/example/nsfw_model.zip -o nsfw_model.zip
unzip nsfw_model.zip -d nsfw
rm nsfw_model.zip
```

### 2. HateSonar Model
The HateSonar model will be downloaded automatically when first used through the Hugging Face Transformers library.

### 3. BERT Model
BERT models will be downloaded automatically through the Transformers library when first used.

## Environment Configuration

### Backend Environment Variables (.env)
```env
# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/deepshield

# AI Model Configuration
MODEL_CACHE_DIR=/app/model_cache
DATASET_DIR=/app/datasets
TRANSFORMERS_CACHE=/app/model_cache/transformers
TORCH_HOME=/app/model_cache/torch

# Instagram API Configuration
INSTAGRAM_APP_ID=your_app_id
INSTAGRAM_APP_SECRET=your_app_secret
INSTAGRAM_ACCESS_TOKEN=your_access_token
```

### Frontend Environment Variables (.env)
```env
VITE_API_URL=http://localhost:8000
VITE_WEBSOCKET_URL=ws://localhost:8000/ws
```

## Running the Application

### Local Development
1. Start MongoDB
```bash
mongod --dbpath /path/to/data/db
```

2. Start Backend
```bash
cd deepshield-backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

3. Start Frontend
```bash
cd deepshield-frontend
pnpm dev  # or npm run dev
```

Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Troubleshooting

### Common Issues

1. **Dataset Download Failures**
   - Ensure you have sufficient disk space
   - Try downloading manually from the source websites
   - Check your internet connection

2. **Model Loading Errors**
   - Verify MODEL_CACHE_DIR is properly set
   - Ensure sufficient RAM is available
   - Check model files are correctly downloaded

3. **MongoDB Connection Issues**
   - Verify MongoDB is running
   - Check MONGODB_URI in .env
   - Ensure MongoDB port (27017) is not blocked



For more detailed troubleshooting, refer to [Troubleshooting.md](./Troubleshooting.md).
