FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    libcairo2-dev \
    libpango1.0-dev \
    pkg-config \
    python3-dev \
    gcc \
    texlive-latex-extra \
    texlive-fonts-extra \
    dvipng \
    ghostscript \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]