import streamlit as st
from typing import List, Dict, Any
import time
import threading
from queue import Queue
import json
from pathlib import Path
import sys
import os

# Add the parent directory to the Python path to import the original scanner
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from loxs import (
    run_lfi_scanner,
    run_or_scanner,
    run_sql_scanner,
    run_xss_scanner,
    run_crlf_scanner
)

class ScannerThread(threading.Thread):
    def __init__(self, scanner_func, urls: List[str], config: Dict[str, Any], results_queue: Queue):
        super().__init__()
        self.scanner_func = scanner_func
        self.urls = urls
        self.config = config
        self.results_queue = results_queue
        self.stop_event = threading.Event()

    def run(self):
        try:
            for url in self.urls:
                if self.stop_event.is_set():
                    break
                
                result = self.scanner_func(
                    url=url,
                    threads=self.config.get('threads', 5),
                    timeout=self.config.get('timeout', 10),
                    user_agent=self.config.get('user_agent'),
                    cookies=self.config.get('cookies'),
                    headers=self.config.get('headers'),
                    success_criteria=self.config.get('success_criteria'),
                    payload_file=self.config.get('payload_file')
                )
                
                self.results_queue.put(result)
                
                # Update progress in session state
                st.session_state.current_scan['scanned'] += 1
                if result.get('vulnerable', False):
                    st.session_state.current_scan['found'] += 1
                
        except Exception as e:
            self.results_queue.put({'error': str(e)})

def run_lfi_scan(urls: List[str], config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Run LFI scan with progress tracking"""
    results_queue = Queue()
    scanner_thread = ScannerThread(run_lfi_scanner, urls, config, results_queue)
    
    # Initialize scan state
    st.session_state.current_scan = {
        'type': 'LFI',
        'start_time': time.time(),
        'scanned': 0,
        'found': 0,
        'total': len(urls)
    }
    
    scanner_thread.start()
    results = []
    
    # Monitor progress
    while scanner_thread.is_alive():
        try:
            result = results_queue.get_nowait()
            results.append(result)
        except Queue.Empty:
            time.sleep(0.1)
        
        # Update progress
        st.session_state.current_scan['duration'] = int(time.time() - st.session_state.current_scan['start_time'])
    
    scanner_thread.join()
    
    # Get any remaining results
    while not results_queue.empty():
        results.append(results_queue.get())
    
    return results

def run_or_scan(urls: List[str], config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Run Open Redirect scan with progress tracking"""
    results_queue = Queue()
    scanner_thread = ScannerThread(run_or_scanner, urls, config, results_queue)
    
    st.session_state.current_scan = {
        'type': 'OR',
        'start_time': time.time(),
        'scanned': 0,
        'found': 0,
        'total': len(urls)
    }
    
    scanner_thread.start()
    results = []
    
    while scanner_thread.is_alive():
        try:
            result = results_queue.get_nowait()
            results.append(result)
        except Queue.Empty:
            time.sleep(0.1)
        
        st.session_state.current_scan['duration'] = int(time.time() - st.session_state.current_scan['start_time'])
    
    scanner_thread.join()
    
    while not results_queue.empty():
        results.append(results_queue.get())
    
    return results

def run_sqli_scan(urls: List[str], config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Run SQL Injection scan with progress tracking"""
    results_queue = Queue()
    scanner_thread = ScannerThread(run_sql_scanner, urls, config, results_queue)
    
    st.session_state.current_scan = {
        'type': 'SQLi',
        'start_time': time.time(),
        'scanned': 0,
        'found': 0,
        'total': len(urls)
    }
    
    scanner_thread.start()
    results = []
    
    while scanner_thread.is_alive():
        try:
            result = results_queue.get_nowait()
            results.append(result)
        except Queue.Empty:
            time.sleep(0.1)
        
        st.session_state.current_scan['duration'] = int(time.time() - st.session_state.current_scan['start_time'])
    
    scanner_thread.join()
    
    while not results_queue.empty():
        results.append(results_queue.get())
    
    return results

def run_xss_scan(urls: List[str], config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Run XSS scan with progress tracking"""
    results_queue = Queue()
    scanner_thread = ScannerThread(run_xss_scanner, urls, config, results_queue)
    
    st.session_state.current_scan = {
        'type': 'XSS',
        'start_time': time.time(),
        'scanned': 0,
        'found': 0,
        'total': len(urls)
    }
    
    scanner_thread.start()
    results = []
    
    while scanner_thread.is_alive():
        try:
            result = results_queue.get_nowait()
            results.append(result)
        except Queue.Empty:
            time.sleep(0.1)
        
        st.session_state.current_scan['duration'] = int(time.time() - st.session_state.current_scan['start_time'])
    
    scanner_thread.join()
    
    while not results_queue.empty():
        results.append(results_queue.get())
    
    return results

def run_crlf_scan(urls: List[str], config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Run CRLF scan with progress tracking"""
    results_queue = Queue()
    scanner_thread = ScannerThread(run_crlf_scanner, urls, config, results_queue)
    
    st.session_state.current_scan = {
        'type': 'CRLF',
        'start_time': time.time(),
        'scanned': 0,
        'found': 0,
        'total': len(urls)
    }
    
    scanner_thread.start()
    results = []
    
    while scanner_thread.is_alive():
        try:
            result = results_queue.get_nowait()
            results.append(result)
        except Queue.Empty:
            time.sleep(0.1)
        
        st.session_state.current_scan['duration'] = int(time.time() - st.session_state.current_scan['start_time'])
    
    scanner_thread.join()
    
    while not results_queue.empty():
        results.append(results_queue.get())
    
    return results

def start_scan(scanner_type: str):
    """Start a new scan based on the scanner type"""
    # Get URLs from input
    urls = []
    if st.session_state.get('url_input'):
        urls.extend([url.strip() for url in st.session_state.url_input.split('\n') if url.strip()])
    if st.session_state.get('uploaded_urls'):
        urls.extend([url.strip() for url in st.session_state.uploaded_urls.read().decode().split('\n') if url.strip()])
    
    if not urls:
        st.error("Please provide at least one URL to scan")
        return
    
    # Get configuration
    config = {
        'threads': st.session_state.config.get('threads', 5),
        'timeout': st.session_state.config.get('timeout', 10),
        'user_agent': st.session_state.config.get('user_agent'),
        'cookies': json.loads(st.session_state.config.get('cookies', '{}')),
        'headers': json.loads(st.session_state.config.get('headers', '{}')),
        'success_criteria': st.session_state.get('success_criteria', '').split('\n'),
        'payload_file': st.session_state.get('payload_file')
    }
    
    # Run appropriate scanner
    scanner_map = {
        'LFI Scanner': run_lfi_scan,
        'OR Scanner': run_or_scan,
        'SQLi Scanner': run_sqli_scan,
        'XSS Scanner': run_xss_scan,
        'CRLF Scanner': run_crlf_scan
    }
    
    scanner_func = scanner_map.get(scanner_type)
    if not scanner_func:
        st.error(f"Unknown scanner type: {scanner_type}")
        return
    
    try:
        results = scanner_func(urls, config)
        st.session_state.scan_results.extend(results)
        
        # Save to scan history
        scan_record = {
            'timestamp': time.time(),
            'type': scanner_type,
            'urls_scanned': len(urls),
            'vulnerabilities_found': len([r for r in results if r.get('vulnerable', False)]),
            'duration': st.session_state.current_scan['duration']
        }
        st.session_state.scan_history.append(scan_record)
        
    except Exception as e:
        st.error(f"Error during scan: {str(e)}")
    finally:
        st.session_state.current_scan = None

def stop_scan():
    """Stop the current scan"""
    if st.session_state.get('current_scan'):
        st.session_state.current_scan['stop'] = True
        st.warning("Stopping scan... Please wait for current operations to complete.")

def clear_results():
    """Clear current scan results"""
    st.session_state.scan_results = []
    st.success("Results cleared successfully!") 