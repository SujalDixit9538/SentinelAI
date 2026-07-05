"""
SentinelAI Analyst Feedback Core.
Integrates human-in-the-loop validation actions back into the live ML pipeline weights.
"""

import pandas as pd
import numpy as np
from SentinelAI.preprocessing.preprocessor import NIDSPreprocessor
from SentinelAI.training.model import NIDSClassifier

class FeedbackManager:
    """Manages structural runtime adjustments based on analyst overriding labels."""
    
    def __init__(self, model_wrapper: NIDSClassifier, preprocessor_wrapper: NIDSPreprocessor):
        self.model = model_wrapper
        self.preprocessor = preprocessor_wrapper
        self.corrections_count = 0
        
    def process_analyst_correction(self, raw_packet: pd.DataFrame, correct_label: int) -> bool:
        """Transforms human overrides and triggers real-time model retraining weights via SGD optimization."""
        X_processed = self.preprocessor.transform(raw_packet)
        y_correct = np.array([correct_label])
        
        self.model.incremental_train(X_processed, y_correct)
        self.corrections_count += 1
        self.model.save()
        
        return True
