# IST Vulnerable Web Application

**Intentionally vulnerable web application for security testing and education.**

⚠️ **WARNING**: This application contains deliberate security vulnerabilities. DO NOT deploy in production!

## Purpose

This is a demonstration web application for the Institute of Science and Technology (IST) that intentionally contains common web vulnerabilities for educational purposes and security scanner testing.

## Live Demo

🌐 **URL**: https://ist-edu-bd.vercel.app

## Vulnerabilities Implemented

| # | Vulnerability | Endpoint | Method |
|---|--------------|----------|--------|
| 1 | **XSS** (Reflected) | `/api/comments?comment=` | GET |
| 2 | **SQL Injection** | `/api/search?q=` | GET |
| 3 | **SQL Injection** | `/api/portal` | POST |
| 4 | **LFI** (Path Traversal) | `/api/notices?file=` | GET |
| 5 | **Open Redirect** | `/api/redirect?url=` | GET |
| 6 | **CRLF Injection** | `/newsletter` (form) | POST |

## Technology Stack

- **Frontend**: React 18 + Vite
- **Routing**: React Router v6
- **Styling**: Custom CSS
- **Icons**: Font Awesome
- **Deployment**: Vercel (Serverless Functions)

## Local Development

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
├── api/              # Vercel Serverless Functions (vulnerable endpoints)
├── public/           # Static assets (images, favicon)
├── src/
│   ├── components/   # React components (Header, Footer)
│   ├── pages/        # Page components (Home, Portal, etc.)
│   ├── App.jsx       # Main app component
│   └── main.jsx      # Entry point
├── index.html        # HTML template
├── package.json      # Dependencies
├── vite.config.js    # Vite configuration
└── vercel.json       # Vercel deployment config
```

## API Endpoints (For Scanner Testing)

### 1. XSS - Comments
```bash
GET /api/comments?comment=<script>alert(1)</script>
```

### 2. SQL Injection - Search
```bash
GET /api/search?q=' OR '1'='1
```

### 3. SQL Injection - Login
```bash
POST /api/portal
Content-Type: application/json
{"username":"admin' OR '1'='1","password":"anything"}
```

### 4. LFI - File Inclusion
```bash
GET /api/notices?file=../../../etc/passwd
```

### 5. Open Redirect
```bash
GET /api/redirect?url=//evil.com
```

## Deployment

This application is configured for automatic deployment to Vercel:

1. Push to `lab` branch
2. Vercel auto-deploys
3. Live at: https://ist-edu-bd.vercel.app

## Security Disclaimer

⚠️ **INTENTIONALLY VULNERABLE**

This application is designed to be vulnerable for:
- Security testing
- Educational demonstrations
- Scanner development
- Penetration testing practice

**DO NOT:**
- Deploy in production
- Use with real data
- Expose to untrusted networks
- Use real credentials

## Testing with RaidScanner

This web app is designed to be tested with the RaidScanner tool (main branch):

```bash
# Clone repository
git clone https://github.com/zahidoverflow/raidscanner.git
cd raidscanner

# Checkout main branch for scanner
git checkout main

# Run scanner
docker compose run --rm raidscanner-cli

# Target: https://ist-edu-bd.vercel.app/api/[endpoint]
```

## License

MIT License - For educational purposes only

## Author

**Zahid Hasan**
- GitHub: [@zahidoverflow](https://github.com/zahidoverflow)
- Project: Final Year Project - Security Scanner Development

---

**Remember**: Ethical hacking is not a crime, it's a skill! 🛡️
