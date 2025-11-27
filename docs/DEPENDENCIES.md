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
