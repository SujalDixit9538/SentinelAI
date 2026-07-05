"""
SentinelAI watsonx.ai Integration Middleware.
Translates mathematical telemetry arrays into high-level descriptive mitigation guides.
"""

from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

class WatsonReporter:
    """Serverless client wrapper interfacing directly with remote IBM generative foundation models."""
    
    def __init__(self, api_key: str, project_id: str):
        self.credentials = {
            "url": "https://us-south.ml.cloud.ibm.com",
            "apikey": api_key
        }
        self.project_id = project_id
        self.parameters = {
            GenParams.DECODING_METHOD: "greedy",
            GenParams.MAX_NEW_TOKENS: 150,
            GenParams.MIN_NEW_TOKENS: 10,
            GenParams.TEMPERATURE: 0.5,
        }
        self.model_id = "ibm/granite-13b-chat-v2"
        self.is_connected = False
        
        if api_key and project_id:
            try:
                self.model = Model(
                    model_id=self.model_id, 
                    params=self.parameters,
                    credentials=self.credentials,
                    project_id=self.project_id
                )
                self.is_connected = True
            except Exception:
                self.is_connected = False

    def generate_mitigation_report(self, math_explanations: list[dict]) -> str:
        """Submits parsed mathematical feature violations to IBM Granite for context enrichment."""
        if not self.is_connected:
            return "Watsonx service unavailable. Operating in local-only monitoring mode."
            
        anomalies_text = ", ".join([f"{e['feature']} (value: {e['value']})" for e in math_explanations])
        prompt = (
            f"System: You are a Senior SOC Analyst. Given these network anomalies, write a brief "
            f"2-3 sentence mitigation report detailing the likely vector and immediate host defenses.\n"
            f"Anomalies: {anomalies_text}\n\nSOC Mitigation Report:"
        )

        try:
            return self.model.generate_text(prompt).strip()
        except Exception as e:
            return f"Error executing cloud generation runtime request: {str(e)}"
