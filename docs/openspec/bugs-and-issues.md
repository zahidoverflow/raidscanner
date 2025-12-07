# Project Analysis Summary - Bugs and Issues

## Test Date: 2025-12-07

## Executive Summary

Both projects (DVWU vulnerable app and RaidScanner) are **mostly functional** with some **critical bugs** that affect scanner-target compatibility. The scanner successfully detects vulnerabilities for LFI, SQLi, and Open Redirect, but fails to detect CRLF due to a mismatch between how DVWU simulates the vulnerability and how the scanner detects it.

---

## Critical Bugs

### Bug 1: CRLF Detection Mismatch (Scanner + DVWU)
**Severity**: Critical
**Impact**: CRLF scanner reports 0 vulnerabilities on DVWU

**Root Cause**:
- DVWU's `/api/newsletter` detects CRLF input but returns an **HTML response** indicating detection
- RaidScanner checks for actual **HTTP header injection** (`Set-Cookie` header)
- These approaches are incompatible

**DVWU Behavior** (`server.cjs:284-298`):
```javascript
// Returns HTML body, not injected header
if (hasCRLF) {
    return res.status(200).send(`
        <h1>CRLF Injection Detected</h1>
        <pre>X-Subscriber-Email: ${email}</pre>
    `);
}
```

**Scanner Behavior** (`scanner_engine.py:516-519`):
```python
# Only checks for header injection
if 'Set-Cookie' in response.headers:
    if 'crlf=injection' in set_cookie:
        is_vulnerable = True
```

**Fix Options**:
1. **Option A** (Fix DVWU): Make DVWU actually inject a header when CRLF is detected
2. **Option B** (Fix Scanner): Add response body pattern matching to scanner
3. **Option C** (Fix Both): Implement both for comprehensive detection

---

### Bug 2: Portal Frontend Doesn't Call Backend API
**Severity**: High
**Impact**: SQLi testing only works for exact string match on frontend

**Root Cause**: `Portal.jsx` uses client-side validation instead of calling `/api/portal`

**Current Code** (`Portal.jsx:28-31`):
```javascript
// Hardcoded string comparison instead of API call
if (studentId === "' OR '1'='1' --" || ...) {
    // Only matches exact string
}
```

**Expected Behavior**: Frontend should POST to `/api/portal` and parse the HTML response to determine success.

---

## Medium Bugs

### Bug 3: Report Type Misclassification
**Severity**: Medium
**Impact**: CRLF reports shown as "OR" type in reports list

**Root Cause**: String matching order in `app.py:312-322`
```python
if 'or' in name.lower():  # Matches "report" before "crlf"
    scan_type = 'or'
```

**Fix**: Check CRLF before OR, or use more specific patterns.

---

### Bug 4: Eventlet Python 3.13 Compatibility
**Severity**: Medium (Resolved)
**Impact**: Scanner wouldn't start on Python 3.13

**Resolution**: Upgraded eventlet from 0.36.1 to 0.40.4

**Note**: Eventlet shows deprecation warning. Consider future migration.

---

## Working Features

### DVWU (Vulnerable App)
| Feature | Backend | Frontend | Notes |
|---------|---------|----------|-------|
| XSS Reflected | OK | OK | Uses dangerouslySetInnerHTML |
| XSS Stored | OK | OK | localStorage persistence |
| SQLi Portal | OK | PARTIAL | Frontend uses hardcoded check |
| SQLi Search | OK | Not tested | - |
| LFI Notices | OK | OK | Properly connected |
| Open Redirect | OK | Not tested | - |
| CRLF Newsletter | PARTIAL | Not tested | Returns HTML, not header |

### RaidScanner
| Feature | API | Frontend | Notes |
|---------|-----|----------|-------|
| LFI Scan | OK | OK | 7/55 found on DVWU |
| SQLi Scan | OK | OK | 31/43 found on DVWU |
| XSS Scan | OK | Not tested | Requires Chrome |
| OR Scan | OK | OK | 171/241 found on DVWU |
| CRLF Scan | BUG | BUG | 0/8 found (false negative) |
| Reports | OK | PARTIAL | Type misclassification |
| WebSocket | OK | OK | Real-time progress |

---

## Recommended Fixes (Priority Order)

1. **CRLF Compatibility** - Fix scanner to detect DVWU-style CRLF response OR fix DVWU to inject headers
2. **Portal API Integration** - Connect Portal.jsx to backend API
3. **Report Classification** - Fix string matching order
4. **XSS Scanner Fallback** - Add non-Selenium detection method
5. **Documentation** - Add setup instructions for ChromeDriver

---

## Test Commands Used

```bash
# Start DVWU backend
cd damn-vulnerable-web-university && npm install && npm run build && node server.cjs

# Start RaidScanner
cd raidscanner && python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
pip install --upgrade eventlet  # For Python 3.13
python app.py

# Test DVWU APIs directly
curl "http://localhost:3000/api/comments?comment=<script>alert(1)</script>"
curl "http://localhost:3000/api/portal?username=admin'--&password=anything"
curl "http://localhost:3000/api/search?q='"
curl "http://localhost:3000/api/notices?file=../../../etc/passwd"
curl -D - "http://localhost:3000/api/redirect?url=https://evil.com"
curl "http://localhost:3000/api/newsletter?email=test%0d%0aHeader:value"

# Test Scanner APIs
curl http://localhost:5000/api/payloads
curl -X POST http://localhost:5000/api/scan/lfi -H "Content-Type: application/json" \
  -d '{"urls": ["http://localhost:3000/api/notices?file="], "threads": 3}'
```
