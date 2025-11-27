"""
Platform-independent scanning engine
Core scanning logic without CLI dependencies
"""

import time
import requests
import urllib.parse
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import random


class ScannerEngine:
    """Platform-independent vulnerability scanner"""
    
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.198 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
    ]
    
    def __init__(self):
        self.scan_state = {
            'vulnerability_found': False,
            'vulnerable_urls': [],
            'total_found': 0,
            'total_scanned': 0,
            'current_url': '',
            'progress': 0
        }
        self.callbacks = []
    
    def add_progress_callback(self, callback):
        """Add callback for progress updates"""
        self.callbacks.append(callback)
    
    def _notify_progress(self, data: dict):
        """Notify all callbacks of progress"""
        for callback in self.callbacks:
            try:
                callback(data)
            except:
                pass
    
    def get_random_user_agent(self) -> str:
        """Get random user agent"""
        return random.choice(self.USER_AGENTS)
    
    def scan_lfi(self, urls: List[str], payloads: List[str], 
                 success_criteria: List[str] = None, threads: int = 5) -> Dict[str, Any]:
        """
        Local File Inclusion scanner
        Returns: dict with results and statistics
        """
        if success_criteria is None:
            success_criteria = ['root:x:0:']
        
        results = {
            'scan_type': 'LFI',
            'start_time': time.time(),
            'vulnerable_urls': [],
            'total_found': 0,
            'total_scanned': 0,
            'results': []
        }
        
        def check_lfi(url: str, payload: str) -> Optional[dict]:
            """Check single LFI payload"""
            encoded_payload = urllib.parse.quote(payload.strip())
            target_url = f"{url}{encoded_payload}"
            start_time = time.time()
            
            try:
                response = requests.get(
                    target_url,
                    headers={'User-Agent': self.get_random_user_agent()},
                    timeout=10
                )
                response_time = round(time.time() - start_time, 2)
                
                is_vulnerable = False
                if response.status_code == 200:
                    is_vulnerable = any(
                        pattern in response.text 
                        for pattern in success_criteria
                    )
                
                results['total_scanned'] += 1
                
                if is_vulnerable:
                    results['total_found'] += 1
                    results['vulnerable_urls'].append(target_url)
                
                return {
                    'url': target_url,
                    'payload': payload.strip(),
                    'vulnerable': is_vulnerable,
                    'response_time': response_time,
                    'status_code': response.status_code
                }
            except Exception as e:
                results['total_scanned'] += 1
                return {
                    'url': target_url,
                    'payload': payload.strip(),
                    'vulnerable': False,
                    'error': str(e)
                }
        
        # Scan all URLs
        with ThreadPoolExecutor(max_workers=threads) as executor:
            for url in urls:
                self.scan_state['current_url'] = url
                futures = [
                    executor.submit(check_lfi, url, payload) 
                    for payload in payloads
                ]
                
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        results['results'].append(result)
                        
                        # Notify progress
                        progress_data = {
                            'type': 'lfi',
                            'current_url': url,
                            'scanned': results['total_scanned'],
                            'total': len(urls) * len(payloads),
                            'found': results['total_found']
                        }
                        self._notify_progress(progress_data)
        
        results['end_time'] = time.time()
        results['duration'] = int(results['end_time'] - results['start_time'])
        
        return results
    
    def scan_sqli(self, urls: List[str], payloads: List[str], 
                  threads: int = 5, time_threshold: int = 10) -> Dict[str, Any]:
        """
        Time-based SQL Injection scanner
        Returns: dict with results and statistics
        """
        results = {
            'scan_type': 'SQLi',
            'start_time': time.time(),
            'vulnerable_urls': [],
            'total_found': 0,
            'total_scanned': 0,
            'results': []
        }
        
        def check_sqli(url: str, payload: str) -> Optional[dict]:
            """Check single SQLi payload"""
            url_with_payload = f"{url}{payload}"
            start_time = time.time()
            
            try:
                response = requests.get(
                    url_with_payload,
                    headers={'User-Agent': self.get_random_user_agent()},
                    timeout=30
                )
                response_time = time.time() - start_time
                
                is_vulnerable = response_time >= time_threshold
                results['total_scanned'] += 1
                
                if is_vulnerable:
                    results['total_found'] += 1
                    results['vulnerable_urls'].append(url_with_payload)
                
                return {
                    'url': url_with_payload,
                    'payload': payload.strip(),
                    'vulnerable': is_vulnerable,
                    'response_time': round(response_time, 2),
                    'status_code': response.status_code
                }
            except Exception as e:
                results['total_scanned'] += 1
                return {
                    'url': url_with_payload,
                    'payload': payload.strip(),
                    'vulnerable': False,
                    'error': str(e)
                }
        
        # Scan all URLs
        with ThreadPoolExecutor(max_workers=threads) as executor:
            for url in urls:
                futures = [
                    executor.submit(check_sqli, url, payload) 
                    for payload in payloads
                ]
                
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        results['results'].append(result)
                        
                        progress_data = {
                            'type': 'sqli',
                            'current_url': url,
                            'scanned': results['total_scanned'],
                            'total': len(urls) * len(payloads),
                            'found': results['total_found']
                        }
                        self._notify_progress(progress_data)
        
        results['end_time'] = time.time()
        results['duration'] = int(results['end_time'] - results['start_time'])
        
        return results
    
    def get_scan_summary(self) -> Dict[str, Any]:
        """Get current scan state summary"""
        return {
            'vulnerable_urls': self.scan_state['vulnerable_urls'],
            'total_found': self.scan_state['total_found'],
            'total_scanned': self.scan_state['total_scanned'],
            'current_url': self.scan_state['current_url'],
            'progress': self.scan_state['progress']
        }
