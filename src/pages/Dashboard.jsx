import { useEffect, useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'

function Dashboard() {
  const [student, setStudent] = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    const studentData = localStorage.getItem('student')
    if (!studentData) {
      navigate('/portal')
    } else {
      setStudent(JSON.parse(studentData))
    }
  }, [navigate])

  const handleLogout = () => {
    localStorage.removeItem('student')
    navigate('/portal')
  }

  if (!student) return null

  return (
    <>
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
          <div>
            <h1>Welcome, {student.name}!</h1>
            <p>Student ID: {student.student_id}</p>
          </div>
          <button onClick={handleLogout} className="btn btn-secondary">Logout</button>
        </div>

        <div className="grid">
          <div style={{ background: '#e8f5e9', padding: '1.5rem', borderRadius: '8px' }}>
            <h3>📧 Email</h3>
            <p>{student.email}</p>
          </div>

          <div style={{ background: '#e3f2fd', padding: '1.5rem', borderRadius: '8px' }}>
            <h3>🎓 Department</h3>
            <p>{student.department}</p>
          </div>

          <div style={{ background: '#fff3e0', padding: '1.5rem', borderRadius: '8px' }}>
            <h3>📚 Enrolled Courses</h3>
            <p>5 Active</p>
          </div>

          <div style={{ background: '#fce4ec', padding: '1.5rem', borderRadius: '8px' }}>
            <h3>📊 GPA</h3>
            <p>3.75 / 4.00</p>
          </div>
        </div>
      </div>

      <div className="card">
        <h2>Quick Links</h2>
        <div className="grid" style={{ marginTop: '1rem' }}>
          <Link to="/courses" className="btn">View Courses</Link>
          <Link to="/search" className="btn">Search</Link>
          <Link to="/files" className="btn">Documents</Link>
        </div>
      </div>

      {student.student_id === 'BYPASSED' && (
        <div className="card" style={{ background: '#fff3cd', border: '1px solid #ffc107' }}>
          <p style={{ color: '#856404' }}>
            ℹ️ <strong>Note:</strong> You successfully exploited the SQL injection vulnerability! In a real application, this would be a serious security issue.
          </p>
        </div>
      )}
    </>
  )
}

export default Dashboard
