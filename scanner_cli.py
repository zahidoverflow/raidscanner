#!/usr/bin/env python3
"""
RaidScanner CLI - Interactive Command Line Interface
Uses core scanning modules for all vulnerability detection
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from colorama import Fore, Style, init
from rich import print as rich_print
from rich.panel import Panel
from rich.console import Console

# Import core modules
from core.scanner_engine import ScannerEngine
from core.payload_loader import PayloadLoader
from core.report_generator import ReportGenerator
from utils.platform_helper import clear_screen

init(autoreset=True)
console = Console()

# Initialize core components
scanner = ScannerEngine()
payload_loader = PayloadLoader()
report_gen = ReportGenerator()


def display_menu():
    """Display the main scanner menu"""
    clear_screen()
    
    panel = Panel(r"""
     ██████╗██╗   ██╗██████╗ ███████╗██████╗     ███████╗███████╗ ██████╗██╗   ██╗██████╗ ██╗████████╗██╗   ██╗
    ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗    ██╔════╝██╔════╝██╔════╝██║   ██║██╔══██╗██║╚══██╔══╝╚██╗ ██╔╝
    ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝    ███████╗█████╗  ██║     ██║   ██║██████╔╝██║   ██║    ╚████╔╝ 
    ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗    ╚════██║██╔══╝  ██║     ██║   ██║██╔══██╗██║   ██║     ╚██╔╝  
    ╚██████╗   ██║   ██████╔╝███████╗██║  ██║    ███████║███████╗╚██████╗╚██████╔╝██║  ██║██║   ██║      ██║   
     ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝    ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝   ╚═╝      ╚═╝   
    """,
    style="bold cyan",
    border_style="blue",
    expand=False
    )
    rich_print(panel, "\n")
    
    print(Fore.GREEN + "Welcome to RaidScanner CLI!\n")
    print(Fore.CYAN + "Available Scanners:")
    print(Fore.YELLOW + "  1. LFI Scanner" + Fore.RESET + "        - Local File Inclusion")
    print(Fore.YELLOW + "  2. Open Redirect" + Fore.RESET + "      - Unvalidated Redirects")
    print(Fore.YELLOW + "  3. SQL Injection" + Fore.RESET + "     - Database Injection")
    print(Fore.YELLOW + "  4. XSS Scanner" + Fore.RESET + "        - Cross-Site Scripting")
    print(Fore.YELLOW + "  5. CRLF Injection" + Fore.RESET + "    - HTTP Response Splitting")
    print(Fore.RED + "  6. Exit\n")


def get_urls():
    """Get target URLs from user"""
    print(Fore.CYAN + "\n[?] Enter target URL(s):")
    print(Fore.YELLOW + "    (Enter one URL per line, press Enter twice when done)")
    
    urls = []
    while True:
        url = input(Fore.WHITE + "URL: ").strip()
        if not url:
            break
        urls.append(url)
    
    return urls


def get_threads():
    """Get thread count from user"""
    while True:
        try:
            threads = input(Fore.CYAN + "\n[?] Number of threads (1-10, default 5): ").strip()
            if not threads:
                return 5
            threads = int(threads)
            if 1 <= threads <= 10:
                return threads
            print(Fore.RED + "[!] Please enter a number between 1 and 10")
        except ValueError:
            print(Fore.RED + "[!] Please enter a valid number")


def display_results(results):
    """Display scan results"""
    print(Fore.GREEN + f"\n{'='*70}")
    print(Fore.GREEN + "SCAN RESULTS")
    print(Fore.GREEN + f"{'='*70}\n")
    
    print(Fore.CYAN + f"Scan Type: {results['scan_type']}")
    print(Fore.CYAN + f"Duration: {results['duration']} seconds")
    print(Fore.CYAN + f"Total Scanned: {results['total_scanned']}")
    print(Fore.YELLOW + f"Vulnerabilities Found: {results['total_found']}\n")
    
    if results['total_found'] > 0:
        print(Fore.RED + "VULNERABLE URLS:")
        for url in results['vulnerable_urls']:
            print(Fore.RED + f"  ✗ {url}")
    else:
        print(Fore.GREEN + "✓ No vulnerabilities found")
    
    print(Fore.GREEN + f"\n{'='*70}\n")


def save_report_prompt(scan_type, results):
    """Prompt user to save report"""
    save = input(Fore.CYAN + "\n[?] Save report? (y/n): ").strip().lower()
    if save == 'y':
        try:
            report_path = report_gen.generate_and_save(scan_type, results, format='html')
            print(Fore.GREEN + f"[✓] Report saved: {report_path}")
            
            # Also save JSON
            json_path = report_gen.generate_and_save(scan_type, results, format='json')
            print(Fore.GREEN + f"[✓] JSON report saved: {json_path}")
        except Exception as e:
            print(Fore.RED + f"[✗] Error saving report: {e}")


def run_lfi_scanner():
    """Run LFI scanner"""
    clear_screen()
    print(Fore.GREEN + "LFI Scanner\n")
    
    urls = get_urls()
    if not urls:
        print(Fore.RED + "[!] No URLs provided")
        input(Fore.YELLOW + "\nPress Enter to continue...")
        return
    
    threads = get_threads()
    
    try:
        payloads = payload_loader.load_lfi_payloads()
        print(Fore.YELLOW + f"\n[*] Loaded {len(payloads)} payloads")
        print(Fore.YELLOW + f"[*] Starting scan with {threads} threads...\n")
        
        results = scanner.scan_lfi(urls, payloads, threads=threads)
        display_results(results)
        save_report_prompt('LFI', results)
        
    except Exception as e:
        print(Fore.RED + f"[✗] Error: {e}")
    
    input(Fore.YELLOW + "\nPress Enter to continue...")


def run_or_scanner():
    """Run Open Redirect scanner"""
    clear_screen()
    print(Fore.GREEN + "Open Redirect Scanner\n")
    
    urls = get_urls()
    if not urls:
        print(Fore.RED + "[!] No URLs provided")
        input(Fore.YELLOW + "\nPress Enter to continue...")
        return
    
    threads = get_threads()
    
    try:
        payloads = payload_loader.load_or_payloads()
        print(Fore.YELLOW + f"\n[*] Loaded {len(payloads)} payloads")
        print(Fore.YELLOW + f"[*] Starting scan with {threads} threads...\n")
        
        results = scanner.scan_or(urls, payloads, threads=threads)
        display_results(results)
        save_report_prompt('Open Redirect', results)
        
    except Exception as e:
        print(Fore.RED + f"[✗] Error: {e}")
    
    input(Fore.YELLOW + "\nPress Enter to continue...")


def run_sql_scanner():
    """Run SQL Injection scanner"""
    clear_screen()
    print(Fore.GREEN + "SQL Injection Scanner\n")
    
    urls = get_urls()
    if not urls:
        print(Fore.RED + "[!] No URLs provided")
        input(Fore.YELLOW + "\nPress Enter to continue...")
        return
    
    threads = get_threads()
    
    try:
        payloads = payload_loader.load_sqli_payloads()
        print(Fore.YELLOW + f"\n[*] Loaded {len(payloads)} payloads")
        print(Fore.YELLOW + f"[*] Starting scan with {threads} threads...\n")
        
        results = scanner.scan_sqli(urls, payloads, threads=threads)
        display_results(results)
        save_report_prompt('SQLi', results)
        
    except Exception as e:
        print(Fore.RED + f"[✗] Error: {e}")
    
    input(Fore.YELLOW + "\nPress Enter to continue...")


def run_xss_scanner():
    """Run XSS scanner"""
    clear_screen()
    print(Fore.GREEN + "XSS Scanner\n")
    
    urls = get_urls()
    if not urls:
        print(Fore.RED + "[!] No URLs provided")
        input(Fore.YELLOW + "\nPress Enter to continue...")
        return
    
    threads = min(get_threads(), 3)  # Limit threads for Selenium
    
    try:
        payloads = payload_loader.load_xss_payloads()
        print(Fore.YELLOW + f"\n[*] Loaded {len(payloads)} payloads")
        print(Fore.YELLOW + f"[*] Starting scan with {threads} threads (Selenium-based)...\n")
        
        results = scanner.scan_xss(urls, payloads, threads=threads)
        display_results(results)
        save_report_prompt('XSS', results)
        
    except Exception as e:
        print(Fore.RED + f"[✗] Error: {e}")
    
    input(Fore.YELLOW + "\nPress Enter to continue...")


def run_crlf_scanner():
    """Run CRLF Injection scanner"""
    clear_screen()
    print(Fore.GREEN + "CRLF Injection Scanner\n")
    
    urls = get_urls()
    if not urls:
        print(Fore.RED + "[!] No URLs provided")
        input(Fore.YELLOW + "\nPress Enter to continue...")
        return
    
    threads = get_threads()
    
    try:
        print(Fore.YELLOW + f"\n[*] Using built-in CRLF payloads")
        print(Fore.YELLOW + f"[*] Starting scan with {threads} threads...\n")
        
        results = scanner.scan_crlf(urls, threads=threads)
        display_results(results)
        save_report_prompt('CRLF', results)
        
    except Exception as e:
        print(Fore.RED + f"[✗] Error: {e}")
    
    input(Fore.YELLOW + "\nPress Enter to continue...")


def run_scanner():
    """Main scanner loop"""
    while True:
        try:
            display_menu()
            choice = input(f"\n{Fore.CYAN}[?] Select an option (1-6): {Style.RESET_ALL}").strip()
            
            if choice == '1':
                run_lfi_scanner()
            elif choice == '2':
                run_or_scanner()
            elif choice == '3':
                run_sql_scanner()
            elif choice == '4':
                run_xss_scanner()
            elif choice == '5':
                run_crlf_scanner()
            elif choice == '6':
                print(Fore.RED + "\nExiting RaidScanner...")
                sys.exit(0)
            else:
                print(Fore.RED + "\n[!] Invalid option. Please choose 1-6.")
                input(Fore.YELLOW + "\nPress Enter to continue...")
                
        except KeyboardInterrupt:
            print(Fore.RED + "\n\nExiting RaidScanner...")
            sys.exit(0)
        except Exception as e:
            print(Fore.RED + f"\n[!] Error: {e}")
            input(Fore.YELLOW + "\nPress Enter to continue...")


if __name__ == "__main__":
    run_scanner()
