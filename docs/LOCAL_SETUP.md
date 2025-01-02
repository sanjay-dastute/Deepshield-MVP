# DeepShield Local System Setup Guide

This guide provides detailed instructions for setting up DeepShield on your local system without Docker.

## Directory Structure Setup

```bash
# Create base directories
mkdir -p DeepShield-MVP
cd DeepShield-MVP

# Create frontend structure
mkdir -p deepshield-frontend/{src,public}

# Create backend structure
mkdir -p deepshield-backend/app/{api,core,models,services,tests}
mkdir -p deepshield-backend/app/services/{ai,api,notifications}

# Create AI model and dataset directories
mkdir -p deepshield-backend/app/model_cache/{transformers,torch,nsfw}
mkdir -p deepshield-backend/app/datasets/{faceforensics,nudenet,hatexplain}
```

## Dataset Installation

### 1. FaceForensics++ Dataset
```bash
cd deepshield-backend/app/datasets
# Download FaceForensics++ dataset
wget https://github.com/ondyari/FaceForensics/raw/master/dataset/FaceForensics++ -O faceforensics.zip
unzip faceforensics.zip -d faceforensics
rm faceforensics.zip

# Verify installation
ls faceforensics
# Should show dataset files and directories
```

### 2. NudeNet Dataset
```bash
cd deepshield-backend/app/datasets
# Download NudeNet dataset
wget https://github.com/notAI-tech/NudeNet/raw/v2/dataset/nude.zip -O nudenet.zip
unzip nudenet.zip -d nudenet
rm nudenet.zip

# Verify installation
ls nudenet
# Should show dataset files and directories
```

### 3. HateXplain Dataset
```bash
cd deepshield-backend/app/datasets
# Download HateXplain dataset
wget https://huggingface.co/datasets/hatexplain/raw/main/dataset.zip -O hatexplain.zip
unzip hatexplain.zip -d hatexplain
rm hatexplain.zip

# Verify installation
ls hatexplain
# Should show dataset files and directories
```

## AI Model Installation

### 1. NSFWJS Model
```bash
cd deepshield-backend/app/model_cache
# Download NSFWJS model
wget https://github.com/infinitered/nsfwjs/raw/master/example/nsfw_model.zip -O nsfw_model.zip
unzip nsfw_model.zip -d nsfw
rm nsfw_model.zip

# Verify installation
ls nsfw
# Should show model files
```

### 2. HateSonar Model
The HateSonar model will be downloaded automatically when first used. To pre-download:

```bash
python3 -c "
from transformers import AutoModelForSequenceClassification, AutoTokenizer
model_name = 'Hate-speech-CNERG/bert-base-uncased-hatexplain'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
"
```

### 3. BERT Model
BERT models will be downloaded automatically. To pre-download specific models:

```bash
python3 -c "
from transformers import AutoModelForSequenceClassification, AutoTokenizer
# Multilingual BERT
model_name = 'bert-base-multilingual-uncased'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
"
```

## Environment Setup

### 1. Python Environment
```bash
cd deepshield-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Node.js Environment
```bash
cd deepshield-frontend

# Install pnpm (if not installed)
npm install -g pnpm

# Install dependencies
pnpm install
```

### 3. MongoDB Setup
```bash
# Install MongoDB (Ubuntu)
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu $(lsb_release -cs)/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org

# Start MongoDB service
sudo systemctl start mongod
sudo systemctl enable mongod

# Verify MongoDB is running
mongod --version
```

## Environment Configuration

### 1. Backend Configuration
Create `.env` file in `deepshield-backend`:
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
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

### 2. Frontend Configuration
Create `.env` file in `deepshield-frontend`:
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```env
VITE_API_URL=http://localhost:8000
VITE_WEBSOCKET_URL=ws://localhost:8000/ws
```

## Verification Steps

### 1. Verify Dataset Installation
```bash
cd deepshield-backend/app/datasets
# Check dataset directories
ls -l faceforensics nudenet hatexplain
```

### 2. Verify Model Installation
```bash
cd deepshield-backend/app/model_cache
# Check model directories
ls -l nsfw transformers torch
```

### 3. Verify Backend Setup
```bash
cd deepshield-backend
source venv/bin/activate
python -c "
import torch
from transformers import AutoModelForSequenceClassification
print('PyTorch version:', torch.__version__)
print('CUDA available:', torch.cuda.is_available())
"
```

### 4. Verify Frontend Setup
```bash
cd deepshield-frontend
pnpm run build
```

### 5. Verify MongoDB Connection
```bash
mongosh --eval "db.version()"
```

## Troubleshooting

### Common Issues

1. **Dataset Download Failures**
   - Check internet connection
   - Verify disk space availability
   - Try downloading manually from source websites
   - Check file permissions

2. **Model Loading Errors**
   - Verify Python environment is activated
   - Check CUDA installation if using GPU
   - Verify model cache directory permissions
   - Check available RAM

3. **MongoDB Connection Issues**
   - Verify MongoDB service is running
   - Check MongoDB port availability
   - Verify database user permissions
   - Check firewall settings

4. **Python Package Installation Issues**
   - Update pip: `pip install --upgrade pip`
   - Install build tools: `sudo apt-get install python3-dev build-essential`
   - Check Python version compatibility

5. **Node.js/Frontend Issues**
   - Clear node_modules: `rm -rf node_modules`
   - Clear pnpm cache: `pnpm store prune`
   - Verify Node.js version: `node --version`
   - Check package.json for correct dependencies

For more detailed troubleshooting, refer to [Troubleshooting.md](./Troubleshooting.md).
