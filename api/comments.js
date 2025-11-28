// API endpoint for XSS vulnerability testing
// This allows CLI scanners to detect the vulnerability

export default function handler(req, res) {
    // Enable CORS
    res.setHeader('Access-Control-Allow-Origin', '*')
    res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS')
    res.setHeader('Content-Type', 'text/html; charset=utf-8')

    if (req.method === 'OPTIONS') {
        return res.status(200).end()
    }

    const { comment } = req.query

    if (!comment) {
        return res.status(200).send(`
<!DOCTYPE html>
<html>
<head><title>Comments API</title></head>
<body>
  <h1>Comments API</h1>
  <p>No comment provided. Use ?comment=your_comment</p>
</body>
</html>
    `)
    }

    // VULNERABLE: Reflected XSS - No sanitization!
    // This allows the scanner to detect XSS
    return res.status(200).send(`
<!DOCTYPE html>
<html>
<head>
  <title>Comment Display</title>
  <style>
    body { font-family: Arial, sans-serif; padding: 20px; }
    .comment { background: #f0f0f0; padding: 15px; border-radius: 5px; margin: 20px 0; }
  </style>
</head>
<body>
  <h1>Your Comment</h1>
  <div class="comment">
    ${comment}
  </div>
  <p><small>Comment reflected without sanitization - XSS Vulnerable!</small></p>
</body>
</html>
  `)
}
