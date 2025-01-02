# DeepShield Docker Setup Guide

This guide provides detailed instructions for setting up DeepShield using Docker Desktop.

## Prerequisites

### System Requirements
- Docker Desktop installed and running
- 16GB RAM recommended (8GB minimum)
- 20GB+ free disk space
- Internet connection for pulling images and downloading datasets

### Software Requirements
- Docker Desktop
- Git
- Text editor for configuration files

## Directory Structure

```bash
DeepShield-MVP/
├── docker-compose.yml          # Main Docker Compose configuration
├── .env                       # Environment variables
├── deepshield-frontend/      # Frontend application
│   ├── Dockerfile           # Frontend container configuration
│   └── .dockerignore       # Frontend build exclusions
├── deepshield-backend/       # Backend application
│   ├── Dockerfile          # Backend container configuration
│   ├── .dockerignore      # Backend build exclusions
│   ├── app/
│   │   ├── model_cache/   # AI model storage
│   │   │   ├── transformers/
│   │   │   ├── torch/
│   │   │   └── nsfw/
│   │   └── datasets/      # Dataset storage
│   │       ├── faceforensics/
│   │       ├── nudenet/
│   │       └── hatexplain/
│   └── requirements.txt    # Python dependencies
└── docs/                   # Documentation
```

## Initial Setup

### 1. Clone Repository
```bash
git clone https://github.com/sanjay-dastute/Deepshield-MVP.git
cd Deepshield-MVP
```

### 2. Environment Configuration

Create `.env` file in the root directory:
```bash
# Copy example environment files
cp deepshield-backend/.env.example deepshield-backend/.env
cp deepshield-frontend/.env.example deepshield-frontend/.env
```

Configure backend environment variables in `deepshield-backend/.env`:
```env
# MongoDB Configuration
MONGODB_URI=mongodb://mongodb:27017/deepshield

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

Configure frontend environment variables in `deepshield-frontend/.env`:
```env
VITE_API_URL=http://backend:8000
VITE_WEBSOCKET_URL=ws://backend:8000/ws
```

## Docker Volume Setup

### 1. Create Docker Volumes
```bash
# Create volumes for persistent data
docker volume create deepshield_mongodb_data
docker volume create deepshield_ai_model_cache
docker volume create deepshield_datasets
```

### 2. Volume Structure
```
Volumes:
├── mongodb_data/        # MongoDB data persistence
├── ai_model_cache/      # AI model storage
│   ├── transformers/
│   ├── torch/
│   └── nsfw/
└── datasets/           # Dataset storage
    ├── faceforensics/
    ├── nudenet/
    └── hatexplain/
```

## Dataset and Model Installation

### 1. Create Dataset Installation Script
Create `scripts/download_datasets.sh`:
```bash
#!/bin/bash

# Create directories
mkdir -p /app/datasets/{faceforensics,nudenet,hatexplain}

# Download datasets
cd /app/datasets

# FaceForensics++
curl -L https://github.com/ondyari/FaceForensics/raw/master/dataset/FaceForensics++ -o faceforensics.zip
unzip -q faceforensics.zip -d faceforensics
rm faceforensics.zip

# NudeNet
curl -L https://github.com/notAI-tech/NudeNet/raw/v2/dataset/nude.zip -o nudenet.zip
unzip -q nudenet.zip -d nudenet
rm nudenet.zip

# HateXplain
curl -L https://huggingface.co/datasets/hatexplain/raw/main/dataset.zip -o hatexplain.zip
unzip -q hatexplain.zip -d hatexplain
rm hatexplain.zip
```

### 2. Create Model Installation Script
Create `scripts/download_models.sh`:
```bash
#!/bin/bash

# Create directories
mkdir -p /app/model_cache/{transformers,torch,nsfw}

# Download NSFWJS model
cd /app/model_cache
curl -L https://github.com/infinitered/nsfwjs/raw/master/example/nsfw_model.zip -o nsfw_model.zip
unzip -q nsfw_model.zip -d nsfw
rm nsfw_model.zip

# HateSonar and BERT models will be downloaded automatically through the application
```

## Docker Compose Configuration

The `docker-compose.yml` file is configured with all necessary services:

```yaml
services:
  frontend:
    build:
      context: ./deepshield-frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - VITE_API_URL=http://backend:8000
      - VITE_WEBSOCKET_URL=ws://backend:8000/ws
    depends_on:
      - backend

  backend:
    build:
      context: ./deepshield-backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URI=mongodb://mongodb:27017/deepshield
      - MODEL_CACHE_DIR=/app/model_cache
      - DATASET_DIR=/app/datasets
      - TRANSFORMERS_CACHE=/app/model_cache/transformers
      - TORCH_HOME=/app/model_cache/torch
    volumes:
      - ai_model_cache:/app/model_cache
      - datasets:/app/datasets
    depends_on:
      - mongodb
    deploy:
      resources:
        limits:
          memory: 8G
        reservations:
          memory: 4G

  mongodb:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db

volumes:
  mongodb_data:
  ai_model_cache:
    driver: local
  datasets:
    driver: local
```

## Building and Running

### 1. Build Images
```bash
docker compose build
```

### 2. Start Services
```bash
docker compose up -d
```

### 3. Initialize Datasets and Models
```bash
# Run dataset download script in backend container
docker compose exec backend bash /app/scripts/download_datasets.sh

# Run model download script in backend container
docker compose exec backend bash /app/scripts/download_models.sh
```

## Verification Steps

### 1. Check Container Status
```bash
docker compose ps
```

### 2. Check Logs
```bash
# Backend logs
docker compose logs backend

# Frontend logs
docker compose logs frontend

# MongoDB logs
docker compose logs mongodb
```

### 3. Verify API Access
```bash
# Test backend API
curl http://localhost:8000/health

# Access frontend
open http://localhost:3000
```

### 4. Verify Volume Mounts
```bash
# Check dataset volume
docker compose exec backend ls -l /app/datasets

# Check model cache volume
docker compose exec backend ls -l /app/model_cache
```

## Troubleshooting

### Common Issues

1. **Container Memory Issues**
   ```bash
   # Check container resource usage
   docker stats
   
   # Increase container memory limit in docker-compose.yml if needed
   ```

2. **Volume Mount Problems**
   ```bash
   # Verify volume creation
   docker volume ls
   
   # Inspect volume contents
   docker volume inspect deepshield_ai_model_cache
   ```

3. **Network Issues**
   ```bash
   # Check container networking
   docker network ls
   
   # Inspect network
   docker network inspect deepshield-mvp_default
   ```

4. **Dataset Download Failures**
   ```bash
   # Retry dataset download
   docker compose exec backend bash /app/scripts/download_datasets.sh
   
   # Check available space
   docker compose exec backend df -h
   ```

### Resource Management

1. **Monitoring Resources**
   ```bash
   # Monitor container resource usage
   docker stats
   
   # Check disk space
   docker system df
   ```

2. **Cleanup**
   ```bash
   # Remove unused volumes
   docker volume prune
   
   # Remove unused images
   docker image prune
   ```

For more detailed troubleshooting, refer to [Troubleshooting.md](./Troubleshooting.md).
