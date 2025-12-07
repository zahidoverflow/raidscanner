# Design: Fix Portal API Integration

## Context
The Portal login page was implemented with client-side validation for demo purposes, but this creates inconsistency with the backend API. Users testing SQLi through the UI get different results than testing directly against the API.

## Goals
- Frontend behavior matches backend behavior exactly
- All SQLi payloads that work via API also work via UI
- Maintain educational value by showing SQLi success/failure clearly

## Non-Goals
- Changing backend SQLi detection logic
- Adding new SQLi patterns
- Implementing actual authentication

## Decisions

### Decision 1: Use Fetch API Instead of Axios
**What**: Use native `fetch()` instead of adding axios dependency
**Why**:
- axios is already in package.json but fetch is simpler for this use case
- Response is HTML, not JSON, so axios doesn't add value
- Reduces complexity
**Alternative**: Could use axios with `responseType: 'text'`

### Decision 2: Parse HTML Response for Success Detection
**What**: Check response HTML for specific phrases indicating SQLi success
**Why**: Backend returns HTML pages, not JSON
**Detection Phrases**:
- "Authentication Bypass Successful" - Indicates SQLi worked
- "SQL Injection Detected" - Confirms vulnerability
- "Login Failed" - Indicates failure

### Decision 3: Support Both GET and POST
**What**: Use POST method but URL-encode parameters
**Why**: Backend supports both, POST is more appropriate for login forms
**Implementation**:
```javascript
const response = await fetch('/api/portal', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: studentId, password })
});
```

### Decision 4: Extract User Data from Response
**What**: Parse HTML response to extract user details for dashboard
**Why**: Backend returns user info (User ID, Username, Role) in HTML
**Fallback**: Use default "SQL Injection User" data if parsing fails

## Implementation

### Modified Portal.jsx

```jsx
const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
        // Call backend API instead of client-side validation
        const response = await fetch('/api/portal', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: studentId,
                password: password
            })
        });

        const html = await response.text();

        // Check for SQLi success indicators
        const isSQLiSuccess = html.includes('Authentication Bypass Successful') ||
                              html.includes('SQL Injection Detected');

        // Check for valid login (normal credentials)
        const isValidLogin = html.includes('Welcome') && !html.includes('Failed');

        if (isSQLiSuccess) {
            // SQLi detected - extract user data or use defaults
            const studentData = {
                name: 'SQL Injection User',
                student_id: 'BYPASSED',
                email: 'admin@ist.edu.bd',
                department: 'Security Testing',
                role: 'Administrator (via SQLi)'
            };

            localStorage.setItem('student', JSON.stringify(studentData));
            navigate('/dashboard');
        } else if (response.status === 200 && !html.includes('Login Failed')) {
            // Valid credentials
            const studentData = {
                name: 'John Doe',
                student_id: studentId,
                email: 'john.doe@ist.edu',
                department: 'Computer Science',
                role: 'Student'
            };

            localStorage.setItem('student', JSON.stringify(studentData));
            navigate('/dashboard');
        } else {
            // Login failed
            setError('Invalid credentials');
        }
    } catch (err) {
        setError('Network error. Please try again.');
        console.error('Login error:', err);
    } finally {
        setLoading(false);
    }
};
```

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Network errors break login | Add error handling with user feedback |
| HTML parsing may be fragile | Use multiple indicator phrases |
| Existing tests may break | Test all SQLi payloads documented in UI |

## Migration Plan
1. Backup current Portal.jsx
2. Implement new API-based login
3. Test all documented SQLi payloads
4. Update UI hints if needed to reflect working payloads

## Open Questions
- Should we add a "Testing Mode" toggle to show raw API responses?
- Should valid credentials also go through the API (for consistency)?
