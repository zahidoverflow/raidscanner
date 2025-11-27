# IST Vulnerable Web Application

⚠️ **WARNING: INTENTIONALLY VULNERABLE APPLICATION** ⚠️

This is a deliberately insecure web application created for educational purposes to test the RaidScanner vulnerability scanner.

## 🎓 About

Institute of Science and Technology (IST) - A fictional university website built with React + Vite with intentional security vulnerabilities for testing purposes.

## 🛠️ Tech Stack

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **CSS3** - Styling

## 🐛 Intentional Vulnerabilities

This application contains the following vulnerabilities for testing:

### 1. SQL Injection (SQLi)
- **Location**: `/portal/login` - Login form
- **Location**: `/search?q=` - Course search
- **Location**: `/api/students?department=` - API endpoint
- **Test Payload**: `' OR '1'='1' --`

### 2. Local File Inclusion (LFI)
- **Location**: `/files?file=` - Document viewer
- **Test Payload**: `../../../../etc/passwd`

### 3. Cross-Site Scripting (XSS)
- **Status**: Framework-protected (React escapes by default)
- **Note**: Educational demonstration of React's built-in XSS protection

## 🚀 Quick Start

### Local Development
```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

Visit: http://localhost:3000

### Build for Production
```bash
npm run build
npm run preview
```

### Deploy to Vercel
1. Push to GitHub (lab branch)
2. Import project in Vercel
3. Deploy automatically

## 📝 Test URLs for RaidScanner

### SQL Injection Tests
```
http://localhost:3000/portal (Login form)
http://localhost:3000/search?q=test
```

### LFI Tests
```
http://localhost:3000/files?file=syllabus.txt
http://localhost:3000/files?file=../../../etc/passwd (path traversal)
```

## 🎯 Features

- **Student Portal**: Login system with vulnerable authentication
- **Course Catalog**: Browse available courses
- **Search Function**: Vulnerable search implementation
- **File Viewer**: Document access with LFI vulnerability
- **News Section**: Campus news and announcements
- **API Endpoints**: RESTful API with SQL injection points

## 📚 Sample Credentials

```
Student ID: IST2021001
Password: password123

Admin:
Student ID: IST2020000
Password: admin123
```

## ⚠️ Disclaimer

**DO NOT deploy this application in a production environment!**

This application is:
- ❌ NOT secure
- ❌ NOT for production use
- ✅ For educational purposes only
- ✅ For security testing with RaidScanner
- ✅ For learning about web vulnerabilities

## 📖 Educational Purpose

This application is part of a university final year project to demonstrate:
1. Common web application vulnerabilities
2. Automated vulnerability scanning techniques
3. Security testing methodologies
4. Secure coding practices (by showing what NOT to do)

## 🔒 Security Notes

All vulnerabilities are intentional and documented. Use this application only in controlled environments for:
- Security training
- Scanner testing
- Penetration testing practice
- Academic research

## 📜 License

MIT License - Educational Use Only
