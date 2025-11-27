"""
Payload loading and management
"""

import os
from pathlib import Path
from typing import List, Optional


class PayloadLoader:
    """Load and manage vulnerability payloads"""
    
    def __init__(self, payloads_dir: str = None):
        if payloads_dir:
            self.payloads_dir = Path(payloads_dir)
        else:
            self.payloads_dir = Path(__file__).parent.parent / 'payloads'
    
    def load_payloads(self, filename: str) -> List[str]:
        """Load payloads from file"""
        filepath = self.payloads_dir / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"Payload file not found: {filepath}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                payloads = [line.strip() for line in f if line.strip()]
            return payloads
        except Exception as e:
            raise Exception(f"Error loading payloads from {filepath}: {e}")
    
    def load_lfi_payloads(self) -> List[str]:
        """Load LFI payloads"""
        return self.load_payloads('lfi-payloads.txt')
    
    def load_or_payloads(self) -> List[str]:
        """Load Open Redirect payloads"""
        return self.load_payloads('or.txt')
    
    def load_sqli_payloads(self, db_type: str = 'generic') -> List[str]:
        """Load SQL injection payloads"""
        filename = f'sqli/{db_type}.txt'
        return self.load_payloads(filename)
    
    def load_xss_payloads(self) -> List[str]:
        """Load XSS payloads"""
        return self.load_payloads('xss.txt')
    
    def load_crlf_payloads(self) -> List[str]:
        """Load CRLF payloads"""
        # CRLF payloads are generated dynamically in the scanner
        return []
    
    def list_available_payloads(self) -> dict:
        """List all available payload files"""
        payloads = {}
        
        for file in self.payloads_dir.rglob('*.txt'):
            relative_path = file.relative_to(self.payloads_dir)
            category = relative_path.parent.name if relative_path.parent != Path('.') else 'root'
            
            if category not in payloads:
                payloads[category] = []
            
            payloads[category].append(str(relative_path))
        
        return payloads
    
    def get_payload_count(self, filename: str) -> int:
        """Get count of payloads in a file"""
        try:
            payloads = self.load_payloads(filename)
            return len(payloads)
        except:
            return 0
