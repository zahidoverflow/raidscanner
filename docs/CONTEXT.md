# Damn Vulnerable University - LLM Context File

**Version**: 1.0  
**Last Updated**: 2025-12-03  
**Purpose**: Comprehensive context for AI assistants working with this codebase

---

## Project Overview

### Name
**Damn Vulnerable University (DVU)**

### Description
An intentionally vulnerable web application designed for security testing, education, and tool development. Built as a modern React SPA with serverless API endpoints, featuring realistic vulnerabilities across GET and POST request methods.

### Origin
- Originally part of the **RaidScanner** project (security scanner tool)
- Separated from `lab` branch into standalone repository
- Designed to be scanned by security tools while providing educational value

### Repository
- **GitHub**: `zahidoverflow/damn-vulnerable-university`
- **Live Demo**: https://ist-edu-bd.vercel.app
- **Branch**: `main` (formerly `lab`)

---

## Architecture

### Technology Stack

#### Frontend
- **Framework**: React 18.2.0
- **Build Tool**: Vite 5.0.8
- **Routing**: React Router DOM 6.21.0
- **HTTP Client**: Axios 1.6.2
- **Styling**: Custom CSS (no frameworks like Tailwind)
- **Icons**: Font Awesome (via CDN)

#### Backend
- **Runtime**: Node.js (serverless)
- **Platform**: Vercel Serverless Functions
- **API Location**: `/api` directory
- **Response Format**: HTML (for browser rendering) and JSON (for API clients)

#### Deployment
- **Production**: Vercel (automatic deployment from `main` branch)
- **Local Dev**: Vite dev server (`npm run dev`)
- **Docker**: Multi-stage build (Node.js builder + Nginx server)

### Project Structure

```
damn-vulnerable-university/
├── api/                      # Serverless API endpoints
│   ├── comments.js          # XSS (Reflected & Stored)
│   ├── search.js            # SQL Injection (Search)
│   ├── portal.js            # SQL Injection (Login)
│   ├── newsletter.js        # CRLF Injection
│   ├── notices.js           # LFI (Path Traversal)
│   └── redirect.js          # Open Redirect
├── src/
│   ├── components/
│   │   ├── Header.jsx       # Navigation header
│   │   └── Footer.jsx       # Footer component
│   ├── pages/
│   │   ├── Home.jsx         # Landing page
│   │   ├── About.jsx        # About page
│   │   ├── Portal.jsx       # Login portal (SQLi)
│   │   ├── Search.jsx       # Course search (SQLi)
│   │   ├── Comments.jsx     # Comments section (XSS)
│   │   ├── NoticeBoard.jsx  # Notice board (LFI)
│   │   ├── Redirect.jsx     # URL redirector (Open Redirect)
│   │   ├── Newsletter.jsx   # Newsletter form (CRLF)
│   │   ├── Dashboard.jsx    # Student dashboard
│   │   └── Files.jsx        # File browser
│   ├── App.jsx              # Main app component with routing
│   ├── main.jsx             # Entry point
│   └── index.css            # Global styles
├── public/
│   ├── ist-logo.png         # University logo
│   ├── hero-bg.jpg          # Hero background
│   └── favicon.ico          # Favicon
├── docs/
│   ├── VULNERABILITY_REPORT.md  # Detailed vulnerability analysis
│   └── CONTEXT.md               # This file
├── Dockerfile                   # Multi-stage Docker build
├── docker-compose.yml           # Docker Compose configuration
├── nginx.conf                   # Nginx configuration for production
├── vercel.json                  # Vercel deployment config
├── vite.config.js               # Vite configuration
├── package.json                 # Dependencies and scripts
└── README.md                    # Project documentation
```

---

## Vulnerabilities

### Implementation Philosophy

1. **Realistic**: Vulnerabilities mimic real-world scenarios
2. **Educational**: Each vulnerability includes explanations and examples
3. **Diverse**: Mix of GET and POST methods for comprehensive testing
4. **Functional**: All vulnerabilities are fully exploitable
5. **Documented**: Detailed reports with business impact analysis

### Vulnerability Details

#### 1. Cross-Site Scripting (XSS) - Reflected
- **Endpoint**: `/api/comments?comment=`
- **Method**: GET
- **File**: `api/comments.js`
- **Vulnerability**: URL parameter rendered without sanitization
- **Payload Example**: `?comment=<script>alert(1)</script>`
- **Impact**: Session hijacking, credential theft, phishing
- **OWASP**: A07:2021 - Cross-Site Scripting

**Implementation**:
```javascript
// VULNERABLE: Reflected XSS
return res.status(200).send(`
  <div class="comment">${comment}</div>
`)
```

#### 2. Cross-Site Scripting (XSS) - Stored
- **Endpoint**: `/api/comments` (POST)
- **Method**: POST
- **File**: `api/comments.js`
- **Vulnerability**: User input stored and displayed without sanitization
- **Payload Example**: `{"comment": "<img src=x onerror=alert(1)>"}`
- **Impact**: Persistent XSS affecting all users
- **OWASP**: A07:2021 - Cross-Site Scripting

**Implementation**:
```javascript
// VULNERABLE: Stored XSS
if (req.method === 'POST') {
    const { comment, author } = req.body || {}
    return res.send(`<div>${comment}</div>`)
}
```

#### 3. SQL Injection - Search
- **Endpoint**: `/api/search?q=`
- **Method**: GET
- **File**: `api/search.js`
- **Vulnerability**: Search query concatenated into SQL-like query
- **Payload Example**: `?q=' OR '1'='1`
- **Impact**: Data exfiltration, authentication bypass
- **OWASP**: A03:2021 - Injection

**Implementation**:
```javascript
// VULNERABLE: SQL Injection
if (query.includes("'") || query.includes("UNION")) {
    setError(`Database Error: Syntax error near '${query}'`)
}
```

#### 4. SQL Injection - Login Portal
- **Endpoint**: `/api/portal` (POST)
- **Method**: POST
- **File**: `api/portal.js`
- **Vulnerability**: Username/password used in SQL query without sanitization
- **Payload Example**: `{"username": "admin' OR '1'='1' --", "password": "anything"}`
- **Impact**: Authentication bypass, privilege escalation
- **OWASP**: A03:2021 - Injection

**Implementation**:
```javascript
// VULNERABLE: SQL Injection in authentication
if (studentId === "' OR '1'='1' --" || password === "' OR '1'='1' --") {
    // Authentication bypass successful
    navigate('/dashboard')
}
```

#### 5. CRLF Injection
- **Endpoint**: `/api/newsletter` (POST)
- **Method**: POST
- **File**: `api/newsletter.js`
- **Vulnerability**: Email input with CRLF sequences can inject headers
- **Payload Example**: `{"email": "test@test.com\r\nSet-Cookie: admin=true"}`
- **Impact**: HTTP response splitting, session fixation, cache poisoning
- **OWASP**: A03:2021 - Injection

**Implementation**:
```javascript
// VULNERABLE: CRLF Injection
const hasCRLF = email.includes('\r') || email.includes('\n')
if (hasCRLF) {
    // Simulate header injection
    return res.send(`Headers injected: ${email}`)
}
```

#### 6. Local File Inclusion (LFI) - Path Traversal
- **Endpoint**: `/api/notices?file=`
- **Method**: GET
- **File**: `api/notices.js`
- **Vulnerability**: File parameter allows path traversal
- **Payload Example**: `?file=../../../etc/passwd`
- **Impact**: Sensitive file disclosure, configuration exposure
- **OWASP**: A01:2021 - Broken Access Control

**Implementation**:
```javascript
// VULNERABLE: Path Traversal
if (filename.includes('../') || filename.includes('..\\')) {
    if (filename.includes('/etc/passwd')) {
        // Simulate /etc/passwd content
        return res.send('root:x:0:0:root:/root:/bin/bash...')
    }
}
```

#### 7. Open Redirect
- **Endpoint**: `/api/redirect?url=`
- **Method**: GET
- **File**: `api/redirect.js`
- **Vulnerability**: Redirects to any URL without validation
- **Payload Example**: `?url=//evil.com`
- **Impact**: Phishing, credential theft, malware distribution
- **OWASP**: A01:2021 - Broken Access Control

**Implementation**:
```javascript
// VULNERABLE: No URL validation
useEffect(() => {
    if (url) {
        setTimeout(() => {
            window.location.href = url  // Redirects to ANY URL
        }, 3000)
    }
}, [url])
```

---

## Key Features

### 1. URL Parameter Reflection
All input fields sync with URL query parameters for easy fuzzing:
- **Search**: `?q=`
- **Comments**: `?comment=`
- **Portal**: `?username=`
- **Newsletter**: `?email=`
- **Notices**: `?file=`
- **Redirect**: `?url=`

**Implementation Pattern**:
```javascript
const [searchParams, setSearchParams] = useSearchParams()
const [input, setInput] = useState(searchParams.get('param') || '')

// Update URL only on submit (not while typing)
const handleSubmit = (e) => {
    e.preventDefault()
    setSearchParams({ param: input })
}
```

### 2. Toast Notifications
Success/error messages appear as non-blocking toast notifications:
- **Position**: Top-right corner
- **Animation**: Slide in from right
- **Behavior**: Non-blocking (can interact with page)
- **Close**: Manual close button

**CSS**:
```css
.popup-overlay {
    position: fixed;
    top: 20px;
    right: 20px;
    pointer-events: none;
}

.popup-content {
    width: 350px;
    animation: slideInToast 0.4s forwards;
    pointer-events: auto;
}
```

### 3. Responsive Design
- Mobile-friendly layout
- Adaptive navigation
- Touch-optimized interactions

### 4. Educational Content
Each vulnerability page includes:
- **Attack Context**: Why test this endpoint?
- **Business Impact**: Real-world consequences
- **Sample Payloads**: Click-to-test examples
- **Mitigation Strategies**: How to fix the vulnerability

---

## Development Workflow

### Local Development
```bash
# Install dependencies
npm install

# Run dev server (port 3000)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Docker Development
```bash
# Build and run
npm run docker:up

# View logs
npm run docker:logs

# Stop
npm run docker:down

# Rebuild
npm run docker:build
```

### Vercel Deployment
- **Automatic**: Pushes to `main` branch trigger deployment
- **Manual**: `vercel deploy` (requires Vercel CLI)
- **Configuration**: `vercel.json`

**Key Vercel Settings**:
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "git": {
    "deploymentEnabled": {
      "main": true
    }
  }
}
```

---

## Configuration Files

### vite.config.js
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

### vercel.json
- **Rewrites**: SPA routing with API exclusion
- **Headers**: CORS, security headers
- **Git**: Deploy only from `main` branch

### docker-compose.yml
- **Service**: `web`
- **Port**: `3000:80`
- **Health Check**: HTTP ping
- **Network**: `vuln-network`

### Dockerfile
- **Stage 1**: Node.js builder (npm install + build)
- **Stage 2**: Nginx server (serve static files)
- **Port**: 80
- **User**: Non-root (nginx)

---

## Design Decisions

### Why React + Vite?
- **Modern**: Latest React features and fast HMR
- **Lightweight**: No heavy frameworks
- **Flexible**: Easy to add new vulnerabilities
- **Educational**: Clear component structure

### Why Serverless Functions?
- **Scalability**: Auto-scaling on Vercel
- **Simplicity**: No server management
- **Cost**: Free tier for testing
- **Realistic**: Mimics modern web architectures

### Why Custom CSS?
- **Control**: Full styling control
- **Learning**: No framework abstractions
- **Performance**: No unused CSS
- **Simplicity**: Easy to understand

### Why Both GET and POST?
- **Realism**: Real apps use both methods
- **Diversity**: Tests different attack vectors
- **Education**: Shows method-specific vulnerabilities
- **Scanner Testing**: Comprehensive tool testing

---

## Common Tasks

### Adding a New Vulnerability

1. **Create API Endpoint**: `api/new-vuln.js`
```javascript
export default function handler(req, res) {
    res.setHeader('Access-Control-Allow-Origin', '*')
    // Implement vulnerability
}
```

2. **Create Page Component**: `src/pages/NewVuln.jsx`
```javascript
function NewVuln() {
    const [searchParams, setSearchParams] = useSearchParams()
    // Implement UI
}
```

3. **Add Route**: `src/App.jsx`
```javascript
<Route path="/new-vuln" element={<NewVuln />} />
```

4. **Update Navigation**: `src/components/Header.jsx`
```javascript
<Link to="/new-vuln">New Vuln</Link>
```

5. **Document**: Add to `docs/VULNERABILITY_REPORT.md`

### Modifying Existing Vulnerability

1. **Locate Files**:
   - API: `api/[endpoint].js`
   - UI: `src/pages/[Page].jsx`

2. **Update Logic**: Modify vulnerability behavior

3. **Test**: Verify exploit still works

4. **Document**: Update vulnerability report

### Updating Styles

1. **Global**: `src/index.css`
2. **Component**: `src/pages/[Page].css`
3. **Pattern**: Use CSS variables for consistency

---

## Testing

### Manual Testing
1. Navigate to each page
2. Try sample payloads
3. Verify vulnerability triggers
4. Check URL parameter reflection

### Automated Testing
```bash
# XSS
curl "http://localhost:3000/api/comments?comment=<script>alert(1)</script>"

# SQLi
curl "http://localhost:3000/api/search?q=' OR '1'='1"

# LFI
curl "http://localhost:3000/api/notices?file=../../../etc/passwd"

# CRLF
curl -X POST http://localhost:3000/api/newsletter \
  -H "Content-Type: application/json" \
  -d '{"email":"test\r\nSet-Cookie: admin=true"}'
```

### Scanner Testing
Use tools like:
- OWASP ZAP
- Burp Suite
- Nikto
- SQLMap
- Custom scanners (e.g., RaidScanner)

---

## Troubleshooting

### Common Issues

**Issue**: API endpoints return 404
- **Cause**: Vercel routing misconfigured
- **Fix**: Check `vercel.json` rewrites

**Issue**: XSS not executing
- **Cause**: Browser XSS protection
- **Fix**: Use different payload or disable protection

**Issue**: Docker build fails
- **Cause**: Missing dependencies
- **Fix**: Run `npm install` before building

**Issue**: URL parameters not updating
- **Cause**: Missing `setSearchParams` call
- **Fix**: Ensure `handleSubmit` calls `setSearchParams`

---

## Security Considerations

### What NOT to Do
- ❌ Deploy to production
- ❌ Use real credentials
- ❌ Connect to real databases
- ❌ Expose to internet without firewall
- ❌ Use for unauthorized testing

### What TO Do
- ✅ Use in isolated environments
- ✅ Test with dummy data
- ✅ Obtain proper authorization
- ✅ Document findings
- ✅ Practice responsible disclosure

---

## Future Enhancements

### Planned Features
- [ ] More vulnerabilities (XXE, SSRF, Deserialization)
- [ ] API documentation (Swagger/OpenAPI)
- [ ] Difficulty levels (Easy, Medium, Hard)
- [ ] Hints and walkthroughs
- [ ] Scoring system
- [ ] Multi-language support

### Contribution Ideas
- Add new vulnerability types
- Improve UI/UX
- Add more educational content
- Create video tutorials
- Develop companion scanner tool

---

## References

### OWASP Resources
- [OWASP Top 10 2021](https://owasp.org/Top10/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [OWASP Cheat Sheets](https://cheatsheetseries.owasp.org/)

### Similar Projects
- [DVWA](https://github.com/digininja/DVWA) - Damn Vulnerable Web Application
- [WebGoat](https://github.com/WebGoat/WebGoat) - OWASP WebGoat
- [Juice Shop](https://github.com/juice-shop/juice-shop) - OWASP Juice Shop

### Learning Resources
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [HackTheBox](https://www.hackthebox.com/)
- [TryHackMe](https://tryhackme.com/)

---

## Changelog

### Version 1.0 (2025-12-03)
- Initial standalone release
- Separated from RaidScanner project
- 7 vulnerability types implemented
- Docker support added
- Comprehensive documentation created

---

## Contact

**Author**: Zahid Hasan  
**GitHub**: [@zahidoverflow](https://github.com/zahidoverflow)  
**Project**: Final Year Project - Security Scanner Development  
**Institution**: Institute of Science and Technology (IST)

---

**End of Context File**

This file provides comprehensive context for AI assistants to understand and work with the Damn Vulnerable University codebase effectively.
