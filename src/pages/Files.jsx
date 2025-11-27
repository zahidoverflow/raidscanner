import { useState } from 'react'
import { useSearchParams } from 'react-router-dom'

function Files() {
  const [searchParams] = useSearchParams()
  const fileParam = searchParams.get('file')
  const [selectedFile, setSelectedFile] = useState(fileParam || '')
  const [fileContent, setFileContent] = useState('')
  const [error, setError] = useState('')

  const documents = {
    'syllabus.txt': `INSTITUTE OF SCIENCE AND TECHNOLOGY
Course Syllabus - Fall 2024

Course: CS401 - Cybersecurity Fundamentals
Instructor: Prof. Sarah Johnson
Credits: 4

Course Description:
This course provides a comprehensive introduction to cybersecurity concepts...`,
    
    'schedule.txt': `INSTITUTE OF SCIENCE AND TECHNOLOGY
Academic Schedule - Fall 2024

Important Dates:
August 25, 2024 - Fall Semester Begins
September 2, 2024 - Labor Day (No Classes)...`,
    
    'handbook.txt': `INSTITUTE OF SCIENCE AND TECHNOLOGY
Student Handbook 2024-2025

Welcome to IST!

This handbook provides essential information about university policies...`
  }

  const handleFileSelect = (filename) => {
    setError('')
    setSelectedFile(filename)
    
    // VULNERABLE: LFI simulation
    if (filename.includes('../') || filename.includes('..\\')) {
      setError(`Error reading file: Path traversal detected! Attempted to access: ${filename}`)
      setFileContent('')
    } else if (documents[filename]) {
      setFileContent(documents[filename])
    } else {
      setError(`Error reading file: File not found: ${filename}`)
      setFileContent('')
    }
  }

  return (
    <>
      <div className="card">
        <h1>Document Library</h1>
        <p>Access course materials and university documents.</p>
      </div>

      <div className="card">
        <h2>Available Documents</h2>
        
        <div style={{ display: 'grid', gap: '1rem', marginTop: '1rem' }}>
          <button 
            onClick={() => handleFileSelect('syllabus.txt')}
            style={{ display: 'block', padding: '1rem', background: '#f8f9fa', borderRadius: '5px', textDecoration: 'none', color: '#333', border: '1px solid #ddd', cursor: 'pointer', textAlign: 'left' }}
          >
            📄 Course Syllabus
          </button>
          
          <button 
            onClick={() => handleFileSelect('schedule.txt')}
            style={{ display: 'block', padding: '1rem', background: '#f8f9fa', borderRadius: '5px', textDecoration: 'none', color: '#333', border: '1px solid #ddd', cursor: 'pointer', textAlign: 'left' }}
          >
            📅 Academic Schedule
          </button>
          
          <button 
            onClick={() => handleFileSelect('handbook.txt')}
            style={{ display: 'block', padding: '1rem', background: '#f8f9fa', borderRadius: '5px', textDecoration: 'none', color: '#333', border: '1px solid #ddd', cursor: 'pointer', textAlign: 'left' }}
          >
            📚 Student Handbook
          </button>
        </div>
      </div>

      {error && (
        <div className="error">
          {error}
        </div>
      )}

      {fileContent && (
        <div className="card">
          <h2>{selectedFile}</h2>
          <pre style={{ background: '#f8f9fa', padding: '1rem', borderRadius: '5px', overflow: 'auto' }}>
            {fileContent}
          </pre>
        </div>
      )}

      <div className="vuln-hint">
        ⚠️ <strong>Vulnerability:</strong> This file viewer is vulnerable to LFI (Local File Inclusion). Try: <code>?file=../../../etc/passwd</code>
      </div>
    </>
  )
}

export default Files
