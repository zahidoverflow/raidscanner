# Damn Vulnerable Web University - Complete LLM Context

**Version**: 2.0  
**Last Updated**: 2025-12-05  
**Purpose**: Comprehensive context for AI assistants working with this codebase  
**Project Type**: Intentionally Vulnerable Web Application for Security Education

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Project Identity & Metadata](#project-identity--metadata)
3. [Architecture & Technology Stack](#architecture--technology-stack)
4. [Complete File Inventory](#complete-file-inventory)
5. [Vulnerability Catalog](#vulnerability-catalog)
6. [API Endpoints Reference](#api-endpoints-reference)
7. [React Components](#react-components)
8. [Configuration Files](#configuration-files)
9. [Development Workflow](#development-workflow)
10. [Deployment](#deployment)
11. [Testing](#testing)
12. [Common Tasks](#common-tasks)

---

## Project Overview

### Name & Purpose
**Damn Vulnerable Web University (DVWU)** - An intentionally vulnerable web application designed for:
- 🎯 Security testing and penetration testing practice
- 📚 Cybersecurity education and training
- 🔬 Security scanner tool development and testing
- 💼 Professional security training for developers

### Project Genesis
- **Original Project**: Part of RaidScanner (automated vulnerability scanner)
- **Separation Date**: December 2025
- **Original Branch**: `lab` branch of RaidScanner repository
- **Current Status**: Standalone educational security project
- **Primary Use**: Target application for security testing tools

### Key Features
1. **Modern Stack**: React 18 + Vite + Serverless Functions
2. **7 Vulnerability Types**: XSS, SQLi, LFI, CRLF, Open Redirect
3. **Diverse Attack Vectors**: Both GET and POST methods
4. **Educational**: Business impact analysis + mitigation guides
5. **Production-like**: Realistic architecture mimicking real apps

---

## Project Identity & Metadata

### Repository
- **GitHub**: `zahidoverflow/damn-vulnerable-web-university`
- **Branch**: `main`
- **License**: MIT
- **Version**: 1.0.0
- **Package**: `damn-vulnerable-university`

### Live Deployment
- **URL**: https://ist-edu-bd.vercel.app
- **Platform**: Vercel (auto-deploy on push to main)
- **Alternative**: Docker deployment available

### Contributors
- **Author**: Mohammad Zahidul Islam (@zahidoverflow) - zahidoverflow@gmail.com
- **Contributor**: Osman Faruque (@osmanfaruque)
- **Institution**: Institute of Science and Technology (IST)
- **Context**: Final Year Project - Cybersecurity Research

---

## Architecture & Technology Stack

### Frontend
```
React 18.2.0
├── Build Tool: Vite 5.0.8
├── Routing: React Router DOM 6.21.0
├── HTTP: Axios 1.6.2
├── Styling: Pure CSS (no frameworks)
└── Icons: Font Awesome (CDN)
```

**Dev Server**: Port 3000 (Vite configured)  
**Build Output**: `dist/` directory  
**Features**: Fast HMR, ES Modules, Functional components

### Backend
```
Node.js 18.x
├── Platform: Vercel Serverless Functions
├── Location: /api directory
├── Pattern: One file = one endpoint
└── Response: HTML + JSON hybrid
```

**API Convention**: `api/filename.js` → `/api/filename` endpoint  
**CORS**: Enabled for all endpoints (`Access-Control-Allow-Origin: *`)

### Deployment Architecture
```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │
┌──────▼──────────────────────┐
│  Deployment Options:        │
│  1. Vercel (Production)     │
│  2. Docker (Self-hosted)    │
│  3. Local Dev (Vite)        │
└──────┬──────────────────────┘
       │
┌──────▼──────┐    ┌──────────┐
│ React SPA   │◄──►│ API /api │
│ (Frontend)  │    │ (Backend)│
└─────────────┘    └──────────┘
```

### Dependencies

**Production** (4 total):
- `react` ^18.2.0
- `react-dom` ^18.2.0
- `react-router-dom` ^6.21.0
- `axios` ^1.6.2

**Development** (4 total):
- `@vitejs/plugin-react` ^4.2.1
- `vite` ^5.0.8
- `@types/react` ^18.2.45
- `@types/react-dom` ^18.2.18

---

## Complete File Inventory

### Root Directory
```
damn-vulnerable-web-university/
├── .git/                      # Git repository
├── .gitignore                 # Git ignore rules
├── .mailmap                   # Git author mapping
├── Dockerfile                 # Multi-stage Docker build
├── docker-compose.yml         # Docker Compose config
├── nginx.conf                 # Nginx server config
├── vercel.json                # Vercel deployment config
├── vite.config.js             # Vite build config
├── package.json               # NPM dependencies & scripts
├── package-lock.json          # Dependency lock file
├── index.html                 # SPA entry HTML
└── README.md                  # Project documentation
```

### API Directory (`/api`) - 6 files
```
api/
├── comments.js          # XSS (Reflected & Stored)
├── search.js            # SQL Injection (Search)
├── portal.js            # SQL Injection (Login)
├── newsletter.js        # CRLF Injection
├── notices.js           # LFI (Path Traversal)
└── redirect.js          # Open Redirect
```

### Source Directory (`/src`)
```
src/
├── main.jsx             # React entry point
├── App.jsx              # Root component + routing
├── App.css              # App styles
├── index.css            # Global styles
├── components/
│   ├── Header.jsx       # Navigation header
│   ├── Header.css
│   ├── Footer.jsx       # Footer component
│   └── Footer.css
└── pages/
    ├── Home.jsx         # Landing page
    ├── Home.css
    ├── About.jsx        # About page
    ├── Courses.jsx      # Courses listing
    ├── Portal.jsx       # Login portal (SQLi)
    ├── Dashboard.jsx    # Student dashboard
    ├── Search.jsx       # Course search (SQLi)
    ├── Files.jsx        # File browser
    ├── NoticeBoard.jsx  # Notice viewer (LFI)
    ├── NoticeBoard.css
    ├── Comments.jsx     # Comments (XSS)
    ├── Comments.css
    ├── Redirect.jsx     # URL redirector
    ├── Redirect.css
    ├── Newsletter.jsx   # Newsletter form (CRLF)
    └── Newsletter.css
```
**Total Pages**: 11 routes  
**Total Components**: 2 shared (Header, Footer)

### Public Directory (`/public`)
```
public/
├── ist-logo.png         # University logo (89 KB)
├── ist-front-side.png   # Building image (2.9 MB)
├── vite.svg             # Vite logo
├── robots.txt           # SEO robots file
└── sitemap.xml          # SEO sitemap
```

### Documentation (`/docs`)
```
docs/
├── CONTEXT.md           # This file (LLM context)
└── VULNERABILITY_REPORT.md  # Detailed vulnerability analysis
```

---

## Vulnerability Catalog

### Overview Table
| # | Type | Endpoint | Method | Severity | OWASP |
|---|------|----------|--------|----------|-------|
| 1 | XSS (Reflected) | `/api/comments?comment=` | GET | High | A07:2021 |
| 2 | XSS (Stored) | `/api/comments` | POST | Critical | A07:2021 |
| 3 | SQL Injection | `/api/portal` | POST | Critical | A03:2021 |
| 4 | SQL Injection | `/api/search?q=` | GET | High | A03:2021 |
| 5 | CRLF Injection | `/api/newsletter` | POST | Medium | A03:2021 |
| 6 | LFI/Path Traversal | `/api/notices?file=` | GET | High | A01:2021 |
| 7 | Open Redirect | `/api/redirect?url=` | GET | Medium | A01:2021 |

### Vulnerability Details

#### 1. XSS - Reflected (GET)
**File**: `api/comments.js`  
**Endpoint**: `/api/comments?comment=VALUE`  
**Vulnerable Code**:
```javascript
const { comment } = req.query
return res.send(`<div class="comment">${comment}</div>`)
```
**Payload**: `?comment=<script>alert(1)</script>`  
**Impact**: Session hijacking, credential theft

#### 2. XSS - Stored (POST)
**File**: `api/comments.js`  
**Endpoint**: `/api/comments` (POST body)  
**Vulnerable Code**:
```javascript
if (req.method === 'POST') {
    const { comment } = req.body
    return res.send(`<div>${comment}</div>`)
}
```
**Payload**: `{"comment": "<img src=x onerror=alert(1)>"}`  
**Impact**: Persistent XSS affecting all users

#### 3. SQL Injection - Portal (POST)
**File**: `api/portal.js`  
**Endpoint**: `/api/portal`  
**Vulnerable Code**:
```javascript
const hasSQLi = username.includes("'") || username.includes('OR')
if (hasSQLi) {
    // Authentication bypass simulation
}
```
**Payload**: `{"username": "admin' OR '1'='1' --", "password": "x"}`  
**Impact**: Authentication bypass, data exfiltration

#### 4. SQL Injection - Search (GET)
**File**: `api/search.js`  
**Endpoint**: `/api/search?q=VALUE`  
**Vulnerable Code**:
```javascript
const hasSQLi = query.includes("'") || query.includes('UNION')
if (hasSQLi) {
    // Display SQL error with leaked data
}
```
**Payload**: `?q=' OR '1'='1`  
**Impact**: Database enumeration

#### 5. CRLF Injection (POST)
**File**: `api/newsletter.js`  
**Endpoint**: `/api/newsletter`  
**Vulnerable Code**:
```javascript
const hasCRLF = email.includes('\r') || email.includes('\n')
if (hasCRLF) {
    // Header injection simulation
}
```
**Payload**: `{"email": "test@test.com\r\nSet-Cookie: admin=true"}`  
**Impact**: HTTP response splitting, header injection

#### 6. LFI - Path Traversal (GET)
**File**: `api/notices.js`  
**Endpoint**: `/api/notices?file=VALUE`  
**Vulnerable Code**:
```javascript
if (filename.includes('../') || filename.includes('..\\')) {
    if (filename.includes('/etc/passwd')) {
        // Simulate file content leak
    }
}
```
**Payload**: `?file=../../../../etc/passwd`  
**Impact**: Configuration file exposure, source code leak

#### 7. Open Redirect (GET)
**File**: `api/redirect.js`  
**Endpoint**: `/api/redirect?url=VALUE`  
**Vulnerable Code**:
```javascript
// Frontend redirect without validation
window.location.href = url
```
**Payload**: `?url=https://evil.com`  
**Impact**: Phishing, credential harvesting

---

## API Endpoints Reference

### Common Handler Pattern
All API endpoints follow this pattern:
```javascript
export default function handler(req, res) {
    // Enable CORS
    res.setHeader('Access-Control-Allow-Origin', '*')
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    res.setHeader('Content-Type', 'text/html; charset=utf-8')
    
    if (req.method === 'OPTIONS') {
        return res.status(200).end()
    }
    
    // Vulnerability implementation
}
```

### Endpoint Details

| Endpoint | Methods | Parameters | Response Type |
|----------|---------|------------|---------------|
| `/api/comments` | GET, POST | `comment`, `author` | HTML |
| `/api/search` | GET, POST | `q` | HTML |
| `/api/portal` | POST | `username`, `password` | HTML |
| `/api/newsletter` | POST | `email` | HTML |
| `/api/notices` | GET | `file` | HTML |
| `/api/redirect` | GET | `url` | HTML (redirect) |

---

## React Components

### Routing (`App.jsx`)
```javascript
<Routes>
  <Route path="/" element={<Home />} />
  <Route path="/about" element={<About />} />
  <Route path="/courses" element={<Courses />} />
  <Route path="/portal" element={<Portal />} />
  <Route path="/dashboard" element={<Dashboard />} />
  <Route path="/search" element={<Search />} />
  <Route path="/files" element={<Files />} />
  <Route path="/notices" element={<NoticeBoard />} />
  <Route path="/comments" element={<Comments />} />
  <Route path="/redirect" element={<Redirect />} />
  <Route path="/newsletter" element={<Newsletter />} />
</Routes>
```

### URL Parameter Pattern
All vulnerable pages sync input with URL parameters:
```javascript
const [searchParams, setSearchParams] = useSearchParams()
const [input, setInput] = useState(searchParams.get('param') || '')

const handleSubmit = (e) => {
    e.preventDefault()
    setSearchParams({ param: input })
    // Trigger API call
}
```

### Toast Notification Pattern
Non-blocking notifications appear top-right:
```javascript
const [showPopup, setShowPopup] = useState(false)
const [popupMessage, setPopupMessage] = useState('')

<div className="popup-overlay">
    <div className="popup-content">
        {popupMessage}
        <button onClick={() => setShowPopup(false)}>×</button>
    </div>
</div>
```

---

## Configuration Files

### `package.json`
```json
{
  "name": "damn-vulnerable-university",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "docker:build": "docker compose build",
    "docker:up": "docker compose up -d",
    "docker:down": "docker compose down",
    "docker:logs": "docker compose logs -f"
  }
}
```

### `vite.config.js`
```javascript
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      }
    }
  }
})
```

### `vercel.json`
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "git": {
    "deploymentEnabled": {
      "lab": true
    }
  },
  "rewrites": [
    {"source": "/api/(.*)", "destination": "/api/$1"},
    {"source": "/((?!api/.*).*)", "destination": "/index.html"}
  ]
}
```

### `Dockerfile`
**Multi-stage build**:
- **Stage 1**: Node 18 Alpine - Build React app
- **Stage 2**: Nginx Alpine - Serve static files

```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
```

### `docker-compose.yml`
```yaml
services:
  web:
    build: .
    container_name: damn-vulnerable-university
    ports:
      - "3000:80"
    networks:
      - vuln-network
```

### `nginx.conf`
```nginx
server {
    listen 80;
    root /usr/share/nginx/html;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

---

## Development Workflow

### Setup
```bash
# Clone repository
git clone https://github.com/zahidoverflow/damn-vulnerable-web-university.git
cd damn-vulnerable-web-university

# Install dependencies
npm install

# Start development server
npm run dev
# → http://localhost:3000
```

### Development Commands
```bash
npm run dev          # Start Vite dev server (HMR enabled)
npm run build        # Production build → dist/
npm run preview      # Preview production build
```

### Docker Commands
```bash
npm run docker:build    # Build Docker image
npm run docker:up       # Start container (detached)
npm run docker:down     # Stop container
npm run docker:logs     # View container logs
```

### Git Configuration
```bash
git config user.name "zahidoverflow"
git config user.email "zahidoverflow@gmail.com"
```

---

## Deployment

### Vercel (Production)
1. **Automatic**: Push to `main` branch triggers deployment
2. **Manual**: `vercel deploy` (requires Vercel CLI)
3. **Configuration**: Uses `vercel.json`
4. **Build**: `npm run build`
5. **Output**: `dist/` directory served

**Live URL**: https://ist-edu-bd.vercel.app

### Docker (Self-Hosted)
```bash
# Build and run
docker compose up -d

# Access
http://localhost:3000
```

### Local Development
```bash
npm run dev
# Access: http://localhost:3000
```

---

## Testing

### Manual Testing

#### XSS (GET)
```bash
curl "http://localhost:3000/api/comments?comment=<script>alert(1)</script>"
```

#### XSS (POST)
```bash
curl -X POST http://localhost:3000/api/comments \
  -H "Content-Type: application/json" \
  -d '{"comment":"<script>alert(1)</script>"}'
```

#### SQL Injection (GET)
```bash
curl "http://localhost:3000/api/search?q=' OR '1'='1"
```

#### SQL Injection (POST)
```bash
curl -X POST http://localhost:3000/api/portal \
  -H "Content-Type: application/json" \
  -d '{"username":"admin'\'' OR '\''1'\''='\''1","password":"x"}'
```

#### LFI
```bash
curl "http://localhost:3000/api/notices?file=../../../../etc/passwd"
```

#### CRLF
```bash
curl -X POST http://localhost:3000/api/newsletter \
  -H "Content-Type: application/json" \
  -d '{"email":"test\r\nSet-Cookie: admin=true"}'
```

### Automated Testing
Compatible with:
- **OWASP ZAP** - Web application scanner
- **Burp Suite** - Penetration testing
- **SQLMap** - SQL injection automation
- **Nikto** - Web server scanner
- **Custom scanners** - RaidScanner, etc.

---

## Common Tasks

### Adding New Vulnerability

1. **Create API endpoint**: `api/new-vuln.js`
```javascript
export default function handler(req, res) {
    res.setHeader('Access-Control-Allow-Origin', '*')
    // Implement vulnerability
}
```

2. **Create page component**: `src/pages/NewVuln.jsx`
```javascript
function NewVuln() {
    const [searchParams, setSearchParams] = useSearchParams()
    // Implement UI
}
export default NewVuln
```

3. **Add route**: Update `src/App.jsx`
```javascript
<Route path="/new-vuln" element={<NewVuln />} />
```

4. **Update navigation**: Add link in `src/components/Header.jsx`

5. **Document**: Update `VULNERABILITY_REPORT.md`

### Modifying Existing Vulnerability
1. Locate API: `api/[endpoint].js`
2. Locate UI: `src/pages/[Page].jsx`
3. Update logic
4. Test exploit
5. Update documentation

### Updating Styles
- **Global**: `src/index.css`
- **Component**: `src/pages/[Page].css` or `src/components/[Component].css`
- **Use CSS variables** for consistency

---

## Design Patterns

### 1. URL Parameter Sync
All input fields sync with URL for easy fuzzing:
```javascript
const [searchParams, setSearchParams] = useSearchParams()
const param = searchParams.get('param') || ''
```

### 2. Toast Notifications
Non-blocking, top-right corner, auto-closeable

### 3. Responsive Design
Mobile-first, adaptive navigation

### 4. Educational Content
Each page includes:
- Attack context
- Business impact
- Sample payloads
- Mitigation strategies

---

## Troubleshooting

### Common Issues

**API 404 errors**
- Check `vercel.json` rewrites
- Ensure `/api` directory structure

**XSS not executing**
- Browser XSS protection may block
- Try different payload
- Check Content-Type header

**Docker build fails**
- Run `npm install` first
- Check Node version (need 18.x)

**URL params not updating**
- Ensure `setSearchParams` is called
- Check `handleSubmit` function

---

## Security & Legal

### ⚠️ WARNING
This is an **INTENTIONALLY VULNERABLE** application.

### ✅ Authorized Use
- Security research and education
- Penetration testing practice
- Security tool development
- Authorized security assessments

### ❌ Prohibited
- Production deployment
- Real user data
- Unauthorized testing
- Any illegal activities

### Legal Notice
Unauthorized computer access is illegal under:
- Computer Fraud and Abuse Act (CFAA) - USA
- Computer Misuse Act - UK
- Local cybercrime laws

**Always obtain written authorization before security testing.**

---

## References

### OWASP
- [OWASP Top 10 2021](https://owasp.org/Top10/)
- [Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Cheat Sheets](https://cheatsheetseries.owasp.org/)

### Similar Projects
- [DVWA](https://github.com/digininja/DVWA)
- [WebGoat](https://github.com/WebGoat/WebGoat)
- [Juice Shop](https://github.com/juice-shop/juice-shop)

### Learning
- [PortSwigger Academy](https://portswigger.net/web-security)
- [HackTheBox](https://www.hackthebox.com/)
- [TryHackMe](https://tryhackme.com/)

---

## Changelog

### Version 2.0 (2025-12-05)
- Complete CONTEXT.md rewrite with comprehensive details
- Updated git configuration
- Complete file inventory

### Version 1.0 (2025-12-03)
- Initial standalone release
- Separated from RaidScanner
- 7 vulnerability types
- Docker support
- Comprehensive documentation

---

**End of Context File**

This document provides comprehensive context for AI assistants to understand and work with the Damn Vulnerable Web University codebase effectively.
