import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
import plotly.graph_objects as go
from datetime import datetime

def render_header():
    """Render the application header"""
    st.markdown("""
        <h1 style='text-align: center; color: #FF4B4B;'>
            🔍 VulnaScanner
        </h1>
    """, unsafe_allow_html=True)
    st.markdown(f"""
        <p style='text-align: center; color: #808080;'>
            Version: {st.session_state.config.get('version', 'v2')}
        </p>
    """, unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

def render_sidebar():
    """Render the sidebar configuration options"""
    st.sidebar.header("Configuration")
    
    # Global settings
    st.sidebar.subheader("Global Settings")
    threads = st.sidebar.number_input("Concurrent Threads", min_value=1, max_value=20, value=5)
    timeout = st.sidebar.number_input("Timeout (seconds)", min_value=1, max_value=60, value=10)
    
    # User Agent Configuration
    st.sidebar.subheader("User Agent")
    user_agent_option = st.sidebar.radio(
        "User Agent Option",
        ["Default", "Random", "Custom"]
    )
    if user_agent_option == "Custom":
        custom_user_agent = st.sidebar.text_input("Custom User Agent")
    
    # Headers and Cookies
    st.sidebar.subheader("Headers & Cookies")
    custom_headers = st.sidebar.text_area("Custom Headers (JSON format)")
    cookies = st.sidebar.text_area("Cookies (JSON format)")
    
    # Save configuration button
    if st.sidebar.button("Save Configuration"):
        save_config()
        st.sidebar.success("Configuration saved!")

def render_scanner_interface(scanner_type):
    """Render the main scanner interface"""
    st.header(f"{scanner_type}")
    
    # Input section
    with st.expander("Input Configuration", expanded=True):
        input_col1, input_col2 = st.columns(2)
        
        with input_col1:
            url_input = st.text_area("Enter URL(s)", placeholder="Enter one URL per line")
            uploaded_urls = st.file_uploader("Or upload URL list", type=['txt'])
        
        with input_col2:
            payload_file = st.file_uploader("Upload Custom Payload File", type=['txt'])
            if scanner_type in ["SQLi Scanner", "LFI Scanner"]:
                success_criteria = st.text_area("Success Criteria", placeholder="Enter success patterns, one per line")
    
    # Progress tracking
    if 'current_scan' in st.session_state and st.session_state.current_scan:
        progress_col1, progress_col2, progress_col3 = st.columns(3)
        with progress_col1:
            st.metric("URLs Scanned", st.session_state.current_scan.get('scanned', 0))
        with progress_col2:
            st.metric("Vulnerabilities Found", st.session_state.current_scan.get('found', 0))
        with progress_col3:
            st.metric("Scan Duration", f"{st.session_state.current_scan.get('duration', 0)}s")
        
        progress = st.progress(0)
        status = st.empty()
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Start Scan", type="primary"):
            start_scan(scanner_type)
    with col2:
        if st.button("Stop Scan"):
            stop_scan()
    with col3:
        if st.button("Clear Results"):
            clear_results()
    
    # Results section
    if st.session_state.scan_results:
        render_results_table()
        render_export_options()

def render_settings():
    """Render the settings page"""
    st.header("Settings")
    
    # General Settings
    st.subheader("General Settings")
    st.session_state.config['save_reports'] = st.checkbox(
        "Automatically save reports",
        value=st.session_state.config.get('save_reports', True)
    )
    st.session_state.config['report_format'] = st.selectbox(
        "Default Report Format",
        ['HTML', 'CSV', 'JSON'],
        index=['HTML', 'CSV', 'JSON'].index(st.session_state.config.get('report_format', 'HTML'))
    )
    
    # Rate Limiting
    st.subheader("Rate Limiting")
    st.session_state.config['rate_limit'] = st.number_input(
        "Requests per second",
        min_value=1,
        max_value=100,
        value=st.session_state.config.get('rate_limit', 10)
    )
    
    # Payload Management
    st.subheader("Payload Management")
    payload_type = st.selectbox("Select Payload Type", ["LFI", "OR", "SQLi", "XSS", "CRLF"])
    payload_file = st.file_uploader(f"Upload {payload_type} Payloads", type=['txt'])
    if payload_file:
        save_payload_file(payload_type, payload_file)
    
    # Save Settings
    if st.button("Save Settings"):
        save_config()
        st.success("Settings saved successfully!")

def render_about():
    """Render the about page"""
    st.header("About VulnaScanner")
    
    st.markdown("""
    **VulnaScanner** is a comprehensive web vulnerability scanning tool that helps identify various security issues:
    
    - Local File Inclusion (LFI)
    - Open Redirect (OR)
    - SQL Injection (SQLi)
    - Cross-Site Scripting (XSS)
    - CRLF Injection
    
    ### Features
    - Multi-threaded scanning
    - Customizable payloads
    - Success criteria customization
    - Detailed reporting
    - User-friendly interface
    
    ### Credits
    Created by: Coffinxp, 1hehaq, HexSh1dow, Naho, AnonKryptiQuz, Hghost010
    
    ### Disclaimer
    This tool is intended for educational and ethical testing purposes only. Always obtain proper authorization before testing any web application.
    """)

def render_results_table():
    """Render the results table with filtering and sorting"""
    if not st.session_state.scan_results:
        return
    
    df = pd.DataFrame(st.session_state.scan_results)
    
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_side_bar()
    gb.configure_selection('multiple', use_checkbox=True)
    
    grid_options = gb.build()
    
    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        data_return_mode='AS_INPUT',
        update_mode='MODEL_CHANGED',
        fit_columns_on_grid_load=True,
        theme='streamlit'
    )

def render_export_options():
    """Render export options for scan results"""
    st.subheader("Export Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Copy to Clipboard"):
            copy_to_clipboard()
    
    with col2:
        if st.button("Export to CSV"):
            export_results('csv')
    
    with col3:
        if st.button("Generate HTML Report"):
            export_results('html')

def copy_to_clipboard():
    """Copy results to clipboard"""
    df = pd.DataFrame(st.session_state.scan_results)
    df.to_clipboard(index=False)
    st.success("Results copied to clipboard!")

def save_payload_file(payload_type, file):
    """Save uploaded payload file"""
    try:
        content = file.read().decode()
        with open(f"payloads/{payload_type.lower()}_custom.txt", "w") as f:
            f.write(content)
        st.success(f"{payload_type} payloads saved successfully!")
    except Exception as e:
        st.error(f"Error saving payload file: {str(e)}") 