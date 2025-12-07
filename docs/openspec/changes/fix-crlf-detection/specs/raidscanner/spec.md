## MODIFIED Requirements

### Requirement: HTTP Response Splitting Detection
The system SHALL detect CRLF injection using multiple detection methods:
1. HTTP header injection (Set-Cookie with injected value)
2. Custom indicator headers (X-CRLF-Injection)
3. Response body pattern matching for CRLF-related phrases

#### Scenario: Header injection detection (existing)
- **WHEN** response has `Set-Cookie: crlf=injection` header
- **THEN** mark as vulnerable with detection_method='header_injection'

#### Scenario: Indicator header detection (new)
- **WHEN** response has `X-CRLF-Injection` header present
- **THEN** mark as vulnerable with detection_method='indicator_header'

#### Scenario: Body-based detection (new)
- **WHEN** response body contains CRLF indicator phrases (case-insensitive):
  - "crlf injection"
  - "http response splitting"
  - "header injection detected"
  - "response splitting detected"
- **THEN** mark as vulnerable with detection_method='body_indicator'

#### Scenario: Detection priority
- **WHEN** multiple detection methods match
- **THEN** use first matching method (header > indicator > body)

#### Scenario: No vulnerability found
- **WHEN** none of the detection methods match
- **THEN** mark as safe (vulnerable=false)
