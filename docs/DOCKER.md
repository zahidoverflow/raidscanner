# RaidScanner Docker Guide

## Quick Start

### Prerequisites
- Docker Engine 20.10 or higher
- Docker Compose 2.0 or higher

### Build and Run

**Option 1: Using docker-compose (Recommended)**
```bash
# Build the image
docker-compose build

# Run the scanner interactively
docker-compose run --rm raidscanner
```

**Option 2: Using the run script**
```bash
chmod +x docker-run.sh
./docker-run.sh
```

**Option 3: Using Docker directly**
```bash
# Build the image
docker build -t raidscanner:latest .

# Run the container
docker run -it --rm \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/reports:/app/reports \
  --shm-size=2g \
  raidscanner:latest
```

---

## Volume Mounts

The Docker setup includes these mounted directories:

- `./output` - Stores filtered URLs from the scanner
- `./reports` - Stores HTML vulnerability reports
- `./payloads` - Contains payload files (read-only)

---

## Features

✅ **Fully Isolated Environment** - All dependencies bundled
✅ **Chrome & ChromeDriver** - Pre-configured for XSS/OR scanning
✅ **Xvfb Display Server** - Headless browser support
✅ **Persistent Results** - Reports saved to host machine
✅ **Easy Portability** - Run anywhere Docker is installed

---

## Advanced Usage

### Run with Custom Payloads
```bash
docker-compose run --rm \
  -v $(pwd)/custom-payloads:/app/custom-payloads:ro \
  raidscanner
```

### Access Container Shell
```bash
docker-compose run --rm --entrypoint /bin/bash raidscanner
```

### Run filter.sh Script
```bash
docker-compose run --rm --entrypoint /bin/bash raidscanner -c "./filter.sh"
```

### Clean Up
```bash
# Remove containers
docker-compose down

# Remove image
docker rmi raidscanner:latest

# Remove volumes (caution: deletes results)
docker volume prune
```

---

## Troubleshooting

### Chrome/Selenium Issues
If you encounter Chrome errors, increase shared memory:
```yaml
# In docker-compose.yml
shm_size: '4gb'
```

### Permission Issues
If output files have wrong permissions:
```bash
sudo chown -R $USER:$USER output/ reports/
```

### Network Issues
If scanning external sites fails, check your network:
```bash
docker-compose run --rm raidscanner ping -c 3 google.com
```

---

## Environment Variables

You can customize the environment in `docker-compose.yml`:

```yaml
environment:
  - DISPLAY=:99
  - PYTHONUNBUFFERED=1
  # Add custom variables here
```

---

## Security Notes

⚠️ **Important:** 
- Only use this tool on systems you own or have permission to test
- The container runs with default privileges
- Network access is required for external scanning
- Be mindful of data stored in mounted volumes

---

## Building for Production

For a smaller production image:

```dockerfile
# Use multi-stage build
FROM python:3.11-slim AS builder
# ... build steps ...

FROM python:3.11-slim
COPY --from=builder /app /app
```

---

## Support

For issues related to:
- **Docker setup**: Check Docker logs with `docker-compose logs`
- **Scanner functionality**: Review main application logs
- **Chrome/Selenium**: Ensure adequate memory allocation

---

## System Requirements

**Minimum:**
- 2GB RAM
- 2GB free disk space
- 2 CPU cores

**Recommended:**
- 4GB RAM
- 5GB free disk space
- 4 CPU cores

# 🐳 RaidScanner - Docker Setup Summary

## What Was Added

Your RaidScanner project is now fully Dockerized! Here's what was created:

### Core Docker Files

1. **`Dockerfile`**
   - Base image: Python 3.11 slim
   - Includes Google Chrome & ChromeDriver
   - Xvfb display server for headless browser
   - All Python dependencies pre-installed
   - Working directory: `/app`

2. **`docker-compose.yml`**
   - Service configuration for RaidScanner
   - Volume mounts for output, reports, and payloads
   - Network configuration
   - Shared memory allocation (2GB) for Chrome

3. **`.dockerignore`**
   - Excludes unnecessary files from Docker build
   - Reduces image size
   - Speeds up build process

### Helper Scripts

4. **`docker-run.sh`** (Linux/Mac)
   - Simple build and run script
   - One-command execution

5. **`docker-run.bat`** (Windows)
   - Windows equivalent of docker-run.sh
   - Double-click to run

6. **`docker-commands.sh`**
   - Utility script with common Docker operations
   - Commands: build, run, shell, filter, clean, logs, update

### Documentation

7. **`DOCKER.md`**
   - Complete Docker usage guide
   - Troubleshooting section
   - Advanced usage examples
   - System requirements

8. **`.gitignore`**
   - Prevents committing temporary files
   - Excludes output and reports directories
   - Standard Python gitignore patterns

9. **Updated `README.md`**
   - Added Docker installation as Option 1 (recommended)
   - Quick start guide
   - Links to detailed documentation

---

## 🚀 Quick Start

### For Linux/Mac:
```bash
chmod +x docker-run.sh
./docker-run.sh
```

### For Windows:
```cmd
docker-run.bat
```

### Manual:
```bash
docker-compose build
docker-compose run --rm raidscanner
```

---

## ✨ Benefits

✅ **No Manual Setup** - Everything is pre-configured
✅ **Portable** - Run on any system with Docker
✅ **Isolated** - No conflicts with system packages
✅ **Consistent** - Same environment everywhere
✅ **Easy Sharing** - Share the image with team members
✅ **Quick Deployment** - Deploy to cloud platforms easily

---

## 📂 Directory Structure

```
raidscanner/
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Container orchestration
├── .dockerignore          # Build exclusions
├── docker-run.sh          # Linux/Mac run script
├── docker-run.bat         # Windows run script
├── docker-commands.sh     # Utility commands
├── DOCKER.md              # Full Docker documentation
├── .gitignore             # Git exclusions
├── main.py                # Main application
├── requirements.txt       # Python dependencies
├── filter.sh              # URL filtering script
├── payloads/              # Attack payloads
│   ├── lfi-payloads.txt
│   ├── xss.txt
│   └── sqli/
├── output/                # Scan results (mounted)
└── reports/               # HTML reports (mounted)
```

---

## 🔧 Common Commands

### Build the image:
```bash
docker-compose build
```

### Run the scanner:
```bash
docker-compose run --rm raidscanner
```

### Access container shell:
```bash
docker-compose run --rm --entrypoint /bin/bash raidscanner
```

### Run filter script:
```bash
docker-compose run --rm --entrypoint /bin/bash raidscanner -c "./filter.sh"
```

### Clean up:
```bash
docker-compose down
docker system prune -f
```

### View logs:
```bash
docker-compose logs -f
```

---

## 🎯 Next Steps

1. **Test the setup:**
   ```bash
   docker-compose build
   docker-compose run --rm raidscanner
   ```

2. **Run a scan:**
   - Choose a vulnerability type from the menu
   - Provide target URL or file
   - Select payload file
   - Review results in `./output` or `./reports`

3. **Share your image:**
   ```bash
   # Save image to file
   docker save raidscanner:latest | gzip > raidscanner.tar.gz
   
   # Load on another system
   docker load < raidscanner.tar.gz
   ```

4. **Deploy to cloud:**
   - Push to Docker Hub
   - Deploy to AWS ECS, Azure Container Instances, or Google Cloud Run
   - Use Kubernetes for orchestration

---

## 📝 Notes

- Results are saved to `./output` and `./reports` on your host machine
- Chrome runs in headless mode via Xvfb
- Shared memory is set to 2GB (increase if needed)
- All dependencies are version-locked in requirements.txt
- Container runs as default user (not root)

---

## 🐛 Troubleshooting

**Build fails?**
- Check Docker daemon is running
- Ensure internet connection for package downloads
- Try building with `--no-cache` flag

**Chrome crashes?**
- Increase shared memory in docker-compose.yml
- Check system resources (RAM)

**Permission issues?**
- Run `chmod +x docker-run.sh docker-commands.sh`
- Check volume mount permissions

**Network issues?**
- Verify Docker network settings
- Check firewall rules
- Test with `docker-compose run --rm raidscanner ping google.com`

---

## 📚 Additional Resources

- [DOCKER.md](DOCKER.md) - Complete Docker guide
- [README.md](README.md) - Project documentation
- Docker documentation: https://docs.docker.com/
- Docker Compose: https://docs.docker.com/compose/

---

## 🤝 Contributing

When contributing, remember:
- Test changes in Docker environment
- Update DOCKER.md if adding Docker features
- Keep Dockerfile lean and efficient
- Document new environment variables

---

**Happy Scanning! 🔍**
# 🐳 RaidScanner - Dockerized & Portable!

## ✅ What Was Done

Your RaidScanner project has been fully dockerized with the following additions:

### 📦 Files Created:

1. **`Dockerfile`** - Defines the container image with Python 3.11, Chrome, ChromeDriver, and all dependencies
2. **`docker-compose.yml`** - Orchestrates the container with volume mounts and network settings
3. **`.dockerignore`** - Optimizes Docker builds by excluding unnecessary files
4. **`docker-run.sh`** - Quick run script for Linux/Mac users
5. **`docker-run.bat`** - Quick run script for Windows users
6. **`docker-commands.sh`** - Utility script with common Docker operations
7. **`test-docker-setup.sh`** - Validates Docker environment setup
8. **`DOCKER.md`** - Complete Docker usage documentation
9. **`DOCKER_SETUP.md`** - Setup summary and guide
10. **`.gitignore`** - Git exclusions for clean repository
11. **Updated `README.md`** - Now includes Docker installation as primary method

---

## 🚀 Quick Start Guide

### For Windows Users:

1. **Install Docker Desktop** (if not already installed):
   - Download from: https://www.docker.com/products/docker-desktop
   - Install and enable WSL2 integration
   - Restart your computer if needed

2. **Build and Run**:
   ```cmd
   # Double-click docker-run.bat
   # OR in terminal:
   docker-compose build
   docker-compose run --rm raidscanner
   ```

### For Linux/Mac Users:

1. **Install Docker** (if not already installed):
   ```bash
   # Linux
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   
   # Mac - Download Docker Desktop from docker.com
   ```

2. **Build and Run**:
   ```bash
   chmod +x docker-run.sh
   ./docker-run.sh
   
   # OR manually:
   docker-compose build
   docker-compose run --rm raidscanner
   ```

---

## 🎯 Key Benefits

✅ **Zero Manual Setup** - No need to install Python, Chrome, ChromeDriver, or dependencies
✅ **Cross-Platform** - Works identically on Windows, Mac, and Linux
✅ **Isolated Environment** - Won't conflict with system packages
✅ **Easy Sharing** - Share the entire project, anyone can run it instantly
✅ **Reproducible** - Same environment every time
✅ **Version Controlled** - All dependencies locked to specific versions
✅ **Portable** - Move between machines effortlessly

---

## 📋 Available Commands

### Basic Commands:
```bash
# Build the Docker image
docker-compose build

# Run the scanner interactively
docker-compose run --rm raidscanner

# Access container shell
docker-compose run --rm --entrypoint /bin/bash raidscanner

# Run the URL filter script
docker-compose run --rm --entrypoint /bin/bash raidscanner -c "./filter.sh"

# Clean up
docker-compose down
docker system prune -f
```

### Using Helper Scripts:
```bash
# Test your setup
./test-docker-setup.sh

# Quick run
./docker-run.sh  # Linux/Mac
docker-run.bat   # Windows

# Use utility commands
./docker-commands.sh build
./docker-commands.sh run
./docker-commands.sh shell
./docker-commands.sh clean
```

---

## 📁 Volume Mounts

The Docker setup automatically creates and mounts these directories:

- **`./output/`** - Stores filtered URLs and scan results
- **`./reports/`** - Stores HTML vulnerability reports
- **`./payloads/`** - Contains attack payloads (read-only)

All scan results are automatically saved to your host machine!

---

## 🔧 Configuration

### Adjust Memory for Chrome:
Edit `docker-compose.yml` and change:
```yaml
shm_size: '4gb'  # Increase if Chrome crashes
```

### Add Environment Variables:
Edit `docker-compose.yml`:
```yaml
environment:
  - DISPLAY=:99
  - PYTHONUNBUFFERED=1
  - YOUR_CUSTOM_VAR=value
```

---

## 🐛 Troubleshooting

### Windows WSL2 Issues:
If you see "Docker daemon is not running" in WSL2:
1. Open Docker Desktop
2. Go to Settings → Resources → WSL Integration
3. Enable integration for your WSL2 distro
4. Click "Apply & Restart"

### Build Failures:
```bash
# Clear cache and rebuild
docker-compose build --no-cache
```

### Permission Issues:
```bash
# Linux/Mac - fix script permissions
chmod +x docker-run.sh docker-commands.sh test-docker-setup.sh filter.sh
```

### Chrome/Selenium Crashes:
- Increase `shm_size` in docker-compose.yml
- Check available RAM (minimum 2GB recommended)

---

## 📖 Documentation

- **`DOCKER.md`** - Complete Docker usage guide with advanced examples
- **`DOCKER_SETUP.md`** - Detailed setup documentation
- **`README.md`** - Main project documentation

---

## 🎓 How It Works

1. **Dockerfile** creates an image with:
   - Python 3.11 + all dependencies
   - Google Chrome (stable)
   - ChromeDriver (auto-managed)
   - Xvfb virtual display server
   - Your RaidScanner code

2. **docker-compose.yml** handles:
   - Building the image
   - Running the container
   - Mounting directories for persistent storage
   - Network configuration

3. **When you run it**:
   - Container starts with Xvfb display server
   - Chrome runs headless for XSS/OR scanning
   - Your scans execute inside the isolated container
   - Results save to your local `output/` and `reports/` folders
   - Container stops and cleans up automatically

---

## 🚢 Deployment Options

### Share with Team:
```bash
# Save image to file
docker save raidscanner:latest | gzip > raidscanner.tar.gz

# On another machine
docker load < raidscanner.tar.gz
```

### Push to Docker Hub:
```bash
docker tag raidscanner:latest yourusername/raidscanner:latest
docker push yourusername/raidscanner:latest
```

### Cloud Deployment:
- **AWS ECS**: Deploy container to Amazon ECS
- **Azure Container Instances**: Run on Azure
- **Google Cloud Run**: Serverless container deployment
- **DigitalOcean App Platform**: Easy container hosting

---

## ✨ Next Steps

1. **Test the setup**: Run `./test-docker-setup.sh`
2. **Build the image**: `docker-compose build`
3. **Run your first scan**: `docker-compose run --rm raidscanner`
4. **Check results**: Look in `./output/` and `./reports/`
5. **Share with others**: Commit Docker files to your repo

---

## 🤝 Contributing

If you make improvements:
- Update Dockerfile if changing dependencies
- Update DOCKER.md with new features
- Test in clean Docker environment
- Document new environment variables

---

## 📊 System Requirements

**Minimum:**
- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- 2GB RAM
- 5GB disk space
- Internet connection (for scanning)

**Recommended:**
- 4GB+ RAM
- 10GB+ disk space
- Fast internet connection

---

## 🎉 Success!

Your RaidScanner is now:
- ✅ Fully containerized
- ✅ Easily portable across systems
- ✅ Ready to share with team members
- ✅ Simple to deploy anywhere
- ✅ Isolated and secure

**Happy scanning! 🔍**

For support, see DOCKER.md or open an issue on GitHub.


---

# Dependency Management

# 📦 Dependency Management Guide

## Overview

RaidScanner uses **pinned dependencies** for maximum reproducibility and portability across different systems.

---

## 🎯 Dependency Strategy

### **3-Tier Approach:**

1. **`requirements.txt`** - For local development (includes `windows-curses`)
2. **`requirements-docker.txt`** - For Docker builds (Linux-compatible, pinned versions)
3. **`requirements-lock.txt`** - Complete dependency tree with all transitive dependencies

---

## 📋 Core Dependencies

### Web Automation & Scraping
- **`selenium`** (4.25.0) - Browser automation for XSS/OR scanners
- **`webdriver_manager`** (4.0.2) - Automatic ChromeDriver management
- **`beautifulsoup4`** (4.12.3) - HTML parsing

### HTTP & Networking
- **`requests`** (2.32.3) - HTTP library for vulnerability testing
- **`aiohttp`** (3.10.10) - Async HTTP for concurrent scanning
- **`urllib3`** (2.2.3) - Low-level HTTP operations

### CLI & Terminal UI
- **`colorama`** (0.4.6) - Cross-platform colored terminal output
- **`rich`** (13.9.4) - Rich text and beautiful formatting
- **`prompt_toolkit`** (3.0.48) - Interactive CLI with autocomplete

### Data & Configuration
- **`pyyaml`** (6.0.2) - YAML configuration parsing

### Version Control
- **`gitpython`** (3.1.43) - Git integration

### Web Framework
- **`Flask`** (3.0.3) - Web framework (future features)

---

## 🔒 Version Pinning Strategy

### **Why Pin Versions?**

✅ **Reproducibility** - Same build every time  
✅ **Stability** - No surprise breaking changes  
✅ **Security** - Known vulnerability landscape  
✅ **Portability** - Works identically everywhere  

### **Pinning Levels:**

```python
# Exact pin (recommended for production)
selenium==4.25.0

# Compatible release (allows patch updates)
requests~=2.32.0  # Allows 2.32.x

# Minimum version (not recommended for Docker)
colorama>=0.4.6
```

**RaidScanner uses exact pins for Docker builds.**

---

## 🐳 Docker-Specific Optimizations

### **Multi-Stage Builds (Future Enhancement)**

```dockerfile
# Stage 1: Builder
FROM python:3.11-slim as builder
RUN pip install --user -r requirements-docker.txt

# Stage 2: Runtime
FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
```

### **Layer Caching**

Dependencies are installed in a separate layer before copying application code:

```dockerfile
COPY requirements-docker.txt .
RUN pip install -r requirements-docker.txt  # ← Cached layer
COPY main.py .  # ← Only rebuilds if main.py changes
```

---

## 🔄 Updating Dependencies

### **Check for Updates:**

```bash
# Inside container
docker-compose run --rm --entrypoint pip raidscanner list --outdated

# Local development
pip list --outdated
```

### **Update Specific Package:**

```bash
# Update requirements-docker.txt
webdriver_manager==4.0.3  # Updated version

# Rebuild image
docker-compose build --no-cache
```

### **Update All (Carefully!):**

```bash
# Generate new lockfile
pip freeze > requirements-lock.txt

# Test thoroughly before deploying
```

---

## 🔍 Dependency Audit

### **Security Scanning:**

```bash
# Check for known vulnerabilities
docker-compose run --rm --entrypoint pip raidscanner audit

# Or use safety
pip install safety
safety check -r requirements-docker.txt
```

### **License Compliance:**

```bash
# Check licenses
docker-compose run --rm --entrypoint pip-licenses raidscanner

# Install if needed
pip install pip-licenses
```

---

## 🌍 Platform Compatibility

### **Differences Between Platforms:**

| Dependency | Windows | Linux/Docker | Notes |
|------------|---------|--------------|-------|
| `windows-curses` | ✅ Required | ❌ Excluded | Terminal support |
| `selenium` | ✅ Same | ✅ Same | Platform independent |
| `chromedriver` | Windows binary | Linux binary | Managed by webdriver_manager |

---

## 📊 Dependency Tree

```
raidscanner/
├── selenium (4.25.0)
│   ├── trio (0.27.0)
│   ├── trio-websocket (0.11.1)
│   └── urllib3 (2.2.3)
├── requests (2.32.3)
│   ├── charset-normalizer (3.4.0)
│   ├── idna (3.10)
│   ├── urllib3 (2.2.3)
│   └── certifi (2024.8.30)
├── rich (13.9.4)
│   ├── markdown-it-py (3.0.0)
│   └── pygments (2.18.0)
└── ... (see requirements-lock.txt for complete tree)
```

---

## 🚨 Common Issues & Solutions

### **Issue: Dependency Conflict**

```bash
# Clear pip cache
docker-compose build --no-cache

# Use lockfile for exact versions
pip install -r requirements-lock.txt
```

### **Issue: ChromeDriver Mismatch**

```bash
# webdriver_manager handles this automatically
# If issues persist, clear cache:
rm -rf ~/.wdm
```

### **Issue: SSL Certificate Errors**

```bash
# Update certifi
pip install --upgrade certifi
```

---

## 🔧 Advanced Configuration

### **Custom Dependency Sources:**

```dockerfile
# Use private PyPI server
RUN pip install -r requirements-docker.txt \
    --index-url https://your-pypi-server.com/simple
```

### **Offline Installation:**

```bash
# Download all wheels
pip download -r requirements-docker.txt -d ./wheels

# Install from local wheels
RUN pip install --no-index --find-links=/app/wheels -r requirements-docker.txt
```

---

## 📈 Best Practices

1. ✅ **Always pin versions in Docker builds**
2. ✅ **Test updates in isolated environment first**
3. ✅ **Document why specific versions are used**
4. ✅ **Regularly audit for security vulnerabilities**
5. ✅ **Keep dependencies minimal** (only what's needed)
6. ✅ **Use separate requirements files for different environments**
7. ✅ **Commit lockfiles to version control**

---

## 🔄 Dependency Update Workflow

```bash
# 1. Check for updates
pip list --outdated

# 2. Update requirements-docker.txt
# Edit manually with new versions

# 3. Test locally
pip install -r requirements-docker.txt
python3 main.py

# 4. Rebuild Docker
docker-compose build

# 5. Test in Docker
docker-compose run --rm raidscanner

# 6. Update lockfile
docker-compose run --rm --entrypoint pip raidscanner freeze > requirements-lock.txt

# 7. Commit changes
git commit -am "Update dependencies"
```

---

## 📚 Resources

- **PyPI**: https://pypi.org
- **Safety DB**: https://pyup.io/safety/
- **pip Documentation**: https://pip.pypa.io
- **Poetry** (alternative): https://python-poetry.org

---

**Last Updated:** November 27, 2025  
**Maintained By:** zahidoverflow
