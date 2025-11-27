"""
Configuration management for RaidScanner
"""

import os
from pathlib import Path


class Config:
    """Application configuration"""
    
    # Base paths
    BASE_DIR = Path(__file__).parent.parent
    PAYLOADS_DIR = BASE_DIR / 'payloads'
    OUTPUT_DIR = BASE_DIR / 'output'
    REPORTS_DIR = BASE_DIR / 'reports'
    
    # Web app settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # Scanning settings
    DEFAULT_THREADS = 5
    MAX_THREADS = 10
    DEFAULT_TIMEOUT = 10
    MAX_TIMEOUT = 60
    
    # Security settings
    RATE_LIMIT = "100 per hour"
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')
    
    # Chrome/Selenium settings
    HEADLESS = True
    CHROME_OPTIONS = [
        '--headless',
        '--no-sandbox',
        '--disable-dev-shm-usage',
        '--disable-gpu',
        '--disable-extensions',
        '--disable-browser-side-navigation',
        '--disable-infobars',
        '--disable-notifications'
    ]
    
    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist"""
        cls.OUTPUT_DIR.mkdir(exist_ok=True)
        cls.REPORTS_DIR.mkdir(exist_ok=True)
        cls.PAYLOADS_DIR.mkdir(exist_ok=True)
    
    @classmethod
    def get_payload_file(cls, vuln_type, filename=None):
        """Get path to payload file"""
        if filename:
            return cls.PAYLOADS_DIR / filename
        
        # Default payload files
        defaults = {
            'lfi': 'lfi-payloads.txt',
            'or': 'or.txt',
            'sqli': 'sqli/generic.txt',
            'xss': 'xss.txt',
            'crlf': 'crlf.txt'
        }
        
        return cls.PAYLOADS_DIR / defaults.get(vuln_type, 'default.txt')
