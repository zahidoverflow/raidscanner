import './Footer.css'

function Footer() {
  return (
    <footer className="footer">
      <div className="container">
        <p>&copy; 2024 Institute of Science and Technology. All rights reserved.</p>
        <p style={{ marginTop: '0.5rem', fontSize: '0.9rem', opacity: 0.8 }}>
          📧 contact@ist.edu | 📞 +1 (555) 123-4567 | 📍 123 University Ave, Tech City
        </p>
        <p style={{ marginTop: '1rem', fontSize: '0.85rem', color: '#ff6b6b' }}>
          ⚠️ This is an intentionally vulnerable application for security testing
        </p>
      </div>
    </footer>
  )
}

export default Footer
