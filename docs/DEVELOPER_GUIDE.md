# 🛠️ RaidScanner Developer Guide

## 📋 Table of Contents
- [Architecture](#architecture)
  - [High-Level Overview](#high-level-overview)
  - [Data Flow](#data-flow)
- [Project Structure](#project-structure)
- [Docker Internals](#docker-internals)
- [API Documentation](#api-documentation)
- [Development Workflow](#development-workflow)
  - [Adding New Scanners](#adding-new-scanners)

---

## Architecture

### High-Level Overview

RaidScanner follows a layered architecture:

1.  **User Interface Layer**:
    *   **Web Interface**: Flask-based, uses Socket.IO for real-time updates.
    *   **CLI Interface**: Python-based, uses `rich` and `prompt_toolkit`.

2.  **Web Application Layer** (`app.py`):
    *   Handles HTTP routes and WebSocket events.
    *   Manages scan sessions and background threads.

3.  **Core Logic Layer** (`core/`):
    *   **Scanner Engine**: Platform-agnostic scanning logic (LFI, SQLi, etc.).
    *   **Report Generator**: Creates HTML/JSON reports.
    *   **Payload Loader**: Manages attack vectors.

4.  **Utility Layer** (`utils/`):
    *   **Platform Helper**: OS detection, path management.
    *   **Config**: Centralized settings.

5.  **Network Layer**:
    *   Uses `requests` and `aiohttp` for HTTP scanning.
    *   Uses `Selenium` + `ChromeDriver` for browser-based scanning (XSS, OR).

### Data Flow

1.  **Input**: User submits URLs via Web GUI or CLI.
2.  **Processing**:
    *   Request is validated.
    *   Background thread starts the `ScannerEngine`.
    *   Engine iterates through URLs and Payloads using multiple threads.
3.  **Feedback**:
    *   **Web**: Progress and results emitted via WebSockets (`scan_progress`).
    *   **CLI**: Progress bar updated in terminal.
4.  **Output**:
    *   Vulnerabilities stored in memory during scan.
    *   Final report generated in `reports/` (HTML/JSON).

---

## Project Structure

```
raidscanner/
├── .docker/                    # Docker configuration
│   ├── Dockerfile              # Container build definition
│   ├── compose.yml             # Docker Compose configuration (V2)
│   └── .dockerignore           # Docker build exclusions
│
├── bin/                        # Binary files and executables
│   └── chromedriver-linux64/   # ChromeDriver for Linux
│
├── core/                       # Core scanning logic
│   ├── scanner_engine.py       # Platform-agnostic scanners
│   ├── report_generator.py     # Report creation (HTML/JSON)
│   └── payload_loader.py       # Payload management
│
├── docs/                       # Documentation
│   ├── USER_GUIDE.md           # Complete user documentation
│   └── DEVELOPER_GUIDE.md      # Architecture & contribution guide
│
├── output/                     # Scan results (auto-generated)
│
├── payloads/                   # Attack payloads
│   ├── lfi-payloads.txt
│   ├── xss.txt
│   └── sqli/
│
├── reports/                    # Generated reports (auto-generated)
│
├── scripts/                    # Utility scripts
│   ├── start.sh                # Interactive startup script
│   ├── docker-run.sh           # Run Docker container (Linux/Mac)
│   └── docker-run.bat          # Run Docker container (Windows)
│
├── utils/                      # Utility modules
│   ├── config.py               # Configuration management
│   └── platform_helper.py      # Cross-platform compatibility
│
├── web/                        # Web interface
│   ├── templates/              # HTML Templates
│   └── static/                 # JS/CSS
│
├── app.py                      # Flask web application entry point
├── main.py                     # CLI application entry point
├── compose.yml                 # Symlink to .docker/compose.yml
├── requirements.txt            # Python dependencies (all)
└── requirements-docker.txt     # Docker-specific dependencies
```

---

## Docker Internals

The Docker setup ensures a consistent environment across platforms.

*   **Base Image**: `python:3.11-slim`
*   **Dependencies**:
    *   Google Chrome (Stable)
    *   ChromeDriver (Managed by `webdriver_manager`)
    *   Xvfb (Virtual Display for headless Chrome)
*   **Configuration**:
    *   `shm_size`: Set to 2GB+ to prevent Chrome crashes.
    *   **Volumes**: Maps host directories (`output`, `reports`) to container.

**Build Process:**
1.  Installs system dependencies (Chrome, Xvfb).
2.  Installs Python dependencies from `requirements-docker.txt`.
3.  Copies application code.
4.  Sets entrypoint to `start.sh` (or direct command).

---

## API Documentation

The Web GUI exposes a REST API and WebSocket interface.

### REST Endpoints

*   **POST** `/api/scan/lfi`
    *   Body: `{"urls": ["..."], "threads": 5, "success_criteria": ["root:x:0:"]}`
    *   Starts an LFI scan
*   **POST** `/api/scan/sqli`
    *   Body: `{"urls": ["..."], "threads": 5}`
    *   Starts a SQL Injection scan (time-based)
*   **POST** `/api/scan/xss`
    *   Body: `{"urls": ["..."], "threads": 3}`
    *   Starts an XSS scan (Selenium-based, uses fewer threads)
*   **POST** `/api/scan/or`
    *   Body: `{"urls": ["..."], "threads": 5}`
    *   Starts an Open Redirect scan
*   **POST** `/api/scan/crlf`
    *   Body: `{"urls": ["..."], "threads": 5}`
    *   Starts a CRLF Injection scan
*   **GET** `/api/reports`
    *   Returns list of generated reports
*   **GET** `/api/payloads`
    *   Returns available payload files

### WebSocket Events

*   `connect`: Client connected
*   `scan_progress`: Emitted during scan. Contains `{type, current_url, scanned, total, found}`
*   `scan_complete`: Emitted when scan finishes with full results
*   `scan_error`: Emitted on failure

---

## Development Workflow

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run CLI mode
python main.py

# Run web GUI
python app.py
```

### Docker Development
```bash
# Build and run web GUI
docker compose up -d raidscanner-web

# Or CLI mode
docker compose run --rm raidscanner-cli

# View logs
docker compose logs -f

# Rebuild after changes
docker compose build --no-cache
```

### Adding New Features

#### New Scanner
1. Add scanner logic to `core/scanner_engine.py`
2. Add payloads to `payloads/`
3. Create API endpoint in `app.py` (web mode)
4. Add CLI option to `main.py` (CLI mode)

#### New Web Page
1. Create HTML in `web/templates/`
2. Add static files to `web/static/`
3. Add route in `app.py`

#### New Script
1. Add script to `scripts/`
2. Make executable: `chmod +x scripts/your-script.sh`
3. Document in `docs/`

### Build & Deployment

#### Building Docker Image
```bash
docker compose build
```

#### Publishing
```bash
# Tag image
docker tag raidscanner:latest zahidoverflow/raidscanner:v2.0

# Push to Docker Hub
docker push zahidoverflow/raidscanner:v2.0
```
