# Fix Report Type Misclassification

## Why
CRLF scan reports are incorrectly classified as "OR" (Open Redirect) type in the reports list. This happens because the string matching logic checks for `'or' in name.lower()` which matches the "or" in "rep**or**t" before checking for CRLF.

**Example**:
- Report name: `crlf_report_20251207_142030`
- Expected type: `crlf`
- Actual type: `or` (because "report" contains "or")

## What Changes
- **RaidScanner**: Reorder and improve the scan type detection logic in `app.py`
- Use more specific patterns that don't have false positive matches

## Impact
- Affected specs: `raidscanner` (Report Management feature)
- Affected code: `raidscanner/app.py` (get_reports function)
- Risk: Very low - simple string matching fix
