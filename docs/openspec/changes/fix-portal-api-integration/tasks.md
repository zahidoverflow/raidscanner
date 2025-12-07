# Tasks: Fix Portal API Integration

## 1. Modify Portal.jsx to Call Backend API
- [ ] 1.1 Open `damn-vulnerable-web-university/src/pages/Portal.jsx`
- [ ] 1.2 Import axios or use fetch for API calls
- [ ] 1.3 Modify `handleSubmit` function to POST to `/api/portal`
- [ ] 1.4 Parse HTML response to detect SQLi success indicators:
  - "Authentication Bypass Successful"
  - "SQL Injection Detected"
- [ ] 1.5 Handle both GET and POST methods (backend supports both)

## 2. Update Response Handling
- [ ] 2.1 On SQLi detection: Navigate to dashboard with injected user data
- [ ] 2.2 On valid credentials: Navigate to dashboard with normal user data
- [ ] 2.3 On failure: Show error message

## 3. Handle API Errors
- [ ] 3.1 Add try/catch for network errors
- [ ] 3.2 Show user-friendly error messages
- [ ] 3.3 Add loading state during API call

## 4. Testing
- [ ] 4.1 Test with valid credentials (IST2021001 / password123)
- [ ] 4.2 Test with SQLi payload: `admin'--`
- [ ] 4.3 Test with SQLi payload: `' OR '1'='1' --`
- [ ] 4.4 Test with SQLi payload: `admin' OR 1=1--`
- [ ] 4.5 Test with invalid credentials
- [ ] 4.6 Verify dashboard shows correct user data

## 5. Update Documentation
- [ ] 5.1 Update DVWU spec to reflect API integration
- [ ] 5.2 Document supported SQLi payloads in UI hints
