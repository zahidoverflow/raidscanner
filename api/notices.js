// API endpoint for LFI vulnerability testing
// This allows CLI scanners to detect the vulnerability

export default function handler(req, res) {
    // Enable CORS for scanner
    res.setHeader('Access-Control-Allow-Origin', '*')
    res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS')

    if (req.method === 'OPTIONS') {
        return res.status(200).end()
    }

    const { file } = req.query

    if (!file) {
        return res.status(200).send('No file specified')
    }

    // VULNERABLE: Path traversal detection
    const hasPathTraversal = file.includes('../') ||
        file.includes('....//') ||
        file.includes('..\\') ||
        file.includes('%2e%2e') ||
        file.includes('%2e%2e%2f') ||
        file.includes('..%2f') ||
        file.includes('..%5c')

    const isEtcPasswd = file.toLowerCase().includes('etc/passwd') ||
        file.toLowerCase().includes('etc\\passwd')

    const isWinIni = file.toLowerCase().includes('windows') &&
        file.toLowerCase().includes('win.ini')

    // Simulate LFI vulnerability - return file content
    if (hasPathTraversal && isEtcPasswd) {
        // Return simulated /etc/passwd content
        return res.status(200).send(`root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
`)
    }

    if (hasPathTraversal && isWinIni) {
        // Return simulated win.ini content
        return res.status(200).send(`; for 16-bit app support
[fonts]
[extensions]
[mci extensions]
[files]
[Mail]
MAPI=1
`)
    }

    if (hasPathTraversal) {
        // Generic path traversal detected
        return res.status(200).send(`LFI Vulnerability Detected!
Path traversal attempt: ${file}
This would expose sensitive files in a real application.`)
    }

    // Normal file request
    return res.status(200).send(`Notice: ${file}
This is a normal notice file.`)
}
