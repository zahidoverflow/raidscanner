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

