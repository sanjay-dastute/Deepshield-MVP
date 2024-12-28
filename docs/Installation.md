# DeepShield MVP Installation Guide

## Prerequisites
- Python 3.12+
- Node.js 18+
- MongoDB
- Git

## Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/sanjay-dastute/Deepshield-MVP.git
cd Deepshield-MVP/deepshield-backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the backend directory with the following content:
```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=deepshield
INSTAGRAM_APP_ID=your_instagram_app_id
INSTAGRAM_APP_SECRET=your_instagram_app_secret
INSTAGRAM_ACCESS_TOKEN=your_instagram_access_token
INSTAGRAM_ACCOUNT_ID=your_instagram_account_id
JWT_SECRET=your_jwt_secret
```

5. Start the backend server:
```bash
uvicorn app.main:app --reload
```

The backend API will be available at `http://localhost:8000`

## Frontend Setup

1. Navigate to the frontend directory:
```bash
cd ../deepshield-frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
Create a `.env` file in the frontend directory with:
```env
VITE_API_URL=http://localhost:8000/api/v1
```

4. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## AI Models and Datasets

1. Download required datasets:
```bash
# Create data directory
mkdir -p data/datasets

# Download FaceForensics++ dataset (requires registration)
# Visit https://github.com/ondyari/FaceForensics

# Download NudeNet dataset
wget https://github.com/notAI-tech/NudeNet/releases/download/v0/classifier_model.onnx -O data/datasets/nudenet_classifier.onnx

# Download HateXplain dataset
wget https://github.com/hate-alert/HateXplain/raw/master/Data/dataset.json -O data/datasets/hatexplain.json
```

2. Set up AI models:
The system will automatically download required models on first use:
- NSFWJS (TensorFlow.js)
- HateSonar
- BERT multilingual

## Verification

1. Test the backend:
```bash
pytest
```

2. Verify API access:
```bash
curl http://localhost:8000/healthz
```

3. Check frontend connection:
Open `http://localhost:5173` in your browser and verify that you can:
- Register/login
- Upload content for analysis
- Access the admin dashboard

## Common Setup Issues

See [Troubleshooting.md](Troubleshooting.md) for common setup issues and their solutions.
