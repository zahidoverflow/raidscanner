import { Link } from 'react-router-dom'
import './Home.css'

function Home() {
  const news = [
    { id: 1, title: 'Welcome to IST 2024-2025', content: 'We are excited to welcome all new and returning students!', date: '2024-09-01' },
    { id: 2, title: 'Cybersecurity Workshop', content: 'Join us for a hands-on cybersecurity workshop next week.', date: '2024-10-15' },
    { id: 3, title: 'New Research Lab Opening', content: 'State-of-the-art AI research lab now open for students.', date: '2024-11-01' }
  ]

  return (
    <>
      <div className="hero-section">
        <img src="/ist-front-side.png" alt="IST Campus" className="hero-image" />
      </div>

      <div className="container">
        <div className="grid">
          <div className="card">
            <h2>🎓 About IST</h2>
            <p>Leading institution in technology and science education, fostering innovation and research excellence since 1995.</p>
            <Link to="/about" className="btn">Learn More</Link>
          </div>

          <div className="card">
            <h2>📚 Academic Programs</h2>
            <p>Explore our comprehensive range of undergraduate and graduate programs in Computer Science, IT, and Engineering.</p>
            <Link to="/courses" className="btn">View Courses</Link>
          </div>

          <div className="card">
            <h2>👨‍🎓 Student Portal</h2>
            <p>Access your student dashboard, grades, schedules, and university resources.</p>
            <Link to="/portal" className="btn">Login</Link>
          </div>
        </div>

        <div className="card">
          <h2>📰 Latest News & Announcements</h2>
          {news.map(item => (
            <div key={item.id} style={{ borderLeft: '4px solid #ff6600', paddingLeft: '1rem', marginBottom: '1.5rem' }}>
              <h3 style={{ color: '#ff6600', marginBottom: '0.5rem' }}>{item.title}</h3>
              <p style={{ color: '#666', marginBottom: '0.5rem' }}>{item.content}</p>
              <small style={{ color: '#999' }}>📅 {item.date}</small>
            </div>
          ))}
        </div>
      </div>
    </>
  )
}

export default Home
