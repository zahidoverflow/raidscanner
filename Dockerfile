# syntax=docker/dockerfile:1.4
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    DISPLAY=:99

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    gnupg \
    unzip \
    curl \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    default-jdk \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.com.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .
# Create dummy requirements if not exists to prevent build fail
RUN touch requirements.txt

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install selenium webdriver-manager requests beautifulsoup4 colorama rich prompt_toolkit pyyaml flask flask-socketio eventlet

# Copy application code
COPY . .

# Create directories for output
RUN mkdir -p output reports payloads

# Make scripts executable
RUN chmod +x *.py || true

# Entrypoint script
COPY <<EOF /app/entrypoint.sh
#!/bin/bash
# Start Xvfb
Xvfb :99 -screen 0 1920x1080x24 > /dev/null 2>&1 &

# Run application based on mode
if [ "\$MODE" = "web" ]; then
    python app.py
else
    python main.py "\$@"
fi
EOF

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
