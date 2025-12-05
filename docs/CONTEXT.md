# 🛡️ RaidScanner - Complete Project Context for LLMs

## Project Overview

**RaidScanner** is a modern, production-ready automated vulnerability scanner designed for ethical hacking and security testing. It's a fully functional dual-interface (Web GUI + CLI) application that detects common web vulnerabilities through sophisticated scanning techniques.

### Project Identity
- **Name**: RaidScanner
- **Version**: 2.0
- **Type**: Web Vulnerability Scanner
- **License**: MIT
- **Author**: zahidoverflow
- **Docker Hub**: https://hub.docker.com/r/zahidoverflow/raidscanner
- **GitHub**: https://github.com/zahidoverflow/raidscanner
- **Status**: Production Ready ✅

### Core Purpose
RaidScanner automates the detection of common web application vulnerabilities through intelligent payload testing and response analysis. It's designed for security professionals, penetration testers, and ethical hackers who need a reliable, containerized scanning solution.

---

## 🎯 Supported Vulnerabilities

RaidScanner detects **5 major vulnerability classes**:

1. **LFI (Local File Inclusion)**
   - Detection Method: Request-based pattern matching
   - Success Criteria: Configurable file content patterns (e.g., "root:x:0:")
   - Payloads: ~1238 variations covering different path traversal techniques

2. **SQLi (SQL Injection)**
   - Detection Method: Time-based blind SQL injection
   - Technique: Measures response time delays to detect successful injections
   - Time Threshold: Default 10 seconds
   - Payload Support: Multiple databases (MySQL, PostgreSQL, MSSQL, Oracle, Generic)

3. **XSS (Cross-Site Scripting)**
   - Detection Method: Selenium-based browser automation
   - Capabilities: DOM-based and Reflected XSS detection
   - Alert Detection: Monitors JavaScript alert() execution
   - Source Checking: Analyzes page source for payload reflection
   - Resource Intensive: Uses headless Chrome (max 3 threads recommended)

4. **Open Redirect (OR)**
   - Detection Method: HTTP header and meta tag analysis
   - Checks: Location header redirects and meta refresh tags
   - Payload Validation: Ensures redirect target matches injected URL

5. **CRLF Injection**
   - Detection Method: HTTP response splitting detection
   - Technique: Injects CRLF sequences to test for header injection
   - Indicators: Custom headers appearing in responses

---

## 🏗️ Architecture

### Layered Design

```
┌─────────────────────────────────────────────┐
│        User Interface Layer                 │
│  ┌──────────────┐    ┌──────────────┐      │
│  │  Web GUI     │    │     CLI      │      │
│  │  (Flask)     │    │  (Rich TUI)  │      │
│  └──────────────┘    └──────────────┘      │
└─────────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────────┐
│      Web Application Layer (app.py)         │
│  • REST API Endpoints                       │
│  • WebSocket Events (Socket.IO)             │
│  • Background Thread Management             │
└─────────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────────┐
│         Core Logic Layer (core/)            │
│  ┌──────────────────────────────────────┐  │
│  │ scanner_engine.py                     │  │
│  │ - Platform-agnostic scanning logic    │  │
│  │ - All 5 vulnerability scanners        │  │
│  │ - Progress callback system            │  │
│  └──────────────────────────────────────┘  │
│  ┌──────────────────────────────────────┐  │
│  │ payload_loader.py                     │  │
│  │ - Payload file management             │  │
│  │ - Multi-format support                │  │
│  └──────────────────────────────────────┘  │
│  ┌──────────────────────────────────────┐  │
│  │ report_generator.py                   │  │
│  │ - HTML/JSON report generation         │  │
│  │ - TailwindCSS styled output           │  │
│  └──────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────────┐
│        Utility Layer (utils/)               │
│  • config.py - Configuration management     │
│  • platform_helper.py - OS compatibility    │
└─────────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────────┐
│          Network Layer                      │
│  • requests - HTTP scanning                 │
│  • aiohttp - Async operations               │
│  • Selenium + ChromeDriver - Browser tests  │
└─────────────────────────────────────────────┘
```

### Data Flow

1. **Input Stage**
   - User submits target URLs via Web GUI or CLI
   - Configuration validated (threads, payloads, criteria)

2. **Processing Stage**
   - Background thread spawns to execute scan
   - ScannerEngine initializes with selected scanner type
   - Multi-threaded payload testing begins
   - ThreadPoolExecutor manages concurrent requests

3. **Feedback Stage**
   - **Web**: Real-time WebSocket updates (`scan_progress` events)
   - **CLI**: Live console updates with Rich library
   - Progress data: current URL, scanned count, found vulnerabilities

4. **Output Stage**
   - Vulnerabilities collected in memory
   - ReportGenerator creates HTML/JSON reports
   - Reports saved to `reports/` with timestamps
   - Results displayed in UI

---

## 📁 Complete Project Structure

```
raidscanner/
├── .docker/                        # Docker configuration (isolated)
│   ├── Dockerfile                  # Container build definition
│   ├── compose.yml                 # Docker Compose V2 config
│   ├── .dockerignore               # Build exclusions
│   ├── output/                     # Volume mount for scan results
│   ├── reports/                    # Volume mount for reports
│   └── payloads/                   # Volume mount for payloads
│
├── .git/                           # Git version control
│
├── .github/                        # GitHub Actions workflows (empty)
│
├── bin/                            # Binary executables
│   └── chromedriver-linux64/       # ChromeDriver for Selenium
│       ├── chromedriver            # Linux ChromeDriver binary
│       └── LICENSE.chromedriver    # ChromeDriver license
│
├── core/                           # Core scanning logic (heart of the system)
│   ├── __init__.py                 # Package initializer
│   ├── scanner_engine.py           # Main scanning engine (542 lines)
│   │   └── Class: ScannerEngine
│   │       • scan_lfi() - LFI scanner
│   │       • scan_sqli() - SQLi scanner  
│   │       • scan_xss() - XSS scanner
│   │       • scan_or() - Open Redirect scanner
│   │       • scan_crlf() - CRLF scanner
│   │       • Progress callback system
│   ├── payload_loader.py           # Payload management (77 lines)
│   │   └── Class: PayloadLoader
│   │       • load_payloads() - Generic loader
│   │       • load_lfi_payloads()
│   │       • load_sqli_payloads()
│   │       • load_xss_payloads()
│   │       • load_or_payloads()
│   │       • list_available_payloads()
│   └── report_generator.py         # Report generation (129 lines)
│       └── Class: ReportGenerator
│           • generate_html_report()
│           • generate_json_report()
│           • save_report()
│           • generate_and_save()
│
├── docs/                           # Documentation
│   ├── CONTEXT.md                  # This file - Complete project context
│   ├── DEVELOPER_GUIDE.md          # Architecture & contribution guide
│   └── USER_GUIDE.md               # End-user documentation
│
├── output/                         # Scan results directory (auto-generated)
│   └── (Filtered URLs and raw scan data)
│
├── payloads/                       # Attack payloads library
│   ├── lfi-payloads.txt            # LFI payloads (1,238 bytes)
│   ├── lfi.txt                     # Extended LFI wordlist (5.6 MB)
│   ├── or.txt                      # Open Redirect payloads (7,485 bytes)
│   ├── xss.txt                     # XSS payloads (167 KB)
│   ├── xsspollygots.txt            # XSS polyglots (16 KB)
│   └── sqli/                       # SQL Injection payloads by database
│       ├── generic.txt             # Generic SQLi (1,047 bytes)
│       ├── mysql.txt               # MySQL specific (21 KB)
│       ├── postgresql.txt          # PostgreSQL (7.6 KB)
│       ├── oracle.txt              # Oracle (30 KB)
│       ├── mssql                   # Microsoft SQL Server (4.7 KB)
│       └── xor.txt                 # XOR-based SQLi (2.3 KB)
│
├── reports/                        # Generated reports (auto-generated)
│   └── (HTML and JSON vulnerability reports)
│
├── scripts/                        # Utility scripts
│   ├── start.sh                    # Interactive startup script
│   ├── docker-run.sh               # Run Docker (Linux/Mac)
│   ├── docker-run.bat              # Run Docker (Windows)
│   ├── docker-commands.sh          # Common Docker commands
│   ├── docker-pull.sh              # Pull from Docker Hub
│   └── test-docker-setup.sh        # Docker setup verification
│
├── utils/                          # Utility modules
│   ├── __init__.py                 # Package initializer
│   ├── config.py                   # Configuration management (70 lines)
│   │   └── Class: Config
│   │       • Path configurations
│   │       • Web app settings
│   │       • Scanning parameters
│   │       • Chrome/Selenium options
│   └── platform_helper.py          # Cross-platform compatibility (2.5 KB)
│       └── OS detection and helper functions
│
├── web/                            # Web interface
│   ├── templates/                  # HTML templates
│   │   └── (Flask Jinja2 templates)
│   └── static/                     # Frontend assets
│       └── js/                     # JavaScript files
│           └── (Socket.IO client logic)
│
├── app.py                          # Flask web application entry point (392 lines)
│   • Web routes (/, /scanner/<type>, /reports)
│   • REST API endpoints (5 scanners + reports + payloads)
│   • WebSocket events (Socket.IO)
│   • Error handlers
│
├── scanner_cli.py                  # CLI application entry point (379 lines)
│   • Interactive menu system
│   • All 5 scanner implementations
│   • Real-time progress display
│   • Report generation prompts
│
├── compose.yml                     # Symlink to .docker/compose.yml
│
├── requirements.txt                # Base Python dependencies (16 packages)
│   • webdriver_manager, selenium, aiohttp
│   • beautifulsoup4, colorama, rich
│   • Flask, flask-socketio, requests
│   • prompt_toolkit, pyyaml, eventlet
│
├── requirements-docker.txt         # Docker-specific dependencies with versions
│   • Pinned versions for reproducibility
│
├── requirements-lock.txt           # Locked dependencies with hashes
│
├── requirements-gui.txt            # GUI-specific dependencies
│
├── .gitignore                      # Git ignore rules
│
├── PROJECT_STATUS.md               # Implementation summary & status
│
└── README.md                       # Quick start guide
```

---

## 🔧 Technical Implementation

### Core Scanner Engine (`core/scanner_engine.py`)

#### LFI Scanner
```python
def scan_lfi(urls, payloads, success_criteria=None, threads=5)
```
- **Method**: HTTP request-based pattern matching
- **Process**:
  1. Inject LFI payload into URL parameters
  2. Send HTTP GET request
  3. Analyze response body for success criteria patterns
  4. Examples: "root:x:0:", "bin/bash", Windows registry keys
- **Threading**: Uses ThreadPoolExecutor with configurable workers
- **Callback**: Real-time progress updates via callback system

#### SQLi Scanner
```python
def scan_sqli(urls, payloads, threads=5, time_threshold=10)
```
- **Method**: Time-based blind SQL injection
- **Process**:
  1. Inject time-delay SQL payload (e.g., `SLEEP(10)`)
  2. Measure response time
  3. Compare against baseline and threshold
  4. Detect delays indicating successful injection
- **Time Threshold**: Default 10 seconds, configurable
- **Database Support**: Generic, MySQL, PostgreSQL, MSSQL, Oracle

#### XSS Scanner
```python
def scan_xss(urls, payloads, threads=3)
```
- **Method**: Selenium-based browser automation
- **Process**:
  1. Initialize headless Chrome via Selenium
  2. Inject XSS payload into URL
  3. Load page in browser
  4. Monitor for JavaScript alert() execution
  5. Check page source for payload reflection
- **Threading**: Limited to 3 threads (resource-intensive)
- **WebDriver**: ChromeDriver + Google Chrome
- **Headless Mode**: Xvfb virtual display in Docker

#### Open Redirect Scanner
```python
def scan_or(urls, payloads, threads=5)
```
- **Method**: HTTP header and meta tag analysis
- **Process**:
  1. Inject redirect URL payload
  2. Send request with `allow_redirects=False`
  3. Check `Location` header for payload
  4. Parse HTML for meta refresh tags
  5. Validate redirect target matches payload
- **Indicators**: 300-series status codes, Location header, meta refresh

#### CRLF Scanner
```python
def scan_crlf(urls, threads=5)
```
- **Method**: HTTP response splitting via CRLF injection
- **Process**:
  1. Inject CRLF sequences (`%0d%0a`, `\r\n`)
  2. Attempt to inject custom headers
  3. Analyze response headers for injected content
  4. Detect response splitting vulnerabilities
- **Payloads**: Hardcoded CRLF sequences (context-specific)

### Progress Callback System

All scanners support real-time progress updates:

```python
scanner = ScannerEngine()
scanner.add_progress_callback(lambda data: handle_progress(data))
results = scanner.scan_lfi(urls, payloads)
```

**Callback Data Structure**:
```python
{
    'current_url': 'http://example.com?id=1',
    'scanned': 45,
    'total': 100,
    'found': 3,
    'payload': '../../../etc/passwd',
    'status': 'testing'  # or 'vulnerable', 'safe'
}
```

### Report Generation

#### HTML Reports
- **Styling**: TailwindCSS via CDN
- **Design**: Dark theme with gradient accents
- **Sections**: 
  - Summary statistics (scan type, vulnerabilities, duration)
  - Vulnerable URLs list with clickable links
- **Filename Format**: `{scan_type}_report_YYYYMMDD_HHMMSS.html`

#### JSON Reports
- **Structure**: Hierarchical with metadata
- **Fields**: timestamp, scan_type, summary, vulnerable_urls, detailed_results
- **Use Case**: Programmatic processing, CI/CD integration

---

## 🐳 Docker Implementation

### Dockerfile Breakdown

**Base Image**: `python:3.11-slim`
- Minimal footprint (~50MB base)
- Debian-based for package availability

**System Dependencies**:
- Google Chrome (stable)
- ChromeDriver (auto-downloaded by webdriver_manager)
- Xvfb (X Virtual Framebuffer for headless Chrome)
- Required libraries: libnss3, libatk-bridge2.0-0, libgbm1, etc.

**Security**:
- Non-root user (`scanner` UID 1000)
- Minimal attack surface
- No unnecessary packages

**Optimization**:
- Layer caching for dependencies
- Single RUN commands to minimize layers
- Cleanup of apt cache and temporary files

**Entry Point**:
```bash
Xvfb :99 -screen 0 1920x1080x24 & 
sleep 1
if [ "$MODE" = "web" ]; then 
    python3 app.py
else 
    python3 scanner_cli.py
fi
```

### Docker Compose Services

#### CLI Service (`raidscanner-cli`)
```yaml
environment:
  - MODE=cli
  - DISPLAY=:99
stdin_open: true
tty: true
```
- Interactive terminal
- Runs `scanner_cli.py`

#### Web Service (`raidscanner-web`)
```yaml
environment:
  - MODE=web
ports:
  - "5000:5000"
```
- Runs `app.py`
- Exposes Flask on port 5000

#### Shared Configuration
- **Volumes**: `./output`, `./reports`, `./payloads:ro`
- **Shared Memory**: 2GB for Chrome
- **Resources**: Max 2 CPUs, 4GB RAM
- **Network**: Bridge network `raidscanner_net`

---

## 🌐 Web API Documentation

### REST Endpoints

#### 1. LFI Scan
```http
POST /api/scan/lfi
Content-Type: application/json

{
  "urls": ["http://example.com?file=test"],
  "threads": 5,
  "success_criteria": ["root:x:0:", "bin/bash"]
}
```

**Response**:
```json
{
  "status": "started",
  "message": "LFI scan started with 5 threads"
}
```

#### 2. SQLi Scan
```http
POST /api/scan/sqli
Content-Type: application/json

{
  "urls": ["http://example.com?id=1"],
  "threads": 5,
  "time_threshold": 10
}
```

#### 3. XSS Scan
```http
POST /api/scan/xss
Content-Type: application/json

{
  "urls": ["http://example.com?q=search"],
  "threads": 3
}
```

#### 4. Open Redirect Scan
```http
POST /api/scan/or
Content-Type: application/json

{
  "urls": ["http://example.com?url=https://redirect.com"],
  "threads": 5
}
```

#### 5. CRLF Scan
```http
POST /api/scan/crlf
Content-Type: application/json

{
  "urls": ["http://example.com?param=value"],
  "threads": 5
}
```

#### 6. List Reports
```http
GET /api/reports
```

**Response**:
```json
{
  "reports": [
    {
      "filename": "lfi_report_20241205_142030.html",
      "type": "html",
      "size": 15240,
      "created": "2024-12-05T14:20:30"
    }
  ]
}
```

#### 7. List Payloads
```http
GET /api/payloads
```

**Response**:
```json
{
  "payloads": {
    "root": ["lfi-payloads.txt", "or.txt", "xss.txt"],
    "sqli": ["generic.txt", "mysql.txt", "postgresql.txt"]
  }
}
```

### WebSocket Events (Socket.IO)

#### Client → Server
- `connect`: Client connected
- `ping`: Heartbeat check

#### Server → Client
- `scan_progress`: Real-time scan updates
  ```json
  {
    "type": "lfi",
    "current_url": "http://example.com",
    "scanned": 45,
    "total": 100,
    "found": 3,
    "vulnerable_urls": ["http://example.com?file=../../../etc/passwd"]
  }
  ```
- `scan_complete`: Scan finished
  ```json
  {
    "status": "complete",
    "total_found": 5,
    "duration": 120,
    "report_path": "reports/lfi_report_20241205_142030.html"
  }
  ```
- `scan_error`: Error occurred
  ```json
  {
    "error": "Failed to load payloads",
    "details": "File not found: payloads/custom.txt"
  }
  ```

---

## 💻 CLI Implementation

### Menu System
```
╔════════════════════════════════════════╗
║        RAIDSCANNER v2.0                ║
║   Advanced Vulnerability Scanner       ║
╚════════════════════════════════════════╝

[1] LFI Scanner
[2] SQL Injection Scanner
[3] XSS Scanner
[4] Open Redirect Scanner
[5] CRLF Injection Scanner
[6] Exit

Select option:
```

### Workflow
1. **Scanner Selection**: User chooses vulnerability type
2. **URL Input**: Single URL or file with URL list
3. **Payload Selection**: Choose payload file
4. **Thread Configuration**: Set concurrent threads (1-10)
5. **Scanning**: Real-time progress with Rich library
6. **Results**: Colorized output with vulnerability count
7. **Report Prompt**: Option to save HTML/JSON report

### Features
- **Rich TUI**: Progress bars, tables, panels
- **Colorama**: Cross-platform colored output
- **Prompt Toolkit**: Advanced input handling
- **Real-time Feedback**: Live payload testing updates

---

## 🔐 Security Considerations

### For Users
1. **Authorization Required**: Only scan systems you own or have explicit permission to test
2. **Legal Compliance**: Unauthorized scanning may be illegal in your jurisdiction
3. **Rate Limiting**: Use appropriate thread counts to avoid DoS
4. **Responsible Disclosure**: Report vulnerabilities to affected parties responsibly

### For Developers
1. **Input Validation**: All user inputs sanitized before processing
2. **CORS**: Configurable CORS origins (default: `*` for development)
3. **Rate Limiting**: Implement rate limiting for production deployments
4. **Secret Management**: Use environment variables for sensitive config
5. **Docker Security**: Non-root user, minimal base image, no unnecessary privileges

---

## 🚀 Usage Examples

### Docker Web GUI
```bash
# Start web interface
docker compose up -d raidscanner-web

# Access at http://localhost:5000
# Navigate to scanner type (LFI, SQLi, XSS, OR, CRLF)
# Enter target URLs and configure options
# Monitor real-time results
# Download reports from Reports page
```

### Docker CLI
```bash
# Run interactive CLI
docker compose run --rm raidscanner-cli

# Example session:
# 1. Select [1] LFI Scanner
# 2. Enter URL: http://testphp.vulnweb.com/artists.php?artist=1
# 3. Select payload: payloads/lfi-payloads.txt
# 4. Threads: 5
# 5. Watch real-time scanning
# 6. Save report: Y
```

### Python API (Local Development)
```python
from core.scanner_engine import ScannerEngine
from core.payload_loader import PayloadLoader
from core.report_generator import ReportGenerator

# Initialize components
scanner = ScannerEngine()
loader = PayloadLoader()
report_gen = ReportGenerator()

# Load payloads
lfi_payloads = loader.load_lfi_payloads()

# Configure scanner
urls = ["http://example.com?file=test"]
success_criteria = ["root:x:0:", "bin/bash"]

# Add progress callback
def progress_handler(data):
    print(f"Testing: {data['current_url']} - Found: {data['found']}")

scanner.add_progress_callback(progress_handler)

# Run scan
results = scanner.scan_lfi(
    urls=urls,
    payloads=lfi_payloads,
    success_criteria=success_criteria,
    threads=5
)

# Generate report
report_path = report_gen.generate_and_save('LFI', results, format='html')
print(f"Report saved: {report_path}")
```

---

## 📊 Performance Characteristics

### Threading
- **LFI**: 5 threads (default), up to 10
- **SQLi**: 5 threads (default), up to 10
- **XSS**: 3 threads (recommended max due to Selenium overhead)
- **OR**: 5 threads (default), up to 10
- **CRLF**: 5 threads (default), up to 10

### Resource Usage (Docker)
- **CPU**: 0.5-2.0 cores
- **Memory**: 1-4GB (depending on thread count and scanner type)
- **Disk**: Minimal (reports and logs only)
- **Network**: Outbound HTTP/HTTPS only

### Scan Duration (Estimated)
- **100 URLs, 100 payloads, 5 threads**:
  - LFI: ~5-10 minutes
  - SQLi: ~30-60 minutes (time-based delays)
  - XSS: ~15-30 minutes (browser automation)
  - OR: ~5-10 minutes
  - CRLF: ~5-10 minutes

---

## 🛠️ Development Guide

### Local Development Setup
```bash
# Clone repository
git clone https://github.com/zahidoverflow/raidscanner.git
cd raidscanner

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run CLI
python scanner_cli.py

# Run Web GUI
python app.py
```

### Adding a New Scanner

1. **Update `core/scanner_engine.py`**:
```python
def scan_new_vuln(self, urls, payloads, threads=5):
    """New vulnerability scanner"""
    # Implementation here
    pass
```

2. **Add Payload Loader in `core/payload_loader.py`**:
```python
def load_new_vuln_payloads(self):
    return self.load_payloads('new_vuln.txt')
```

3. **Create API Endpoint in `app.py`**:
```python
@app.route('/api/scan/new_vuln', methods=['POST'])
def scan_new_vuln():
    # Implementation here
    pass
```

4. **Add CLI Option in `scanner_cli.py`**:
```python
def run_new_vuln_scanner():
    # Implementation here
    pass
```

5. **Add Payload File**: `payloads/new_vuln.txt`

6. **Update Documentation**: Add to README, USER_GUIDE, DEVELOPER_GUIDE

### Testing
```bash
# Test Docker build
docker compose build

# Test CLI
docker compose run --rm raidscanner-cli

# Test Web
docker compose up -d raidscanner-web
curl http://localhost:5000/api/payloads

# Stop services
docker compose down
```

### Publishing to Docker Hub
```bash
# Build and tag
docker compose build
docker tag raidscanner:latest zahidoverflow/raidscanner:v2.0
docker tag raidscanner:latest zahidoverflow/raidscanner:latest

# Push
docker push zahidoverflow/raidscanner:v2.0
docker push zahidoverflow/raidscanner:latest
```

---

## 📦 Dependencies

### Core Python Packages
- **Flask 3.0.3**: Web framework
- **flask-socketio 5.3.6**: WebSocket support
- **flask-cors 4.0.1**: CORS handling
- **requests**: HTTP library
- **aiohttp**: Async HTTP client
- **selenium**: Browser automation
- **webdriver_manager**: ChromeDriver management
- **beautifulsoup4**: HTML parsing
- **colorama**: Terminal colors
- **rich**: Advanced terminal UI
- **prompt_toolkit**: Interactive CLI
- **pyyaml**: YAML configuration
- **eventlet 0.36.1**: Async networking
- **GitPython**: Git operations

### System Dependencies (Docker)
- **Google Chrome**: Headless browser
- **ChromeDriver**: Selenium driver
- **Xvfb**: Virtual display server
- **Python 3.11**: Runtime

---

## 🔄 Version History

### v2.0 (Current - Production Ready)
- ✅ Complete modular architecture
- ✅ All 5 scanners fully implemented
- ✅ Dual interface (Web + CLI)
- ✅ Docker containerization
- ✅ Comprehensive documentation
- ✅ Progress callback system
- ✅ HTML/JSON report generation
- ✅ WebSocket real-time updates

### v1.0 (Legacy)
- Monolithic `main.py` (110KB)
- CLI-only interface
- Limited documentation

### Migration Notes
- `main.py` is deprecated but retained for reference
- All functionality ported to `scanner_cli.py` and `core/` modules
- Docker uses new modular architecture

---

## 🚧 Known Limitations

1. **XSS Scanner Performance**
   - Resource-intensive due to Selenium
   - Recommendation: Max 3 threads
   - Improvement: Add regex-based pre-filtering

2. **CRLF Payload Hardcoding**
   - Payloads built-in to scanner
   - Reason: Context-specific nature of CRLF
   - Impact: Minimal (comprehensive payloads included)

3. **Authentication**
   - No built-in authentication for Web GUI
   - Recommendation: Deploy behind reverse proxy with auth

4. **Distributed Scanning**
   - Single-instance only
   - Future: Consider adding queue-based distributed scanning

5. **Database Support**
   - No persistent storage for scan history
   - Current: File-based reports
   - Future: Optional database backend

---

## 🎯 Future Enhancements

### Planned Features
1. **Additional Scanners**
   - XXE (XML External Entity)
   - SSRF (Server-Side Request Forgery)
   - IDOR (Insecure Direct Object Reference)
   - Command Injection

2. **Authentication & Authorization**
   - Multi-user support
   - Role-based access control
   - API key authentication

3. **Database Integration**
   - Scan history storage
   - Trend analysis
   - Recurring scans

4. **Advanced Reporting**
   - PDF export
   - Email notifications
   - Slack/Discord webhooks

5. **Performance Optimization**
   - Async scanning with asyncio
   - Distributed architecture
   - Caching layer

6. **Integration**
   - CI/CD pipeline support
   - REST API clients (Python, JavaScript)
   - Burp Suite plugin

---

## 📝 Configuration Reference

### Environment Variables

#### Web Application
- `HOST`: Bind address (default: `0.0.0.0`)
- `PORT`: Port number (default: `5000`)
- `DEBUG`: Debug mode (default: `False`)
- `SECRET_KEY`: Flask secret key
- `MODE`: Runtime mode (`web` or `cli`)

#### CORS
- `CORS_ORIGINS`: Allowed origins (default: `*`)

#### Scanning
- `DEFAULT_THREADS`: Default thread count (5)
- `MAX_THREADS`: Maximum threads (10)
- `DEFAULT_TIMEOUT`: Request timeout (10s)
- `MAX_TIMEOUT`: Maximum timeout (60s)

#### Display (Docker)
- `DISPLAY`: X11 display (default: `:99`)
- `PYTHONUNBUFFERED`: Unbuffered output (default: `1`)
- `PYTHONDONTWRITEBYTECODE`: Disable bytecode (default: `1`)

### Configuration Files

#### `utils/config.py`
- Central configuration class
- Path management
- Chrome options
- Default values

#### `compose.yml`
- Docker service definitions
- Volume mounts
- Resource limits
- Network configuration

---

## 🧪 Testing Targets

### Safe Testing Environments
1. **DVWA (Damn Vulnerable Web Application)**
   - URL: http://dvwa.co.uk
   - Docker: `docker run -d -p 80:80 vulnerables/web-dvwa`

2. **OWASP WebGoat**
   - URL: https://owasp.org/www-project-webgoat/
   - Docker: `docker run -p 8080:8080 webgoat/goatandwolf`

3. **TestPHP Vulnweb**
   - URL: http://testphp.vulnweb.com
   - Public testing site

4. **BugBounty Platforms** (with authorization)
   - HackerOne
   - Bugcrowd
   - Intigriti

### Never Test On
- ❌ Production systems without authorization
- ❌ Third-party websites without permission
- ❌ Educational institution networks
- ❌ Government or military systems

---

## 📖 Additional Resources

### Documentation Files
- `README.md`: Quick start guide
- `docs/USER_GUIDE.md`: End-user guide
- `docs/DEVELOPER_GUIDE.md`: Developer architecture guide
- `PROJECT_STATUS.md`: Implementation status and summary

### External Resources
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [HackTricks](https://book.hacktricks.xyz/)
- [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)

---

## ⚠️ Legal Disclaimer

**RaidScanner is designed for educational and authorized security testing purposes only.**

### Terms of Use
1. You must have explicit written permission to scan any target system
2. Unauthorized scanning may violate:
   - Computer Fraud and Abuse Act (CFAA) in the USA
   - Computer Misuse Act in the UK
   - Similar laws in other jurisdictions
3. The author(s) and contributors are not responsible for any misuse
4. By using this tool, you agree to:
   - Only scan systems you own or have authorization to test
   - Comply with all applicable laws and regulations
   - Use the tool responsibly and ethically

### Ethical Hacking Guidelines
- **Always obtain proper authorization** before testing
- **Respect scope limitations** defined by the client
- **Handle discovered vulnerabilities responsibly**
- **Follow responsible disclosure practices**
- **Document all testing activities**

---

## 🤝 Contributing

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit (`git commit -m 'Add amazing feature'`)
6. Push (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Contribution Guidelines
- Follow PEP 8 style guide
- Add docstrings to all functions/classes
- Update documentation for new features
- Test Docker builds before submitting
- Include examples in PR description

### Bug Reports
- Use GitHub Issues
- Provide detailed reproduction steps
- Include system information
- Attach logs if applicable

---

## 📧 Contact & Support

- **Author**: zahidoverflow
- **GitHub**: https://github.com/zahidoverflow/raidscanner
- **Docker Hub**: https://hub.docker.com/r/zahidoverflow/raidscanner
- **Issues**: https://github.com/zahidoverflow/raidscanner/issues

---

## 📜 License

**MIT License**

Copyright (c) 2024 zahidoverflow

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## ✅ Project Status: PRODUCTION READY

**RaidScanner v2.0 is fully functional and ready for production use.**

All components are tested and operational:
- ✅ Complete scanner implementations (LFI, SQLi, XSS, OR, CRLF)
- ✅ Full API coverage (REST + WebSocket)
- ✅ Working CLI and Web interfaces
- ✅ No dependency conflicts
- ✅ Proper modular architecture
- ✅ Comprehensive documentation
- ✅ Docker containerization
- ✅ Production-grade security practices

**Last Updated**: December 5, 2024
**Version**: 2.0
**Status**: Active Development & Maintenance

---

*This CONTEXT.md file provides comprehensive project information for AI assistants, LLMs, and human developers. It covers all aspects of RaidScanner to enable complete understanding and effective collaboration.*
