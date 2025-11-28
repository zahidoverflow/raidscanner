import { useSearchParams } from 'react-router-dom'
import { useState } from 'react'
import './Newsletter.css'

function Newsletter() {
    const [searchParams] = useSearchParams()
    const email = searchParams.get('email') || ''
    const [submitted, setSubmitted] = useState(false)

    // VULNERABLE: Detect CRLF injection attempts
    const hasCRLF = email.includes('%0d%0a') || email.includes('%0D%0A') ||
        email.includes('\\r\\n') || email.includes('\\n') ||
        email.includes('\\r') || email.includes('\r\n') ||
        email.includes('\n') || email.includes('\r')

    const handleSubmit = (e) => {
        e.preventDefault()
        setSubmitted(true)
    }

    // Extract potential header injection
    const emailParts = email.split(/(%0d%0a|%0D%0A|\\r\\n|\\n|\\r|\r\n|\n|\r)/i)
    const actualEmail = emailParts[0]
    const injectedHeaders = emailParts.slice(1).filter(p => p && !p.match(/(%0d%0a|%0D%0A|\\r\\n|\\n|\\r|\r\n|\n|\r)/i))

    return (
        <>
            <div className="newsletter-hero">
                <h1>📧 Newsletter Subscription</h1>
                <p>Stay updated with IST news and events</p>
            </div>

            <div className="container">
                <div className="newsletter-content">
                    <div className="newsletter-box">
                        <h2>Subscribe to Our Newsletter</h2>

                        <div className="newsletter-info">
                            <p>Enter your email in the URL parameter:</p>
                            <code>/newsletter?email=your@email.com</code>
                        </div>

                        {email && (
                            <div className={`subscription-result ${hasCRLF ? 'vulnerable' : 'normal'}`}>
                                <h3>{hasCRLF ? '⚠️ CRLF Injection Detected!' : '✅ Email Received'}</h3>

                                <div className="email-details">
                                    <p><strong>Email:</strong></p>
                                    <code className="email-value">{actualEmail}</code>

                                    {hasCRLF && injectedHeaders.length > 0 && (
                                        <div className="injected-headers">
                                            <p><strong>⚠️ Injected Headers Detected:</strong></p>
                                            <pre className="header-injection">
                                                {injectedHeaders.join('\n')}
                                            </pre>
                                        </div>
                                    )}

                                    {hasCRLF && (
                                        <div className="crlf-explanation">
                                            <h4>CRLF Injection Vulnerability</h4>
                                            <p>This input contains CRLF (Carriage Return Line Feed) sequences:</p>
                                            <ul>
                                                <li><code>%0d%0a</code> - URL-encoded CRLF</li>
                                                <li><code>\r\n</code> - Literal CRLF</li>
                                            </ul>
                                            <p><strong>Impact:</strong> An attacker could inject malicious HTTP headers, potentially:</p>
                                            <ul>
                                                <li>Setting cookies (<code>Set-Cookie:</code>)</li>
                                                <li>Redirecting users (<code>Location:</code>)</li>
                                                <li>Cache poisoning (<code>Content-Length: 0</code>)</li>
                                                <li>XSS via headers</li>
                                            </ul>
                                        </div>
                                    )}
                                </div>

                                {!hasCRLF && !submitted && (
                                    <button className="btn" onClick={handleSubmit}>Subscribe</button>
                                )}

                                {submitted && !hasCRLF && (
                                    <div className="success-message">
                                        ✅ Thank you for subscribing!
                                    </div>
                                )}
                            </div>
                        )}

                        {!email && (
                            <div className="newsletter-placeholder">
                                <div className="placeholder-icon">✉️</div>
                                <h3>No email provided</h3>
                                <p>Add an <code>?email=</code> parameter to the URL</p>
                            </div>
                        )}
                    </div>

                    <div className="vuln-hint">
                        ⚠️ <strong>CRLF Injection Vulnerability:</strong> This page doesn't sanitize email input.
                        <br /><br />
                        CRLF sequences (<code>%0d%0a</code> or <code>\r\n</code>) can inject HTTP headers.
                        <br /><br />
                        <strong>Try:</strong> <code>?email=test@test.com%0d%0aSet-Cookie: admin=true</code>
                        <br />
                        <strong>Or:</strong> <code>?email=test%0d%0aContent-Length: 0</code>
                    </div>

                    <div className="sample-emails">
                        <h3>Sample Inputs (Click to Test)</h3>
                        <div className="sample-list">
                            <a href="/newsletter?email=student@ist.edu.bd">Valid Email</a>
                            <a href="/newsletter?email=test@test.com%0d%0aSet-Cookie: admin=true">CRLF - Cookie Injection</a>
                            <a href="/newsletter?email=test%0d%0aLocation: https://evil.com">CRLF - Redirect Injection</a>
                            <a href="/newsletter?email=test%0d%0aContent-Length: 0">CRLF - Cache Poisoning</a>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}

export default Newsletter
