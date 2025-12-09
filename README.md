# 🛡️ RaidScanner

[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-zahidoverflow%2Fraidscanner-blue?logo=docker)](https://hub.docker.com/r/zahidoverflow/raidscanner)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/selenium-4.0+-green.svg)](https://www.selenium.dev/)
[![Flask](https://img.shields.io/badge/flask-3.0-red.svg)](https://flask.palletsprojects.com/)

**RaidScanner** is an advanced, production-ready automated web vulnerability scanner with both **Web GUI** and **CLI** interfaces. Designed for ethical hacking and security testing, it detects critical web vulnerabilities including **LFI (Local File Inclusion)**, **SQLi (SQL Injection)**, **XSS (Cross-Site Scripting)**, **Open Redirect**, and **CRLF Injection**.

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture & Technology Stack](#-architecture--technology-stack)
- [Quick Start](#-quick-start-docker)
- [Installation Methods](#-installation-methods)
- [Usage Guide](#-usage-guide)
- [Vulnerability Detection Methods](#-vulnerability-detection-methods)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Performance & Optimization](#-performance--optimization)
- [Output & Reports](#-output--reports)
- [Testing Targets](#-testing-targets)
- [Troubleshooting](#-troubleshooting)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [Legal Disclaimer](#-legal-disclaimer)
- [License](#-license)

---

## 🎯 Overview

RaidScanner is a comprehensive web security scanning tool built as a **university thesis project** to demonstrate modern vulnerability detection techniques. It combines traditional HTTP-based scanning with browser automation using Selenium WebDriver to detect both server-side and client-side vulnerabilities.

### What Makes RaidScanner Unique?

- **Dual Interface**: Choose between modern Web GUI or powerful CLI
- **Real-time Updates**: WebSocket-based live progress tracking
- **Browser Automation**: Selenium-powered detection for JavaScript-rendered applications
- **Containerized**: Fully Dockerized for consistent cross-platform execution
- **Production Ready**: Modular architecture with comprehensive error handling
- **Educational Focus**: Well-documented codebase designed for learning

### Use Cases

✅ **Security Audits**: Assess web applications for common OWASP Top 10 vulnerabilities  
✅ **Penetration Testing**: Automated reconnaissance and vulnerability detection  
✅ **CTF Competitions**: Quickly identify vulnerable endpoints in capture-the-flag challenges  
✅ **Education**: Learn vulnerability detection techniques through practical implementation  
✅ **Development**: Integrate into CI/CD pipelines for security testing

---

## ✨ Key Features

### Comprehensive Vulnerability Detection

| Vulnerability | Status | Detection Method | Highlights |
|--------------|--------|-----------------|-----------|
| **LFI** (Local File Inclusion) | ✅ | Selenium + Pattern Matching | Detects file access via path traversal |
| **SQLi** (SQL Injection) | ✅ | Time-based + Error-based | Authentication bypass detection |
| **XSS** (Cross-Site Scripting) | ✅ | Browser Automation + Alert Detection | Reflected & DOM-based XSS |
| **Open Redirect** | ✅ | URL Analysis + JavaScript Parsing | Header & client-side redirects |
| **CRLF Injection** | ✅ | HTTP Response Splitting | Header injection detection |

### Advanced Features

🚀 **Multi-threaded Scanning**: Configurable concurrency (1-10 threads)  
📊 **Real-time Dashboard**: Live progress updates via WebSocket  
📁 **Multiple Output Formats**: HTML & JSON reports  
🎨 **Modern UI**: Gradient-based dark theme with Tailwind CSS  
🔧 **Customizable Payloads**: Easily modify or add payload files  
🐳 **Docker Support**: One-command deployment with volume persistence  
🎯 **Smart Detection**: Context-aware vulnerability identification  
⚡ **Performance Optimized**: Resource-efficient Selenium execution

---

## 🏗️ Architecture & Technology Stack

### System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface Layer                 │
│  ┌──────────────────┐       ┌──────────────────┐      │
│  │   Web GUI        │       │   CLI Interface   │      │
│  │ (Flask + Socket) │       │ (Rich + Colorama) │      │
│  └────────┬─────────┘       └────────┬─────────┘      │
└───────────┼──────────────────────────┼─────────────────┘
            │                          │
┌───────────┴──────────────────────────┴─────────────────┐
│              Application Layer (app.py)                 │
│  • Route Handling    • WebSocket Events                │
│  • Session Management • Background Tasks               │
└────────────────────────┬───────────────────────────────┘
                         │
┌────────────────────────┴───────────────────────────────┐
│                 Core Logic Layer (core/)               │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │Scanner Engine│  │Report Gen    │  │Payload Load │ │
│  │(5 scanners)  │  │(HTML/JSON)   │  │(Management) │ │
│  └──────┬───────┘  └──────────────┘  └─────────────┘ │
└─────────┼──────────────────────────────────────────────┘
          │
┌─────────┴────────────────────────────────────────────┐
│           Network & Browser Layer                     │
│  ┌─────────────────┐     ┌─────────────────┐        │
│  │ Requests/AIOHTTP│     │ Selenium + Chrome│        │
│  │  (HTTP Scanning)│     │ (Browser Testing)│        │
│  └─────────────────┘     └─────────────────┘        │
└──────────────────────────────────────────────────────┘
```

### Technology Stack

#### Backend
- **Python 3.11**: Core language for optimal performance
- **Flask 3.0.3**: Web framework for RESTful API
- **Flask-SocketIO 5.3.6**: Real-time bidirectional communication
- **Eventlet 0.36.1**: Asynchronous networking library

#### Scanning & Automation
- **Selenium 4.0+**: Browser automation for JavaScript-heavy sites
- **ChromeDriver**: Headless Chrome for realistic rendering
- **Requests**: HTTP library for traditional scanning
- **AIOHTTP**: Async HTTP client for concurrent requests
- **BeautifulSoup4**: HTML/XML parsing

#### CLI & UI
- **Rich**: Beautiful terminal interface with progress bars
- **Colorama**: Cross-platform colored terminal text
- **Prompt Toolkit**: Interactive CLI components

#### DevOps & Infrastructure
- **Docker**: Containerization for consistent environments
- **Docker Compose**: Multi-container orchestration
- **Xvfb**: Virtual framebuffer for headless GUI execution
- **Chrome (Stable)**: Latest browser for accurate testing

---

## 🚀 Quick Start (Docker)

The easiest and recommended way to run RaidScanner is using Docker. No manual dependency installation required!

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) (20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (2.0+)

### 1️⃣ Web GUI Mode (Recommended)

Perfect for beginners and visual learners. Provides a beautiful dashboard with real-time updates.

```bash
# Start the web interface
docker compose up -d raidscanner-web

# Access at http://localhost:5000
```

**Features:**
- 📊 Interactive dashboard with scanner cards
- 🔴 Real-time vulnerability detection
- 📈 Live progress bars and statistics
- 📄 Report viewer with download options

### 2️⃣ CLI Mode (Advanced)

For terminal enthusiasts and automation workflows. Provides a rich interactive CLI.

```bash
# Start the interactive CLI
docker compose run --rm raidscanner-cli
```

**Features:**
- 🎯 Menu-driven interface
- 📊 Live progress bars
- 🎨 Color-coded output
- 💾 Automatic report saving

### 3️⃣ Stop Services

```bash
# Stop web service
docker compose down

# Remove all containers and volumes
docker compose down -v
```

---

## 🛠️ Installation Methods

### Method 1: Docker (Recommended) ⭐

**Advantages:**
- ✅ No dependency conflicts
- ✅ Consistent environment across all platforms
- ✅ Chrome and ChromeDriver pre-installed
- ✅ Automatic volume mounting
- ✅ Easy updates via Docker Hub

```bash
# Clone repository
git clone https://github.com/zahidoverflow/raidscanner.git
cd raidscanner

# Pull pre-built image (optional)
docker pull zahidoverflow/raidscanner:latest

# Or build locally
docker compose build

# Run Web GUI
docker compose up -d raidscanner-web

# Run CLI
docker compose run --rm raidscanner-cli
```

### Method 2: Manual Installation (Advanced)

**Requirements:**
- Python 3.11+
- Google Chrome (latest stable)
- ChromeDriver (matching Chrome version)

```bash
# Clone repository
git clone https://github.com/zahidoverflow/raidscanner.git
cd raidscanner

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install ChromeDriver
# Linux: Download from https://chromedriver.chromium.org/
# Or use: pip install webdriver-manager

# Run Web GUI
python app.py

# Run CLI
python scanner_cli.py
```

**Note**: Manual installation requires system-specific configuration of Chrome and ChromeDriver paths.

---

## 📖 Usage Guide

### Web GUI Workflow

1. **Start the Service**
   ```bash
   docker compose up -d raidscanner-web
   ```

2. **Access Dashboard**
   - Open browser: `http://localhost:5000`
   - You'll see 6 scanner cards + Reports viewer

3. **Select Scanner**
   - Click on any scanner card (e.g., "LFI Scanner")
   - Configuration panel appears

4. **Configure Scan**
   - **URLs**: Enter target URLs (one per line)
     ```
     http://example.com/page?file=
     http://test.com/view?id=
     ```
   - **Threads**: Adjust concurrency (1-10, default: 5)
   - **Payloads**: Use default or select custom file

5. **Execute Scan**
   - Click "Start Scan" button
   - Watch real-time progress updates
   - Vulnerabilities appear as they're found

6. **View Reports**
   - Click "Reports" card on dashboard
   - Browse scan history
   - Download HTML/JSON reports

### CLI Workflow

1. **Start CLI**
   ```bash
   docker compose run --rm raidscanner-cli
   ```

2. **Main Menu**
   ```
   [ RaidScanner ]
   
   Available Scanners:
     1. LFI Scanner       - Local File Inclusion
     2. Open Redirect     - Unvalidated Redirects
     3. SQL Injection     - Database Injection
     4. XSS Scanner       - Cross-Site Scripting
     5. CRLF Injection    - HTTP Response Splitting
     6. Exit
   ```

3. **Input Target URLs**
   - Enter URLs one per line
   - Press Enter twice when done
   - Or provide a file path with URLs

4. **Select Payload File**
   - Choose from available payload files
   - Or enter custom payload file path

5. **Configure Threads**
   - Enter 1-10 (default: 5)
   - Lower for resource-constrained systems

6. **Monitor Progress**
   - Live progress bar displays scan status
   - Vulnerabilities shown in real-time
   - Final summary with statistics

7. **Access Reports**
   - HTML reports saved to `./reports/`
   - JSON data saved for programmatic access

---

## 🔍 Vulnerability Detection Methods

### 1. LFI (Local File Inclusion)

**Detection Technique**: Selenium-based browser automation with content analysis

**How It Works:**
1. Injects file traversal payloads (e.g., `../../../etc/passwd`)
2. Renders page using Chrome WebDriver
3. Checks if file content appears (not "File not found" message)
4. Validates against false positives

**Payloads Used:**
- Path traversal: `../../../etc/passwd`
- Encoded variants: `%2e%2e%2f`, `..%2f`
- Null byte injection: `../../../etc/passwd%00`
- Windows paths: `..\..\windows\win.ini`

**Success Indicators:**
- `root:x:0:` (Linux passwd file)
- `boot loader` (Windows boot.ini)
- Absence of "File not found:" message

### 2. SQLi (SQL Injection)

**Detection Technique**: Hybrid approach (Time-based + Error-based)

**Time-Based Detection:**
1. Injects delay payloads: `' AND SLEEP(5)--`
2. Measures response time
3. If response time ≥ threshold → Vulnerable

**Error-Based Detection:**
1. Injects syntax-breaking payloads: `' OR '1'='1`
2. Checks response for SQL error messages
3. Detects patterns like "SQL Error", "syntax error", "detected injection"

**Payloads Used:**
- Authentication bypass: `' OR '1'='1'--`
- Union-based: `' UNION SELECT NULL,NULL--`
- Time-based: `' AND SLEEP(5)--`
- Stacked queries: `'; DROP TABLE users--`

**Database Support:**
- MySQL, PostgreSQL, MSSQL, Oracle
- Generic payloads for maximum compatibility

### 3. XSS (Cross-Site Scripting)

**Detection Technique**: Selenium-based alert detection + source code analysis

**How It Works:**
1. Injects XSS payloads into URL parameters
2. Renders page in headless Chrome
3. Checks for `alert()` execution
4. Falls back to source code inspection for encoded payloads

**Payloads Used:**
- Basic: `<script>alert(1)</script>`
- Event handlers: `<img src=x onerror=alert(1)>`
- SVG vectors: `<svg onload=alert(1)>`
- Polyglots: Mixed-context payloads

**Detection Methods:**
- Alert popup detection (primary)
- Payload reflection in source (secondary)
- DOM mutation analysis

### 4. Open Redirect

**Detection Technique**: Multi-method redirect detection

**Detection Methods:**
1. **HTTP Headers**: Checks `Location` header
2. **Meta Refresh**: Parses `<meta http-equiv="refresh">`
3. **JavaScript**: Detects `window.location` assignments
4. **URL Change**: Monitors browser navigation

**Payloads Used:**
- `http://evil.com`
- `//evil.com` (protocol-relative)
- `https://evil.com@good.com`
- `javascript:alert(1)`

**Validation:**
- Confirms actual redirection occurred
- Checks if payload URL appears in destination

### 5. CRLF Injection

**Detection Technique**: HTTP response header manipulation

**How It Works:**
1. Injects CRLF sequences: `%0d%0aSet-Cookie:injected=1`
2. Checks response headers for injected content
3. Validates successful header splitting

**Payloads Used:**
- `%0d%0aSet-Cookie:crlf=injection`
- `\r\nSet-Cookie:crlf=injection`
- Unicode variants: `%E5%98%8A%E5%98%8D`
- Null byte combinations

**Success Indicators:**
- "CRLF injection" message in response
- "HTTP response splitting" detected
- Injected headers visible

---

## 📁 Project Structure

```
raidscanner/
├── 📄 app.py                      # Flask web application (469 lines)
├── 📄 scanner_cli.py              # CLI interface (381 lines)
├── 📄 compose.yml                 # Docker Compose configuration
├── 📄 requirements.txt            # Python dependencies
├── 📄 requirements-docker.txt     # Docker-specific dependencies
├── 📄 README.md                   # This file
│
├── 📁 .docker/                    # Docker configuration
│   ├── Dockerfile                # Container build definition
│   └── .dockerignore             # Build exclusions
│
├── 📁 core/                       # Core scanning engine
│   ├── __init__.py
│   ├── scanner_engine.py         # 744 lines - All scanner logic
│   ├── report_generator.py       # 129 lines - HTML/JSON reports
│   └── payload_loader.py         # 70 lines - Payload management
│
├── 📁 utils/                      # Utility modules
│   ├── __init__.py
│   ├── config.py                 # 70 lines - Configuration
│   └── platform_helper.py        # Cross-platform helpers
│
├── 📁 web/                        # Web interface
│   ├── templates/
│   │   ├── index.html            # Dashboard
│   │   ├── scanner.html          # Scanner configuration
│   │   └── reports.html          # Report viewer
│   └── static/
│       └── js/
│           └── main.js           # 352 lines - Frontend logic
│
├── 📁 payloads/                   # Attack payloads
│   ├── lfi-payloads.txt          # LFI vectors
│   ├── sqli.txt                  # SQL injection payloads
│   ├── xss.txt                   # XSS payloads (optimized)
│   ├── or.txt                    # Open redirect URLs
│   └── sqli/                     # Database-specific payloads
│       ├── mysql.txt
│       ├── postgresql.txt
│       ├── mssql
│       └── oracle.txt
│
├── 📁 reports/                    # Generated reports (auto-created)
│   ├── lfi_report_*.html
│   ├── sqli_report_*.json
│   └── ...
│
├── 📁 output/                     # Raw scan data (auto-created)
│
├── 📁 docs/                       # Documentation
│   ├── CONTEXT.md                # 300 lines - Full project context
│   ├── USER_GUIDE.md             # 171 lines - User documentation
│   ├── DEVELOPER_GUIDE.md        # 274 lines - Architecture guide
│   └── openspec/                 # OpenSpec documentation
│
├── 📁 bin/                        # Binary executables
│   └── chromedriver-linux64/     # ChromeDriver for Linux
│
└── 📁 scripts/                    # Utility scripts
    ├── start.sh                  # Interactive startup
    ├── docker-run.sh             # Linux/Mac runner
    └── docker-run.bat            # Windows runner
```

**Key Files:**

- `core/scanner_engine.py`: Heart of the application - contains all 5 scanners
- `app.py`: Flask web server with WebSocket support
- `web/static/js/main.js`: Frontend JavaScript for real-time updates
- `compose.yml`: Docker orchestration configuration

---

## ⚙️ Configuration

### Environment Variables

```bash
# Web Server
HOST=0.0.0.0              # Listen address
PORT=5000                 # Web server port
DEBUG=False               # Debug mode
SECRET_KEY=your-secret    # Flask secret key

# Scanning
DEFAULT_THREADS=5         # Default concurrency
MAX_THREADS=10            # Maximum allowed threads
DEFAULT_TIMEOUT=10        # Request timeout (seconds)

# Chrome/Selenium
DISPLAY=:99               # Virtual display for Xvfb
```

### Docker Compose Configuration

```yaml
services:
  raidscanner-web:
    image: zahidoverflow/raidscanner:latest
    ports:
      - "5000:5000"
    volumes:
      - ./output:/app/output
      - ./reports:/app/reports
      - ./payloads:/app/payloads:ro
    environment:
      - MODE=web
    shm_size: '2gb'  # Required for Chrome
```

### Chrome Options

Configured in `utils/config.py`:

```python
CHROME_OPTIONS = [
    '--headless',                    # Run without GUI
    '--no-sandbox',                  # Required for Docker
    '--disable-dev-shm-usage',       # Overcome limited /dev/shm
    '--disable-gpu',                 # Disable GPU acceleration
    '--disable-extensions',          # No extensions
    '--disable-browser-side-navigation',
    '--disable-infobars',
    '--disable-notifications'
]
```

### Custom Payloads

Add custom payloads to `./payloads/` directory:

```bash
# Create custom LFI payload file
echo "../../../custom/path" >> ./payloads/custom-lfi.txt

# Create custom SQLi payloads
cat > ./payloads/custom-sqli.txt << EOF
' OR 1=1--
' UNION SELECT NULL--
' AND SLEEP(10)--
EOF
```

---

## ⚡ Performance & Optimization

### Resource Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 2 cores | 4+ cores |
| RAM | 2 GB | 4 GB |
| Disk | 1 GB | 5 GB |
| Network | Stable connection | High bandwidth |

### Thread Configuration

- **LFI**: 3-5 threads (Selenium-intensive)
- **SQLi**: 3-5 threads (Time-based delays)
- **XSS**: 2-3 threads (Browser overhead)
- **Open Redirect**: 3-5 threads (Network-bound)
- **CRLF**: 3-5 threads (Lightweight)

### Performance Tips

1. **Adjust Thread Count**: Lower threads for resource-constrained systems
2. **Use SSD**: Faster disk I/O for Chrome cache
3. **Increase shm_size**: Set to 2GB+ in Docker for Chrome stability
4. **Filter Payloads**: Remove unnecessary payloads for faster scans
5. **Network**: Ensure stable connection to target

### Optimization Techniques

```python
# Example: Reduce XSS payload file for faster scans
head -n 100 payloads/xss.txt > payloads/xss-quick.txt

# Use custom payload in CLI or Web GUI
```

---

## 📊 Output & Reports

### Report Formats

#### 1. HTML Reports

Beautiful, interactive HTML reports with Tailwind CSS styling:

```html
Location: ./reports/{type}_report_{timestamp}.html
Features:
  - Summary statistics
  - Vulnerable URLs with direct links
  - Color-coded severity
  - Responsive design
  - Printable format
```

**Example**: `reports/lfi_report_20251209_090022.html`

#### 2. JSON Reports

Machine-readable JSON for automation:

```json
{
  "scan_type": "LFI",
  "timestamp": "2025-12-09T09:00:22",
  "summary": {
    "total_found": 5,
    "total_scanned": 150,
    "duration": 45
  },
  "vulnerable_urls": [...],
  "detailed_results": [...]
}
```

**Example**: `reports/lfi_report_20251209_090022.json`

### File Management

Docker automatically maps these directories:

| Host Directory | Container Path | Purpose |
|---------------|----------------|---------|
| `./payloads/` | `/app/payloads` | Input: Attack payloads (read-only) |
| `./output/` | `/app/output` | Output: Raw scan data |
| `./reports/` | `/app/reports` | Reports: HTML/JSON vulnerability reports |

**Accessing Reports:**

```bash
# View latest LFI report
open ./reports/lfi_report_*.html  # macOS
xdg-open ./reports/lfi_report_*.html  # Linux
start ./reports/lfi_report_*.html  # Windows

# Parse JSON programmatically
python -m json.tool reports/sqli_report_*.json
```

---

## 🎯 Testing Targets

RaidScanner has been tested against various intentionally vulnerable applications:

### 1. DVWU (Damn Vulnerable Web University) ⭐

**Compatibility**: Excellent (Custom-built for this project)

```bash
# Clone DVWU
git clone https://github.com/zahidoverflow/dvwu.git
cd dvwu

# Start DVWU
npm install
npm start

# Scan with RaidScanner
# LFI: http://localhost:3000/api/download?file=
# SQLi: http://localhost:3000/api/search?query=
# XSS: http://localhost:3000/api/comment?text=
# OR: http://localhost:3000/api/redirect?url=
# CRLF: http://localhost:3000/api/newsletter?email=
```

### 2. DVWA (Damn Vulnerable Web Application)

**Compatibility**: Good (Requires security level: Low)

### 3. OWASP WebGoat

**Compatibility**: Moderate (Some lessons compatible)

### 4. bWAPP

**Compatibility**: Good (Multiple vulnerability types)

### 5. TestPHP Vulnweb (Online)

**URL**: `http://testphp.vulnweb.com/`  
**Compatibility**: Excellent (Public test site)

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Web GUI Not Loading

```bash
# Check if container is running
docker ps

# View logs
docker logs raidscanner-web

# Restart service
docker compose restart raidscanner-web
```

#### 2. Chrome/ChromeDriver Errors

```
Error: Chrome failed to start
Solution: Increase Docker shm_size to 2GB
```

```yaml
# In compose.yml
shm_size: '2gb'
```

#### 3. Connection Timeout

```
Error: Connection timeout
Solution: Increase timeout in utils/config.py
```

```python
DEFAULT_TIMEOUT = 30  # Increase from 10
```

#### 4. Permission Denied (Linux)

```bash
# Fix volume permissions
sudo chown -R $USER:$USER ./output ./reports
chmod -R 755 ./output ./reports
```

#### 5. WebSocket Connection Failed

```
Error: WebSocket disconnected
Solution: Check CORS settings and firewall
```

```python
# In app.py
CORS(app, resources={r"/*": {"origins": "*"}})
```

### Debug Mode

Enable debug logging:

```bash
# Set environment variable
export DEBUG=True

# Run with verbose logging
docker compose up raidscanner-web
```

---

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directory:

### 1. [User Guide](docs/USER_GUIDE.md)
- Installation instructions
- Web GUI walkthrough
- CLI usage guide
- Troubleshooting tips

### 2. [Developer Guide](docs/DEVELOPER_GUIDE.md)
- Architecture overview
- API documentation
- Adding new scanners
- Contributing guidelines

### 3. [Context Guide](docs/CONTEXT.md)
- Complete project context (300 lines)
- Technical implementation details
- Performance characteristics
- Version history

### 4. OpenSpec Documentation
- Detailed feature analysis
- Bug tracking
- Project specifications
- Change proposals

---

## 🤝 Contributing

Contributions are welcome! This project was built for educational purposes and community improvement.

### How to Contribute

1. **Fork the Repository**
   ```bash
   git clone https://github.com/zahidoverflow/raidscanner.git
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/new-scanner
   ```

3. **Make Changes**
   - Add new scanner in `core/scanner_engine.py`
   - Update documentation
   - Add tests

4. **Test Thoroughly**
   ```bash
   # Test web mode
   docker compose up -d raidscanner-web
   
   # Test CLI mode
   docker compose run --rm raidscanner-cli
   ```

5. **Submit Pull Request**
   - Clear description of changes
   - Link to related issues
   - Include test results

### Development Setup

```bash
# Clone repository
git clone https://github.com/zahidoverflow/raidscanner.git
cd raidscanner

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run in development mode
export DEBUG=True
python app.py
```

### Adding New Scanners

See [Developer Guide](docs/DEVELOPER_GUIDE.md) for detailed instructions on:
- Scanner architecture
- Adding detection methods
- Integrating with Web GUI and CLI
- Writing tests

---

## ⚠️ Legal Disclaimer

### Important Notice

This tool is designed for **educational purposes** and **authorized security testing only**.

**You MUST have explicit written permission** to scan any target system. Unauthorized scanning is **illegal** in most jurisdictions and may result in:

- ⚖️ Criminal prosecution
- 💰 Civil lawsuits
- 🚫 Network bans
- 📋 Legal penalties

### Responsible Usage

✅ **Authorized Activities:**
- Scanning your own applications
- Penetration testing with client authorization
- Security research on intentionally vulnerable platforms (DVWA, DVWU, etc.)
- Educational use in controlled environments
- CTF competitions

❌ **Prohibited Activities:**
- Scanning systems without permission
- Malicious exploitation of vulnerabilities
- Unauthorized data access
- Denial of service attacks
- Distribution of exploit results

### Liability

The **author and contributors** are **not responsible** for:
- Any misuse of this tool
- Damage caused to target systems
- Legal consequences of unauthorized scanning
- Data breaches or loss
- Third-party actions

**By using RaidScanner, you agree to:**
1. Use it only on authorized targets
2. Comply with all applicable laws
3. Take full responsibility for your actions
4. Respect privacy and security of others

---

## 📄 License

This project is licensed under the **MIT License** - see below for details:

```
MIT License

Copyright (c) 2025 Zahid Hasan Polash (zahidoverflow)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

- **OWASP** - For security research and vulnerability documentation
- **Selenium** - For browser automation capabilities
- **Flask** - For the excellent web framework
- **Docker** - For containerization technology
- **Security Community** - For continuous education and improvement

---

## 📧 Contact & Support

- **Author**: Zahid Hasan Polash (zahidoverflow)
- **GitHub**: [https://github.com/zahidoverflow/raidscanner](https://github.com/zahidoverflow/raidscanner)
- **Docker Hub**: [https://hub.docker.com/r/zahidoverflow/raidscanner](https://hub.docker.com/r/zahidoverflow/raidscanner)
- **Issues**: [GitHub Issues](https://github.com/zahidoverflow/raidscanner/issues)

---

## 🌟 Star This Project

If you find RaidScanner useful for your security testing or educational purposes, please consider giving it a ⭐ on GitHub!

---

<div align="center">

**Made with ❤️ for the Security Community**

</div>
