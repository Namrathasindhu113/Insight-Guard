import streamlit as st
import pandas as pd
import requests
import os
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards
import numpy as np
# -----------------------------------
# 🔧 App configuration
# -----------------------------------
st.set_page_config(
    page_title="Insight Guard Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ---- SAFE AUTO REFRESH ----
import time

# Simple refresh logic using Streamlit session state
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()

# If 30 seconds passed since last refresh
if time.time() - st.session_state.last_refresh > 30:
    st.session_state.last_refresh = time.time()
    st.rerun()
# ---- END AUTO REFRESH ----


# -----------------------------------
# 🎨 Custom CSS styling
# -----------------------------------
st.markdown("""
    <style>
        /* === Cyber Dashboard Theme === */
        @keyframes bg-anim {
            0% { background-position: 0 0; }
            100% { background-position: 1000px 1000px; }
        }

        .stApp {
            background-color: #0a0a0f;
            background-image: linear-gradient(135deg, rgba(0,255,255,0.08) 1px, transparent 1px),
                              linear-gradient(225deg, rgba(0,255,255,0.08) 1px, transparent 1px);
            background-size: 40px 40px;
            animation: bg-anim 60s linear infinite;
            color: #e0e0e0;
        }

        h1, h2, h3, h4 {
            color: #00f5ff !important;
            text-shadow: 0 0 8px rgba(0,255,255,0.6);
        }

        /* Metric Cards */
        div[data-testid="stMetric"] {
            background: linear-gradient(135deg, rgba(0,255,255,0.08), rgba(0,255,255,0.02));
            border: 1px solid rgba(0,255,255,0.3);
            border-radius: 15px;
            padding: 15px;
            margin: 6px;
            box-shadow: 0 0 15px rgba(0,255,255,0.2);
            transition: all 0.3s ease;
        }

        div[data-testid="stMetric"]:hover {
            transform: scale(1.03);
            box-shadow: 0 0 20px rgba(0,255,255,0.5);
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #0d1117;
            border-right: 2px solid rgba(0,255,255,0.1);
        }

        /* Tables */
        .stDataFrame {
            background-color: #10131a;
            color: #d9faff !important;
            border-radius: 12px;
        }

        /* Buttons */
        button[kind="primary"] {
            background: linear-gradient(90deg, #00f5ff, #007bff);
            border: none;
            color: white;
            font-weight: 600;
            border-radius: 10px;
            transition: all 0.3s ease;
        }

        button[kind="primary"]:hover {
            transform: scale(1.05);
            box-shadow: 0 0 10px rgba(0,255,255,0.6);
        }

        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# -----------------------------------
# 🧠 Fetch data from backend
# -----------------------------------
backend_url = os.environ.get("BACKEND_URL", "http://localhost:8000")

try:
    resp = requests.get(f"{backend_url}/score", timeout=5).json()
except Exception as e:
    st.error(f"❌ Failed to fetch scores from {backend_url}/score — {e}")
    st.stop()

if not resp:
    st.warning("⚠️ No data available. Run `/train` in backend first.")
    st.stop()

df = pd.DataFrame(resp)

# -----------------------------------
# 🧾 Dashboard Header
# -----------------------------------
st.title("🛡️ INSIGHT GUARD – Risk Analytics Dashboard")
st.markdown("""
<style>
@keyframes glow {
  0% { color: #00b4d8; text-shadow: 0 0 5px #00b4d8; }
  50% { color: #48cae4; text-shadow: 0 0 20px #48cae4; }
  100% { color: #00b4d8; text-shadow: 0 0 5px #00b4d8; }
}
h1 {
  animation: glow 2s ease-in-out infinite;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
    <h3 style='text-align: center; color: #00f5ff; text-shadow: 0 0 15px #00f5ff;'>
        🔐 Real-Time Threat Monitoring | Cyber Risk Intelligence
    </h3>
    <hr style='border: 1px solid rgba(0,255,255,0.3);'>
""", unsafe_allow_html=True)
st.subheader("Monitoring user behavior and anomaly risks in real-time")

# -----------------------------------
# 📊 Metric Summary Cards
# -----------------------------------
col1, col2, col3 = st.columns(3)

avg_risk = df['risk_score'].mean()
max_risk = df['risk_score'].max()
critical_users = (df['risk_score'] > 80).sum()

col1.metric("Average Risk Score", f"{avg_risk:.1f}")
col2.metric("Highest Risk", f"{max_risk:.1f}")
col3.metric("Critical Users", critical_users)

style_metric_cards()
# === Cyber Risk Pulse Radar ===
import streamlit.components.v1 as components
pulse_html = """
<div style="display:flex;justify-content:center;margin-top:30px;">
  <div style="position:relative;width:150px;height:150px;border-radius:50%;
              background:radial-gradient(circle at center,
              rgba(0,255,255,0.5) 0%,rgba(0,255,255,0.1) 60%,rgba(0,255,255,0) 70%);
              animation:pulse 2s infinite;">
  </div>
</div>
<style>
@keyframes pulse {
  0% {transform:scale(0.8);opacity:0.6;}
  50% {transform:scale(1.05);opacity:1;}
  100% {transform:scale(0.8);opacity:0.6;}
}
</style>
"""
components.html(pulse_html, height=180)
st.markdown("<h5 style='text-align:center;color:#00f5ff;'>System Health – Monitoring Active</h5>", unsafe_allow_html=True)
st.divider()

# -----------------------------------
# 👥 Risk Overview Table
# -----------------------------------
st.markdown("### 👥 User Risk Overview")
st.dataframe(df[['user','risk_score','rule_score','iso_score']], use_container_width=True)
st.divider()

# -----------------------------------
# 📈 Individual Risk Trend
# -----------------------------------
selected_user = st.selectbox("Select user to view trend:", df['user'].unique())
user_score = df.loc[df['user'] == selected_user, 'risk_score'].values[0]

# Generate a mock 7-day trend
days = pd.date_range(end=pd.Timestamp.now(), periods=7).strftime("%Y-%m-%d")
trend = [max(0, user_score + (i-3)*5 + np.random.randn()*3) for i in range(7)]

chart = px.line(x=days, y=trend, labels={'x':'Date','y':'Risk Score'},
                title=f"📈 7-Day Risk Trend for {selected_user}")
st.plotly_chart(chart, use_container_width=True)

# -----------------------------------
# 📋 User Details Section
# -----------------------------------
st.markdown("### 🧾 User Details")
st.json(df[df['user'] == selected_user].to_dict(orient='records')[0])

# -----------------------------------
# ⚙️ Sidebar Controls
# -----------------------------------
st.sidebar.title("⚙️ Controls")
refresh_btn = st.sidebar.button("🔄 Refresh Now")

st.sidebar.markdown("### 📁 Upload Custom Log File")

uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded CSV
    uploaded_df = pd.read_csv(uploaded_file)

    st.markdown("### 🔍 Uploaded Log Preview")
    st.dataframe(uploaded_df.head(), use_container_width=True)

    # Optionally, send uploaded file to backend for scoring
    if st.sidebar.button("🚀 Analyze Uploaded Logs"):
        try:
            # Send file content to backend
            backend_url = os.environ.get("BACKEND_URL", "http://localhost:8000")
            files = {"file": uploaded_file.getvalue()}
            response = requests.post(f"{backend_url}/upload", files=files)

            if response.status_code == 200:
                st.success("✅ File sent for analysis successfully!")
            else:
                st.error(f"❌ Upload failed — {response.text}")
        except Exception as e:
            st.error(f"Failed to connect to backend: {e}")

if refresh_btn:
    st.rerun()

 # === Live Alert Ticker ===
alert_html = """
<div style="position:fixed;bottom:0;width:100%;background:#001219;
            color:#00f5ff;font-weight:600;padding:8px 0;text-align:center;
            border-top:1px solid rgba(0,255,255,0.3);
            overflow:hidden;white-space:nowrap;">
  <div id="scrollText" style="display:inline-block;animation:scroll-left 20s linear infinite;">
    🚨 Insight Guard Active | User 1 High Risk Detected | System Stable | Monitoring Network Anomalies | No new breaches reported 🚨
  </div>
</div>
<style>
@keyframes scroll-left {
  0% {transform:translateX(100%);}
  100% {transform:translateX(-100%);}
}
</style>
"""
components.html(alert_html, height=40)
   
