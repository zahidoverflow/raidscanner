# Fix CRLF Detection Mismatch

## Why
The CRLF scanner reports 0 vulnerabilities when scanning DVWU, even though DVWU correctly detects and reports CRLF injection attempts. This is a critical false negative that undermines the scanner's reliability.

**Root Cause**: The scanner checks only for HTTP header injection (`Set-Cookie` header), but DVWU simulates CRLF detection by returning an HTML response body indicating the vulnerability was found - it doesn't actually inject headers.

## What Changes
- **RaidScanner**: Add response body pattern matching to CRLF detection logic
- **DVWU** (optional): Can also be enhanced to actually inject a custom header for more realistic simulation

## Impact
- Affected specs: `raidscanner` (CRLF Scanner feature)
- Affected code: `raidscanner/core/scanner_engine.py` (scan_crlf method)
- Risk: Low - additive change, doesn't break existing detection logic
