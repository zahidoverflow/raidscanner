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

  // Handle POST request (Stored XSS)
  if (req.method === 'POST') {
    const { comment, author } = req.body || {}

    if (!comment) {
      return res.status(400).send('Comment required')
    }

    // VULNERABLE: Stored XSS
    // In a real app, this would be saved to DB and displayed to other users
    return res.status(200).send(`
<!DOCTYPE html>
<html>
<head><title>Comment Posted</title></head>
<body>
  <h1>Comment Posted Successfully</h1>
  <div class="stored-comment">
    <p><strong>Author:</strong> ${author || 'Anonymous'}</p>
    <div class="content">
      ${comment}
    </div>
  </div>
  <p>Your comment has been stored and will be visible to all users.</p>
  <p><small>Stored XSS Vulnerability: Input saved without sanitization</small></p>
</body>
</html>
        `)
  }

  // Handle GET request (Reflected XSS)
  const { comment } = req.query

  if (!comment) {
    return res.status(200).send(`
<!DOCTYPE html>
<html>
<head><title>Comments API</title></head>
<body>
  <h1>Comments API</h1>
  <p>GET: Use ?comment=your_comment for Reflected XSS</p>
  <p>POST: Send JSON { "comment": "..." } for Stored XSS</p>
</body>
</html>
    `)
  }

  // VULNERABLE: Reflected XSS - No sanitization!
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
