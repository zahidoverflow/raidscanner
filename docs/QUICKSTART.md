# 🚀 RaidScanner Quick Start Guide

## Choose Your Interface

### 🌐 Web GUI (Recommended for Beginners)

**1. Start Web Interface:**
```bash
docker compose up raidscanner-web
```

**2. Open Browser:**
Navigate to: http://localhost:5000

**3. Use the Interface:**
- Click on a scanner card (LFI or SQLi)
- Enter target URLs (one per line)
- Adjust threads (1-10)
- Click "Start Scan"
- Watch real-time results!

**4. View Reports:**
Click the "Reports" card to see scan history

---

### 💻 CLI Mode (Traditional Terminal)

**Start CLI:**
```bash
docker compose up raidscanner-cli
```

Follow the interactive menu.

---

## First Time Setup

### Prerequisites
- ✅ Docker installed
- ✅ Docker Compose installed
- ✅ Internet connection

**That's it! No Python, Chrome, or other dependencies needed on your host machine.**

### Installation
```bash
# Clone repository
git clone https://github.com/zahidoverflow/raidscanner.git
cd raidscanner

# Pull pre-built image (fastest)
docker pull zahidoverflow/raidscanner:latest

# OR build locally
docker compose build
```

---

## Quick Test

### Test LFI Scanner (Web GUI)
1. Start web: `docker compose up raidscanner-web`
2. Open: http://localhost:5000
3. Click "LFI Scanner" card
4. Enter test URL: `https://example.com?page=test`
5. Click "Start Scan"

### Test SQLi Scanner (Web GUI)
1. Click "SQLi Scanner" card
2. Enter test URL: `https://example.com?id=1`
3. Set threads: 5
4. Click "Start Scan"

---

## Common Commands

### Docker Commands
```bash
# Start web interface
docker compose up raidscanner-web

# Start CLI mode
docker compose up raidscanner-cli

# Start both
docker compose up

# Run in background
docker compose up -d raidscanner-web

# Stop services
docker compose down

# View logs
docker compose logs -f raidscanner-web

# Rebuild after changes
docker compose build --no-cache
```

### Direct Docker Run
```bash
# Web mode
docker run -d -p 5000:5000 \
  -v $(pwd)/output:/app/output \
  -e MODE=web \
  zahidoverflow/raidscanner:latest

# CLI mode
docker run -it \
  -v $(pwd)/output:/app/output \
  zahidoverflow/raidscanner:latest
```

---

## Troubleshooting

### Web GUI Not Loading
```bash
# Check if port 5000 is available
netstat -an | grep 5000

# Check container status
docker ps

# Check logs
docker compose logs raidscanner-web
```

### Can't Connect to Scanner
- Ensure Docker is running
- Check firewall settings
- Verify port 5000 is not blocked
- Try accessing from localhost, not remote IP

### Reports Not Saving
```bash
# Check directory permissions
ls -la output/ reports/

# Create directories
mkdir -p output reports
chmod 777 output reports
```

---

## URLs to Remember

| Service | URL | Purpose |
|---------|-----|---------|
| Web GUI | http://localhost:5000 | Main interface |
| Reports | http://localhost:5000/reports | View scan history |
| API Docs | See WEB_GUI.md | API reference |

---

## File Locations

### Inside Container
- **Payloads**: `/app/payloads/`
- **Output**: `/app/output/`
- **Reports**: `/app/reports/`

### On Host (Mounted)
- **Output**: `./output/`
- **Reports**: `./reports/`
- **Payloads**: `./payloads/`

---

## Scanner Comparison

| Scanner | Status | Detection Method |
|---------|--------|------------------|
| LFI | ✅ Ready | Pattern matching |
| SQLi | ✅ Ready | Time-based blind |
| XSS | ⏳ Coming | Selenium automation |
| OR | ⏳ Coming | Redirect detection |
| CRLF | ⏳ Coming | Header injection |

---

## Performance Tips

### For Speed
- Increase threads to 10
- Use wired connection
- Run Docker on SSD

### For Accuracy
- Decrease threads to 3-5
- Use smaller payload sets
- Test one URL at a time

---

## Security Warning

⚠️ **IMPORTANT**: 
- Only scan systems you own or have permission to test
- Unauthorized scanning is illegal
- This tool is for educational and authorized testing only

---

## Getting Help

### Documentation
- **Full Guide**: [WEB_GUI.md](WEB_GUI.md)
- **Docker Guide**: [DOCKER.md](DOCKER.md)
- **Implementation**: [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)

### Resources
- **GitHub**: https://github.com/zahidoverflow/raidscanner
- **Docker Hub**: https://hub.docker.com/r/zahidoverflow/raidscanner

### Common Issues
1. **"Port 5000 already in use"**: Change port in docker compose.yml
2. **"Connection refused"**: Check if container is running
3. **"Chrome error"**: Container needs more memory (increase shm_size)

---

## Next Steps

1. ✅ Try a test scan
2. ✅ Explore the web interface
3. ✅ View generated reports
4. 📚 Read full documentation
5. 🛠️ Customize payloads
6. 🚀 Use in authorized testing

---

**Happy Scanning! 🔍**

For detailed information, see [WEB_GUI.md](WEB_GUI.md)
