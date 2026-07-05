"""
SentinelAI Interactive SOC Dashboard.
Orchestrates streaming packets, O(F) explainability, and secure watsonx.ai reporting.
"""

import sys
import os
import pandas as pd
import gradio as gr
from dotenv import load_dotenv, find_dotenv

# --- Dynamic Path Resolution ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
if project_root not in sys.path:
    sys.path.append(project_root)

# Load variables from the hidden .env file securely
load_dotenv(find_dotenv())

from SentinelAI.preprocessing.preprocessor import NIDSPreprocessor
from SentinelAI.training.model import NIDSClassifier
from SentinelAI.explainability.explainer import ThreatExplainer
from SentinelAI.explainability.watson_reporter import WatsonReporter
from SentinelAI.training.feedback import FeedbackManager

# --- Runtime Dependency Injection ---
prep = NIDSPreprocessor.load('SentinelAI/models/preprocessor.pkl')
mod = NIDSClassifier.load('SentinelAI/models/nids_model.pkl')
exp = ThreatExplainer(mod, prep)
fb = FeedbackManager(mod, prep)

# Fetch credentials securely from the environment
watson = WatsonReporter(
    api_key=os.getenv("IBM_API_KEY"), 
    project_id=os.getenv("WATSONX_PROJECT_ID")
)

# Load blind test dataset for real-time simulation
df = pd.read_csv('/content/Test_data.csv')

def analyze_packet(current_idx: int) -> tuple:
    if current_idx >= len(df):
        current_idx = 0
        
    raw_payload = df.iloc[[current_idx]]
    X_stream = prep.transform(raw_payload)
    threat_prob = mod.predict_proba(X_stream)[0][1]
    prediction = 1 if threat_prob > 0.5 else 0
    
    status = "🚨 ALERT: MALICIOUS TRAFFIC DETECTED" if prediction == 1 else "✅ TRAFFIC NORMAL"
    explanation_text = "No anomaly detected."
    watson_report = "N/A - Traffic is normal."
    
    if prediction == 1:
        explanations = exp.explain(X_stream)
        explanation_text = "\n".join([f"• {e['feature']}: Impact {e['impact_score']} (Value: {e['value']})" for e in explanations])
        watson_report = watson.generate_mitigation_report(explanations)
        
    return (
        current_idx + 1, 
        raw_payload.iloc[0].to_dict(), 
        f"{threat_prob:.4f}", 
        status, 
        explanation_text, 
        watson_report, 
        raw_payload
    )

def process_feedback(raw_payload_state: pd.DataFrame) -> str:
    if raw_payload_state is not None:
        fb.process_analyst_correction(raw_payload_state, correct_label=0)
        return "✅ Model weights updated successfully via Online Learning!"
    return "⚠️ No packet loaded to correct."

# --- UI Architecture Layout ---
with gr.Blocks(theme=gr.themes.Monochrome()) as app:
    gr.Markdown("# 🛡️ SentinelAI: Hybrid NIDS with watsonx.ai")
    
    packet_idx = gr.State(value=0)
    raw_packet_state = gr.State(value=None)
    
    with gr.Row():
        next_btn = gr.Button("➡️ Intercept Next Network Packet (Unseen Test Data)", variant="primary")
        
    with gr.Row():
        with gr.Column():
            gr.Markdown("### Raw Packet Payload")
            packet_display = gr.JSON(label="Intercepted Data")
            
        with gr.Column():
            gr.Markdown("### AI Threat Assessment")
            threat_score = gr.Textbox(label="Threat Score")
            status_display = gr.Textbox(label="System Status")
            explanation_display = gr.Textbox(label="Mathematical Explainer (O(F))", lines=3)
            watson_display = gr.Textbox(label="Watsonx.ai SOC Mitigation Report", lines=4)
            
            gr.Markdown("### Analyst Feedback")
            feedback_btn = gr.Button("Flag as Normal (Retrain Model)")
            feedback_status = gr.Textbox(label="Feedback Status")

    next_btn.click(
        fn=analyze_packet,
        inputs=[packet_idx],
        outputs=[packet_idx, packet_display, threat_score, status_display, explanation_display, watson_display, raw_packet_state]
    )
    
    feedback_btn.click(fn=process_feedback, inputs=[raw_packet_state], outputs=[feedback_status])

if __name__ == "__main__":
    app.launch(share=True, debug=False)
