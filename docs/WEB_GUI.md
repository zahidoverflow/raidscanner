# RaidScanner Web GUI

## Overview

RaidScanner now features a modern, cross-platform web-based GUI built with Flask, TailwindCSS, and Socket.IO for real-time vulnerability scanning.

## Features

### 🎨 Modern UI
- **TailwindCSS Design**: Beautiful, responsive interface
- **Real-time Updates**: Live scan progress via WebSocket
- **Dark Theme**: Easy on the eyes for security professionals
- **Interactive Cards**: Visual scanner selection

### 🔍 Available Scanners
- ✅ **LFI Scanner** - Local File Inclusion detection
- ✅ **SQLi Scanner** - Time-based SQL Injection detection
- ⏳ **XSS Scanner** - Cross-Site Scripting (Coming Soon)
- ⏳ **OR Scanner** - Open Redirect (Coming Soon)
- ⏳ **CRLF Scanner** - HTTP Header Injection (Coming Soon)

### 📊 Scan Features
- Multiple URL scanning
- Adjustable thread count (1-10)
- Real-time progress tracking
- Live vulnerability reporting
- Automatic report generation
- Report history viewer
- HTML & JSON export formats

## Quick Start

### Option 1: Docker (Recommended)

```bash
# Run web interface in background
docker compose up -d raidscanner-web

# Or run both CLI and Web
docker compose up -d

# View logs
docker compose logs -f raidscanner-web
```

Access the web interface at: **http://localhost:5000**

### Option 2: Docker Hub Image

```bash
# Pull and run
docker pull zahidoverflow/raidscanner:latest
docker run -d -p 5000:5000 \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/reports:/app/reports \
  --shm-size=2g \
  --name raidscanner-web \
  zahidoverflow/raidscanner:latest
```

### Option 3: Direct Python Execution (Advanced - Not Recommended)

⚠️ **Note**: This requires manual installation of all dependencies on your host machine. Use Docker (Option 1) for easier setup.

```bash
# Install dependencies (requires Chrome and ChromeDriver installed)
pip install -r requirements.txt

# Start web server
python app.py
```

### Option 3: Using Start Script (Inside Container)

```bash
# This script runs inside the Docker container
docker exec -it raidscanner-web bash
./scripts/start.sh
# Select option 1 for Web Interface
```

## Usage Guide

### 1. Select a Scanner
Click on any available scanner card from the dashboard:
- **LFI Scanner** (Cyan)
- **SQLi Scanner** (Red)
- More scanners coming soon

### 2. Configure Scan
- **Enter URLs**: One URL per line
- **Adjust Threads**: Use slider (1-10 concurrent requests)
- Click **Start Scan**

### 3. Monitor Progress
- Real-time progress bar
- Live vulnerability notifications
- Current URL being scanned
- Statistics: Scanned count & Found count

### 4. View Results
- Vulnerabilities displayed immediately as found
- Complete summary after scan
- Download reports (HTML/JSON)

### 5. Access Reports
- Click **Reports** card on dashboard
- Filter by scanner type or date
- Search reports by keywords
- Download in HTML or JSON format

## API Endpoints

### Scan Endpoints
```
POST /api/scan/lfi
POST /api/scan/sqli
POST /api/scan/xss    (Coming Soon)
POST /api/scan/or     (Coming Soon)
POST /api/scan/crlf   (Coming Soon)
```

**Request Body:**
```json
{
  "urls": ["https://example.com", "https://test.com"],
  "threads": 5
}
```

### Report Endpoints
```
GET  /api/reports              - List all reports
GET  /api/reports/download     - Download specific report
GET  /api/payloads             - List available payloads
```

### WebSocket Events
```
connect          - Client connected
disconnect       - Client disconnected
scan_progress    - Real-time scan updates
scan_complete    - Scan finished
scan_error       - Error occurred
```

## Architecture

### Backend (Flask)
- **app.py**: Main application entry
- **core/scanner_engine.py**: Platform-agnostic scanning logic
- **core/report_generator.py**: HTML/JSON report generation
- **core/payload_loader.py**: Payload file management
- **utils/config.py**: Configuration management
- **utils/platform_helper.py**: Cross-platform compatibility

### Frontend
- **web/templates/index.html**: Main dashboard
- **web/templates/reports.html**: Report viewer
- **web/static/js/main.js**: Real-time WebSocket client
- **TailwindCSS**: Styling via CDN
- **Socket.IO**: Real-time communication
- **Font Awesome**: Icon library

## Configuration

Edit `utils/config.py` to customize:

```python
# Web Server
HOST = '0.0.0.0'
PORT = 5000
DEBUG = False

# Directories
OUTPUT_DIR = 'output'
REPORTS_DIR = 'reports'
PAYLOADS_DIR = 'payloads'

# Security
SECRET_KEY = 'your-secret-key-here'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
```

## Docker Deployment

### Build Custom Image
```bash
docker build -t yourusername/raidscanner:latest .
```

### Run Web Interface
```bash
docker run -d \
  -p 5000:5000 \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/reports:/app/reports \
  -e MODE=web \
  --name raidscanner-web \
  zahidoverflow/raidscanner:latest
```

### Run CLI Interface
```bash
docker run -it \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/reports:/app/reports \
  -e MODE=cli \
  --name raidscanner-cli \
  zahidoverflow/raidscanner:latest
```

## Development

### Project Structure
```
raidscanner/
├── app.py                  # Flask application
├── main.py                 # CLI application
├── core/
│   ├── scanner_engine.py   # Scanning logic
│   ├── report_generator.py # Report creation
│   └── payload_loader.py   # Payload management
├── utils/
│   ├── config.py           # Configuration
│   └── platform_helper.py  # Platform utilities
├── web/
│   ├── templates/
│   │   ├── index.html      # Dashboard
│   │   └── reports.html    # Report viewer
│   └── static/
│       └── js/
│           └── main.js     # Frontend logic
├── payloads/               # Attack payloads
├── output/                 # Scan results
└── reports/                # Generated reports
```

### Adding New Scanners

1. **Backend**: Add scan method in `core/scanner_engine.py`
2. **API Route**: Add endpoint in `app.py`
3. **Frontend**: Update `web/templates/index.html` scanner card
4. **JavaScript**: Handle new scanner type in `main.js`

Example:
```python
# In core/scanner_engine.py
def scan_xss(self, urls, payloads, threads=5):
    results = []
    # Implementation
    return results

# In app.py
@app.route('/api/scan/xss', methods=['POST'])
def scan_xss():
    # Handle request
    pass
```

## Browser Compatibility

Tested and working on:
- ✅ Chrome/Chromium
- ✅ Firefox
- ✅ Edge
- ✅ Safari
- ✅ Opera

Requires modern browser with:
- WebSocket support
- JavaScript enabled
- CSS Grid/Flexbox support

## Security Considerations

### For Authorized Testing Only
⚠️ **IMPORTANT**: Only use RaidScanner on systems you own or have explicit permission to test.

### Security Features
- Non-root user in Docker
- Input validation
- CORS configuration
- Rate limiting (recommended in production)
- HTTPS support (configure reverse proxy)

### Production Deployment

**Use a reverse proxy (Nginx/Apache) with HTTPS:**

```nginx
server {
    listen 443 ssl;
    server_name scanner.yourdomain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

## Troubleshooting

### Web Interface Won't Start
```bash
# Check if port 5000 is in use
netstat -tulpn | grep 5000

# Use different port
export PORT=8080
python app.py
```

### Can't Connect to WebSocket
- Ensure firewall allows port 5000
- Check CORS configuration
- Verify browser console for errors

### Chrome/Selenium Issues
```bash
# In Docker, check Xvfb is running
docker exec raidscanner-web ps aux | grep Xvfb

# Verify Chrome version matches ChromeDriver
docker exec raidscanner-web google-chrome --version
```

### Reports Not Generating
```bash
# Check directory permissions
ls -la output/ reports/

# Create directories if missing
mkdir -p output reports
chmod 777 output reports
```

## Performance Tuning

### Optimize for Speed
- Increase thread count (max: 10)
- Use fast network connection
- Run in Docker for better isolation
- Use SSD for reports storage

### Optimize for Accuracy
- Decrease thread count (recommended: 5)
- Adjust timeout values in config
- Use smaller payload lists for targeted testing

## Roadmap

### Phase 1: ✅ Core Web Interface
- [x] Flask application setup
- [x] Real-time WebSocket integration
- [x] LFI Scanner implementation
- [x] SQLi Scanner implementation
- [x] Modern UI with TailwindCSS

### Phase 2: ⏳ Additional Scanners
- [ ] XSS Scanner (with Selenium)
- [ ] Open Redirect Scanner
- [ ] CRLF Injection Scanner

### Phase 3: 📋 Enhanced Features
- [ ] User authentication
- [ ] Scan scheduling
- [ ] Team collaboration
- [ ] Custom payload management
- [ ] Advanced filtering
- [ ] Export to PDF/CSV

### Phase 4: 🚀 Advanced Features
- [ ] API rate limiting
- [ ] Webhook notifications
- [ ] Integration with CI/CD
- [ ] Plugin system
- [ ] Machine learning detection

## Support

### Resources
- **GitHub**: https://github.com/zahidoverflow/raidscanner
- **Docker Hub**: https://hub.docker.com/r/zahidoverflow/raidscanner
- **Documentation**: See README.md, DOCKER.md

### Common Issues
See [Troubleshooting](#troubleshooting) section above.

### Contributing
Contributions welcome! Please:
1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Submit pull request

## License

RaidScanner is provided for educational and authorized security testing purposes only.

---

**Built with ❤️ by zahidoverflow**
