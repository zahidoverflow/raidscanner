# Damn Vulnerable Web University (DVWU) - Specification

## Overview
DVWU is an intentionally vulnerable web application designed for security testing and education. It simulates a university website with multiple vulnerability types for scanner testing.

---

## Feature: XSS Vulnerability (Comments API)

### Requirement: Reflected XSS via GET Parameter
The system SHALL reflect user input from URL parameters without sanitization.

#### Scenario: Script tag injection via GET
- **WHEN** user visits `/api/comments?comment=<script>alert(1)</script>`
- **THEN** the script tag is rendered in the HTML response without encoding

#### Scenario: Frontend reflected XSS
- **WHEN** user visits `/comments?comment=<script>alert(1)</script>`
- **THEN** the React frontend renders the payload via `dangerouslySetInnerHTML`

**Status**: WORKING (Backend: Yes, Frontend: Yes)

---

### Requirement: Stored XSS via POST Submission
The system SHALL store and display user comments without sanitization.

#### Scenario: Stored XSS persistence
- **WHEN** user POSTs `{"comment": "<script>alert(1)</script>", "author": "test"}` to `/api/comments`
- **THEN** the comment is stored and returned with unescaped HTML

**Status**: WORKING (Backend: Yes, Frontend: Yes via localStorage)

---

## Feature: SQL Injection Vulnerability (Portal API)

### Requirement: Authentication Bypass via SQLi
The system SHALL simulate SQL injection vulnerability on login form.

#### Scenario: Backend SQLi detection
- **WHEN** user sends `username=admin'--&password=anything` to `/api/portal`
- **THEN** the response shows "Authentication Bypass Successful!" with admin user data

#### Scenario: Frontend SQLi detection
- **WHEN** user enters SQLi payload in the portal login form
- **THEN** the frontend checks for exact string `' OR '1'='1' --` only

**Status**: PARTIAL BUG
- Backend: WORKING - Detects various SQLi patterns (`'`, `--`, `OR`, `1=1`)
- Frontend: BUG - Only accepts exact string `' OR '1'='1' --`, doesn't call backend API

**Bug Details** (`Portal.jsx:28-31`):
```javascript
// Frontend uses hardcoded check instead of calling backend API
if (studentId === "' OR '1'='1' --" || ...) {
  // This only matches the exact string
}
```

---

## Feature: SQL Injection Vulnerability (Search API)

### Requirement: Error-based SQLi on Search
The system SHALL expose SQL error messages when injection is detected.

#### Scenario: SQL error exposure
- **WHEN** user sends `?q='` to `/api/search`
- **THEN** response shows SQL syntax error with leaked database schema

**Status**: WORKING (Backend: Yes, Frontend: Unknown - not tested)

---

## Feature: Local File Inclusion (Notices API)

### Requirement: Path Traversal Detection
The system SHALL simulate LFI vulnerability when path traversal is detected.

#### Scenario: /etc/passwd disclosure
- **WHEN** user sends `?file=../../../etc/passwd` to `/api/notices`
- **THEN** response contains simulated passwd file content

#### Scenario: Windows hosts file disclosure
- **WHEN** user sends `?file=/windows/system32/drivers/etc/hosts`
- **THEN** response contains simulated hosts file content

**Status**: WORKING (Backend: Yes, Frontend: Yes - properly connected)

---

## Feature: Open Redirect Vulnerability

### Requirement: Unvalidated URL Redirect
The system SHALL redirect to any URL without validation.

#### Scenario: External redirect
- **WHEN** user sends `?url=https://evil.com` to `/api/redirect`
- **THEN** response has `Location: https://evil.com` header with 302 status

**Status**: WORKING (Backend: Yes)

---

## Feature: CRLF Injection (Newsletter API)

### Requirement: HTTP Response Splitting Detection
The system SHALL detect CRLF characters in input.

#### Scenario: CRLF detection response
- **WHEN** user sends `?email=test@test.com%0d%0aInjected-Header:value` to `/api/newsletter`
- **THEN** response shows "CRLF Injection Detected" with the split content displayed

**Status**: PARTIAL BUG
- Backend: WORKING - Detects CRLF but returns HTML response (not actual header injection)
- Scanner: BUG - Scanner checks for `Set-Cookie` header but backend doesn't inject headers

**Bug Details**: The backend simulates CRLF detection by returning an HTML page, not by actually injecting headers. This causes the scanner to report 0 vulnerabilities even though the backend detects the attack.

---

## Architecture

### Backend Stack
- **Runtime**: Node.js with Express.js
- **Port**: 3000
- **Dependencies**: express, cors

### Frontend Stack
- **Framework**: React 18 with Vite
- **Router**: react-router-dom v6
- **State**: localStorage for stored comments

### API Endpoints
| Endpoint | Method | Vulnerability |
|----------|--------|---------------|
| `/api/comments` | GET/POST | XSS (Reflected/Stored) |
| `/api/portal` | GET/POST | SQLi (Auth Bypass) |
| `/api/search` | GET/POST | SQLi (Error-based) |
| `/api/notices` | GET | LFI (Path Traversal) |
| `/api/redirect` | GET | Open Redirect |
| `/api/newsletter` | GET/POST | CRLF Injection |

---

## Known Issues

### Issue 1: Portal Frontend Doesn't Call Backend API
**Severity**: High
**Location**: `src/pages/Portal.jsx:19-45`
**Description**: The frontend login form uses client-side validation instead of calling the backend `/api/portal` API. This means the SQLi detection only works for exact string matches.
**Fix Required**: Modify `handleSubmit` to call the backend API and parse the response.

### Issue 2: CRLF Vulnerability Simulation Is Incomplete
**Severity**: Medium
**Location**: `server.cjs:271-309`
**Description**: The CRLF endpoint detects injection but returns HTML instead of actually injecting headers. This makes it undetectable by the scanner.
**Fix Options**:
1. Make backend actually inject headers for scanner detection
2. OR modify scanner to check response body for "CRLF Injection Detected"

### Issue 3: Search Frontend Not Tested
**Severity**: Low
**Description**: The Search page (`/search`) was not fully tested for frontend-backend integration.
