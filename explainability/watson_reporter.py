"""SentinelAI watsonx Orchestrate Integration Middleware."""
import os
import requests

class WatsonReporter:
    """Serverless client wrapper interfacing directly with IBM watsonx Orchestrate Agents."""
    
    def __init__(self, api_key: str, project_id: str):
        # Dynamically pulls credentials from environment secrets
        self.api_key = api_key or os.getenv("IBM_API_KEY")
        self.agent_id = os.getenv("WATSONX_AGENT_ID") 
        self.service_url = os.getenv("WATSONX_SERVICE_URL")
        self.is_connected = True if self.api_key else False

    def get_iam_token(self):
        """Exchanges the IBM Cloud API key for a temporary bearer token."""
        url = "https://iam.cloud.ibm.com/identity/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = f"grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={self.api_key}"
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        return response.json().get("access_token")

    def generate_mitigation_report(self, math_explanations: list[dict]) -> str:
        """Submits parsed telemetry to the deployed watsonx Orchestrate SOC Agent."""
        if not self.is_connected:
            return "Watsonx service unavailable. Operating in local-only monitoring mode."

        anomalies_text = ", ".join([f"{e['feature']} (value: {e['value']})" for e in math_explanations])
        prompt = f"Anomalies: {anomalies_text}"

        try:
            token = self.get_iam_token()
            
            url = f"{self.service_url}/v1/orchestrate/{self.agent_id}/chat/completions"
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "stream": False,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }

            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            text_response = result.get("choices", [{}])[0].get("message", {}).get("content", "No response generated.")
            
            # Remove Markdown asterisks to enforce clean plain text in the UI
            return text_response.replace("**", "").replace("*", "")

        except requests.exceptions.RequestException as e:
            return "Watsonx service currently unavailable. Dashboard operating in local threat assessment mode."
        except Exception as e:
            return "Watsonx service currently unavailable. Dashboard operating in local threat assessment mode."
