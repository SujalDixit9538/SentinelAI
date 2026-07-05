import sys
import os
import streamlit as st
import pandas as pd

# --- CRITICAL PATH FIX ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
if project_root not in sys.path:
    sys.path.append(project_root)

from SentinelAI.preprocessing.preprocessor import NIDSPreprocessor
from SentinelAI.training.model import NIDSClassifier
from SentinelAI.explainability.explainer import ThreatExplainer
from SentinelAI.training.feedback import FeedbackManager

# Page Config
st.set_page_config(page_title="SentinelAI NIDS", layout="wide")
st.title("🛡️ SentinelAI: Network Intrusion Detection System")

# Load Components 
@st.cache_resource
def load_system():
    prep = NIDSPreprocessor.load('SentinelAI/models/preprocessor.pkl')
    mod = NIDSClassifier.load('SentinelAI/models/nids_model.pkl')
    exp = ThreatExplainer(mod, prep)
    fb = FeedbackManager(mod, prep)
    data = pd.read_csv('/content/Train_data.csv')
    return prep, mod, exp, fb, data

preprocessor, model, explainer, feedback_mgr, df = load_system()

# Session State for tracking simulation progress
if 'packet_idx' not in st.session_state:
    st.session_state.packet_idx = 0

# --- Sidebar UI ---
st.sidebar.header("System Controls")
# HOTFIX 1: Removed emoji to prevent iconPosition JS loading errors
if st.sidebar.button("Analyze Next Packet"):
    st.session_state.packet_idx += 1

# --- Main UI ---
current_idx = st.session_state.packet_idx
packet_df = df.iloc[[current_idx]]
raw_payload = packet_df.drop(columns=['class'])

st.subheader(f"Intercepted Packet #{current_idx}")

# HOTFIX 2: Replaced st.dataframe() with st.json(). 
# It is immune to localtunnel drops and looks like a real SOC data feed.
st.json(raw_payload.iloc[0].to_dict())

# Pipeline Processing
with st.spinner("Analyzing packet..."):
    X_stream = preprocessor.transform(raw_payload)
    threat_prob = model.predict_proba(X_stream)[0][1]
    prediction = 1 if threat_prob > 0.5 else 0

# Display Results
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Threat Score (Probability of Attack)", value=f"{threat_prob:.4f}")
    if prediction == 1:
        st.error("ALERT: MALICIOUS TRAFFIC DETECTED")
    else:
        st.success("TRAFFIC NORMAL")
        
with col2:
    if prediction == 1:
        st.subheader("Brain of the AI (Explainability)")
        explanations = explainer.explain(X_stream)
        for exp in explanations:
            st.write(f"- **{exp['feature']}**: Impact Weight of `{exp['impact_score']}` (Value: {exp['value']})")
            
        st.warning("Is this a False Positive?")
        # HOTFIX 3: Simplified button text
        if st.button("Flag as Normal (Retrain Model)"):
            feedback_mgr.process_analyst_correction(raw_payload, 0)
            st.success("Model updated successfully via Online Learning!")
