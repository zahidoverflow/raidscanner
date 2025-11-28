import { useState, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import './NoticeBoard.css'

function NoticeBoard() {
  const [searchParams] = useSearchParams()
  const fileParam = searchParams.get('file')
  const [selectedFile, setSelectedFile] = useState(fileParam || '')
  const [fileContent, setFileContent] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  // Available notice files
  const notices = {
    'admission-notice-2024.txt': {
      title: 'Admission Notice 2024-2025',
      content: `INSTITUTE OF SCIENCE AND TECHNOLOGY
Admission Notice for Academic Year 2024-2025

Applications are invited for admission to the following programs:
- B.Sc. in Computer Science and Engineering
- B.Sc. in Information Technology
- B.Sc. in Software Engineering

Eligibility: SSC & HSC with minimum GPA 3.5
Application Deadline: December 31, 2024
Admission Test Date: January 15, 2025

For more information, visit: www.ist.edu.bd/admission
Contact: admission@ist.edu.bd | +880-2-9876543`,
      date: '2024-11-01'
    },
    'exam-schedule-fall2024.txt': {
      title: 'Final Exam Schedule - Fall 2024',
      content: `INSTITUTE OF SCIENCE AND TECHNOLOGY
Final Examination Schedule - Fall Semester 2024

CS401 - Cybersecurity Fundamentals
Date: December 10, 2024 | Time: 10:00 AM - 1:00 PM

CS301 - Web Development
Date: December 12, 2024 | Time: 2:00 PM - 5:00 PM

IT202 - Database Management Systems
Date: December 15, 2024 | Time: 10:00 AM - 1:00 PM

Exam Venue: Main Examination Hall
Students must bring their ID cards.`,
      date: '2024-11-15'
    },
    'scholarship-announcement.txt': {
      title: 'Merit Scholarship Announcement',
      content: `INSTITUTE OF SCIENCE AND TECHNOLOGY
Merit-Based Scholarship Program 2024

We are pleased to announce scholarships for outstanding students:

Full Tuition Waiver: Top 5 students (CGPA 3.90+)
50% Tuition Waiver: Next 10 students (CGPA 3.75+)
25% Tuition Waiver: Next 20 students (CGPA 3.50+)

Application Process:
1. Submit academic transcripts
2. Write a 500-word essay
3. Provide two recommendation letters

Deadline: November 30, 2024
Contact: scholarship@ist.edu.bd`,
      date: '2024-10-20'
    },
    'workshop-cybersecurity.txt': {
      title: 'Cybersecurity Workshop - Registration Open',
      content: `INSTITUTE OF SCIENCE AND TECHNOLOGY
Cybersecurity Workshop 2024

Topic: "Ethical Hacking and Penetration Testing"
Speaker: Dr. Sarah Johnson, Cybersecurity Expert

Date: December 5-6, 2024
Time: 9:00 AM - 5:00 PM
Venue: Computer Lab 3

Topics Covered:
- Web Application Security
- SQL Injection
- Cross-Site Scripting (XSS)
- Security Testing Tools

Registration: Free for IST students
Limited seats available!
Register at: events@ist.edu.bd`,
      date: '2024-11-10'
    }
  }

  // VULNERABLE: LFI simulation - matches scanner payloads
  useEffect(() => {
    if (fileParam) {
      handleFileLoad(fileParam)
    }
  }, [fileParam])

  const handleFileLoad = (filename) => {
    setError('')
    setFileContent('')
    setLoading(true)
    setSelectedFile(filename)

    // Simulate loading delay
    setTimeout(() => {
      // VULNERABLE: Path traversal detection
      if (filename.includes('../') || filename.includes('..\\\\') || 
          filename.includes('%2e%2e%2f') || filename.includes('%2e%2e%5c')) {
        
        // Simulate LFI vulnerability - matches scanner payloads
        if (filename.includes('/etc/passwd') || filename.includes('\\\\windows\\\\system32')) {
          setError(`🔓 LFI VULNERABILITY DETECTED!
          
Path Traversal Attempt: ${filename}

This would expose sensitive system files in a real application!

Simulated /etc/passwd content:
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
mysql:x:105:108:MySQL Server:/var/lib/mysql:/bin/false

⚠️ In a real scenario, this could lead to:
- System file disclosure
- Configuration file access
- Credential exposure
- Full system compromise`)
        } else {
          setError(`⚠️ Path Traversal Detected!

Attempted to access: ${filename}

This application is vulnerable to Local File Inclusion (LFI).
An attacker could potentially access sensitive files outside the intended directory.

Common LFI payloads that work:
- ../../../etc/passwd
- ..\\\\..\\\\..\\\\windows\\\\system32\\\\config\\\\sam
- ....//....//....//etc/passwd`)
        }
      } else if (notices[filename]) {
        setFileContent(notices[filename].content)
      } else {
        setError(`File not found: ${filename}

Available files:
${Object.keys(notices).join('\\n')}`)
      }
      setLoading(false)
    }, 300)
  }

  return (
    <>
      <div className="notice-hero">
        <h1>📢 Notice Board</h1>
        <p>Official announcements and important notices</p>
      </div>

      <div className="container">
        <div className="notice-layout">
          {/* Sidebar with notice list */}
          <div className="notice-sidebar">
            <h2>📋 All Notices</h2>
            <div className="notice-list">
              {Object.entries(notices).map(([filename, notice]) => (
                <div 
                  key={filename}
                  className={`notice-item ${selectedFile === filename ? 'active' : ''}`}
                  onClick={() => handleFileLoad(filename)}
                >
                  <h3>{notice.title}</h3>
                  <small>📅 {notice.date}</small>
                </div>
              ))}
            </div>

            <div className="vuln-hint" style={{ marginTop: '1.5rem' }}>
              ⚠️ <strong>LFI Vulnerability:</strong> This page is vulnerable to Local File Inclusion.
              <br /><br />
              Try: <code>?file=../../../etc/passwd</code>
              <br />
              Or: <code>?file=....//....//etc/passwd</code>
            </div>
          </div>

          {/* Main content area */}
          <div className="notice-content">
            {loading && (
              <div className="loading">
                <div className="spinner"></div>
                <p>Loading notice...</p>
              </div>
            )}

            {error && (
              <div className="error-box">
                <pre>{error}</pre>
              </div>
            )}

            {fileContent && !error && !loading && (
              <div className="notice-display">
                <div className="notice-header">
                  <h2>{notices[selectedFile]?.title}</h2>
                  <span className="notice-date">📅 {notices[selectedFile]?.date}</span>
                </div>
                <div className="notice-body">
                  <pre>{fileContent}</pre>
                </div>
                <div className="notice-footer">
                  <p><strong>File:</strong> <code>{selectedFile}</code></p>
                  <p><strong>URL:</strong> <code>/notices?file={selectedFile}</code></p>
                </div>
              </div>
            )}

            {!selectedFile && !loading && (
              <div className="notice-placeholder">
                <div className="placeholder-icon">📄</div>
                <h3>Select a notice to view</h3>
                <p>Choose from the list on the left to read the full notice</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  )
}

export default NoticeBoard
