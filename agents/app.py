"""
Phase 4: Streamlit Web UI
Beautiful frontend for the SOC analyst
"""

import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd

# ─────────────────────────────────────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="CyberSentinel | Autonomous SOC Analyst",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton > button {
        width: 100%;
        padding: 0.5rem;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
    }
    .severity-critical {
        background-color: #ff4444;
        color: white;
        padding: 0.5rem;
        border-radius: 0.25rem;
        font-weight: bold;
    }
    .severity-high {
        background-color: #ff9944;
        color: white;
        padding: 0.5rem;
        border-radius: 0.25rem;
        font-weight: bold;
    }
    .severity-medium {
        background-color: #ffdd44;
        color: black;
        padding: 0.5rem;
        border-radius: 0.25rem;
        font-weight: bold;
    }
    .severity-low {
        background-color: #44ff44;
        color: black;
        padding: 0.5rem;
        border-radius: 0.25rem;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("# 🛡️ CyberSentinel")
st.markdown("## Autonomous SOC Analyst")
st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    api_url = st.text_input("API URL", value="http://localhost:8000")
    
    st.markdown("---")
    st.markdown("### 📚 Sample Alerts")
    
    if st.button("Load Sample Alerts"):
        try:
            response = requests.get(f"{api_url}/sample-alerts")
            st.session_state.sample_alerts = response.json()["alerts"]
            st.success("Sample alerts loaded!")
        except Exception as e:
            st.error(f"Failed to load samples: {e}")

# ─────────────────────────────────────────────────────────────────────────────
# Main Content
# ─────────────────────────────────────────────────────────────────────────────

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🔍 Submit Security Alert")
    
    # Input method
    input_method = st.radio("Input method:", ["Text", "Paste"], horizontal=True)
    
    if input_method == "Text":
        alert_text = st.text_area(
            "Security Alert",
            placeholder="Paste your security alert here...",
            height=150
        )
    else:
        alert_text = st.text_area(
            "Security Alert",
            placeholder="Paste your security alert here...",
            height=150
        )
    
    alert_id = st.text_input("Alert ID", value="ALERT-001")
    
    col_submit, col_clear = st.columns(2)
    
    with col_submit:
        submit_button = st.button("🚀 Analyze Alert", use_container_width=True)
    
    with col_clear:
        if st.button("Clear", use_container_width=True):
            alert_text = ""
            st.rerun()

with col2:
    st.markdown("### 📊 Quick Stats")
    
    # Display stats
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Status", "Ready", "✅")
    with col_b:
        st.metric("API", "Connected", "🟢")
    
    st.markdown("---")
    st.markdown("**Model Version:** 1.0")
    st.markdown("**Components:**")
    st.markdown("- Triage Agent")
    st.markdown("- Threat Correlator")
    st.markdown("- Playbook Generator")
    st.markdown("- Reporter Agent")

# ─────────────────────────────────────────────────────────────────────────────
# Process Alert
# ─────────────────────────────────────────────────────────────────────────────

if submit_button:
    if not alert_text.strip():
        st.error("Please enter an alert!")
    else:
        with st.spinner("🔄 Analyzing alert... (Processing through all agents)"):
            try:
                # Call API
                response = requests.post(
                    f"{api_url}/analyze",
                    json={
                        "alert_text": alert_text,
                        "alert_id": alert_id
                    }
                )
                
                if response.status_code == 200:
                    report = response.json()
                    st.session_state.report = report
                    st.success("✅ Analysis complete!")
                else:
                    st.error(f"API Error: {response.status_code}")
                    st.error(response.text)
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to API. Is it running?")
                st.info("Run: `python -m uvicorn api:app --reload`")
            except Exception as e:
                st.error(f"Error: {e}")

# ─────────────────────────────────────────────────────────────────────────────
# Display Report
# ─────────────────────────────────────────────────────────────────────────────

if "report" in st.session_state:
    report = st.session_state.report
    
    st.markdown("---")
    st.markdown("## 📋 Incident Response Report")
    
    # Summary section
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        severity = report["severity"]
        if severity == "CRITICAL":
            st.markdown(f'<div class="severity-critical">🔴 {severity}</div>', unsafe_allow_html=True)
        elif severity == "HIGH":
            st.markdown(f'<div class="severity-high">🟠 {severity}</div>', unsafe_allow_html=True)
        elif severity == "MEDIUM":
            st.markdown(f'<div class="severity-medium">🟡 {severity}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="severity-low">🟢 {severity}</div>', unsafe_allow_html=True)
    
    with col2:
        st.metric("Category", report["category"])
    
    with col3:
        st.metric("Alert ID", report["alert_id"])
    
    with col4:
        escalation = "🚨 YES" if report["escalation_required"] else "✅ NO"
        st.metric("Escalation", escalation)
    
    # Threat Intelligence
    st.markdown("### 🎯 Threat Intelligence")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**MITRE ATT&CK Techniques:**")
        for technique in report["mitre_techniques"]:
            st.markdown(f"- `{technique}`")
    
    with col2:
        st.markdown("**Threat Actors:**")
        for actor in report["threat_actors"]:
            st.markdown(f"- {actor}")
    
    # Response Playbook
    st.markdown("### 📋 Incident Response Playbook")
    
    for step in report["response_steps"]:
        with st.expander(f"Step {step['step_number']}: {step['title']}", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"**Time:** {step['estimated_time']}")
            with col2:
                priority = step['priority']
                color = "🔴" if priority == "IMMEDIATE" else "🟠" if priority == "HIGH" else "🟡"
                st.markdown(f"**Priority:** {color} {priority}")
            with col3:
                pass
            
            st.markdown(step['description'])
    
    # Recommendations
    st.markdown("### 💡 Recommendations")
    for i, rec in enumerate(report["recommendations"], 1):
        st.markdown(f"{i}. {rec}")
    
    # Download options
    st.markdown("---")
    st.markdown("### 📥 Export Report")
    
    col1, col2 = st.columns(2)
    
    with col1:
        json_str = json.dumps(report, indent=2)
        st.download_button(
            label="📄 Download as JSON",
            data=json_str,
            file_name=f"{report['alert_id']}_report.json",
            mime="application/json"
        )
    
    with col2:
        # Generate text report
        text_report = f"""
CyberSentinel Incident Response Report
{'='*60}

Alert ID: {report['alert_id']}
Severity: {report['severity']}
Category: {report['category']}
Timestamp: {report['timestamp']}

THREAT INTELLIGENCE
{'='*60}
MITRE Techniques: {', '.join(report['mitre_techniques'])}
Threat Actors: {', '.join(report['threat_actors'])}

RESPONSE PLAYBOOK
{'='*60}
"""
        for step in report['response_steps']:
            text_report += f"\nStep {step['step_number']}: {step['title']}\n"
            text_report += f"- {step['description']}\n"
            text_report += f"- Time: {step['estimated_time']} | Priority: {step['priority']}\n"
        
        text_report += f"\n\nRECOMMENDATIONS\n{'='*60}\n"
        for rec in report['recommendations']:
            text_report += f"- {rec}\n"
        
        st.download_button(
            label="📝 Download as TXT",
            data=text_report,
            file_name=f"{report['alert_id']}_report.txt",
            mime="text/plain"
        )

# ─────────────────────────────────────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888;">
    <p>CyberSentinel v1.0 | Autonomous SOC Analyst</p>
    <p>Built with Python, LangChain, and Streamlit</p>
</div>
""", unsafe_allow_html=True)