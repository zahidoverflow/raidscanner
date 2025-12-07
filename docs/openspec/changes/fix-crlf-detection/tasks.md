# Tasks: Fix CRLF Detection

## 1. Update Scanner CRLF Detection Logic
- [ ] 1.1 Open `raidscanner/core/scanner_engine.py`
- [ ] 1.2 Locate `check_crlf` function (around line 500)
- [ ] 1.3 Add response body pattern matching after header check
- [ ] 1.4 Add detection patterns for common CRLF indicators:
  - "CRLF Injection Detected"
  - "HTTP Response Splitting"
  - "header injection"
  - Presence of CRLF characters in response body context

## 2. Update DVWU CRLF Response (Optional Enhancement)
- [ ] 2.1 Open `damn-vulnerable-web-university/server.cjs`
- [ ] 2.2 Locate `/api/newsletter` handler (around line 271)
- [ ] 2.3 Add custom header injection: `X-CRLF-Injection: detected`
- [ ] 2.4 Keep existing HTML response for visual feedback

## 3. Testing
- [ ] 3.1 Start both applications
- [ ] 3.2 Run CRLF scan against DVWU newsletter endpoint
- [ ] 3.3 Verify vulnerabilities are detected (expected: > 0)
- [ ] 3.4 Check generated report contains vulnerable URLs

## 4. Update Documentation
- [ ] 4.1 Update scanner spec to document body-based detection
- [ ] 4.2 Update DVWU spec to document header injection behavior
