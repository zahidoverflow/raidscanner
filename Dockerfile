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
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies in a single layer
RUN apt-get update && apt-get install -y --no-install-recommends \
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
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install Google Chrome (pinned version for stability)
RUN wget -q -O /tmp/google-chrome-stable_current_amd64.deb \
    https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get update \
    && apt-get install -y --no-install-recommends /tmp/google-chrome-stable_current_amd64.deb \
    && rm /tmp/google-chrome-stable_current_amd64.deb \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Verify Chrome installation
RUN google-chrome --version

# Set working directory
WORKDIR /app

# Copy and install Python dependencies first (better layer caching)
COPY requirements-docker.txt .

# Upgrade pip and install dependencies with locked versions
RUN pip install --upgrade pip==24.3.1 setuptools==75.6.0 wheel==0.45.1 \
    && pip install --no-cache-dir -r requirements-docker.txt \
    && pip list

# Copy application files
COPY main.py filter.sh ./
COPY payloads/ ./payloads/
COPY chromedriver-linux64/ /usr/local/bin/

# Set permissions
RUN chmod +x filter.sh 2>/dev/null || true \
    && if [ -f /usr/local/bin/chromedriver ]; then chmod +x /usr/local/bin/chromedriver; fi

# Create necessary directories with proper permissions
RUN mkdir -p /app/output /app/reports \
    && chmod 777 /app/output /app/reports

# Health check (optional but recommended)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import sys; sys.exit(0)" || exit 1

# Non-root user for security (optional but recommended)
RUN useradd -m -u 1000 scanner \
    && chown -R scanner:scanner /app
USER scanner

# Start Xvfb and run the application
CMD ["/bin/bash", "-c", "Xvfb :99 -screen 0 1920x1080x24 > /dev/null 2>&1 & sleep 1 && python3 main.py"]
