# Project Analysis: Zooel Security Testing Environment

## Overview

This directory contains two complementary security testing projects:

1. **RaidScanner** - A web vulnerability scanner
2. **Damn Vulnerable Web University (DVWU)** - A deliberately vulnerable web application

These projects work together as a security testing and educational environment.

---

## Project 1: RaidScanner

### Purpose
A modern, automated vulnerability scanner for ethical hacking and security testing.

### Tech Stack
- **Backend**: Python 3.11, Flask, Flask-SocketIO
- **Browser Automation**: Selenium, Chrome/ChromeDriver
- **Container**: Docker with Xvfb for headless Chrome

### Features
| Feature | Status | Description |
|---------|--------|-------------|
| LFI Scanner | ✅ Working | Local File Inclusion detection |
| SQLi Scanner | ✅ Working | SQL Injection detection |
| XSS Scanner | ✅ Working | Cross-Site Scripting detection |
| Open Redirect | ✅ Working | URL redirection flaw detection |
| CRLF Injection | ✅ Working | HTTP Response Splitting detection |
| Web GUI | ✅ Fixed | Flask web interface (templates were missing, now created) |
| CLI Mode | ✅ Working | Interactive terminal scanner |
| Report Generation | ✅ Working | HTML/JSON vulnerability reports |

### Issues Found & Fixed
1. **Missing Templates**: The `web/templates/` folder was empty. Created:
   - `index.html` - Main dashboard
   - `scanner.html` - Scanner configuration page
   - `reports.html` - Reports viewer

### Access URLs
- **Web GUI**: http://localhost:5000
- **Scanner API**: http://localhost:5000/api/scan/{type}

---

## Project 2: Damn Vulnerable Web University (DVWU)

### Purpose
An intentionally vulnerable web application for:
- Security testing practice
- Penetration testing training
- Security scanner development/testing
- Cybersecurity education

### Tech Stack
- **Frontend**: React 18, Vite, React Router v6
- **Backend**: Express.js (local), Vercel Serverless Functions (production)
- **Container**: Docker with Node.js

### Vulnerabilities Implemented
| # | Vulnerability | Endpoint | OWASP | Severity |
|---|--------------|----------|-------|----------|
| 1 | Reflected XSS | `/api/comments?comment=` | A03:2021 | High |
| 2 | Stored XSS | `POST /api/comments` | A03:2021 | Critical |
| 3 | SQLi (Auth) | `/api/portal` | A03:2021 | Critical |
| 4 | SQLi (Search) | `/api/search?q=` | A03:2021 | High |
| 5 | LFI/Path Traversal | `/api/notices?file=` | A01:2021 | High |
| 6 | CRLF Injection | `/api/newsletter` | A03:2021 | Medium |
| 7 | Open Redirect | `/api/redirect?url=` | A01:2021 | Medium |

### Issues Found & Fixed
1. **Missing Server for Local APIs**: Vercel serverless functions don't work locally with just nginx
   - Created `server.cjs` - Express server to serve API endpoints locally
   - Modified `Dockerfile` to use Express instead of nginx-only

2. **Docker Build Issue**: `npm ci --only=production` skipped devDependencies needed for build
   - Fixed to use `npm ci` without flags

3. **ES Module Compatibility**: Package.json had `"type": "module"` but server used CommonJS
   - Renamed server to `server.cjs`

### Access URLs
- **Web App**: http://localhost:3001
- **API Endpoints**: http://localhost:3001/api/{endpoint}

---

## Running Both Projects

### Prerequisites
- Docker Engine 20.10+
- Docker Compose 2.0+

### Quick Start

```bash
# Navigate to the zooel directory
cd /mnt/DABCEB02BCEAD851/Projects/For_Clients/zooel

# Start DVWU (vulnerable target)
cd damn-vulnerable-web-university
docker compose up -d

# Start RaidScanner (vulnerability scanner)
cd ../raidscanner
docker compose up -d raidscanner-web
```

### Testing Example

1. Open RaidScanner: http://localhost:5000
2. Click "LFI Scanner"
3. Enter target URL: `http://host.docker.internal:3001/api/notices?file=FUZZ`
4. Start scan to detect LFI vulnerability

---

## Project Structure

```
zooel/
├── damn-vulnerable-web-university/
│   ├── api/                  # Vulnerable API endpoints (Vercel functions)
│   ├── src/                  # React frontend source
│   ├── server.cjs            # Local Express server (created)
│   ├── Dockerfile            # Docker build (fixed)
│   └── docker-compose.yml
│
├── raidscanner/
│   ├── core/                 # Scanner engine modules
│   ├── payloads/             # Vulnerability payload files
│   ├── web/
│   │   ├── static/           # CSS, JS assets
│   │   └── templates/        # Flask templates (created)
│   ├── app.py               # Flask web application
│   ├── scanner_cli.py       # CLI scanner
│   └── compose.yml
│
└── openspec/
    └── project-analysis.md   # This document
```

---

## Security Notice

⚠️ **EDUCATIONAL USE ONLY**

Both projects are designed for authorized security testing and education:
- Never deploy DVWU in production
- Always obtain permission before scanning systems
- RaidScanner should only be used on systems you own or have authorization to test

---

## Port Summary

| Service | Host Port | Container Port |
|---------|-----------|----------------|
| DVWU | 3001 | 3000 |
| RaidScanner Web | 5000 | 5000 |

*Note: Ports were modified from defaults (3000, 5000) to avoid conflicts with other services.*
