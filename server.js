const express = require('express');
const bodyParser = require('body-parser');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.static('public'));
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Database setup
const db = new sqlite3.Database(':memory:');

// Initialize database with sample data
db.serialize(() => {
  // Students table
  db.run(`CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    student_id TEXT,
    department TEXT,
    password TEXT
  )`);

  // Courses table
  db.run(`CREATE TABLE courses (
    id INTEGER PRIMARY KEY,
    course_code TEXT,
    course_name TEXT,
    instructor TEXT,
    credits INTEGER
  )`);

  // News table
  db.run(`CREATE TABLE news (
    id INTEGER PRIMARY KEY,
    title TEXT,
    content TEXT,
    date TEXT
  )`);

  // Insert sample students (vulnerable passwords)
  const students = [
    ['John Doe', 'john.doe@ist.edu', 'IST2021001', 'Computer Science', 'password123'],
    ['Jane Smith', 'jane.smith@ist.edu', 'IST2021002', 'Information Technology', 'admin'],
    ['Mike Johnson', 'mike.j@ist.edu', 'IST2021003', 'Software Engineering', '123456'],
    ['Sarah Williams', 'sarah.w@ist.edu', 'IST2021004', 'Data Science', 'qwerty'],
    ['Admin User', 'admin@ist.edu', 'IST2020000', 'Administration', 'admin123']
  ];

  students.forEach(student => {
    db.run('INSERT INTO students (name, email, student_id, department, password) VALUES (?, ?, ?, ?, ?)', student);
  });

  // Insert sample courses
  const courses = [
    ['CS101', 'Introduction to Programming', 'Dr. Robert Brown', 3],
    ['CS201', 'Data Structures and Algorithms', 'Prof. Emily Davis', 4],
    ['CS301', 'Web Development', 'Dr. Michael Chen', 3],
    ['CS401', 'Cybersecurity Fundamentals', 'Prof. Sarah Johnson', 4],
    ['IT202', 'Database Management Systems', 'Dr. James Wilson', 3]
  ];

  courses.forEach(course => {
    db.run('INSERT INTO courses (course_code, course_name, instructor, credits) VALUES (?, ?, ?, ?)', course);
  });

  // Insert sample news
  const news = [
    ['Welcome to IST 2024-2025', 'We are excited to welcome all new and returning students!', '2024-09-01'],
    ['Cybersecurity Workshop', 'Join us for a hands-on cybersecurity workshop next week.', '2024-10-15'],
    ['New Research Lab Opening', 'State-of-the-art AI research lab now open for students.', '2024-11-01']
  ];

  news.forEach(item => {
    db.run('INSERT INTO news (title, content, date) VALUES (?, ?, ?)', item);
  });
});

// Routes

// Home page
app.get('/', (req, res) => {
  db.all('SELECT * FROM news ORDER BY date DESC', [], (err, news) => {
    if (err) {
      return res.status(500).send('Database error');
    }
    res.render('index', { news });
  });
});

// About page
app.get('/about', (req, res) => {
  res.render('about');
});

// Courses page
app.get('/courses', (req, res) => {
  db.all('SELECT * FROM courses', [], (err, courses) => {
    if (err) {
      return res.status(500).send('Database error');
    }
    res.render('courses', { courses });
  });
});

// Student portal login page
app.get('/portal', (req, res) => {
  res.render('portal', { error: null });
});

// VULNERABLE: SQL Injection in login
app.post('/portal/login', (req, res) => {
  const { student_id, password } = req.body;
  
  // Intentionally vulnerable SQL query
  const query = `SELECT * FROM students WHERE student_id = '${student_id}' AND password = '${password}'`;
  
  db.get(query, [], (err, student) => {
    if (err) {
      return res.render('portal', { error: 'Database error' });
    }
    
    if (student) {
      res.render('dashboard', { student });
    } else {
      res.render('portal', { error: 'Invalid credentials' });
    }
  });
});

// VULNERABLE: SQL Injection in search
app.get('/search', (req, res) => {
  const searchQuery = req.query.q || '';
  
  if (!searchQuery) {
    return res.render('search', { results: [], query: '' });
  }
  
  // Intentionally vulnerable SQL query
  const query = `SELECT * FROM courses WHERE course_name LIKE '%${searchQuery}%' OR course_code LIKE '%${searchQuery}%'`;
  
  db.all(query, [], (err, results) => {
    if (err) {
      return res.render('search', { results: [], query: searchQuery, error: err.message });
    }
    res.render('search', { results, query: searchQuery, error: null });
  });
});

// VULNERABLE: LFI (Local File Inclusion)
app.get('/files', (req, res) => {
  const filename = req.query.file;
  
  if (!filename) {
    return res.render('files');
  }
  
  // Intentionally vulnerable - no path sanitization
  const filePath = path.join(__dirname, 'documents', filename);
  
  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      return res.send(`<h1>Error reading file</h1><p>${err.message}</p><a href="/files">Back</a>`);
    }
    res.send(`<pre>${data}</pre><br><a href="/files">Back</a>`);
  });
});

// VULNERABLE: XSS in comments/news
app.get('/news/:id', (req, res) => {
  const newsId = req.params.id;
  
  db.get('SELECT * FROM news WHERE id = ?', [newsId], (err, newsItem) => {
    if (err || !newsItem) {
      return res.status(404).send('News not found');
    }
    res.render('news-detail', { news: newsItem, comments: [] });
  });
});

// VULNERABLE: Open Redirect
app.get('/redirect', (req, res) => {
  const url = req.query.url;
  
  if (!url) {
    return res.send('Missing URL parameter');
  }
  
  // Intentionally vulnerable - no URL validation
  res.redirect(url);
});

// VULNERABLE: CRLF Injection in headers
app.get('/download', (req, res) => {
  const filename = req.query.filename || 'document.pdf';
  
  // Intentionally vulnerable - no sanitization of filename
  res.setHeader('Content-Disposition', `attachment; filename=${filename}`);
  res.send('File content here');
});

// API endpoint - Student list (for testing)
app.get('/api/students', (req, res) => {
  const department = req.query.department;
  
  if (department) {
    // Vulnerable to SQL injection
    const query = `SELECT id, name, email, student_id, department FROM students WHERE department = '${department}'`;
    db.all(query, [], (err, students) => {
      if (err) {
        return res.status(500).json({ error: err.message });
      }
      res.json(students);
    });
  } else {
    db.all('SELECT id, name, email, student_id, department FROM students', [], (err, students) => {
      if (err) {
        return res.status(500).json({ error: 'Database error' });
      }
      res.json(students);
    });
  }
});

// 404 handler
app.use((req, res) => {
  res.status(404).render('404');
});

app.listen(PORT, () => {
  console.log(`🎓 IST Vulnerable Web App running on http://localhost:${PORT}`);
  console.log('⚠️  WARNING: This is an INTENTIONALLY VULNERABLE application for security testing!');
});
