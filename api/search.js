// API endpoint for SQL Injection vulnerability testing
// This allows CLI scanners to detect the vulnerability

export default function handler(req, res) {
    // Enable CORS
    res.setHeader('Access-Control-Allow-Origin', '*')
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    res.setHeader('Content-Type', 'text/html; charset=utf-8')

    if (req.method === 'OPTIONS') {
        return res.status(200).end()
    }

    let query = ''

    if (req.method === 'GET') {
        query = req.query.q || ''
    } else if (req.method === 'POST') {
        query = req.body.q || req.body.search || ''
    }

    if (!query) {
        return res.status(200).send(`
<!DOCTYPE html>
<html>
<head><title>Search API</title></head>
<body>
  <h1>Search API</h1>
  <p>No search query provided. Use ?q=your_query</p>
</body>
</html>
    `)
    }

    // VULNERABLE: SQL Injection detection
    const hasSQLi = query.includes("'") ||
        query.includes('"') ||
        query.includes('--') ||
        query.includes('OR') ||
        query.includes('UNION') ||
        query.includes('SELECT') ||
        query.includes('1=1') ||
        query.includes('DROP') ||
        query.includes('/*') ||
        query.includes('*/') ||
        query.includes(';')

    if (hasSQLi) {
        // Return SQL error or data leak simulation
        return res.status(200).send(`
<!DOCTYPE html>
<html>
<head><title>SQL Error</title></head>
<body>
  <h1>Database Error</h1>
  <div style="background: #ffe6e6; padding: 15px; border-left: 4px solid #ff0000; margin: 20px 0;">
    <h3>SQL Syntax Error</h3>
    <pre>
Error in SQL query: SELECT * FROM courses WHERE name LIKE '%${query}%'

You have an error in your SQL syntax near '${query}'

Vulnerable Query: SELECT * FROM courses WHERE name LIKE '%${query}%'
    </pre>
  </div>
  <h3>Database Leak (SQL Injection Successful):</h3>
  <table border="1" style="border-collapse: collapse; width: 100%;">
    <tr style="background: #f0f0f0;">
      <th>ID</th><th>Username</th><th>Email</th><th>Role</th>
    </tr>
    <tr>
      <td>1</td><td>admin</td><td>admin@ist.edu.bd</td><td>administrator</td>
    </tr>
    <tr>
      <td>2</td><td>student</td><td>student@ist.edu.bd</td><td>user</td>
    </tr>
    <tr>
      <td>3</td><td>teacher</td><td>teacher@ist.edu.bd</td><td>staff</td>
    </tr>
  </table>
  <p><small>SQL Injection Detected! Query: ${query}</small></p>
</body>
</html>
    `)
    }

    // Normal search result
    return res.status(200).send(`
<!DOCTYPE html>
<html>
<head><title>Search Results</title></head>
<body>
  <h1>Search Results</h1>
  <p>Searching for: <strong>${query}</strong></p>
  <ul>
    <li>Computer Science - BSc Program</li>
    <li>Information Technology - MSc Program</li>
  </ul>
</body>
</html>
  `)
}
