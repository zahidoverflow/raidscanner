# RaidScanner - Specification

## Overview
RaidScanner is a web-based vulnerability scanner with support for multiple vulnerability types. It provides a Flask backend with WebSocket support for real-time scan progress and a simple HTML/JS frontend.

---

## Feature: LFI (Local File Inclusion) Scanner

### Requirement: Path Traversal Detection
The system SHALL test URLs for LFI vulnerabilities using payload injection.

#### Scenario: Detect /etc/passwd exposure
- **WHEN** scanner sends LFI payloads to target URL
- **THEN** scanner detects vulnerability if response contains `root:x:0:` or other LFI indicators

#### Scenario: Report generation
- **WHEN** scan completes
- **THEN** HTML and JSON reports are saved to `/reports/` directory

**Status**: WORKING
- Backend API: `/api/scan/lfi` (POST)
- Detection: Pattern matching in response body
- Payloads: 55 payloads from `payloads/lfi-payloads.txt`
- Test Result: Found 7/55 vulnerabilities on DVWU

---

## Feature: SQLi (SQL Injection) Scanner

### Requirement: Time-based and Error-based SQLi Detection
The system SHALL detect SQLi via response time analysis and error pattern matching.

#### Scenario: Time-based detection
- **WHEN** response time exceeds 10 seconds threshold
- **THEN** mark as vulnerable (time-based SQLi)

#### Scenario: Error-based detection
- **WHEN** response contains SQL error patterns (syntax error, ORA-, etc.)
- **THEN** mark as vulnerable (error-based SQLi)

**Status**: WORKING
- Backend API: `/api/scan/sqli` (POST)
- Detection: Time threshold (10s) + error pattern matching
- Payloads: Generic SQLi payloads from `payloads/sqli/generic.txt`
- Test Result: Found 31/43 vulnerabilities on DVWU

---

## Feature: XSS (Cross-Site Scripting) Scanner

### Requirement: DOM-based XSS Detection via Selenium
The system SHALL use headless Chrome to detect XSS via alert dialogs.

#### Scenario: Alert-based detection
- **WHEN** browser shows JavaScript alert after payload injection
- **THEN** mark as vulnerable

#### Scenario: Reflection detection
- **WHEN** payload appears unescaped in page source
- **THEN** mark as vulnerable

**Status**: WORKING (requires Chrome/ChromeDriver)
- Backend API: `/api/scan/xss` (POST)
- Detection: Selenium WebDriver with alert monitoring
- Threads: Limited to 3 (Selenium resource constraints)
- Payloads: XSS payloads from `payloads/xss.txt`

---

## Feature: Open Redirect Scanner

### Requirement: Redirect URL Validation Bypass Detection
The system SHALL detect open redirects via Location header and client-side redirects.

#### Scenario: Server-side redirect detection
- **WHEN** response has Location header containing the payload
- **THEN** mark as vulnerable

#### Scenario: Client-side redirect detection (partial)
- **WHEN** response body contains JS redirect with payload
- **THEN** mark as vulnerable

**Status**: WORKING
- Backend API: `/api/scan/or` (POST)
- Detection: Location header + JS pattern matching
- Payloads: 241 payloads from `payloads/or.txt`
- Test Result: Found 171/241 vulnerabilities on DVWU

---

## Feature: CRLF Injection Scanner

### Requirement: HTTP Response Splitting Detection
The system SHALL detect CRLF injection by checking for injected headers.

#### Scenario: Header injection detection
- **WHEN** response has `Set-Cookie: crlf=injection` header
- **THEN** mark as vulnerable

**Status**: BUG - NOT DETECTING DVWU VULNERABILITY
- Backend API: `/api/scan/crlf` (POST)
- Detection: Only checks for `Set-Cookie` header injection
- Issue: DVWU returns HTML body response, not actual header injection
- Test Result: Found 0/8 vulnerabilities on DVWU (false negative)

**Bug Details** (`core/scanner_engine.py:500-520`):
```python
# Scanner only checks for header injection
if 'Set-Cookie' in response.headers:
    set_cookie = response.headers['Set-Cookie']
    if 'crlf=injection' in set_cookie:
        is_vulnerable = True
```

**Fix Required**: Add body-based detection for DVWU-style responses:
```python
# Also check response body for CRLF indicators
if 'CRLF Injection Detected' in response.text:
    is_vulnerable = True
```

---

## Feature: Report Management

### Requirement: Report Listing and Download
The system SHALL list and allow download of scan reports.

#### Scenario: List reports
- **WHEN** user visits `/api/reports`
- **THEN** returns JSON array of all reports with metadata

#### Scenario: Download report
- **WHEN** user visits `/api/reports/download?path=...`
- **THEN** returns the report file for download

**Status**: PARTIAL BUG
- Listing: WORKING
- Download: WORKING
- Issue: Report type classification is wrong for CRLF reports

**Bug Details** (`app.py:312-322`):
```python
# CRLF reports are misclassified as 'or' (Open Redirect)
if 'or' in name.lower():
    scan_type = 'or'
elif 'crlf' in name.lower():
    scan_type = 'crlf'
```
The `if 'or' in name.lower()` check matches before CRLF because "report" contains "or".

**Fix Required**: Change order or use `startswith`:
```python
if name.lower().startswith('crlf'):
    scan_type = 'crlf'
elif 'or' in name.lower() and 'report' not in name.lower():
    scan_type = 'or'
```

---

## Feature: Real-time Progress via WebSocket

### Requirement: Live Scan Progress Updates
The system SHALL emit scan progress via Socket.IO.

#### Scenario: Progress emission
- **WHEN** scan is running
- **THEN** emit `scan_progress` events with current status

#### Scenario: Completion notification
- **WHEN** scan completes
- **THEN** emit `scan_complete` event with results

**Status**: WORKING
- Events: `scan_progress`, `scan_complete`, `scan_error`
- Async: Uses eventlet for background tasks

---

## Architecture

### Backend Stack
- **Framework**: Flask 3.0.3 with Flask-SocketIO
- **Async**: eventlet 0.40.4 (upgraded from 0.36.1 for Python 3.13 compatibility)
- **Port**: 5000

### Core Components
| Component | Location | Purpose |
|-----------|----------|---------|
| `app.py` | Root | Flask app, routes, WebSocket handlers |
| `scanner_engine.py` | `core/` | Vulnerability scanning logic |
| `payload_loader.py` | `core/` | Load payloads from files |
| `report_generator.py` | `core/` | Generate HTML/JSON reports |
| `config.py` | `utils/` | Configuration management |

### API Endpoints
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Dashboard page |
| `/scanner/<type>` | GET | Scanner configuration page |
| `/reports` | GET | Reports viewer page |
| `/api/payloads` | GET | List available payloads |
| `/api/scan/lfi` | POST | Start LFI scan |
| `/api/scan/sqli` | POST | Start SQLi scan |
| `/api/scan/xss` | POST | Start XSS scan |
| `/api/scan/or` | POST | Start Open Redirect scan |
| `/api/scan/crlf` | POST | Start CRLF scan |
| `/api/reports` | GET | List reports |
| `/api/reports/download` | GET | Download report |

---

## Known Issues

### Issue 1: CRLF Scanner Cannot Detect DVWU Vulnerability
**Severity**: High
**Location**: `core/scanner_engine.py:474-570`
**Description**: The CRLF scanner only checks for actual header injection (`Set-Cookie` header), but DVWU's CRLF endpoint returns an HTML response indicating detection rather than actually injecting headers.
**Fix Required**: Add response body pattern matching for CRLF indicators.

### Issue 2: Report Type Misclassification
**Severity**: Low
**Location**: `app.py:312-322`
**Description**: CRLF reports are classified as "OR" because the string "or" appears in "report".
**Fix Required**: Reorder conditions or use more specific matching.

### Issue 3: Eventlet Deprecation Warning
**Severity**: Info
**Location**: `app.py:7`
**Description**: Eventlet shows deprecation warning. Consider migrating to alternative async framework in future.

### Issue 4: XSS Scanner Requires ChromeDriver
**Severity**: Medium
**Description**: XSS scanning requires Chrome and ChromeDriver to be installed. No graceful fallback if unavailable.

---

## Test Results Summary

| Scan Type | Vulnerabilities Found | Total Tested | Status |
|-----------|----------------------|--------------|--------|
| LFI | 7 | 55 | WORKING |
| SQLi | 31 | 43 | WORKING |
| XSS | Not tested | - | Requires Chrome |
| Open Redirect | 171 | 241 | WORKING |
| CRLF | 0 | 8 | BUG (false negative) |
