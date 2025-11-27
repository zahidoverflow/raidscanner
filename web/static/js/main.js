// Socket.IO Connection
let socket = null;
let currentScanType = '';
let scanResults = [];

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeSocketIO();
});

// Initialize Socket.IO connection
function initializeSocketIO() {
    socket = io({
        transports: ['websocket', 'polling'],
        reconnection: true,
        reconnectionDelay: 1000,
        reconnectionDelayMax: 5000,
        reconnectionAttempts: 5
    });

    // Connection status handlers
    socket.on('connect', function() {
        updateConnectionStatus('connected');
        console.log('Connected to server');
    });

    socket.on('disconnect', function() {
        updateConnectionStatus('disconnected');
        console.log('Disconnected from server');
    });

    socket.on('connect_error', function() {
        updateConnectionStatus('error');
        console.error('Connection error');
    });

    // Scan progress handler
    socket.on('scan_progress', function(data) {
        updateProgress(data);
    });

    // Scan complete handler
    socket.on('scan_complete', function(data) {
        handleScanComplete(data);
    });

    // Error handler
    socket.on('scan_error', function(data) {
        handleScanError(data);
    });
}

// Update connection status indicator
function updateConnectionStatus(status) {
    const statusElement = document.getElementById('connectionStatus');
    
    const statusConfig = {
        'connected': {
            text: 'Connected',
            color: 'green',
            icon: 'fa-circle-check'
        },
        'disconnected': {
            text: 'Disconnected',
            color: 'red',
            icon: 'fa-circle-xmark'
        },
        'error': {
            text: 'Connection Error',
            color: 'red',
            icon: 'fa-triangle-exclamation'
        }
    };

    const config = statusConfig[status] || statusConfig['disconnected'];
    
    statusElement.innerHTML = `
        <span class="w-2 h-2 bg-${config.color}-500 rounded-full mr-2 ${status === 'connected' ? 'animate-pulse' : ''}"></span>
        ${config.text}
    `;
}

// Start scan configuration
function startScan(scannerType) {
    currentScanType = scannerType;
    
    // Update UI
    document.getElementById('scannerType').innerText = scannerType.toUpperCase();
    document.getElementById('configPanel').classList.remove('hidden');
    
    // Scroll to config panel
    document.getElementById('configPanel').scrollIntoView({ behavior: 'smooth' });
}

// Hide configuration panel
function hideConfig() {
    document.getElementById('configPanel').classList.add('hidden');
    document.getElementById('scanForm').reset();
}

// Show coming soon message
function showComingSoon(feature) {
    alert(`${feature} scanner is coming soon! Currently implementing the web interface.`);
}

// Submit scan form
function submitScan(event) {
    event.preventDefault();
    
    // Get form values
    const urlsText = document.getElementById('urls').value;
    const urls = urlsText.split('\n').filter(url => url.trim() !== '');
    const threads = parseInt(document.getElementById('threads').value);
    
    if (urls.length === 0) {
        alert('Please enter at least one URL');
        return;
    }
    
    // Validate URLs
    const invalidUrls = urls.filter(url => !isValidUrl(url.trim()));
    if (invalidUrls.length > 0) {
        alert(`Invalid URL(s):\n${invalidUrls.join('\n')}`);
        return;
    }
    
    // Hide config, show results
    hideConfig();
    showResultsPanel();
    
    // Start scan
    startScanning(currentScanType, urls, threads);
}

// Validate URL format
function isValidUrl(url) {
    try {
        const urlObj = new URL(url);
        return urlObj.protocol === 'http:' || urlObj.protocol === 'https:';
    } catch (e) {
        return false;
    }
}

// Show results panel
function showResultsPanel() {
    scanResults = [];
    document.getElementById('resultsPanel').classList.remove('hidden');
    document.getElementById('progressBar').style.width = '0%';
    document.getElementById('progressText').innerText = '0%';
    document.getElementById('scanStats').innerText = 'Scanned: 0 | Found: 0';
    document.getElementById('currentUrl').innerText = '';
    document.getElementById('resultsList').innerHTML = `
        <p class="text-gray-400 text-center py-8">
            <i class="fas fa-spinner fa-spin text-3xl mb-2"></i><br>
            Initializing scan...
        </p>
    `;
    
    // Scroll to results
    document.getElementById('resultsPanel').scrollIntoView({ behavior: 'smooth' });
}

// Start scanning via API
function startScanning(scanType, urls, threads) {
    const endpoint = `/api/scan/${scanType}`;
    
    fetch(endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            urls: urls,
            threads: threads
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'started') {
            console.log('Scan started successfully');
        } else {
            handleScanError({ error: data.message || 'Failed to start scan' });
        }
    })
    .catch(error => {
        console.error('Error starting scan:', error);
        handleScanError({ error: 'Failed to connect to server' });
    });
}

// Update progress from socket events
function updateProgress(data) {
    // Update progress bar
    const progress = Math.round(data.progress || 0);
    document.getElementById('progressBar').style.width = progress + '%';
    document.getElementById('progressText').innerText = progress + '%';
    
    // Update stats
    const scanned = data.scanned || 0;
    const found = data.found || 0;
    document.getElementById('scanStats').innerText = `Scanned: ${scanned} | Found: ${found}`;
    
    // Update current URL
    if (data.current_url) {
        document.getElementById('currentUrl').innerText = data.current_url;
    }
    
    // Add vulnerability if found
    if (data.vulnerability) {
        addVulnerability(data.vulnerability);
    }
    
    // Update results list
    if (data.message) {
        updateResultsList(data.message, data.type || 'info');
    }
}

// Add vulnerability to results
function addVulnerability(vuln) {
    scanResults.push(vuln);
    
    const resultsList = document.getElementById('resultsList');
    
    // Clear initialization message if this is the first result
    if (scanResults.length === 1) {
        resultsList.innerHTML = '';
    }
    
    const vulnElement = document.createElement('div');
    vulnElement.className = 'bg-red-900/20 border-2 border-red-500 rounded-lg p-4 hover:bg-red-900/30 transition';
    vulnElement.innerHTML = `
        <div class="flex items-start">
            <i class="fas fa-exclamation-triangle text-red-500 text-xl mr-3 mt-1"></i>
            <div class="flex-1">
                <h4 class="font-semibold text-red-500 mb-2">Vulnerability Found!</h4>
                <p class="text-sm text-gray-300 mb-2"><strong>URL:</strong> ${escapeHtml(vuln.url)}</p>
                ${vuln.payload ? `<p class="text-sm text-gray-300 mb-2"><strong>Payload:</strong> <code class="bg-gray-700 px-2 py-1 rounded">${escapeHtml(vuln.payload)}</code></p>` : ''}
                ${vuln.parameter ? `<p class="text-sm text-gray-300"><strong>Parameter:</strong> ${escapeHtml(vuln.parameter)}</p>` : ''}
            </div>
        </div>
    `;
    
    resultsList.insertBefore(vulnElement, resultsList.firstChild);
}

// Update results list with status messages
function updateResultsList(message, type = 'info') {
    const resultsList = document.getElementById('resultsList');
    
    const typeConfig = {
        'info': { icon: 'fa-info-circle', color: 'blue' },
        'success': { icon: 'fa-check-circle', color: 'green' },
        'warning': { icon: 'fa-exclamation-circle', color: 'yellow' },
        'error': { icon: 'fa-times-circle', color: 'red' }
    };
    
    const config = typeConfig[type] || typeConfig['info'];
    
    const messageElement = document.createElement('div');
    messageElement.className = `bg-gray-700/50 rounded-lg p-3 text-sm flex items-center`;
    messageElement.innerHTML = `
        <i class="fas ${config.icon} text-${config.color}-500 mr-2"></i>
        <span class="text-gray-300">${escapeHtml(message)}</span>
    `;
    
    // Keep only last 10 status messages
    if (resultsList.children.length > 20) {
        const statusMessages = Array.from(resultsList.children).filter(el => 
            el.classList.contains('bg-gray-700/50')
        );
        if (statusMessages.length > 10) {
            statusMessages[statusMessages.length - 1].remove();
        }
    }
    
    resultsList.appendChild(messageElement);
    resultsList.scrollTop = resultsList.scrollHeight;
}

// Handle scan completion
function handleScanComplete(data) {
    updateProgress({ progress: 100 });
    
    const resultsList = document.getElementById('resultsList');
    
    const summaryElement = document.createElement('div');
    summaryElement.className = 'bg-green-900/20 border-2 border-green-500 rounded-lg p-6 mt-4';
    summaryElement.innerHTML = `
        <div class="text-center">
            <i class="fas fa-check-circle text-green-500 text-5xl mb-4"></i>
            <h3 class="text-2xl font-bold mb-4">Scan Complete!</h3>
            <div class="grid grid-cols-2 gap-4 mb-6">
                <div class="bg-gray-700/50 rounded-lg p-4">
                    <p class="text-3xl font-bold text-cyan-500">${data.total_scanned || 0}</p>
                    <p class="text-sm text-gray-400">URLs Scanned</p>
                </div>
                <div class="bg-gray-700/50 rounded-lg p-4">
                    <p class="text-3xl font-bold text-red-500">${scanResults.length}</p>
                    <p class="text-sm text-gray-400">Vulnerabilities</p>
                </div>
            </div>
            ${data.report_path ? `
                <a href="/reports" class="inline-flex items-center bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold transition">
                    <i class="fas fa-file-alt mr-2"></i>View Report
                </a>
            ` : ''}
        </div>
    `;
    
    resultsList.insertBefore(summaryElement, resultsList.firstChild);
}

// Handle scan error
function handleScanError(data) {
    const resultsList = document.getElementById('resultsList');
    
    resultsList.innerHTML = `
        <div class="bg-red-900/20 border-2 border-red-500 rounded-lg p-6 text-center">
            <i class="fas fa-exclamation-triangle text-red-500 text-5xl mb-4"></i>
            <h3 class="text-2xl font-bold mb-2">Scan Error</h3>
            <p class="text-gray-300">${escapeHtml(data.error || 'An unknown error occurred')}</p>
            <button onclick="hideResults()" class="mt-4 bg-red-500 hover:bg-red-600 text-white px-6 py-2 rounded-lg font-semibold transition">
                Close
            </button>
        </div>
    `;
}

// Hide results panel
function hideResults() {
    document.getElementById('resultsPanel').classList.add('hidden');
}

// Escape HTML to prevent XSS in displayed results
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Handle keyboard shortcuts
document.addEventListener('keydown', function(event) {
    // ESC key to close panels
    if (event.key === 'Escape') {
        if (!document.getElementById('configPanel').classList.contains('hidden')) {
            hideConfig();
        }
    }
});
