import { Link } from 'react-router-dom'
import './Header.css'

function Header() {
  return (
    <header className="header">
      <div className="container">
        <div className="header-content">
          <div className="logo">
            <h1>IST</h1>
            <p>Institute of Science and Technology</p>
          </div>
          <nav>
            <ul>
              <li><Link to="/">Home</Link></li>
              <li><Link to="/about">About</Link></li>
              <li><Link to="/courses">Courses</Link></li>
              <li><Link to="/portal">Student Portal</Link></li>
              <li><Link to="/search">Search</Link></li>
            </ul>
          </nav>
        </div>
      </div>
    </header>
  )
}

export default Header
