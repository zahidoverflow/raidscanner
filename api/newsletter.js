// API endpoint for CRLF Injection vulnerability testing
// This allows CLI scanners to detect the vulnerability via POST

export default function handler(req, res) {
    // Enable CORS
    res.setHeader('Access-Control-Allow-Origin', '*')
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS')

    if (req.method === 'OPTIONS') {
        return res.status(200).end()
    }

    if (req.method !== 'POST') {
        return res.status(405).send('Method Not Allowed')
    }

    const { email } = req.body || {}

    if (!email) {
        return res.status(200).send('Email required')
    }

    // VULNERABLE: CRLF Injection
    // In a real app, this might set headers like:
    // res.setHeader('X-Subscriber-Email', email)

    const hasCRLF = email.includes('\r') || email.includes('\n') ||
        email.includes('%0d') || email.includes('%0a')

    if (hasCRLF) {
        // Simulate the vulnerability by reflecting the headers that would be injected
        // or by actually setting them if the platform allows (Vercel might sanitize, so we simulate)

        return res.status(200).send(`
<!DOCTYPE html>
<html>
<head><title>Subscription Failed</title></head>
<body>
  <h1>CRLF Injection Detected</h1>
  <p>The application attempted to set headers based on your input:</p>
  <pre>
Set-Cookie: session_id=...
X-Subscriber-Email: ${email}
  </pre>
  <p><strong>Vulnerability:</strong> HTTP Response Splitting / CRLF Injection</p>
  <p>Your input contained newline characters which could allow header injection.</p>
</body>
</html>
        `)
    }

    return res.status(200).send(`
<!DOCTYPE html>
<html>
<body>
  <h1>Subscribed!</h1>
  <p>Thank you for subscribing with: ${email}</p>
</body>
</html>
    `)
}
