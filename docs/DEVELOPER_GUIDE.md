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
├── app.py                  # Flask Web Application
├── main.py                 # CLI Application
├── core/                   # Core Logic
│   ├── scanner_engine.py   # Scanning implementation
│   ├── report_generator.py # Report creation
│   └── payload_loader.py   # Payload management
├── utils/                  # Utilities
│   ├── config.py           # Configuration
│   └── platform_helper.py  # OS helpers
├── web/                    # Frontend Assets
│   ├── templates/          # HTML Templates
│   └── static/             # JS/CSS
├── payloads/               # Attack Vectors
├── output/                 # Raw Output
├── reports/                # Generated Reports
├── Dockerfile              # Docker Image Definition
└── compose.yml             # Docker Compose Config
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

*   **POST** `/api/scan/<type>` (e.g., `lfi`, `sqli`)
    *   Body: `{"urls": ["..."], "threads": 5}`
    *   Starts a scan.
*   **GET** `/api/reports`
    *   Returns list of generated reports.
*   **GET** `/api/payloads`
    *   Returns available payload files.

### WebSocket Events

*   `connect`: Client connected.
*   `scan_progress`: Emitted during scan. Contains `{progress, scanned, found, vulnerability}`.
*   `scan_complete`: Emitted when scan finishes.
*   `scan_error`: Emitted on failure.

---

## Development Workflow

### Adding New Scanners

1.  **Backend (`core/scanner_engine.py`)**:
    *   Implement `scan_<type>(self, urls, payloads, threads)` method.
    *   Ensure it returns a list of results.

2.  **API Route (`app.py`)**:
    *   Add `@app.route('/api/scan/<type>', methods=['POST'])`.
    *   Call the new scanner method in a background thread.

3.  **Frontend (`web/templates/index.html`)**:
    *   Add a new Card for the scanner.
    *   Update `web/static/js/main.js` to handle the new type if necessary.

4.  **Payloads**:
    *   Add default payload file in `payloads/`.
