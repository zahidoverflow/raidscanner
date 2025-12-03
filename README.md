# 🎓 Damn Vulnerable University (DVU)

**An intentionally vulnerable web application for security testing and education**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Vercel](https://img.shields.io/badge/Vercel-Deployed-black.svg)](https://vercel.com)

> ⚠️ **WARNING**: This application contains deliberate security vulnerabilities. **DO NOT** deploy in production or expose to untrusted networks!

---

## 📋 Table of Contents

- [About](#about)
- [Live Demo](#live-demo)
- [Vulnerabilities](#vulnerabilities)
- [Technology Stack](#technology-stack)
- [Quick Start](#quick-start)
- [Docker Deployment](#docker-deployment)
- [Local Development](#local-development)
- [API Endpoints](#api-endpoints)
- [Testing Guide](#testing-guide)
- [Security Disclaimer](#security-disclaimer)
- [License](#license)

---

## 🎯 About

**Damn Vulnerable University (DVU)** is a modern, intentionally vulnerable web application designed for:

- 🔍 **Security Testing**: Practice vulnerability scanning and penetration testing
- 📚 **Education**: Learn about common web vulnerabilities (OWASP Top 10)
- 🛠️ **Tool Development**: Test and develop security scanning tools
- 🎓 **Training**: Hands-on cybersecurity training for students and professionals

DVU simulates a university website with realistic features and common vulnerabilities found in real-world applications.

---

## 🌐 Live Demo

**URL**: [https://ist-edu-bd.vercel.app](https://ist-edu-bd.vercel.app)

The application is deployed on Vercel and accessible for testing. All vulnerabilities are functional and can be exploited via the web interface or API endpoints.

---

## 🐛 Vulnerabilities

DVU implements **7 major vulnerability types** across **GET and POST** request methods:

| # | Vulnerability | Endpoint | Method | Severity | OWASP |
|---|--------------|----------|--------|----------|-------|
| 1 | **XSS (Reflected)** | `/api/comments?comment=` | GET | High | A07:2021 |
| 2 | **XSS (Stored)** | `/api/comments` | POST | Critical | A07:2021 |
| 3 | **SQL Injection (Search)** | `/api/search?q=` | GET | High | A03:2021 |
| 4 | **SQL Injection (Login)** | `/api/portal` | POST | Critical | A03:2021 |
| 5 | **CRLF Injection** | `/api/newsletter` | POST | Medium | A03:2021 |
| 6 | **LFI (Path Traversal)** | `/api/notices?file=` | GET | High | A01:2021 |
| 7 | **Open Redirect** | `/api/redirect?url=` | GET | Medium | A01:2021 |

### Attack Vector Distribution
- **GET-based**: 4 vulnerabilities (XSS reflected, LFI, Open Redirect, SQLi search)
- **POST-based**: 3 vulnerabilities (XSS stored, SQLi portal, CRLF)

For detailed vulnerability analysis, see [`docs/VULNERABILITY_REPORT.md`](docs/VULNERABILITY_REPORT.md)

---

## 🛠️ Technology Stack

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **React Router v6** - Client-side routing
- **Axios** - HTTP client
- **Custom CSS** - Styling (no frameworks)

### Backend
- **Vercel Serverless Functions** - API endpoints
- **Node.js** - Runtime environment

### Deployment
- **Vercel** - Cloud hosting
- **Docker** - Containerization
- **Nginx** - Production web server

---

## 🚀 Quick Start

### Prerequisites
- **Node.js** 18+ and npm
- **Docker** (optional, for containerized deployment)
- **Git**

### Clone Repository
```bash
git clone https://github.com/zahidoverflow/damn-vulnerable-university.git
cd damn-vulnerable-university
```

### Install Dependencies
```bash
npm install
```

### Run Development Server
```bash
npm run dev
```

Visit: `http://localhost:3000`

---

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and start
npm run docker:up

# Or manually
docker compose up -d
```

Visit: `http://localhost:3000`

### Using Docker CLI

```bash
# Build image
docker build -t damn-vulnerable-university .

# Run container
docker run -d -p 3000:80 --name dvu damn-vulnerable-university
```

### Docker Commands

```bash
# View logs
npm run docker:logs

# Stop containers
npm run docker:down

# Restart
npm run docker:restart

# Rebuild
npm run docker:build
```

---

## 💻 Local Development

### Development Mode
```bash
npm run dev
```
- Hot reload enabled
- Runs on `http://localhost:3000`
- API proxy configured for `/api` routes

### Build for Production
```bash
npm run build
```
- Outputs to `dist/` directory
- Optimized and minified

### Preview Production Build
```bash
npm run preview
```

---

## 🔌 API Endpoints

All API endpoints are serverless functions deployed on Vercel. They can be tested directly or via the web interface.

### 1. XSS - Reflected (GET)
```bash
GET /api/comments?comment=<script>alert(1)</script>
```

### 2. XSS - Stored (POST)
```bash
POST /api/comments
Content-Type: application/json

{
  "comment": "<img src=x onerror=alert(document.cookie)>",
  "author": "Attacker"
}
```

### 3. SQL Injection - Search (GET)
```bash
GET /api/search?q=' OR '1'='1
```

### 4. SQL Injection - Login (POST)
```bash
POST /api/portal
Content-Type: application/json

{
  "username": "admin' OR '1'='1' --",
  "password": "anything"
}
```

### 5. CRLF Injection (POST)
```bash
POST /api/newsletter
Content-Type: application/json

{
  "email": "test@test.com\r\nSet-Cookie: admin=true"
}
```

### 6. LFI - Path Traversal (GET)
```bash
GET /api/notices?file=../../../etc/passwd
```

### 7. Open Redirect (GET)
```bash
GET /api/redirect?url=//evil.com
```

---

## 🧪 Testing Guide

### Manual Testing

1. **Navigate** to the live demo or local instance
2. **Explore** each page (Home, Portal, Search, Comments, etc.)
3. **Test** vulnerabilities using the sample payloads provided in the UI
4. **Observe** the vulnerable behavior (XSS execution, SQL errors, etc.)

### Automated Testing

Use security scanners like:
- **OWASP ZAP**
- **Burp Suite**
- **Nikto**
- **SQLMap**
- **Custom scanners**

Example with `curl`:
```bash
# Test XSS
curl "https://ist-edu-bd.vercel.app/api/comments?comment=<script>alert(1)</script>"

# Test SQLi
curl "https://ist-edu-bd.vercel.app/api/search?q=' OR '1'='1"

# Test LFI
curl "https://ist-edu-bd.vercel.app/api/notices?file=../../../etc/passwd"
```

### URL Parameter Fuzzing

All input fields automatically update the URL query parameters, making it easy to:
- Copy URLs for testing
- Share specific test cases
- Fuzz parameters with automated tools

---

## ⚠️ Security Disclaimer

### **INTENTIONALLY VULNERABLE**

This application is designed to be vulnerable for:
- Security testing
- Educational demonstrations
- Scanner development
- Penetration testing practice

### **DO NOT:**
- ❌ Deploy in production
- ❌ Use with real data
- ❌ Expose to untrusted networks
- ❌ Use real credentials
- ❌ Connect to production databases

### **Legal Notice**

This tool is for **authorized testing only**. Unauthorized access to computer systems is illegal. Always obtain proper authorization before testing any system.

---

## 📁 Project Structure

```
damn-vulnerable-university/
├── api/                    # Vercel Serverless Functions
│   ├── comments.js        # XSS (Reflected & Stored)
│   ├── search.js          # SQL Injection (Search)
│   ├── portal.js          # SQL Injection (Login)
│   ├── newsletter.js      # CRLF Injection
│   ├── notices.js         # LFI (Path Traversal)
│   └── redirect.js        # Open Redirect
├── src/
│   ├── components/        # React components
│   ├── pages/            # Page components
│   ├── App.jsx           # Main app component
│   └── main.jsx          # Entry point
├── public/               # Static assets
├── docs/                 # Documentation
│   ├── VULNERABILITY_REPORT.md
│   └── CONTEXT.md        # LLM context file
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── nginx.conf           # Nginx configuration
├── vercel.json          # Vercel deployment config
└── package.json         # Dependencies

```

---

## 📚 Documentation

- **[Vulnerability Report](docs/VULNERABILITY_REPORT.md)** - Detailed analysis of each vulnerability
- **[LLM Context](docs/CONTEXT.md)** - Comprehensive project context for AI assistants
- **[Vercel Deployment](vercel.json)** - Deployment configuration

---

## 🤝 Contributing

Contributions are welcome! If you'd like to add new vulnerabilities or improve existing ones:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Zahid Hasan**
- GitHub: [@zahidoverflow](https://github.com/zahidoverflow)
- Project: Final Year Project - Security Scanner Development

---

## 🙏 Acknowledgments

- Inspired by **DVWA** (Damn Vulnerable Web Application)
- Built for educational purposes at **Institute of Science and Technology (IST)**
- OWASP Top 10 vulnerability references

---

## 📞 Support

For issues, questions, or suggestions:
- Open an [Issue](https://github.com/zahidoverflow/damn-vulnerable-university/issues)
- Submit a [Pull Request](https://github.com/zahidoverflow/damn-vulnerable-university/pulls)

---

**Remember**: *Ethical hacking is not a crime, it's a skill!* 🛡️

Use this tool responsibly and always with proper authorization.
