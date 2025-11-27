"""
Platform-specific helper functions
Cross-platform compatibility layer
"""

import os
import platform
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


def get_chrome_driver_path():
    """Get correct ChromeDriver for current OS"""
    system = platform.system()
    
    try:
        if system == "Windows":
            return ChromeDriverManager().install()
        elif system == "Linux":
            return ChromeDriverManager().install()
        elif system == "Darwin":  # macOS
            return ChromeDriverManager().install()
        else:
            return ChromeDriverManager().install()
    except Exception as e:
        print(f"Error installing ChromeDriver: {e}")
        return None


def clear_screen():
    """Cross-platform screen clear"""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_default_chrome_path():
    """Find Chrome installation"""
    system = platform.system()
    
    if system == "Windows":
        paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
        ]
    elif system == "Linux":
        paths = [
            "/usr/bin/google-chrome",
            "/usr/bin/chromium-browser",
            "/usr/bin/chromium",
            "/snap/bin/chromium"
        ]
    elif system == "Darwin":  # macOS
        paths = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium"
        ]
    else:
        return None
    
    for path in paths:
        if os.path.exists(path):
            return path
    return None


def get_platform_info():
    """Get current platform information"""
    return {
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
        'processor': platform.processor()
    }


def is_windows():
    """Check if running on Windows"""
    return platform.system() == "Windows"


def is_linux():
    """Check if running on Linux"""
    return platform.system() == "Linux"


def is_macos():
    """Check if running on macOS"""
    return platform.system() == "Darwin"
