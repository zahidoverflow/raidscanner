"""
Report generation in multiple formats
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any


class ReportGenerator:
    """Generate vulnerability scan reports"""
    
    def __init__(self, output_dir: str = None):
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            self.output_dir = Path(__file__).parent.parent / 'reports'
        
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_html_report(self, scan_type: str, results: Dict[str, Any]) -> str:
        """Generate HTML report"""
        total_found = results.get('total_found', 0)
        total_scanned = results.get('total_scanned', 0)
        duration = results.get('duration', 0)
        vulnerable_urls = results.get('vulnerable_urls', [])
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RaidScanner Report - {scan_type}</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-900 text-white">
    <div class="container mx-auto px-6 py-8">
        <div class="bg-gray-800 rounded-lg p-6 border border-cyan-500 mb-6">
            <h1 class="text-3xl font-bold bg-gradient-to-r from-cyan-500 to-blue-500 bg-clip-text text-transparent mb-4">
                Security Scan Report
            </h1>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="bg-gray-700 rounded p-4">
                    <div class="text-gray-400 text-sm">Scan Type</div>
                    <div class="text-2xl font-bold text-cyan-500">{scan_type}</div>
                </div>
                <div class="bg-gray-700 rounded p-4">
                    <div class="text-gray-400 text-sm">Vulnerabilities</div>
                    <div class="text-2xl font-bold text-red-500">{total_found}</div>
                </div>
                <div class="bg-gray-700 rounded p-4">
                    <div class="text-gray-400 text-sm">URLs Scanned</div>
                    <div class="text-2xl font-bold text-blue-500">{total_scanned}</div>
                </div>
                <div class="bg-gray-700 rounded p-4">
                    <div class="text-gray-400 text-sm">Duration</div>
                    <div class="text-2xl font-bold text-green-500">{duration}s</div>
                </div>
            </div>
        </div>
        
        <div class="bg-gray-800 rounded-lg p-6 border border-red-500">
            <h2 class="text-2xl font-semibold mb-4">Vulnerable URLs</h2>
            <div class="space-y-2">
"""
        
        for url in vulnerable_urls:
            html_content += f"""
                <div class="bg-red-900 border-l-4 border-red-500 p-3 rounded">
                    <a href="{url}" target="_blank" class="font-mono text-sm break-all hover:text-cyan-500">
                        {url}
                    </a>
                </div>
"""
        
        html_content += """
            </div>
        </div>
    </div>
</body>
</html>
"""
        return html_content
    
    def generate_json_report(self, scan_type: str, results: Dict[str, Any]) -> str:
        """Generate JSON report"""
        report = {
            'scan_type': scan_type,
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_found': results.get('total_found', 0),
                'total_scanned': results.get('total_scanned', 0),
                'duration': results.get('duration', 0)
            },
            'vulnerable_urls': results.get('vulnerable_urls', []),
            'detailed_results': results.get('results', [])
        }
        
        return json.dumps(report, indent=2)
    
    def save_report(self, content: str, filename: str, format: str = 'html') -> Path:
        """Save report to file"""
        if not filename.endswith(f'.{format}'):
            filename = f"{filename}.{format}"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath
    
    def generate_and_save(self, scan_type: str, results: Dict[str, Any], 
                         format: str = 'html') -> Path:
        """Generate and save report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{scan_type.lower()}_report_{timestamp}"
        
        if format == 'html':
            content = self.generate_html_report(scan_type, results)
        elif format == 'json':
            content = self.generate_json_report(scan_type, results)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        return self.save_report(content, filename, format)
