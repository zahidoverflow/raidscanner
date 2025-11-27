import { useState } from 'react'

function Search() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [error, setError] = useState('')

  const allCourses = [
    { id: 1, code: 'CS101', name: 'Introduction to Programming', instructor: 'Dr. Robert Brown', credits: 3 },
    { id: 2, code: 'CS201', name: 'Data Structures and Algorithms', instructor: 'Prof. Emily Davis', credits: 4 },
    { id: 3, code: 'CS301', name: 'Web Development', instructor: 'Dr. Michael Chen', credits: 3 },
    { id: 4, code: 'CS401', name: 'Cybersecurity Fundamentals', instructor: 'Prof. Sarah Johnson', credits: 4 },
    { id: 5, code: 'IT202', name: 'Database Management Systems', instructor: 'Dr. James Wilson', credits: 3 }
  ]

  const handleSearch = (e) => {
    e.preventDefault()
    setError('')

    // VULNERABLE: Simulating SQL injection in search
    // Real query would be: SELECT * FROM courses WHERE course_name LIKE '%${query}%' OR course_code LIKE '%${query}%'
    
    if (query.includes("'") || query.includes("UNION") || query.includes("--")) {
      setError(`Database Error: Syntax error near '${query}'. This might indicate a SQL injection attempt!`)
      setResults([])
    } else {
      const filtered = allCourses.filter(course => 
        course.name.toLowerCase().includes(query.toLowerCase()) ||
        course.code.toLowerCase().includes(query.toLowerCase())
      )
      setResults(filtered)
    }
  }

  return (
    <>
      <div className="card">
        <h1>Search Courses</h1>
        
        <form onSubmit={handleSearch}>
          <div className="form-group">
            <input 
              type="text" 
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search by course name or code..." 
              style={{ fontSize: '1.1rem' }} 
            />
          </div>
          <button type="submit" className="btn">Search</button>
        </form>

        {error && (
          <div className="error" style={{ marginTop: '1rem' }}>
            <strong>Database Error:</strong> {error}
            <p style={{ marginTop: '0.5rem', fontSize: '0.9rem' }}>This might indicate a SQL injection attempt!</p>
          </div>
        )}
      </div>

      {results.length > 0 && (
        <div className="card">
          <h2>Search Results ({results.length})</h2>
          
          {results.map(course => (
            <div key={course.id} style={{ borderLeft: '4px solid #667eea', paddingLeft: '1rem', marginBottom: '1.5rem' }}>
              <h3 style={{ color: '#667eea' }}>{course.code} - {course.name}</h3>
              <p><strong>Instructor:</strong> {course.instructor}</p>
              <p><strong>Credits:</strong> {course.credits}</p>
            </div>
          ))}
        </div>
      )}

      {query && results.length === 0 && !error && (
        <div className="card">
          <p>No results found for "{query}"</p>
        </div>
      )}

      <div className="vuln-hint">
        ⚠️ <strong>Vulnerability:</strong> This search is vulnerable to SQL injection. Try: <code>' UNION SELECT 1,2,3,4,5 --</code>
      </div>
    </>
  )
}

export default Search
