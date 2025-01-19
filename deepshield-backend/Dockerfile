# Build stage for AI dependencies
FROM python:3.12-slim as ai-builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install AI dependencies first
COPY requirements-ai.txt .
RUN pip install --no-cache-dir -r requirements-ai.txt

# Final stage
FROM python:3.12-slim

WORKDIR /app

# Copy AI packages from builder
COPY --from=ai-builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Install base requirements
COPY requirements-base.txt .
RUN pip install --no-cache-dir -r requirements-base.txt

# Create necessary directories
RUN mkdir -p /app/models /app/datasets /app/credentials

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV AI_MODELS_PATH=/app/models
ENV DATASET_PATH=/app/datasets
ENV USE_CPU_ONLY=true

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
