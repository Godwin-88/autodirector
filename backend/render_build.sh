#!/bin/bash
# Render native-Python build script.
# Installs the system packages the backend needs (ffmpeg/Manim/LaTeX/Playwright),
# then installs Python dependencies. Render runs this from the service rootDir (backend/).
set -e

echo "Installing system dependencies (ffmpeg, Manim, LaTeX...)"
apt-get update
apt-get install -y \
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
    || echo "Some apt packages failed (tolerating) — app may still boot if the package is optional"

echo "Installing Python dependencies"
pip install -r requirements.txt

echo "Installing Playwright browsers (best-effort)"
playwright install --with-deps chromium 2>/dev/null || true

echo "Build complete."