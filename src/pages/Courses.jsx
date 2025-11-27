function Courses() {
  const courses = [
    { id: 1, code: 'CS101', name: 'Introduction to Programming', instructor: 'Dr. Robert Brown', credits: 3 },
    { id: 2, code: 'CS201', name: 'Data Structures and Algorithms', instructor: 'Prof. Emily Davis', credits: 4 },
    { id: 3, code: 'CS301', name: 'Web Development', instructor: 'Dr. Michael Chen', credits: 3 },
    { id: 4, code: 'CS401', name: 'Cybersecurity Fundamentals', instructor: 'Prof. Sarah Johnson', credits: 4 },
    { id: 5, code: 'IT202', name: 'Database Management Systems', instructor: 'Dr. James Wilson', credits: 3 }
  ]

  return (
    <>
      <div className="card">
        <h1>Course Catalog</h1>
        <p>Browse our comprehensive selection of courses across various disciplines.</p>
      </div>

      {courses.map(course => (
        <div key={course.id} className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
            <div>
              <h2 style={{ color: '#667eea' }}>{course.code} - {course.name}</h2>
              <p style={{ margin: '0.5rem 0' }}><strong>Instructor:</strong> {course.instructor}</p>
              <p><strong>Credits:</strong> {course.credits}</p>
            </div>
            <button className="btn">Enroll</button>
          </div>
        </div>
      ))}
    </>
  )
}

export default Courses
