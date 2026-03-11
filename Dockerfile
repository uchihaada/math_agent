FROM python:3.13-slim

ENV PIP_NO_CACHE_DIR=1
ENV OMP_NUM_THREADS=1
ENV PYTORCH_NO_CUDA_MEMORY_CACHING=1
ENV MALLOC_TRIM_THRESHOLD_=100000

RUN apt-get update && apt-get install -y ffmpeg tesseract-ocr \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir torch torchvision torchaudio \
    --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT"]