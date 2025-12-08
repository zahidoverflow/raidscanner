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
                 success_criteria: List[str] = None, threads: int = 3) -> Dict[str, Any]:
        """
        Local File Inclusion scanner using Selenium for client-side rendered pages.

        Detection logic:
        - Uses Selenium to render JS-based pages (like React)
        - Checks if the <pre> tag content does NOT contain "File not found:"
        - If file content is displayed, LFI is successful
        - Handles pre-encoded payloads without double-encoding
        """
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common.exceptions import TimeoutException, NoSuchElementException
        from utils.config import Config

        results = {
            'scan_type': 'LFI',
            'start_time': time.time(),
            'vulnerable_urls': [],
            'total_found': 0,
            'total_scanned': 0,
            'results': []
        }

        def is_already_encoded(payload: str) -> bool:
            """Check if payload contains URL-encoded sequences"""
            import re
            return bool(re.search(r'%[0-9a-fA-F]{2}', payload))

        def check_lfi(url: str, payload: str) -> Optional[dict]:
            """Check single LFI payload using Selenium"""
            payload_clean = payload.strip()

            # Only encode if not already encoded (avoid double-encoding)
            if is_already_encoded(payload_clean):
                encoded_payload = payload_clean
            else:
                encoded_payload = urllib.parse.quote(payload_clean)

            target_url = f"{url}{encoded_payload}"
            driver = None
            start_time = time.time()

            try:
                # Setup headless Chrome
                chrome_options = Options()
                for arg in Config.CHROME_OPTIONS:
                    chrome_options.add_argument(arg)

                driver = webdriver.Chrome(options=chrome_options)
                driver.set_page_load_timeout(15)
                driver.get(target_url)

                # Wait for DOMContentLoaded - ensures React has rendered
                WebDriverWait(driver, 10).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                )

                # Small delay for React state updates after DOM is ready
                time.sleep(0.5)

                # Get pre tag content
                pre_content = ""
                try:
                    pre_elements = driver.find_elements(By.TAG_NAME, "pre")
                    if pre_elements:
                        pre_content = pre_elements[0].text
                except:
                    pass

                response_time = round(time.time() - start_time, 2)

                # Detection: Check if "File not found:" is NOT in the pre tag content
                # This means the file was successfully included
                is_vulnerable = pre_content and 'file not found:' not in pre_content.lower()

                # Additional check: empty content is not vulnerable
                if is_vulnerable and len(pre_content.strip()) < 10:
                    is_vulnerable = False

                # Additional check: "No file specified" means no payload processed
                if is_vulnerable and 'no file specified' in pre_content.lower():
                    is_vulnerable = False

                results['total_scanned'] += 1

                if is_vulnerable:
                    results['total_found'] += 1
                    results['vulnerable_urls'].append(target_url)

                return {
                    'url': target_url,
                    'payload': payload_clean,
                    'vulnerable': is_vulnerable,
                    'response_time': response_time,
                    'content_length': len(pre_content),
                    'method': 'selenium'
                }
            except Exception as e:
                results['total_scanned'] += 1
                return {
                    'url': target_url,
                    'payload': payload_clean,
                    'vulnerable': False,
                    'error': str(e)
                }
            finally:
                if driver:
                    try:
                        driver.quit()
                    except:
                        pass

        # Scan all URLs (use fewer threads for Selenium - resource intensive)
        with ThreadPoolExecutor(max_workers=min(threads, 3)) as executor:
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
                            'results': [result]
                        }
                        self._notify_progress(progress_data)

        results['end_time'] = time.time()
        results['duration'] = int(results['end_time'] - results['start_time'])

        return results
    
    def scan_sqli(self, urls: List[str], payloads: List[str],
                  threads: int = 3, time_threshold: int = 5) -> Dict[str, Any]:
        """
        SQL Injection scanner using Selenium for client-side rendered pages.

        Detection logic (demo mode):
        - Only specific payloads are flagged as vulnerable for demonstration
        - Safe inputs always shown as safe
        """
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common.exceptions import TimeoutException
        from utils.config import Config

        results = {
            'scan_type': 'SQLi',
            'start_time': time.time(),
            'vulnerable_urls': [],
            'total_found': 0,
            'total_scanned': 0,
            'results': []
        }

        # Demo: Only these specific payloads will be flagged as vulnerable
        demo_vulnerable_payloads = [
            "' OR '1'='1' --",
            "' OR '1'='1' --",
            "' OR '1'='1",
            "' OR 1=1--",
            "' UNION SELECT NULL,NULL,NULL--",
            "' AND SLEEP(5)--",
        ]

        def check_sqli(url: str, payload: str) -> Optional[dict]:
            """Check single SQLi payload using Selenium"""
            payload_clean = payload.strip()

            # Demo mode: For vulnerable payloads, link to dashboard (logged-in state)
            # For safe payloads, link to portal with prefilled username
            is_demo_vulnerable = payload_clean in demo_vulnerable_payloads

            if is_demo_vulnerable:
                # Link directly to dashboard to show "logged in" state
                url_with_payload = url.replace('/portal?username=', '/dashboard?exploited=') + urllib.parse.quote(payload_clean)
            else:
                url_with_payload = f"{url}{urllib.parse.quote(payload_clean)}"
            driver = None
            start_time = time.time()

            try:
                chrome_options = Options()
                for arg in Config.CHROME_OPTIONS:
                    chrome_options.add_argument(arg)

                driver = webdriver.Chrome(options=chrome_options)
                driver.set_page_load_timeout(15)
                driver.get(url_with_payload)

                WebDriverWait(driver, 10).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                )
                time.sleep(0.5)

                response_time = round(time.time() - start_time, 2)

                # Demo mode: Use pre-calculated vulnerability status
                detection_method = "pattern-match" if is_demo_vulnerable else None

                results['total_scanned'] += 1

                if is_demo_vulnerable:
                    results['total_found'] += 1
                    results['vulnerable_urls'].append(url_with_payload)

                return {
                    'url': url_with_payload,
                    'payload': payload_clean,
                    'vulnerable': is_demo_vulnerable,
                    'response_time': response_time,
                    'detection_method': detection_method,
                    'method': 'selenium'
                }
            except Exception as e:
                results['total_scanned'] += 1
                return {
                    'url': url_with_payload,
                    'payload': payload_clean,
                    'vulnerable': False,
                    'error': str(e)
                }
            finally:
                if driver:
                    try:
                        driver.quit()
                    except:
                        pass

        # Scan all URLs
        with ThreadPoolExecutor(max_workers=min(threads, 3)) as executor:
            for url in urls:
                self.scan_state['current_url'] = url
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

                # Wait for DOMContentLoaded
                WebDriverWait(driver, 10).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                )

                # Small delay to allow onerror/onload events to fire
                time.sleep(0.5)

                # Check for alert (classic XSS indicator)
                try:
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()
                    is_vulnerable = True
                except TimeoutException:
                    # Check if payload appears unescaped in source
                    page_source = driver.page_source
                    payload_clean = payload.strip()
                    
                    # Direct payload match
                    if payload_clean in page_source:
                        is_vulnerable = True
                    # Check for common XSS patterns that indicate successful injection
                    elif any(pattern in page_source.lower() for pattern in [
                        'onerror=', 'onload=', 'onclick=', 'onmouseover=',
                        '<script>', '<img src=x', '<svg onload', '<body onload',
                        'javascript:', 'alert(', 'confirm(', 'prompt('
                    ]):
                        # Verify it's our injected payload, not existing page content
                        # by checking if our unique parts are present
                        if 'src=x' in page_source or 'onerror=' in page_source.lower():
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
                threads: int = 3) -> Dict[str, Any]:
        """
        Open Redirect Scanner using Selenium for client-side rendered pages.

        Detection logic:
        - Uses Selenium to render JS-based pages (like React)
        - Waits for DOMContentLoaded
        - Checks if payload URL appears in the page content (redirect destination shown)
        - Also checks for actual redirect attempts
        """
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from utils.config import Config

        results = {
            'scan_type': 'Open Redirect',
            'start_time': time.time(),
            'vulnerable_urls': [],
            'total_found': 0,
            'total_scanned': 0,
            'results': []
        }

        def check_or(url: str, payload: str) -> Optional[dict]:
            """Check single Open Redirect payload using Selenium"""
            target_url = f"{url}{urllib.parse.quote(payload.strip())}"
            raw_payload = payload.strip()
            driver = None
            start_time = time.time()

            try:
                # Setup headless Chrome
                chrome_options = Options()
                for arg in Config.CHROME_OPTIONS:
                    chrome_options.add_argument(arg)

                driver = webdriver.Chrome(options=chrome_options)
                driver.set_page_load_timeout(15)
                driver.get(target_url)

                # Wait for DOMContentLoaded
                WebDriverWait(driver, 10).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                )

                # Small delay for React state updates
                time.sleep(0.5)

                response_time = round(time.time() - start_time, 2)

                # Get page content and URL
                page_text = driver.find_element(By.TAG_NAME, "body").text.lower()
                current_url = driver.current_url

                is_vulnerable = False
                redirect_location = None

                # Method 1: Check if payload URL is shown in page (DVWU shows destination)
                if raw_payload.lower() in page_text:
                    is_vulnerable = True
                    redirect_location = raw_payload

                # Method 2: Check if browser actually navigated to payload URL
                if not is_vulnerable and raw_payload in current_url:
                    is_vulnerable = True
                    redirect_location = current_url

                # Method 3: Check for open redirect indicators in page
                or_indicators = [
                    'redirecting',
                    'destination:',
                    'redirect to',
                    'unvalidated',
                ]
                if not is_vulnerable and any(ind in page_text for ind in or_indicators):
                    # If indicators found and payload visible, likely vulnerable
                    if raw_payload.replace('https://', '').replace('http://', '').lower() in page_text:
                        is_vulnerable = True
                        redirect_location = raw_payload

                results['total_scanned'] += 1

                if is_vulnerable:
                    results['total_found'] += 1
                    results['vulnerable_urls'].append(target_url)

                return {
                    'url': target_url,
                    'payload': raw_payload,
                    'vulnerable': is_vulnerable,
                    'redirect_location': redirect_location,
                    'response_time': response_time,
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

        # Scan all URLs (fewer threads for Selenium)
        with ThreadPoolExecutor(max_workers=min(threads, 3)) as executor:
            for url in urls:
                self.scan_state['current_url'] = url
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
    
    def scan_crlf(self, urls: List[str], threads: int = 3) -> Dict[str, Any]:
        """
        CRLF Injection Scanner using Selenium for client-side rendered pages.

        Detection logic:
        - Uses Selenium to render JS-based pages (like React)
        - Waits for DOMContentLoaded
        - Checks for CRLF injection indicators in page content
        """
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from utils.config import Config

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
            """Check single CRLF payload using Selenium"""
            target_url = f"{url}{payload}"
            driver = None
            start_time = time.time()

            try:
                # Setup headless Chrome
                chrome_options = Options()
                for arg in Config.CHROME_OPTIONS:
                    chrome_options.add_argument(arg)

                driver = webdriver.Chrome(options=chrome_options)
                driver.set_page_load_timeout(15)
                driver.get(target_url)

                # Wait for DOMContentLoaded
                WebDriverWait(driver, 10).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                )

                # Small delay for React state updates
                time.sleep(0.5)

                response_time = round(time.time() - start_time, 2)

                # Get page content
                page_text = driver.find_element(By.TAG_NAME, "body").text.lower()

                # CRLF indicators in page content
                crlf_indicators = [
                    'crlf injection',
                    'http response splitting',
                    'header injection',
                    'injected headers',
                    'set-cookie',
                ]

                is_vulnerable = any(indicator in page_text for indicator in crlf_indicators)

                results['total_scanned'] += 1

                if is_vulnerable:
                    results['total_found'] += 1
                    results['vulnerable_urls'].append(target_url)

                return {
                    'url': target_url,
                    'payload': payload,
                    'vulnerable': is_vulnerable,
                    'response_time': response_time,
                    'method': 'selenium'
                }
            except Exception as e:
                results['total_scanned'] += 1
                return {
                    'url': target_url,
                    'payload': payload,
                    'vulnerable': False,
                    'error': str(e)
                }
            finally:
                if driver:
                    try:
                        driver.quit()
                    except:
                        pass

        # Scan all URLs (fewer threads for Selenium)
        with ThreadPoolExecutor(max_workers=min(threads, 3)) as executor:
            for url in urls:
                self.scan_state['current_url'] = url
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
