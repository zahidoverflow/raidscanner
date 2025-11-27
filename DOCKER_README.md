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
