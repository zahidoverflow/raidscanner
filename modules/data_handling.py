import streamlit as st
import json
import yaml
from pathlib import Path
import pandas as pd
from datetime import datetime
import os
import time

def load_config() -> dict:
    """Load configuration from config file"""
    config_path = Path("config.yml")
    if config_path.exists():
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    return {
        'version': 'v2',
        'save_reports': True,
        'report_format': 'HTML',
        'rate_limit': 10,
        'threads': 5,
        'timeout': 10,
        'user_agent': None,
        'cookies': '{}',
        'headers': '{}'
    }

def save_config():
    """Save current configuration to file"""
    config_path = Path("config.yml")
    with open(config_path, 'w') as f:
        yaml.dump(st.session_state.config, f)

def load_scan_history() -> list:
    """Load scan history from file"""
    history_path = Path("scan_history.json")
    if history_path.exists():
        with open(history_path, 'r') as f:
            return json.load(f)
    return []

def save_scan_history():
    """Save scan history to file"""
    history_path = Path("scan_history.json")
    with open(history_path, 'w') as f:
        json.dump(st.session_state.scan_history, f)

def export_results(format_type: str):
    """Export scan results in specified format"""
    if not st.session_state.scan_results:
        st.warning("No results to export")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if format_type == 'csv':
        df = pd.DataFrame(st.session_state.scan_results)
        output_path = f"reports/scan_results_{timestamp}.csv"
        os.makedirs("reports", exist_ok=True)
        df.to_csv(output_path, index=False)
        st.success(f"Results exported to {output_path}")
    
    elif format_type == 'json':
        output_path = f"reports/scan_results_{timestamp}.json"
        os.makedirs("reports", exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(st.session_state.scan_results, f, indent=2)
        st.success(f"Results exported to {output_path}")
    
    elif format_type == 'html':
        from modules.report_generation import generate_report
        output_path = f"reports/scan_results_{timestamp}.html"
        os.makedirs("reports", exist_ok=True)
        generate_report(st.session_state.scan_results, output_path)
        st.success(f"Report generated at {output_path}")

def validate_url(url: str) -> bool:
    """Validate URL format"""
    import re
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None

def sanitize_input(input_str: str) -> str:
    """Sanitize user input"""
    import html
    return html.escape(input_str)

def load_payloads(payload_type: str) -> list:
    """Load payloads from file"""
    payload_path = Path(f"payloads/{payload_type.lower()}.txt")
    if not payload_path.exists():
        return []
    
    with open(payload_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def save_payloads(payload_type: str, payloads: list):
    """Save payloads to file"""
    payload_path = Path(f"payloads/{payload_type.lower()}.txt")
    os.makedirs("payloads", exist_ok=True)
    
    with open(payload_path, 'w') as f:
        f.write('\n'.join(payloads))

def get_scan_statistics() -> dict:
    """Get statistics from scan history"""
    if not st.session_state.scan_history:
        return {
            'total_scans': 0,
            'total_urls': 0,
            'total_vulnerabilities': 0,
            'avg_duration': 0
        }
    
    stats = {
        'total_scans': len(st.session_state.scan_history),
        'total_urls': sum(scan['urls_scanned'] for scan in st.session_state.scan_history),
        'total_vulnerabilities': sum(scan['vulnerabilities_found'] for scan in st.session_state.scan_history),
        'avg_duration': sum(scan['duration'] for scan in st.session_state.scan_history) / len(st.session_state.scan_history)
    }
    
    return stats

def rate_limit_check() -> bool:
    """Check if current request is within rate limits"""
    current_time = time.time()
    rate_limit = st.session_state.config.get('rate_limit', 10)
    
    if 'last_request_time' not in st.session_state:
        st.session_state.last_request_time = current_time
        return True
    
    time_diff = current_time - st.session_state.last_request_time
    if time_diff < (1 / rate_limit):
        return False
    
    st.session_state.last_request_time = current_time
    return True 