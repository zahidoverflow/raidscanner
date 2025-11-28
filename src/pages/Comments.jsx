import { useSearchParams } from 'react-router-dom'
import './Comments.css'

function Comments() {
    const [searchParams] = useSearchParams()
    const comment = searchParams.get('comment') || ''

    return (
        <>
            <div className="comments-hero">
                <h1>💬 Comments Section</h1>
                <p>Share your thoughts about IST</p>
            </div>

            <div className="container">
                <div className="comments-content">
                    <h2>Leave a Comment</h2>

                    <div className="comment-form-info">
                        <p>Enter your comment in the URL parameter:</p>
                        <code>/comments?comment=Your+comment+here</code>
                    </div>

                    {comment && (
                        <div className="comment-display">
                            <h3>Your Comment:</h3>
                            {/* VULNERABLE: Reflected XSS - No sanitization! */}
                            <div
                                className="comment-content"
                                dangerouslySetInnerHTML={{ __html: comment }}
                            />
                        </div>
                    )}

                    {!comment && (
                        <div className="comment-placeholder">
                            <div className="placeholder-icon">💭</div>
                            <h3>No comment provided</h3>
                            <p>Add a <code>?comment=</code> parameter to the URL to display your comment</p>
                        </div>
                    )}

                    <div className="vuln-hint">
                        ⚠️ <strong>XSS Vulnerability:</strong> This page is vulnerable to Cross-Site Scripting (XSS).
                        <br /><br />
                        The comment parameter is rendered without sanitization using <code>dangerouslySetInnerHTML</code>.
                        <br /><br />
                        <strong>Try:</strong> <code>?comment=&lt;script&gt;alert(1)&lt;/script&gt;</code>
                        <br />
                        <strong>Or:</strong> <code>?comment=&lt;img src=x onerror=alert(1)&gt;</code>
                    </div>

                    <div className="sample-comments">
                        <h3>Sample Comments (Click to Test)</h3>
                        <div className="sample-list">
                            <a href="/comments?comment=Great university!">Great university!</a>
                            <a href="/comments?comment=<b>Bold comment</b>">Bold comment (HTML)</a>
                            <a href="/comments?comment=<script>alert('XSS')</script>">XSS Test (script tag)</a>
                            <a href="/comments?comment=<img src=x onerror=alert(1)>">XSS Test (img tag)</a>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}

export default Comments
