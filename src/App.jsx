import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Header from './components/Header'
import Footer from './components/Footer'
import Home from './pages/Home'
import About from './pages/About'
import Courses from './pages/Courses'
import Portal from './pages/Portal'
import Dashboard from './pages/Dashboard'
import Search from './pages/Search'
import Files from './pages/Files'
import './App.css'

function App() {
  return (
    <Router>
      <div className="App">
        <div className="warning-banner">
          ⚠️ INTENTIONALLY VULNERABLE APPLICATION - FOR EDUCATIONAL TESTING ONLY ⚠️
        </div>
        <Header />
        <main className="container">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/about" element={<About />} />
            <Route path="/courses" element={<Courses />} />
            <Route path="/portal" element={<Portal />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/search" element={<Search />} />
            <Route path="/files" element={<Files />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  )
}

export default App
