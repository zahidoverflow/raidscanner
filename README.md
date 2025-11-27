# 🛡️ RaidScanner

[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-zahidoverflow%2Fraidscanner-blue?logo=docker)](https://hub.docker.com/r/zahidoverflow/raidscanner)
[![Docker Image Size](https://img.shields.io/docker/image-size/zahidoverflow/raidscanner/latest)](https://hub.docker.com/r/zahidoverflow/raidscanner)
[![Docker Pulls](https://img.shields.io/docker/pulls/zahidoverflow/raidscanner)](https://hub.docker.com/r/zahidoverflow/raidscanner)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern, automated vulnerability scanner designed for ethical hacking and security testing. RaidScanner detects common web vulnerabilities including Local File Inclusion (LFI), SQL Injection (SQLi), Cross-Site Scripting (XSS), Open Redirect (OR), and CRLF Injection.

## ✨ Features

- 🌐 **Dual Interface**: Modern web GUI + traditional CLI
- 🚀 **Real-time Updates**: Live scan progress via WebSocket
- 🎯 **Multiple Scanners**: LFI, SQLi, XSS, OR, CRLF detection
- ⚡ **Multi-threaded**: High-performance concurrent scanning
- 📊 **Rich Reports**: HTML and JSON export formats
- 🐳 **Docker Ready**: Pre-built images on Docker Hub
- 🎨 **Modern UI**: TailwindCSS-based responsive design
- 🔧 **Customizable**: Adjustable payloads and success criteria

## 🚀 Quick Start

### Prerequisites

- Docker Engine 20.10+
- Docker Compose V2 (2.0+)

### Installation & Usage

**1. Pull and run the pre-built image (fastest):**

```bash
# Web GUI Mode (Recommended)
docker run -d -p 5000:5000 \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/reports:/app/reports \
  --shm-size=2g \
  --name raidscanner-web \
  zahidoverflow/raidscanner:latest

# Access at: http://localhost:5000
```

```bash
# CLI Mode
docker run -it --rm \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/reports:/app/reports \
  --shm-size=2g \
  zahidoverflow/raidscanner:latest
```

**2. Or clone and use Docker Compose:**

```bash
git clone https://github.com/zahidoverflow/raidscanner.git
cd raidscanner

# Start Web GUI
docker compose up -d raidscanner-web

# Access at: http://localhost:5000
```

That's it! No manual dependency installation required. 🎉

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [🚀 Quick Start Guide](docs/QUICKSTART.md) | Get started in 5 minutes |
| [🌐 Web GUI Guide](docs/WEB_GUI.md) | Web interface documentation |
| [🐳 Docker Guide](docs/DOCKER.md) | Complete Docker reference |
| [🏗️ Architecture](docs/ARCHITECTURE.md) | System design and components |

## 🎯 Usage Examples

### Web GUI Mode

1. **Start the web interface:**
   ```bash
   docker compose up -d raidscanner-web
   ```

2. **Open your browser:** http://localhost:5000

3. **Select a scanner** (LFI or SQLi)

4. **Enter target URLs** (one per line)

5. **Adjust threads** (1-10) and click **Start Scan**

6. **Monitor real-time results** and download reports

### CLI Mode

```bash
# Interactive CLI
docker compose run --rm raidscanner-cli

# Or direct run
docker run -it --rm \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/reports:/app/reports \
  --shm-size=2g \
  zahidoverflow/raidscanner:latest
```

Follow the interactive menu to select scanner type, provide URLs, and configure options.

## 🔍 Supported Scanners

| Scanner | Status | Detection Method | Use Case |
|---------|--------|------------------|----------|
| **LFI** | ✅ Ready | Pattern matching | Detect Local File Inclusion |
| **SQLi** | ✅ Ready | Time-based blind | SQL Injection detection |
| **XSS** | ⏳ Coming Soon | Selenium automation | Cross-Site Scripting |
| **OR** | ⏳ Coming Soon | Redirect detection | Open Redirect |
| **CRLF** | ⏳ Coming Soon | Header injection | HTTP Header Injection |

## 📊 Output & Reports

RaidScanner generates comprehensive reports in multiple formats:

- **HTML Reports**: Visual, styled reports with vulnerability details
- **JSON Export**: Machine-readable format for automation
- **Console Output**: Real-time colored terminal output
- **File Output**: Saved vulnerable URLs for further analysis

Reports are saved to:
- `./reports/` - HTML and JSON reports
- `./output/` - Filtered vulnerable URLs

## 🛠️ Configuration

### Docker Compose Commands

```bash
# Start services
docker compose up -d raidscanner-web       # Web GUI (background)
docker compose up raidscanner-cli          # CLI (interactive)

# View logs
docker compose logs -f raidscanner-web

# Stop services
docker compose down

# Rebuild after changes
docker compose build --no-cache

# Pull latest image
docker compose pull
```

### Environment Variables

```bash
# Set mode (web or cli)
docker run -e MODE=web zahidoverflow/raidscanner:latest

# Adjust shared memory (for Chrome/Selenium)
docker run --shm-size=4g zahidoverflow/raidscanner:latest
```

### Custom Payloads

```bash
# Mount custom payloads directory
docker run -it \
  -v $(pwd)/custom-payloads:/app/payloads:ro \
  zahidoverflow/raidscanner:latest
```

## 🏗️ Architecture

```
raidscanner/
├── core/                 # Scanning engines
│   ├── scanner_engine.py
│   ├── report_generator.py
│   └── payload_loader.py
├── web/                  # Web interface
│   ├── templates/
│   └── static/
├── payloads/             # Attack payloads
├── scripts/              # Helper scripts
├── .docker/              # Docker configuration
└── docs/                 # Documentation
```

**Technologies:**
- Python 3.11+
- Flask 3.0 + Socket.IO (Web)
- Selenium + ChromeDriver (Browser automation)
- TailwindCSS (UI)
- Docker (Containerization)

## 📦 Installation Methods

### Method 1: Docker Hub (Recommended)

```bash
# Pull latest
docker pull zahidoverflow/raidscanner:latest

# Or specific version
docker pull zahidoverflow/raidscanner:v2.0-web
```

**Benefits:**
- ✅ No build time
- ✅ Pre-configured environment
- ✅ Works on Windows, Mac, Linux
- ✅ Isolated dependencies

### Method 2: Docker Compose (Development)

```bash
git clone https://github.com/zahidoverflow/raidscanner.git
cd raidscanner
docker compose build
docker compose up
```

### Method 3: Manual Installation (Not Recommended)

⚠️ **Warning**: Manual installation requires Chrome, ChromeDriver, and Python dependencies on your host. Use Docker for easier setup.

<details>
<summary>Click to expand manual installation steps</summary>

```bash
# Clone repository
git clone https://github.com/zahidoverflow/raidscanner.git
cd raidscanner

# Install Python dependencies
pip install -r requirements.txt

# Install Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb

# Install ChromeDriver
wget https://storage.googleapis.com/chrome-for-testing-public/128.0.6613.119/linux64/chromedriver-linux64.zip
unzip chromedriver-linux64.zip
sudo mv chromedriver-linux64/chromedriver /usr/bin/

# Run CLI
python main.py

# Or run Web GUI
python app.py
```
</details>

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Change port in .docker/compose.yml
ports:
  - "8080:5000"  # Change 5000 to 8080
```

### Chrome/Selenium Errors
```bash
# Increase shared memory
docker compose up -d --shm-size=4g
```

### Permission Issues
```bash
# Fix output directory permissions
mkdir -p output reports
chmod 777 output reports
```

### Container Won't Start
```bash
# Check logs
docker compose logs -f raidscanner-web

# Restart services
docker compose restart
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**IMPORTANT**: This tool is for educational and authorized security testing purposes only.

- ✅ Only scan systems you **own** or have **explicit written permission** to test
- ❌ Unauthorized scanning of third-party systems is **illegal**
- ⚖️ Users are responsible for complying with all applicable laws

The developers assume no liability for misuse or damage caused by this software.

## 🔗 Links

- **GitHub Repository**: https://github.com/zahidoverflow/raidscanner
- **Docker Hub**: https://hub.docker.com/r/zahidoverflow/raidscanner
- **Issues**: https://github.com/zahidoverflow/raidscanner/issues
- **Documentation**: [docs/](docs/)

## 📧 Contact

For questions, suggestions, or security concerns, please open an issue on GitHub.

---

**Built with ❤️ for the security community**

*Happy Ethical Hacking! 🔍🛡️*
