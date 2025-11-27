# IST Vulnerable Web Application

⚠️ **WARNING: INTENTIONALLY VULNERABLE APPLICATION** ⚠️

This is a deliberately insecure web application created for educational purposes to test the RaidScanner vulnerability scanner.

## 🎓 About

Institute of Science and Technology (IST) - A fictional university website with intentional security vulnerabilities for testing purposes.

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
- **Location**: `/news/:id` - News comments (when implemented)
- **Test Payload**: `<script>alert('XSS')</script>`

### 4. Open Redirect (OR)
- **Location**: `/redirect?url=`
- **Test Payload**: `https://evil.com`

### 5. CRLF Injection
- **Location**: `/download?filename=`
- **Test Payload**: `file.pdf%0d%0aContent-Type:%20text/html%0d%0a%0d%0a<script>alert('CRLF')</script>`

## 🚀 Deployment

### Vercel (Recommended)
1. Fork/clone this repository
2. Connect to Vercel
3. Deploy from the `lab` branch
4. Auto-deploys on every push

### Local Development
```bash
cd vulnerable-webapp
npm install
npm run dev
```

Visit: http://localhost:3000

## 📝 Test URLs for RaidScanner

### SQL Injection Tests
```
http://localhost:3000/portal/login
http://localhost:3000/search?q=test
http://localhost:3000/api/students?department=Computer Science
```

### LFI Tests
```
http://localhost:3000/files?file=sample.txt
```

### Open Redirect Tests
```
http://localhost:3000/redirect?url=https://google.com
```

### CRLF Tests
```
http://localhost:3000/download?filename=test.pdf
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
