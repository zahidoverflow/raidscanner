# Fix Portal Frontend API Integration

## Why
The Student Portal login form (`Portal.jsx`) uses client-side hardcoded string comparison instead of calling the backend `/api/portal` endpoint. This means:
1. Only the exact payload `' OR '1'='1' --` is detected as SQLi
2. Other valid SQLi payloads like `admin'--` don't work through the UI
3. Frontend behavior doesn't match backend behavior
4. Security testers get inconsistent results between UI and direct API testing

## What Changes
- **DVWU Frontend**: Modify `Portal.jsx` to call the backend `/api/portal` API
- Parse the HTML response to determine if SQLi was successful
- Show appropriate feedback based on actual backend response

## Impact
- Affected specs: `dvwu` (Portal/SQLi feature)
- Affected code: `damn-vulnerable-web-university/src/pages/Portal.jsx`
- Risk: Low - improves consistency between frontend and backend
- **BREAKING**: Users who relied on exact string match will now have broader detection
