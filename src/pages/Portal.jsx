import { useState, useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'

function Portal() {
  const [searchParams, setSearchParams] = useSearchParams()
  const [studentId, setStudentId] = useState(searchParams.get('username') || '')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()

  // Initialize from URL
  useEffect(() => {
    const username = searchParams.get('username')
    if (username) {
      setStudentId(username)
    }
  }, [searchParams])

  const handleSubmit = (e) => {
    e.preventDefault()

    // Update URL on submit
    setSearchParams({ username: studentId })

    // VULNERABLE: Simulating SQL injection vulnerability
    // In a real backend, this would be: SELECT * FROM students WHERE student_id = '${studentId}' AND password = '${password}'

    if (studentId === "' OR '1'='1' --" ||
      password === "' OR '1'='1' --" ||
      (studentId === 'IST2021001' && password === 'password123') ||
      (studentId === 'IST2020000' && password === 'admin123')) {

      const studentData = {
        name: studentId.includes("'") ? 'SQL Injection User' : 'John Doe',
        student_id: studentId.includes("'") ? 'BYPASSED' : studentId,
        email: 'john.doe@ist.edu',
        department: 'Computer Science'
      }

      localStorage.setItem('student', JSON.stringify(studentData))
      navigate('/dashboard')
    } else {
      setError('Invalid credentials')
    }
  }

  return (
    <div className="card" style={{ maxWidth: '500px', margin: '0 auto' }}>
      <h1>Student Portal Login</h1>
      <p style={{ marginBottom: '2rem' }}>Access your student dashboard and university resources.</p>

      {error && <div className="error">{error}</div>}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="student_id">Student ID</label>
          <input
            type="text"
            id="student_id"
            value={studentId}
            onChange={(e) => setStudentId(e.target.value)}
            placeholder="IST2021001"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter your password"
            required
          />
        </div>

        <button type="submit" className="btn" style={{ width: '100%' }}>Login</button>
      </form>

      <div style={{ marginTop: '2rem', paddingTop: '1rem', borderTop: '1px solid #ddd', textAlign: 'center' }}>
        <p style={{ fontSize: '0.9rem', color: '#666' }}>
          For testing: <br />
          <code>Student ID: IST2021001</code><br />
          <code>Password: password123</code>
        </p>
      </div>

      <div className="vuln-hint">
        ⚠️ <strong>Vulnerability:</strong> This form is vulnerable to SQL injection. Try: <code>' OR '1'='1' --</code>
      </div>
    </div>
  )
}

export default Portal
