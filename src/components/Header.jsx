import { Link } from 'react-router-dom'
import './Header.css'

function Header() {
  return (
    <>
      <div className="top-bar">
        <div className="container">
          <div className="top-bar-content">
            <div className="top-left">
              <span>📧 info@ist.edu.bd</span>
              <span className="separator">|</span>
              <span>Sitemap</span>
              <span className="separator">|</span>
              <span>FAQ</span>
              <span className="separator">|</span>
              <span>Hotline: 617 2093 7910</span>
            </div>
            <div className="top-right">
              <a href="#" aria-label="Facebook"><i className="fab fa-facebook-f"></i></a>
              <a href="#" aria-label="YouTube"><i className="fab fa-youtube"></i></a>
              <a href="#" aria-label="LinkedIn"><i className="fab fa-linkedin-in"></i></a>
            </div>
          </div>
        </div>
      </div>
      
      <header className="header">
        <div className="container">
          <div className="header-content">
            <div className="logo">
              <img src="/ist-logo.png" alt="IST Logo" className="logo-img" />
              <div className="logo-text">
                <h1>Institute of Science and Technology</h1>
                <p>a center of excellence for education</p>
              </div>
            </div>
            <div className="header-right">
              <button className="payment-btn">Online Payment System</button>
              <nav>
                <ul>
                  <li><Link to="/">Home</Link></li>
                  <li><Link to="/about">About</Link></li>
                  <li><Link to="/courses">Academics</Link></li>
                  <li><Link to="/portal">Student Portal</Link></li>
                  <li><Link to="/search">Search</Link></li>
                </ul>
              </nav>
            </div>
          </div>
        </div>
      </header>
    </>
  )
}

export default Header
