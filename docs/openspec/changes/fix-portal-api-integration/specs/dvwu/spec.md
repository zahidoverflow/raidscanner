## MODIFIED Requirements

### Requirement: Authentication Bypass via SQLi
The system SHALL validate login credentials via the backend API and detect SQL injection attempts.

#### Scenario: Frontend calls backend API
- **WHEN** user submits login form with any credentials
- **THEN** frontend SHALL POST to `/api/portal` with username and password
- **AND** parse HTML response to determine success/failure

#### Scenario: SQLi success detection
- **WHEN** backend response contains "Authentication Bypass Successful" or "SQL Injection Detected"
- **THEN** frontend SHALL navigate to dashboard with SQLi user data:
  - name: "SQL Injection User"
  - student_id: "BYPASSED"
  - role: "Administrator (via SQLi)"

#### Scenario: Valid credentials success
- **WHEN** backend response has status 200 and does not contain "Login Failed"
- **THEN** frontend SHALL navigate to dashboard with legitimate user data

#### Scenario: Login failure
- **WHEN** backend response contains "Login Failed" or "Invalid"
- **THEN** frontend SHALL display "Invalid credentials" error message

#### Scenario: Network error handling
- **WHEN** API call fails due to network error
- **THEN** frontend SHALL display "Network error. Please try again."
- **AND** log error to console for debugging

#### Scenario: Loading state
- **WHEN** API call is in progress
- **THEN** frontend SHALL disable submit button
- **AND** show loading indicator

## REMOVED Requirements

### Requirement: Client-side SQLi Detection (REMOVED)
~~The frontend SHALL check for exact string match `' OR '1'='1' --` for SQLi detection.~~

**Reason**: Replaced with API-based detection for consistency
**Migration**: All SQLi testing now goes through backend API
