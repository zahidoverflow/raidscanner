# Design: Fix CRLF Detection

## Context
The CRLF scanner was designed for real-world scenarios where successful CRLF injection results in actual HTTP header manipulation. However, DVWU (and many other intentionally vulnerable apps) simulate vulnerabilities by returning informational responses rather than actually being exploitable.

## Goals
- Scanner detects CRLF vulnerabilities in both real-world and simulated scenarios
- Maintain backward compatibility with existing header-based detection
- Minimize false positives

## Non-Goals
- Full exploitation of CRLF (we only need detection)
- Supporting every possible CRLF simulation style

## Decisions

### Decision 1: Dual Detection Strategy
**What**: Check both HTTP headers AND response body for CRLF indicators
**Why**: Covers real-world exploitation AND simulated vulnerable apps
**Alternatives Considered**:
- Only fix DVWU to inject headers - Would work but limits scanner's usefulness
- Only check body - Would miss real header injection

### Decision 2: Pattern Matching for Body Detection
**What**: Use case-insensitive substring matching for common CRLF indicator phrases
**Why**: Simple, fast, low false positive rate with specific phrases
**Patterns**:
```python
CRLF_BODY_INDICATORS = [
    'crlf injection',
    'http response splitting',
    'header injection detected',
    'response splitting detected',
    'x-injected-header',
]
```

### Decision 3: Add Custom Header to DVWU (Optional)
**What**: DVWU sets `X-CRLF-Injection: detected` header when CRLF is found
**Why**: Provides realistic header-based detection path
**Trade-off**: Makes DVWU behavior more complex but more realistic

## Implementation

### Scanner Change (`scanner_engine.py`)

```python
def check_crlf(url: str, payload: str) -> Optional[dict]:
    """Check single CRLF payload"""
    target_url = f"{url}{payload}"

    try:
        response = requests.get(
            target_url,
            headers={'User-Agent': self.get_random_user_agent()},
            timeout=10,
            allow_redirects=False
        )

        is_vulnerable = False
        injected_header = None
        detection_method = None

        # Method 1: Check if our injected header appears in response headers
        if 'Set-Cookie' in response.headers:
            set_cookie = response.headers['Set-Cookie']
            if 'crlf=injection' in set_cookie:
                is_vulnerable = True
                injected_header = set_cookie
                detection_method = 'header_injection'

        # Method 2: Check for custom CRLF indicator header (DVWU style)
        if not is_vulnerable and 'X-CRLF-Injection' in response.headers:
            is_vulnerable = True
            detection_method = 'indicator_header'

        # Method 3: Check response body for CRLF indicators
        if not is_vulnerable:
            response_lower = response.text.lower()
            crlf_indicators = [
                'crlf injection',
                'http response splitting',
                'header injection detected',
                'response splitting detected',
            ]
            for indicator in crlf_indicators:
                if indicator in response_lower:
                    is_vulnerable = True
                    detection_method = 'body_indicator'
                    break

        # ... rest of function
```

### DVWU Change (`server.cjs`) - Optional

```javascript
// CRLF Injection - Newsletter API
app.all('/api/newsletter', (req, res) => {
    // ... existing code ...

    if (hasCRLF) {
        // Add indicator header for scanner detection
        res.setHeader('X-CRLF-Injection', 'detected');

        // Keep existing HTML response for visual feedback
        return res.status(200).send(`...`);
    }
});
```

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| False positives from body matching | Use specific phrases unlikely to appear normally |
| Performance impact | Minimal - only adds string matching |
| Breaking existing tests | Additive change - existing detection still works |

## Migration Plan
1. Deploy scanner change first
2. Test against DVWU - should now detect vulnerabilities
3. Optionally deploy DVWU header change for better realism
4. No rollback needed - changes are backward compatible

## Open Questions
- Should we add confidence scores based on detection method?
- Should body-based detection be configurable/optional?
