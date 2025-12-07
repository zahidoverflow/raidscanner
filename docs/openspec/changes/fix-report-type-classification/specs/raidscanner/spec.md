## MODIFIED Requirements

### Requirement: Report Listing and Download
The system SHALL correctly classify scan reports by type based on filename prefix.

#### Scenario: LFI report classification
- **WHEN** report filename starts with "lfi_" or contains "lfi_report"
- **THEN** report type SHALL be "lfi"

#### Scenario: SQLi report classification
- **WHEN** report filename starts with "sqli_" or contains "sql"
- **THEN** report type SHALL be "sqli"

#### Scenario: XSS report classification
- **WHEN** report filename starts with "xss_"
- **THEN** report type SHALL be "xss"

#### Scenario: Open Redirect report classification
- **WHEN** report filename starts with "openredirect_" or "or_"
- **THEN** report type SHALL be "or"
- **AND** SHALL NOT match on substring "or" within other words like "report"

#### Scenario: CRLF report classification
- **WHEN** report filename starts with "crlf_"
- **THEN** report type SHALL be "crlf"

#### Scenario: Unknown report type
- **WHEN** report filename does not match any known pattern
- **THEN** report type SHALL be "unknown"

#### Scenario: Classification priority (new)
- **WHEN** classifying report type
- **THEN** check patterns in this order:
  1. CRLF (most specific)
  2. XSS
  3. SQLi
  4. LFI
  5. Open Redirect (use "openredirect" or "or_" prefix, not substring)
  6. Unknown (fallback)
