# Design: Fix Report Type Classification

## Context
The current implementation uses simple substring matching with `'or' in name.lower()`, which incorrectly matches "report" and causes CRLF reports to be classified as Open Redirect.

## Goals
- Correct report type classification for all scan types
- Simple, maintainable code
- No false positives

## Non-Goals
- Support for custom/external report types
- Changing report naming convention

## Decisions

### Decision 1: Use Prefix Matching
**What**: Check if filename starts with type prefix instead of substring matching
**Why**: More precise, avoids false positives
**Trade-off**: Requires consistent naming (already in place)

### Decision 2: Check Specific Types First
**What**: Order checks from most specific to most generic
**Why**: Prevents more generic patterns from matching first

### Decision 3: Use "openredirect" Pattern for OR
**What**: Match on "openredirect_" prefix instead of "or" substring
**Why**: The report generator already uses "openredirect_report_" naming

## Implementation

### Current Code (Buggy)
```python
# app.py:312-322
scan_type = 'unknown'
if 'lfi' in name.lower():
    scan_type = 'lfi'
elif 'sqli' in name.lower() or 'sql' in name.lower():
    scan_type = 'sqli'
elif 'xss' in name.lower():
    scan_type = 'xss'
elif 'or' in name.lower():       # BUG: matches "report"
    scan_type = 'or'
elif 'crlf' in name.lower():     # Never reached for CRLF
    scan_type = 'crlf'
```

### Fixed Code
```python
# Determine scan type from filename using prefix matching
scan_type = 'unknown'
name_lower = name.lower()

# Check most specific patterns first
if name_lower.startswith('crlf_') or 'crlf_report' in name_lower:
    scan_type = 'crlf'
elif name_lower.startswith('xss_') or 'xss_report' in name_lower:
    scan_type = 'xss'
elif name_lower.startswith('sqli_') or 'sqli_report' in name_lower or 'sql_' in name_lower:
    scan_type = 'sqli'
elif name_lower.startswith('lfi_') or 'lfi_report' in name_lower:
    scan_type = 'lfi'
elif name_lower.startswith('openredirect_') or name_lower.startswith('or_'):
    scan_type = 'or'
```

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| New naming conventions break | Use both prefix AND contains pattern |
| Order matters | Well-documented, tested |

## Migration Plan
1. Deploy code change
2. Existing reports will be reclassified on next API call
3. No data migration needed

## Open Questions
- Should we add a `scan_type` field to the JSON report for authoritative classification?
