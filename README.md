# 🛡️ RaidScanner

[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-zahidoverflow%2Fraidscanner-blue?logo=docker)](https://hub.docker.com/r/zahidoverflow/raidscanner)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**RaidScanner** is a modern, automated vulnerability scanner designed for ethical hacking. It detects common web vulnerabilities including **LFI**, **SQLi**, **XSS**, **Open Redirect**, and **CRLF Injection**.

---

## 🚀 Quick Start (Docker)

The easiest way to run RaidScanner is using Docker. No manual dependency installation required.

### 1. Web GUI Mode (Recommended)
Starts the web interface at `http://localhost:5000`.

```bash
docker compose up -d raidscanner-web
```

### 2. CLI Mode
Starts the interactive command-line interface.

```bash
docker compose run --rm raidscanner-cli
```

---

## 📂 File Management

RaidScanner automatically maps folders so you can easily manage files on your host machine:

| Folder | Description |
|--------|-------------|
| `./payloads/` | **Input**: Place your custom payload files here. |
| `./output/` | **Output**: Raw scan results are saved here. |
| `./reports/` | **Reports**: HTML/JSON vulnerability reports are saved here. |

> **Tip**: When the CLI asks for a payload file path, just enter the filename (e.g., `sqli.txt`) if it's inside the `./payloads` folder.

---

## 🛠️ Installation

**Prerequisites**: [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/).

1. **Clone the repository:**
   ```bash
   git clone https://github.com/zahidoverflow/raidscanner.git
   cd raidscanner
   ```

2. **Build the image (optional, first time only):**
   ```bash
   docker compose build
   ```

---

## 📖 Documentation

- [**User Guide**](docs/USER_GUIDE.md): Detailed usage instructions and troubleshooting.
- [**Developer Guide**](docs/DEVELOPER_GUIDE.md): Architecture and contribution guidelines.

---

## ⚠️ Disclaimer

This tool is for **educational and authorized security testing purposes only**. You must have explicit permission to scan any target. The author is not responsible for any misuse.
