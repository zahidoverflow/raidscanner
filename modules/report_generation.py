import streamlit as st
from datetime import datetime
import json
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def generate_report(results: list, output_path: str):
    """Generate an HTML report from scan results"""
    
    # Convert results to DataFrame for easier manipulation
    df = pd.DataFrame(results)
    
    # Get scan statistics
    total_urls = len(results)
    vulnerable_urls = len([r for r in results if r.get('vulnerable', False)])
    scan_duration = st.session_state.current_scan.get('duration', 0) if st.session_state.current_scan else 0
    
    # Create vulnerability distribution pie chart
    fig_vuln_dist = go.Figure(data=[go.Pie(
        labels=['Vulnerable', 'Not Vulnerable'],
        values=[vulnerable_urls, total_urls - vulnerable_urls],
        hole=.3
    )])
    fig_vuln_dist.update_layout(title='Vulnerability Distribution')
    
    # Create vulnerability type distribution bar chart if available
    if 'vulnerability_type' in df.columns:
        vuln_type_counts = df['vulnerability_type'].value_counts()
        fig_vuln_types = go.Figure(data=[go.Bar(
            x=vuln_type_counts.index,
            y=vuln_type_counts.values
        )])
        fig_vuln_types.update_layout(title='Vulnerability Types')
        vuln_types_chart = fig_vuln_types.to_html(full_html=False)
    else:
        vuln_types_chart = ""
    
    # Generate HTML report
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>VulnaScanner Scan Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background-color: white;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
            .header {{
                text-align: center;
                margin-bottom: 30px;
            }}
            .stats-container {{
                display: flex;
                justify-content: space-around;
                margin-bottom: 30px;
            }}
            .stat-box {{
                text-align: center;
                padding: 20px;
                background-color: #f8f9fa;
                border-radius: 5px;
                min-width: 200px;
            }}
            .stat-value {{
                font-size: 24px;
                font-weight: bold;
                color: #007bff;
            }}
            .stat-label {{
                color: #6c757d;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th, td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}
            th {{
                background-color: #f8f9fa;
            }}
            tr:hover {{
                background-color: #f5f5f5;
            }}
            .chart-container {{
                margin: 30px 0;
            }}
            .vulnerability-details {{
                margin-top: 30px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>VulnaScanner Scan Report</h1>
                <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="stats-container">
                <div class="stat-box">
                    <div class="stat-value">{total_urls}</div>
                    <div class="stat-label">URLs Scanned</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">{vulnerable_urls}</div>
                    <div class="stat-label">Vulnerabilities Found</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">{scan_duration}s</div>
                    <div class="stat-label">Scan Duration</div>
                </div>
            </div>
            
            <div class="chart-container">
                {fig_vuln_dist.to_html(full_html=False)}
            </div>
            
            <div class="chart-container">
                {vuln_types_chart}
            </div>
            
            <div class="vulnerability-details">
                <h2>Detailed Results</h2>
                <table>
                    <thead>
                        <tr>
                            <th>URL</th>
                            <th>Vulnerability Type</th>
                            <th>Payload</th>
                            <th>Details</th>
                        </tr>
                    </thead>
                    <tbody>
    """
    
    # Add table rows for each result
    for result in results:
        if result.get('vulnerable', False):
            html_content += f"""
                <tr>
                    <td>{result.get('url', 'N/A')}</td>
                    <td>{result.get('vulnerability_type', 'N/A')}</td>
                    <td>{result.get('payload', 'N/A')}</td>
                    <td>{result.get('details', 'N/A')}</td>
                </tr>
            """
    
    html_content += """
                    </tbody>
                </table>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Save the report
    with open(output_path, 'w') as f:
        f.write(html_content)

def generate_scan_summary(results: list) -> dict:
    """Generate a summary of scan results"""
    total_urls = len(results)
    vulnerable_urls = len([r for r in results if r.get('vulnerable', False)])
    
    vulnerability_types = {}
    for result in results:
        if result.get('vulnerable', False):
            vuln_type = result.get('vulnerability_type', 'Unknown')
            vulnerability_types[vuln_type] = vulnerability_types.get(vuln_type, 0) + 1
    
    return {
        'total_urls': total_urls,
        'vulnerable_urls': vulnerable_urls,
        'vulnerability_types': vulnerability_types,
        'scan_duration': st.session_state.current_scan.get('duration', 0) if st.session_state.current_scan else 0
    }

def create_vulnerability_chart(results: list):
    """Create a Plotly chart for vulnerability distribution"""
    df = pd.DataFrame(results)
    
    if 'vulnerability_type' in df.columns:
        fig = px.pie(
            df[df['vulnerable'] == True],
            names='vulnerability_type',
            title='Vulnerability Distribution'
        )
        return fig
    return None 