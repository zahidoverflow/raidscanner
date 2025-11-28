import { useSearchParams } from 'react-router-dom'
import { useState, useEffect } from 'react'
import './Comments.css'

function Comments() {
    const [searchParams] = useSearchParams()
    const reflectedComment = searchParams.get('comment') || ''

    // Stored XSS - comments from localStorage
    const [storedComments, setStoredComments] = useState([])
    const [newComment, setNewComment] = useState('')
    const [author, setAuthor] = useState('')

    // Load stored comments on mount
    useEffect(() => {
        const saved = localStorage.getItem('ist_comments')
        if (saved) {
            try {
                setStoredComments(JSON.parse(saved))
            } catch (e) {
                localStorage.removeItem('ist_comments')
            }
        }
    }, [])

    // POST-based comment submission (Stored XSS)
    const handleSubmit = (e) => {
        e.preventDefault()
        if (!newComment.trim()) return

        const comment = {
            id: Date.now(),
            text: newComment,
            author: author || 'Anonymous',
            date: new Date().toISOString()
        }

        const updated = [...storedComments, comment]
        setStoredComments(updated)

        // VULNERABLE: Store without sanitization
        localStorage.setItem('ist_comments', JSON.stringify(updated))

        // Reset form
        setNewComment('')
        setAuthor('')
    }

    const deleteComment = (id) => {
        const updated = storedComments.filter(c => c.id !== id)
        setStoredComments(updated)
        localStorage.setItem('ist_comments', JSON.stringify(updated))
    }

    const clearAll = () => {
        setStoredComments([])
        localStorage.removeItem('ist_comments')
    }

    return (
        <>
            <div className="comments-hero">
                <h1>💬 Comments Section</h1>
                <p>Share your thoughts about IST</p>
            </div>

            <div className="container">
                <div className="comments-content">

                    {/* Reflected XSS Section (GET) */}
                    <div className="xss-section">
                        <h2>🔴 Reflected XSS (GET Parameter)</h2>

                        <div className="method-badge get">Method: GET</div>

                        <div className="comment-form-info">
                            <p>Test reflected XSS via URL parameter:</p>
                            <code>/comments?comment=Your+comment+here</code>
                        </div>

                        {reflectedComment && (
                            <div className="comment-display">
                                <h3>Reflected Comment:</h3>
                                {/* VULNERABLE: Reflected XSS */}
                                <div
                                    className="comment-content"
                                    dangerouslySetInnerHTML={{ __html: reflectedComment }}
                                />
                            </div>
                        )}

                        {!reflectedComment && (
                            <div className="comment-placeholder">
                                <div className="placeholder-icon">💭</div>
                                <p>Add <code>?comment=</code> parameter to URL</p>
                            </div>
                        )}
                    </div>

                    {/* Stored XSS Section (POST) */}
                    <div className="xss-section stored">
                        <h2>🔴 Stored XSS (POST Submission)</h2>

                        <div className="method-badge post">Method: POST</div>

                        <div className="stored-info">
                            <p><strong>📌 More Dangerous:</strong> Stored XSS affects ALL users</p>
                            <p>Comments are saved to localStorage and displayed to everyone</p>
                        </div>

                        <form onSubmit={handleSubmit} className="comment-post-form">
                            <div className="form-row">
                                <input
                                    type="text"
                                    value={author}
                                    onChange={(e) => setAuthor(e.target.value)}
                                    placeholder="Your name (optional)"
                                    className="author-input"
                                />
                            </div>
                            <div className="form-row">
                                <textarea
                                    value={newComment}
                                    onChange={(e) => setNewComment(e.target.value)}
                                    placeholder="Write your comment..."
                                    className="comment-textarea"
                                    rows="4"
                                />
                            </div>
                            <div className="form-actions">
                                <button type="submit" className="btn btn-primary">
                                    Post Comment
                                </button>
                                {storedComments.length > 0 && (
                                    <button type="button" onClick={clearAll} className="btn btn-danger">
                                        Clear All ({storedComments.length})
                                    </button>
                                )}
                            </div>
                        </form>

                        {/* Display stored comments */}
                        <div className="stored-comments">
                            <h3>Stored Comments ({storedComments.length})</h3>

                            {storedComments.length === 0 && (
                                <p className="no-comments">No comments yet. Be the first to comment!</p>
                            )}

                            {storedComments.map(comment => (
                                <div key={comment.id} className="stored-comment">
                                    <div className="comment-header">
                                        <strong>{comment.author}</strong>
                                        <span className="comment-date">
                                            {new Date(comment.date).toLocaleString()}
                                        </span>
                                    </div>
                                    {/* VULNERABLE: Stored XSS - renders HTML without sanitization */}
                                    <div
                                        className="comment-body"
                                        dangerouslySetInnerHTML={{ __html: comment.text }}
                                    />
                                    <button
                                        onClick={() => deleteComment(comment.id)}
                                        className="btn-delete"
                                    >
                                        Delete
                                    </button>
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className="vuln-hint">
                        ⚠️ <strong>XSS Vulnerabilities (Both Types):</strong>
                        <br /><br />
                        <strong>1. Reflected XSS (GET):</strong> URL parameter rendered without sanitization<br />
                        <code>?comment=&lt;script&gt;alert(1)&lt;/script&gt;</code>
                        <br /><br />
                        <strong>2. Stored XSS (POST):</strong> Comments stored and displayed to all users<br />
                        <code>Post: &lt;img src=x onerror=alert(document.cookie)&gt;</code>
                    </div>

                    <div className="sample-comments">
                        <h3>Sample XSS Payloads (Click to Test)</h3>
                        <div className="sample-grid">
                            <div className="sample-column">
                                <h4>Reflected (GET)</h4>
                                <a href="/comments?comment=<script>alert('XSS')</script>">Script tag</a>
                                <a href="/comments?comment=<img src=x onerror=alert(1)>">IMG onerror</a>
                                <a href="/comments?comment=<svg onload=alert(1)>">SVG onload</a>
                            </div>
                            <div className="sample-column">
                                <h4>Stored (POST)</h4>
                                <button onClick={() => setNewComment('<script>alert("Stored XSS")</script>')}>
                                    Script tag
                                </button>
                                <button onClick={() => setNewComment('<img src=x onerror=alert(document.cookie)>')}>
                                    Cookie theft
                                </button>
                                <button onClick={() => setNewComment('<svg onload=alert("Persistent")>')}>
                                    SVG persistent
                                </button>
                            </div>
                        </div>
                    </div>

                    <div className="attack-context">
                        <h3>🎯 Attack Context: Why Test Comment Systems?</h3>
                        <div className="context-content">
                            <p><strong>Target:</strong> User-generated content (comments, reviews, profiles)</p>
                            <p><strong>Thought Process:</strong></p>
                            <ul>
                                <li>Comments are common on university websites (announcements, forums)</li>
                                <li>User input is often displayed without proper sanitization</li>
                                <li>Stored XSS is more dangerous - affects all users viewing the page</li>
                                <li>GET parameters allow social engineering via crafted URLs</li>
                                <li>POST submissions are standard for form-based attacks</li>
                            </ul>
                            <p><strong>Business Impact:</strong></p>
                            <ul className="business-impact">
                                <li>💰 <strong>Financial:</strong> Account takeovers leading to fraudulent transactions</li>
                                <li>📊 <strong>Data Breach:</strong> Theft of session cookies, credentials, PII</li>
                                <li>⚖️ <strong>Legal:</strong> GDPR violations ($20M+ fines), lawsuits</li>
                                <li>📉 <strong>Reputation:</strong> Loss of student/faculty trust, negative publicity</li>
                                <li>🎓 <strong>Academic:</strong> Grade manipulation, transcript tampering</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}

export default Comments
