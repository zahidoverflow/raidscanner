// API endpoint for Open Redirect vulnerability testing
// This allows CLI scanners to detect the vulnerability

export default function handler(req, res) {
    // Enable CORS
    res.setHeader('Access-Control-Allow-Origin', '*')
    res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS')

    if (req.method === 'OPTIONS') {
        return res.status(200).end()
    }

    const { url } = req.query

    if (!url) {
        return res.status(200).send('No redirect URL specified')
    }

    // VULNERABLE: Open Redirect - No validation!
    // Redirect to any URL provided
    res.setHeader('Location', url)
    return res.status(302).send(`Redirecting to: ${url}`)
}
