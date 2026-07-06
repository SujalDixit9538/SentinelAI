"""
SentinelAI O(F) Threat Explainability Layer.
Extracts decision logic weights via mathematical coefficients directly from the linear model.
"""

import numpy as np
from preprocessing.preprocessor import NIDSPreprocessor
from training.model import NIDSClassifier

class ThreatExplainer:
    """High-speed mathematical interpreter designed for millisecond streaming packet auditing."""
    
    def __init__(self, model_wrapper: NIDSClassifier, preprocessor_wrapper: NIDSPreprocessor):
        self.model = model_wrapper.model
        self.preprocessor = preprocessor_wrapper.preprocessor
        self.feature_names = self.preprocessor.get_feature_names_out()
        self.coef_ = self.model.coef_[0]
        
    def explain(self, X_stream: np.ndarray, top_k: int = 3) -> list[dict]:
        """Calculates exact input feature directional impacts contributing to an attack signature warning."""
        packet_features = X_stream[0] if X_stream.ndim > 1 else X_stream
        contributions = packet_features * self.coef_
        
        feature_data = list(zip(self.feature_names, packet_features, contributions))
        sorted_impacts = sorted(feature_data, key=lambda x: x[2], reverse=True)
        
        explanations = []
        for name, val, impact in sorted_impacts[:top_k]:
            clean_name = name.split('__')[-1] 
            explanations.append({
                "feature": clean_name,
                "value": round(float(val), 4),
                "impact_score": round(float(impact), 4)
            })
            
        return explanations
