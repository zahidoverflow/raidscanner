# Use Python 3.11 slim as base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    DISPLAY=:99

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    xvfb \
    fonts-liberation \
    libnss3 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libatspi2.0-0 \
    libwayland-client0 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O /tmp/google-chrome-stable_current_amd64.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get update \
    && apt-get install -y /tmp/google-chrome-stable_current_amd64.deb \
    && rm /tmp/google-chrome-stable_current_amd64.deb \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements-docker.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-docker.txt

# Copy the rest of the application
COPY . .

# Copy ChromeDriver (if pre-downloaded)
COPY chromedriver-linux64/ /usr/local/bin/

# Make sure chromedriver is executable
RUN if [ -f /usr/local/bin/chromedriver ]; then chmod +x /usr/local/bin/chromedriver; fi

# Create output directory
RUN mkdir -p /app/output /app/reports

# Set permissions
RUN chmod +x filter.sh || true

# Start Xvfb in the background and run the main script
ENTRYPOINT ["/bin/bash", "-c", "Xvfb :99 -screen 0 1920x1080x24 > /dev/null 2>&1 & python3 main.py"]
