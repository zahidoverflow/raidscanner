import { useSearchParams, useNavigate } from 'react-router-dom'
import { useEffect, useState } from 'react'
import './Redirect.css'

function Redirect() {
    const [searchParams] = useSearchParams()
    const navigate = useNavigate()
    const url = searchParams.get('url')
    const [countdown, setCountdown] = useState(3)
    const [redirecting, setRedirecting] = useState(false)

    useEffect(() => {
        if (url) {
            setRedirecting(true)

            // Countdown timer
            const timer = setInterval(() => {
                setCountdown(prev => {
                    if (prev <= 1) {
                        clearInterval(timer)
                        // VULNERABLE: No validation - redirects to ANY URL
                        window.location.href = url
                        return 0
                    }
                    return prev - 1
                })
            }, 1000)

            return () => clearInterval(timer)
        }
    }, [url])

    if (!url) {
        return (
            <>
                <div className="redirect-hero">
                    <h1>🔗 URL Redirector</h1>
                    <p>Redirect to external links</p>
                </div>

                <div className="container">
                    <div className="redirect-content">
                        <h2>No Redirect URL Provided</h2>

                        <div className="redirect-info">
                            <p>Use the <code>url</code> parameter to redirect to another site:</p>

                            <form
                                onSubmit={(e) => {
                                    e.preventDefault()
                                    const formData = new FormData(e.target)
                                    const url = formData.get('url')
                                    if (url) {
                                        // Update URL param to trigger redirect
                                        window.location.href = `/redirect?url=${encodeURIComponent(url)}`
                                    }
                                }}
                                style={{ margin: '1rem 0', display: 'flex', gap: '0.5rem' }}
                            >
                                <input
                                    name="url"
                                    type="text"
                                    placeholder="https://example.com"
                                    className="email-input"
                                    style={{ flex: 1 }}
                                />
                                <button type="submit" className="btn btn-primary">Go</button>
                            </form>
                        </div>

                        <div className="vuln-hint">
                            ⚠️ <strong>Open Redirect Vulnerability:</strong> This page redirects to ANY URL without validation.
                            <br /><br />
                            An attacker can craft malicious links that appear to be from IST but redirect to phishing sites.
                            <br /><br />
                            <strong>Try:</strong> <code>?url=//google.com</code>
                            <br />
                            <strong>Or:</strong> <code>?url=https://evil.com</code>
                        </div>

                        <div className="sample-redirects">
                            <h3>Sample Redirects (Click to Test)</h3>
                            <div className="sample-list">
                                <a href="/redirect?url=https://www.google.com">Google (Full URL)</a>
                                <a href="/redirect?url=//google.com">Google (Protocol-relative)</a>
                                <a href="/redirect?url=///google.com">Google (Triple slash)</a>
                                <a href="/redirect?url=https://github.com">GitHub</a>
                            </div>
                        </div>
                    </div>
                </div>
            </>
        )
    }

    return (
        <>
            <div className="redirect-hero redirect-active">
                <h1>⏳ Redirecting...</h1>
                <p>Please wait</p>
            </div>

            <div className="container">
                <div className="redirect-content">
                    <div className="redirect-box">
                        <div className="redirect-icon">🔄</div>
                        <h2>Redirecting in {countdown}...</h2>

                        <div className="redirect-details">
                            <p><strong>Destination:</strong></p>
                            <code className="redirect-url">{url}</code>
                        </div>

                        <div className="redirect-actions">
                            <a href={url} className="btn">Go Now</a>
                            <button className="btn btn-secondary" onClick={() => navigate('/')}>Cancel</button>
                        </div>

                        <div className="vuln-warning">
                            ⚠️ This redirect is unvalidated. You are being redirected to an external site.
                            <br />
                            In a real application, this could be a phishing attack.
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}

export default Redirect
