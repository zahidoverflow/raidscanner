"""
RaidScanner Web Application
Flask-based GUI for vulnerability scanning
"""

# Eventlet monkey-patching must be done FIRST, before any other imports
import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, jsonify, request, send_from_directory, send_file
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import time
from pathlib import Path
from datetime import datetime

# Import core modules
from core.scanner_engine import ScannerEngine
from core.report_generator import ReportGenerator
from core.payload_loader import PayloadLoader
from utils.config import Config

# Initialize Flask app
app = Flask(__name__, 
            static_folder='web/static',
            template_folder='web/templates')
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['JSON_SORT_KEYS'] = False

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": Config.CORS_ORIGINS}})

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Initialize core components
# Note: ScannerEngine is created per-scan to ensure isolation between concurrent scans
report_gen = ReportGenerator()
payload_loader = PayloadLoader()

# Ensure directories exist
Config.ensure_directories()


# ============================================================================
# WEB ROUTES
# ============================================================================

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html')


@app.route('/scanner/<scan_type>')
def scanner_page(scan_type):
    """Scanner configuration page"""
    return render_template('scanner.html', scan_type=scan_type)


@app.route('/reports')
def reports_page():
    """Reports viewer page"""
    return render_template('reports.html')


# ============================================================================
# API ROUTES
# ============================================================================

@app.route('/api/payloads')
def get_payloads():
    """Get available payload files"""
    try:
        payloads = payload_loader.list_available_payloads()
        return jsonify({'success': True, 'payloads': payloads})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/scan/lfi', methods=['POST'])
def scan_lfi():
    """LFI Scan Endpoint"""
    try:
        data = request.json
        urls = data.get('urls', [])
        threads = data.get('threads', 5)
        success_criteria = data.get('success_criteria', ['root:x:0:'])
        scan_id = data.get('scan_id')  # Get scan ID from request

        if not urls:
            return jsonify({'success': False, 'error': 'No URLs provided'}), 400

        # Load payloads
        payloads = payload_loader.load_lfi_payloads()

        # Create a new scanner instance for this scan (ensures isolation)
        scanner = ScannerEngine()

        def progress_callback(progress_data):
            progress_data['scan_id'] = scan_id  # Include scan ID in progress
            socketio.emit('scan_progress', progress_data)

        scanner.add_progress_callback(progress_callback)

        # Run scan in background using socketio's background task (works with eventlet)
        def run_scan():
            try:
                results = scanner.scan_lfi(urls, payloads, success_criteria, threads)

                # Generate and save report
                report_gen.generate_and_save('LFI', results, 'html')
                report_gen.generate_and_save('LFI', results, 'json')

                socketio.emit('scan_complete', {
                    'success': True,
                    'results': results,
                    'scan_id': scan_id  # Include scan ID in completion
                })
            except Exception as e:
                socketio.emit('scan_error', {
                    'success': False,
                    'error': str(e),
                    'scan_id': scan_id  # Include scan ID in error
                })

        socketio.start_background_task(run_scan)

        return jsonify({'success': True, 'message': 'Scan started'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/scan/sqli', methods=['POST'])
def scan_sqli():
    """SQLi Scan Endpoint"""
    try:
        data = request.json
        urls = data.get('urls', [])
        threads = data.get('threads', 5)
        scan_id = data.get('scan_id')  # Get scan ID from request

        if not urls:
            return jsonify({'success': False, 'error': 'No URLs provided'}), 400

        # Load payloads
        payloads = payload_loader.load_sqli_payloads()

        # Create a new scanner instance for this scan (ensures isolation)
        scanner = ScannerEngine()

        def progress_callback(progress_data):
            progress_data['scan_id'] = scan_id  # Include scan ID in progress
            socketio.emit('scan_progress', progress_data)

        scanner.add_progress_callback(progress_callback)

        # Run scan in background using socketio's background task (works with eventlet)
        def run_scan():
            try:
                results = scanner.scan_sqli(urls, payloads, threads)

                # Generate and save report
                report_gen.generate_and_save('SQLi', results, 'html')
                report_gen.generate_and_save('SQLi', results, 'json')

                socketio.emit('scan_complete', {
                    'success': True,
                    'results': results,
                    'scan_id': scan_id  # Include scan ID in completion
                })
            except Exception as e:
                socketio.emit('scan_error', {
                    'success': False,
                    'error': str(e),
                    'scan_id': scan_id  # Include scan ID in error
                })

        socketio.start_background_task(run_scan)

        return jsonify({'success': True, 'message': 'Scan started'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/scan/xss', methods=['POST'])
def scan_xss():
    """XSS Scan Endpoint"""
    try:
        data = request.json
        urls = data.get('urls', [])
        threads = data.get('threads', 3)
        scan_id = data.get('scan_id')  # Get scan ID from request

        if not urls:
            return jsonify({'success': False, 'error': 'No URLs provided'}), 400

        payloads = payload_loader.load_xss_payloads()

        # Create a new scanner instance for this scan (ensures isolation)
        scanner = ScannerEngine()

        def progress_callback(progress_data):
            progress_data['scan_id'] = scan_id  # Include scan ID in progress
            socketio.emit('scan_progress', progress_data)

        scanner.add_progress_callback(progress_callback)

        def run_scan():
            try:
                results = scanner.scan_xss(urls, payloads, threads)

                # Generate and save report
                report_gen.generate_and_save('XSS', results, 'html')
                report_gen.generate_and_save('XSS', results, 'json')

                socketio.emit('scan_complete', {
                    'success': True,
                    'results': results,
                    'scan_id': scan_id  # Include scan ID in completion
                })
            except Exception as e:
                socketio.emit('scan_error', {
                    'success': False,
                    'error': str(e),
                    'scan_id': scan_id  # Include scan ID in error
                })

        socketio.start_background_task(run_scan)

        return jsonify({'success': True, 'message': 'Scan started'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/scan/or', methods=['POST'])
def scan_or():
    """Open Redirect Scan Endpoint"""
    try:
        data = request.json
        urls = data.get('urls', [])
        threads = data.get('threads', 5)
        scan_id = data.get('scan_id')  # Get scan ID from request

        if not urls:
            return jsonify({'success': False, 'error': 'No URLs provided'}), 400

        payloads = payload_loader.load_or_payloads()

        # Create a new scanner instance for this scan (ensures isolation)
        scanner = ScannerEngine()

        def progress_callback(progress_data):
            progress_data['scan_id'] = scan_id  # Include scan ID in progress
            socketio.emit('scan_progress', progress_data)

        scanner.add_progress_callback(progress_callback)

        def run_scan():
            try:
                results = scanner.scan_or(urls, payloads, threads)

                # Generate and save report
                report_gen.generate_and_save('OpenRedirect', results, 'html')
                report_gen.generate_and_save('OpenRedirect', results, 'json')

                socketio.emit('scan_complete', {
                    'success': True,
                    'results': results,
                    'scan_id': scan_id  # Include scan ID in completion
                })
            except Exception as e:
                socketio.emit('scan_error', {
                    'success': False,
                    'error': str(e),
                    'scan_id': scan_id  # Include scan ID in error
                })

        socketio.start_background_task(run_scan)

        return jsonify({'success': True, 'message': 'Scan started'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/scan/crlf', methods=['POST'])
def scan_crlf():
    """CRLF Injection Scan Endpoint"""
    try:
        data = request.json
        urls = data.get('urls', [])
        threads = data.get('threads', 5)
        scan_id = data.get('scan_id')  # Get scan ID from request

        if not urls:
            return jsonify({'success': False, 'error': 'No URLs provided'}), 400

        # Create a new scanner instance for this scan (ensures isolation)
        scanner = ScannerEngine()

        def progress_callback(progress_data):
            progress_data['scan_id'] = scan_id  # Include scan ID in progress
            socketio.emit('scan_progress', progress_data)

        scanner.add_progress_callback(progress_callback)

        def run_scan():
            try:
                results = scanner.scan_crlf(urls, threads)

                # Generate and save report
                report_gen.generate_and_save('CRLF', results, 'html')
                report_gen.generate_and_save('CRLF', results, 'json')

                socketio.emit('scan_complete', {
                    'success': True,
                    'results': results,
                    'scan_id': scan_id  # Include scan ID in completion
                })
            except Exception as e:
                socketio.emit('scan_error', {
                    'success': False,
                    'error': str(e),
                    'scan_id': scan_id  # Include scan ID in error
                })

        socketio.start_background_task(run_scan)

        return jsonify({'success': True, 'message': 'Scan started'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/reports', methods=['GET'])
def get_reports():
    """List available reports"""
    try:
        reports_dir = Path(Config.REPORTS_DIR)
        reports = []
        
        if reports_dir.exists():
            for report_file in reports_dir.glob('*.html'):
                # Parse report metadata
                name = report_file.stem
                date = datetime.fromtimestamp(report_file.stat().st_mtime)
                
                # Extract scan type from filename using prefix matching
                scan_type = 'unknown'
                name_lower = name.lower()

                # Check most specific patterns first to avoid false positives
                if name_lower.startswith('crlf_') or 'crlf_report' in name_lower:
                    scan_type = 'crlf'
                elif name_lower.startswith('xss_') or 'xss_report' in name_lower:
                    scan_type = 'xss'
                elif name_lower.startswith('sqli_') or 'sqli_report' in name_lower or 'sql_' in name_lower:
                    scan_type = 'sqli'
                elif name_lower.startswith('lfi_') or 'lfi_report' in name_lower:
                    scan_type = 'lfi'
                elif name_lower.startswith('openredirect_') or name_lower.startswith('or_'):
                    scan_type = 'or'
                
                reports.append({
                    'name': name,
                    'type': scan_type,
                    'date': date.isoformat(),
                    'path': str(report_file),
                    'vulnerabilities': 0,  # TODO: Parse from report
                    'urls_tested': 0,  # TODO: Parse from report
                    'payloads': 0  # TODO: Parse from report
                })
        
        # Sort by date, newest first
        reports.sort(key=lambda x: x['date'], reverse=True)
        
        return jsonify({'reports': reports})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reports/download')
def download_report():
    """Download a specific report"""
    try:
        report_path = request.args.get('path')
        format_type = request.args.get('format', 'html')
        
        if not report_path:
            return jsonify({'error': 'Report path required'}), 400
        
        file_path = Path(report_path)
        
        if not file_path.exists():
            return jsonify({'error': 'Report not found'}), 404
        
        # Handle JSON format
        if format_type == 'json':
            json_path = file_path.with_suffix('.json')
            if json_path.exists():
                return send_file(json_path, as_attachment=True)
            else:
                return jsonify({'error': 'JSON report not found'}), 404
        
        # Default to HTML
        return send_file(file_path, as_attachment=True)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# WEBSOCKET EVENTS
# ============================================================================

@socketio.on('connect')
def handle_connect():
    """Client connected"""
    emit('connected', {'message': 'Connected to RaidScanner', 'timestamp': time.time()})


@socketio.on('disconnect')
def handle_disconnect():
    """Client disconnected"""
    print('Client disconnected')


@socketio.on('ping')
def handle_ping():
    """Ping/pong for connection check"""
    emit('pong', {'timestamp': time.time()})


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("=" * 80)
    print("🚀 RaidScanner Web Interface")
    print("=" * 80)
    print(f"📍 URL: http://{Config.HOST}:{Config.PORT}")
    print(f"🔧 Debug Mode: {Config.DEBUG}")
    print("=" * 80)
    print("\nPress Ctrl+C to stop the server\n")
    
    socketio.run(
        app,
        debug=Config.DEBUG,
        host=Config.HOST,
        port=Config.PORT,
        allow_unsafe_werkzeug=True
    )
