import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from st_aggrid import AgGrid, GridOptionsBuilder
import plotly.graph_objects as go
from pathlib import Path
import json
import yaml
import time
from datetime import datetime

# Import scanner modules
from modules.ui_components import (
    render_sidebar,
    render_header,
    render_scanner_interface,
    render_settings,
    render_about
)
from modules.scanner_integration import (
    run_lfi_scan,
    run_or_scan,
    run_sqli_scan,
    run_xss_scan,
    run_crlf_scan
)
from modules.data_handling import (
    load_config,
    save_config,
    load_scan_history,
    save_scan_history,
    export_results
)
from modules.report_generation import generate_report

# Set page config
st.set_page_config(
    page_title="VulnaScanner",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .stButton>button {
        width: 100%;
    }
    .reportview-container {
        background: #0E1117;
    }
    </style>
    """, unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'scan_history' not in st.session_state:
        st.session_state.scan_history = []
    if 'current_scan' not in st.session_state:
        st.session_state.current_scan = None
    if 'scan_results' not in st.session_state:
        st.session_state.scan_results = []
    if 'config' not in st.session_state:
        st.session_state.config = load_config()

def main():
    """Main application function"""
    initialize_session_state()
    
    # Render header
    render_header()
    
    # Sidebar navigation
    with st.sidebar:
        selected = option_menu(
            "Navigation",
            ["LFI Scanner", "OR Scanner", "SQLi Scanner", "XSS Scanner", "CRLF Scanner", "Settings", "About"],
            icons=['shield', 'arrow-return-right', 'database', 'code-slash', 'file-earmark-text', 'gear', 'info-circle'],
            menu_icon="list",
            default_index=0,
        )
        
        render_sidebar()
    
    # Main content
    if selected in ["LFI Scanner", "OR Scanner", "SQLi Scanner", "XSS Scanner", "CRLF Scanner"]:
        render_scanner_interface(selected)
    elif selected == "Settings":
        render_settings()
    elif selected == "About":
        render_about()

if __name__ == "__main__":
    main() 