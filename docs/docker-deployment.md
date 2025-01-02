# Docker Deployment Guide for DeepShield MVP

## Prerequisites
- Docker installed on your system
- Docker Compose installed
- Git installed
- At least 8GB RAM recommended for AI model processing

## Step 1: Clone the Repository
```bash
git clone https://github.com/sanjay-dastute/Deepshield-MVP.git
cd Deepshield-MVP
```

## Step 2: Environment Setup
1. Create backend environment file:
```bash
cp deepshield-backend/.env.example deepshield-backend/.env
```

2. Create frontend environment file:
```bash
cp deepshield-frontend/.env.example deepshield-frontend/.env
```

3. Configure environment variables:
- Backend (.env):
  ```
  MONGODB_URL=mongodb://mongodb:27017/deepshield
  DATASET_DIR=/app/datasets
  MODEL_CACHE_DIR=/app/model_cache
  INSTAGRAM_APP_ID=your_instagram_app_id
  INSTAGRAM_APP_SECRET=your_instagram_app_secret
  ```

- Frontend (.env):
  ```
  VITE_API_URL=http://localhost:8000
  VITE_WEBSOCKET_URL=ws://localhost:8000/ws
  ```

## Step 3: Build and Start Services
```bash
# Build all services
docker-compose build

# Start the services
docker-compose up -d
```

## Step 4: Verify Installation
1. Backend API: http://localhost:8000/docs
2. Frontend App: http://localhost:3000
3. MongoDB: mongodb://localhost:27017

## Service Architecture
The application consists of the following services:

1. Frontend (React.js):
   - Port: 3000
   - Features:
     - User authentication
     - Content reporting
     - KYC verification
     - Admin panel

2. Backend (FastAPI):
   - Port: 8000
   - Features:
     - AI model integration
     - Content moderation
     - Profile verification
     - API endpoints

3. MongoDB:
   - Port: 27017
   - Stores:
     - User data
     - Content reports
     - Verification status

## AI Models and Datasets
The following models and datasets are automatically downloaded during container build:

1. Models:
   - NSFWJS (Content filtering)
   - HateSonar (Abuse detection)
   - BERT (Multilingual text analysis)
   - DeepFace (Face verification)

2. Datasets:
   - FaceForensics++ (Deepfake detection)
   - NudeNet (Explicit content detection)
   - HateXplain (Abuse identification)

## Troubleshooting
1. If services fail to start:
   ```bash
   # View logs
   docker-compose logs -f

   # Restart services
   docker-compose down
   docker-compose up -d
   ```

2. If AI models fail to load:
   ```bash
   # Clear model cache
   docker-compose down
   rm -rf ./deepshield-backend/model_cache
   docker-compose up -d
   ```

3. Database connection issues:
   ```bash
   # Reset MongoDB
   docker-compose down -v
   docker-compose up -d
   ```

## Development Workflow
1. Make changes to code
2. Rebuild affected services:
   ```bash
   docker-compose build backend  # or frontend
   docker-compose up -d
   ```

## Resource Requirements
- Disk Space: ~10GB (including AI models and datasets)
- RAM: 8GB minimum, 16GB recommended
- CPU: 4 cores recommended for AI processing

## Security Notes
- Default ports are exposed only to localhost
- Sensitive data should be properly configured in .env files
- AI model weights are cached locally for performance
