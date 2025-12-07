# Tasks: Fix Report Type Classification

## 1. Update Report Type Detection Logic
- [ ] 1.1 Open `raidscanner/app.py`
- [ ] 1.2 Locate `get_reports` function (around line 298)
- [ ] 1.3 Reorder type checks: specific types first, generic last
- [ ] 1.4 Use prefix matching instead of substring matching
- [ ] 1.5 Handle "openredirect" as the full pattern for OR type

## 2. Testing
- [ ] 2.1 Run various scans to generate reports of each type
- [ ] 2.2 Call `/api/reports` endpoint
- [ ] 2.3 Verify each report type is correctly classified:
  - `lfi_report_*` -> type: "lfi"
  - `sqli_report_*` -> type: "sqli"
  - `xss_report_*` -> type: "xss"
  - `openredirect_report_*` -> type: "or"
  - `crlf_report_*` -> type: "crlf"
- [ ] 2.4 Check reports page UI shows correct types

## 3. Update Documentation
- [ ] 3.1 Update raidscanner spec with correct type detection logic
