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
                # Check response regardless of status code
                # Check for success criteria (case-insensitive)
                response_text_lower = response.text.lower()
                
                is_vulnerable = any(
                    pattern.lower() in response_text_lower 
                    for pattern in success_criteria
                )
                    
                # Also check for common LFI indicators/warnings
                if not is_vulnerable:
                    lfi_indicators = [
                        "path traversal detected",
                        "vulnerable to local file inclusion",
                        "warning: include(",
                        "failed to open stream",
                        "root:x:0:0",
                        "[boot loader]",
                        "drivers",
                        "intentionally vulnerable application",
                        "failed to open stream"
                    ]
                    is_vulnerable = any(indicator in response_text_lower for indicator in lfi_indicators)
                
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
                        
                        # Notify progress with individual result
                        progress_data = {
                            'type': 'lfi',
                            'current_url': url,
                            'scanned': results['total_scanned'],
                            'total': len(urls) * len(payloads),
                            'found': results['total_found'],
                            'results': [result]  # Send individual result for real-time display
                        }
                        self._notify_progress(progress_data)
        
        results['end_time'] = time.time()
        results['duration'] = int(results['end_time'] - results['start_time'])
        
        return results
    
    def scan_sqli(self, urls: List[str], payloads: List[str], 
                  threads: int = 5, time_threshold: int = 10) -> Dict[str, Any]:
        """
        SQL Injection scanner (Time-based + Error-based)
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
            url_with_payload = f"{url}{urllib.parse.quote(payload.strip())}"
            start_time = time.time()
            
            try:
                response = requests.get(
                    url_with_payload,
                    headers={'User-Agent': self.get_random_user_agent()},
                    timeout=30
                )
                response_time = time.time() - start_time
                
                # Check 1: Time-based detection
                is_vulnerable = response_time >= time_threshold

                # Check 2: Error-based detection (if not already found)
                if not is_vulnerable:
                    # Common SQL error patterns (including DVWU specific)
                    sql_errors = [
                        "sql error",
                        "mysql error",
                        "syntax error",
                        "ora-", 
                        "unclosed quotation mark",
                        "detected injection attempt", # DVWU specific
                        "vulnerable to sql injection" # DVWU specific
                    ]
                    response_text_lower = response.text.lower()
                    is_vulnerable = any(error in response_text_lower for error in sql_errors)

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
                            'found': results['total_found'],
                            'results': [result]
                        }
                        self._notify_progress(progress_data)
        
        results['end_time'] = time.time()
        results['duration'] = int(results['end_time'] - results['start_time'])
        
        return results
    
    def scan_xss(self, urls: List[str], payloads: List[str], 
                 threads: int = 3) -> Dict[str, Any]:
        """
        XSS Scanner using Selenium for DOM-based and Reflected XSS
        Uses fewer threads due to Selenium resource requirements
        """
        results = {
            'scan_type': 'XSS',
            'start_time': time.time(),
            'vulnerable_urls': [],
            'total_found': 0,
            'total_scanned': 0,
            'results': []
        }
        
        def check_xss(url: str, payload: str) -> Optional[dict]:
            """Check single XSS payload"""
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.common.exceptions import TimeoutException, WebDriverException
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from utils.config import Config
            
            target_url = f"{url}{urllib.parse.quote(payload.strip())}"
            driver = None
            is_vulnerable = False
            
            try:
                # Setup headless Chrome
                chrome_options = Options()
                for arg in Config.CHROME_OPTIONS:
                    chrome_options.add_argument(arg)
                
                driver = webdriver.Chrome(options=chrome_options)
                driver.set_page_load_timeout(10)
                driver.get(target_url)
                
                # Check for alert (classic XSS indicator)
                try:
                    WebDriverWait(driver, 3).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()
                    is_vulnerable = True
                except TimeoutException:
                    # Also check if payload appears unescaped in source
                    # DVWU returns hybrid HTML, check if raw payload exists
                    page_source = driver.page_source
                    if payload.strip() in page_source:
                        is_vulnerable = True
                
                results['total_scanned'] += 1
                
                if is_vulnerable:
                    results['total_found'] += 1
                    results['vulnerable_urls'].append(target_url)
                
                return {
                    'url': target_url,
                    'payload': payload.strip(),
                    'vulnerable': is_vulnerable,
                    'method': 'selenium'
                }
            except Exception as e:
                results['total_scanned'] += 1
                return {
                    'url': target_url,
                    'payload': payload.strip(),
                    'vulnerable': False,
                    'error': str(e)
                }
            finally:
                if driver:
                    try:
                        driver.quit()
                    except:
                        pass
        
        # Scan all URLs (use fewer threads for Selenium)
        with ThreadPoolExecutor(max_workers=min(threads, 3)) as executor:
            for url in urls:
                futures = [
                    executor.submit(check_xss, url, payload) 
                    for payload in payloads
                ]
                
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        results['results'].append(result)
                        
                        progress_data = {
                            'type': 'xss',
                            'current_url': url,
                            'scanned': results['total_scanned'],
                            'total': len(urls) * len(payloads),
                            'found': results['total_found'],
                            'results': [result]
                        }
                        self._notify_progress(progress_data)
        
        results['end_time'] = time.time()
        results['duration'] = int(results['end_time'] - results['start_time'])
        
        return results
    
    def scan_or(self, urls: List[str], payloads: List[str], 
                threads: int = 5) -> Dict[str, Any]:
        """
        Open Redirect Scanner
        Checks if Location header, meta refresh, or JS redirect contains payload
        """
        results = {
            'scan_type': 'Open Redirect',
            'start_time': time.time(),
            'vulnerable_urls': [],
            'total_found': 0,
            'total_scanned': 0,
            'results': []
        }
        
        def check_or(url: str, payload: str) -> Optional[dict]:
            """Check single Open Redirect payload"""
            # Ensure payload is URL-encoded for the request
            target_url = f"{url}{urllib.parse.quote(payload.strip())}"
            # For checking in response, we use the raw payload
            raw_payload = payload.strip()
            
            try:
                response = requests.get(
                    target_url,
                    headers={'User-Agent': self.get_random_user_agent()},
                    timeout=10,
                    allow_redirects=False
                )
                
                is_vulnerable = False
                redirect_location = None
                
                # Method 1: Check Location header (Server-side redirect)
                if 'Location' in response.headers:
                    location = response.headers['Location']
                    if raw_payload in location:
                        is_vulnerable = True
                        redirect_location = location
                
                # Method 2: Check Client-side redirects (Meta + JS)
                if not is_vulnerable and response.status_code == 200:
                    response_text = response.text
                    
                    # Check for JS redirects (window.location = ...)
                    # Common patterns: window.location.href =, window.location =, location.href =
                    js_redirect_patterns = [
                        f'window.location.href = "{raw_payload}"',
                        f"window.location.href = '{raw_payload}'",
                        f'window.location = "{raw_payload}"',
                        f'location.href = "{raw_payload}"'
                    ]
                    
                    if raw_payload in response_text:
                        # Loose check first, then verify if it looks like a redirect structure
                        if any(pattern in response_text for pattern in js_redirect_patterns):
                             is_vulnerable = True
                        elif f'meta http-equiv="refresh" content="0;url={raw_payload}"' in response_text.lower():
                             is_vulnerable = True
                        # Fallback: simple match if we suspect it's just reflected in a script tag (DVWU specific)
                        elif f'<script>window.location.href = "{raw_payload}"</script>' in response_text:
                             is_vulnerable = True

                results['total_scanned'] += 1
                
                if is_vulnerable:
                    results['total_found'] += 1
                    results['vulnerable_urls'].append(target_url)
                
                return {
                    'url': target_url,
                    'payload': payload.strip(),
                    'vulnerable': is_vulnerable,
                    'redirect_location': redirect_location,
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
                futures = [
                    executor.submit(check_or, url, payload) 
                    for payload in payloads
                ]
                
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        results['results'].append(result)
                        
                        progress_data = {
                            'type': 'or',
                            'current_url': url,
                            'scanned': results['total_scanned'],
                            'total': len(urls) * len(payloads),
                            'found': results['total_found'],
                            'results': [result]
                        }
                        self._notify_progress(progress_data)
        
        results['end_time'] = time.time()
        results['duration'] = int(results['end_time'] - results['start_time'])
        
        return results
    
    def scan_crlf(self, urls: List[str], threads: int = 5) -> Dict[str, Any]:
        """
        CRLF Injection Scanner
        Tests for HTTP Response Splitting via CRLF sequences
        """
        # Generate CRLF payloads dynamically
        payloads = [
            '%0d%0aSet-Cookie:crlf=injection',
            '%0aSet-Cookie:crlf=injection',
            '%0dSet-Cookie:crlf=injection',
            '%0d%0a%0d%0aHTTP/1.1%20200%20OK',
            '%E5%98%8A%E5%98%8DSet-Cookie:crlf=injection',
            '\r\nSet-Cookie:crlf=injection',
            '\nSet-Cookie:crlf=injection',
            '\rSet-Cookie:crlf=injection'
        ]
        
        results = {
            'scan_type': 'CRLF',
            'start_time': time.time(),
            'vulnerable_urls': [],
            'total_found': 0,
            'total_scanned': 0,
            'results': []
        }
        
        def check_crlf(url: str, payload: str) -> Optional[dict]:
            """Check single CRLF payload"""
            target_url = f"{url}{payload}"
            
            try:
                response = requests.get(
                    target_url,
                    headers={'User-Agent': self.get_random_user_agent()},
                    timeout=10,
                    allow_redirects=False
                )
                
                is_vulnerable = False
                injected_header = None
                
                # Check if our injected header appears in response
                if 'Set-Cookie' in response.headers:
                    set_cookie = response.headers['Set-Cookie']
                    if 'crlf=injection' in set_cookie:
                        is_vulnerable = True
                        injected_header = set_cookie
                
                results['total_scanned'] += 1
                
                if is_vulnerable:
                    results['total_found'] += 1
                    results['vulnerable_urls'].append(target_url)
                
                return {
                    'url': target_url,
                    'payload': payload,
                    'vulnerable': is_vulnerable,
                    'injected_header': injected_header,
                    'status_code': response.status_code
                }
            except Exception as e:
                results['total_scanned'] += 1
                return {
                    'url': target_url,
                    'payload': payload,
                    'vulnerable': False,
                    'error': str(e)
                }
        
        # Scan all URLs
        with ThreadPoolExecutor(max_workers=threads) as executor:
            for url in urls:
                futures = [
                    executor.submit(check_crlf, url, payload) 
                    for payload in payloads
                ]
                
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        results['results'].append(result)
                        
                        progress_data = {
                            'type': 'crlf',
                            'current_url': url,
                            'scanned': results['total_scanned'],
                            'total': len(urls) * len(payloads),
                            'found': results['total_found'],
                            'results': [result]
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
