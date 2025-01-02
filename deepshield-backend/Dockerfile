FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1-mesa-glx \
    curl \
    unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for AI models and datasets
ENV MODEL_CACHE_DIR=/app/model_cache \
    DATASET_DIR=/app/datasets \
    TRANSFORMERS_CACHE=/app/model_cache/transformers \
    TORCH_HOME=/app/model_cache/torch \
    PYTHONPATH=/app

# Create necessary directories
RUN mkdir -p \
    /app/model_cache/transformers \
    /app/model_cache/torch \
    /app/datasets \
    /app/models/face \
    /app/models/deepfake

# Copy requirements first for better caching
COPY requirements.txt .

# Install PyTorch CPU version (since we're deploying locally)
RUN pip install --no-cache-dir torch==2.2.0 torchvision==0.17.0 --index-url https://download.pytorch.org/whl/cpu

# Install other requirements
RUN pip install --no-cache-dir -r requirements.txt

# Download and extract datasets
RUN curl -L https://github.com/ondyari/FaceForensics/raw/master/dataset/FaceForensics++ -o /app/datasets/faceforensics.zip && \
    curl -L https://github.com/notAI-tech/NudeNet/raw/v2/dataset/nude.zip -o /app/datasets/nudenet.zip && \
    curl -L https://huggingface.co/datasets/hatexplain/raw/main/dataset.zip -o /app/datasets/hatexplain.zip && \
    cd /app/datasets && \
    unzip -q faceforensics.zip && \
    unzip -q nudenet.zip && \
    unzip -q hatexplain.zip && \
    rm *.zip

# Download NSFWJS model
RUN curl -L https://github.com/infinitered/nsfwjs/raw/master/example/nsfw_model.zip -o /app/model_cache/nsfw_model.zip && \
    cd /app/model_cache && \
    unzip -q nsfw_model.zip && \
    rm nsfw_model.zip

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
