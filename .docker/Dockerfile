# Use Python 3.11 slim as base image
FROM python:3.11-slim

# Metadata
LABEL maintainer="zahidoverflow"
LABEL description="RaidScanner - Web Vulnerability Scanner"
LABEL version="2.0"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    DISPLAY=:99 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    CHROME_BIN=/usr/bin/google-chrome \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    libnss3 \
    default-jdk \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
COPY requirements-gui.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r requirements-gui.txt

# Copy application code
COPY . .

# Create directories for output
RUN mkdir -p output reports payloads

# Expose port for Web GUI
EXPOSE 5000

# Default command (can be overridden by docker-compose)
CMD ["/bin/bash", "-c", "Xvfb :99 -screen 0 1920x1080x24 & if [ \"$MODE\" = \"web\" ]; then python3 app.py; else python3 main.py; fi"]
