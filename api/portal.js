// API endpoint for SQL Injection in login (Portal)
// This allows CLI scanners to detect the vulnerability

export default function handler(req, res) {
    // Enable CORS
    res.setHeader('Access-Control-Allow-Origin', '*')
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS')
    res.setHeader('Content-Type', 'text/html; charset=utf-8')

    if (req.method === 'OPTIONS') {
        return res.status(200).end()
    }

    if (req.method !== 'POST') {
        return res.status(405).send('Method Not Allowed')
    }

    const { username, password } = req.body || {}

    if (!username || !password) {
        return res.status(200).send(`
<!DOCTYPE html>
<html>
<head><title>Login Failed</title></head>
<body>
  <h1>Login Failed</h1>
  <p>Username and password required</p>
</body>
</html>
    `)
    }

    // VULNERABLE: SQL Injection in authentication
    const hasSQLi = username.includes("'") ||
        username.includes('"') ||
        username.includes('--') ||
        username.includes('OR') ||
        username.toLowerCase().includes("or '1'='1") ||
        username.toLowerCase().includes("or 1=1") ||
        username.includes('admin') && username.includes("'")

    if (hasSQLi) {
        // Authentication bypass successful!
        return res.status(200).send(`
<!DOCTYPE html>
<html>
<head><title>Login Successful - SQL Injection!</title></head>
<body style="font-family: Arial, sans-serif; padding: 20px;">
  <div style="background: #d4edda; border: 1px solid #c3e6cb; padding: 20px; border-radius: 5px;">
    <h1 style="color: #155724;">✅ Authentication Bypass Successful!</h1>
    <p><strong>SQL Injection Detected</strong></p>
    <p>Username: <code>${username}</code></p>
    <p>Password: <code>${password}</code></p>
    
    <h3>Vulnerable Query:</h3>
    <pre style="background: #f8f9fa; padding: 15px; border-left: 4px solid #dc3545;">
SELECT * FROM users WHERE username='${username}' AND password='${password}'
    </pre>
    
    <h3>Logged in as:</h3>
    <ul>
      <li>User ID: 1</li>
      <li>Username: admin</li>
      <li>Role: Administrator</li>
      <li>Email: admin@ist.edu.bd</li>
    </ul>
    
    <p style="color: #721c24; background: #f8d7da; padding: 10px; border-radius: 3px;">
      <strong>Security Warning:</strong> SQL Injection vulnerability allows authentication bypass!
    </p>
  </div>
</body>
</html>
    `)
    }

    // Normal login failure
    return res.status(401).send(`
<!DOCTYPE html>
<html>
<head><title>Login Failed</title></head>
<body>
  <h1>Login Failed</h1>
  <p>Invalid username or password</p>
  <p>Username: ${username}</p>
</body>
</html>
  `)
}
