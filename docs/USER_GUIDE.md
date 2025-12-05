# 🛡️ RaidScanner User Guide

## 📋 Table of Contents
- [Introduction](#introduction)
- [Quick Start](#quick-start)
- [Installation & Setup](#installation--setup)
  - [Option 1: Docker (Recommended)](#option-1-docker-recommended)
  - [Option 2: Manual Installation](#option-2-manual-installation)
- [Using the Web GUI](#using-the-web-gui)
- [Using the CLI](#using-the-cli)
- [Troubleshooting](#troubleshooting)

---

## Introduction

**RaidScanner** is a modern, automated vulnerability scanner designed for ethical hacking and security testing. It detects common web vulnerabilities including:
- **LFI** (Local File Inclusion)
- **SQLi** (SQL Injection)
- **XSS** (Cross-Site Scripting)
- **OR** (Open Redirect)
- **CRLF** (Carriage Return Line Feed Injection)

It features both a **Web GUI** for ease of use and a **CLI** for terminal lovers.

---

## Quick Start

### 🌐 Web GUI (Recommended for Beginners)

1. **Start Web Interface:**
   ```bash
   docker compose up -d raidscanner-web
   ```

2. **Open Browser:**
   Go to `http://localhost:5000`

3. **Use the Interface:**
   - Click on a scanner card (e.g., LFI Scanner).
   - Enter target URLs (one per line).
   - Adjust threads (1-10).
   - Click "Start Scan".
   - Watch real-time results!

4. **View Reports:**
   Click the "Reports" card to see scan history.

### 💻 CLI Mode (Traditional Terminal)

**Start CLI:**
```bash
docker compose run --rm raidscanner-cli
```
Follow the interactive menu to select scanner type and configure options.

---

## Installation & Setup

### Option 1: Docker (Recommended)

Docker provides a fully isolated environment with all dependencies (Chrome, Python, etc.) pre-installed.

**Prerequisites:**
- Docker Engine 20.10+
- Docker Compose 2.0+

**Setup:**
1. **Clone Repository:**
   ```bash
   git clone https://github.com/zahidoverflow/raidscanner.git
   cd raidscanner
   ```

2. **Build & Run:**
   ```bash
   # Build the image
   docker compose build

   # Run Web GUI
   docker compose up -d raidscanner-web
   ```

**Volume Mounts:**
- `./output`: Stores filtered URLs.
- `./reports`: Stores HTML vulnerability reports.
- `./payloads`: Contains payload files (read-only).

### Option 2: Manual Installation (Advanced)

⚠️ **Note**: Requires installing Chrome, ChromeDriver, and Python dependencies on your host machine.

1. **Install Python Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Chrome & ChromeDriver:**
   - Ensure Google Chrome is installed.
   - Ensure ChromeDriver matches your Chrome version and is in your PATH.

3. **Run the Application:**
   ```bash
   # Web GUI
   python app.py

   # CLI
   python scanner_cli.py
   ```

---

## Using the Web GUI

The Web GUI provides a modern interface for scanning.

### Features
- **Real-time Updates**: See vulnerabilities as they are found.
- **Interactive Cards**: Visual scanner selection.
- **Reports**: View and download HTML/JSON reports.

### Workflow
1. **Select a Scanner**: Click on a card (LFI, SQLi, etc.).
2. **Configure**:
   - **URLs**: Enter one URL per line.
   - **Payloads**: Select default or upload custom.
   - **Threads**: Adjust concurrent threads (default 5).
3. **Monitor**: Watch the progress bar and live results.
4. **Analyze**: View the final report in the "Reports" section.

---

## Using the CLI

The CLI offers a robust, interactive terminal experience.

### Workflow
1. **Select Scanner**: Choose from the menu (LFI, SQLi, etc.).
2. **Input**: Provide a single URL or a file containing URLs.
3. **Payloads**: Select a payload file.
4. **Threads**: Set the number of threads.
5. **Results**: View results in the terminal and check the `reports/` folder for the HTML report.

---

## Troubleshooting

### Web GUI Not Loading
- **Check Port**: Ensure port 5000 is free.
- **Check Logs**: `docker compose logs raidscanner-web`
- **Restart**: `docker compose restart raidscanner-web`

### Chrome/Selenium Issues
- **Memory**: If Chrome crashes in Docker, increase shared memory in `docker-compose.yml`:
  ```yaml
  shm_size: '4gb'
  ```
- **Version Mismatch**: If running manually, ensure Chrome and ChromeDriver versions match.

### Permissions
- If reports aren't saving, check folder permissions:
  ```bash
  chmod 777 output reports
  ```

### Network Issues
- Ensure Docker has internet access.
- Test connectivity: `docker compose run --rm raidscanner-cli ping google.com`
