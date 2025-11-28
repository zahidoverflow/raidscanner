#!/usr/bin/env python3
"""
RaidScanner CLI Wrapper
Safe wrapper script that properly invokes scanner functions
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from colorama import Fore, Style, init
from rich import print as rich_print
from rich.panel import Panel

init(autoreset=True)

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

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
    
    print(Fore.GREEN + "Welcome to the RaidScanner CLI!\n")
    print(Fore.CYAN + "Available Scanners:")
    print(Fore.YELLOW + "  1. LFI Scanner" + Fore.RESET + "        - Local File Inclusion")
    print(Fore.YELLOW + "  2. Open Redirect" + Fore.RESET + "      - Unvalidated Redirects")
    print(Fore.YELLOW + "  3. SQL Injection" + Fore.RESET + "     - Database Injection")
    print(Fore.YELLOW + "  4. XSS Scanner" + Fore.RESET + "        - Cross-Site Scripting")
    print(Fore.YELLOW + "  5. CRLF Injection" + Fore.RESET + "    - HTTP Response Splitting")
    print(Fore.RED + "  6. Exit\n")

def run_scanner():
    """Main scanner loop"""
    # Import scanner functions (these will work because we fixed the issue)
    try:
        from main import run_lfi_scanner, run_or_scanner, run_sql_scanner, run_xss_scanner, run_crlf_scanner
    except ImportError as e:
        print(Fore.RED + f"Error importing scanners: {e}")
        print(Fore.YELLOW + "Make sure main.py is in the same directory")
        sys.exit(1)
    
    while True:
        try:
            display_menu()
            choice = input(f"\n{Fore.CYAN}[?] Select an option (1-6): {Style.RESET_ALL}").strip()
            
            if choice == '1':
                clear_screen()
                print(Fore.GREEN + "Starting LFI Scanner...\n")
                run_lfi_scanner()
                
            elif choice == '2':
                clear_screen()
                print(Fore.GREEN + "Starting Open Redirect Scanner...\n")
                run_or_scanner()
                
            elif choice == '3':
                clear_screen()
                print(Fore.GREEN + "Starting SQL Injection Scanner...\n")
                run_sql_scanner()
                
            elif choice == '4':
                clear_screen()
                print(Fore.GREEN + "Starting XSS Scanner...\n")
                run_xss_scanner()
                
            elif choice == '5':
                clear_screen()
                print(Fore.GREEN + "Starting CRLF Injection Scanner...\n")
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
