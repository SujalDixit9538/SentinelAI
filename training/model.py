"""
SentinelAI Online Learning Classifier.
Implements memory-safe Stochastic Gradient Descent for streaming environments.
"""

import joblib
import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score, classification_report

class NIDSClassifier:
    """Wrapper for the core threat classification algorithm supporting online partial fits."""
    
    def __init__(self):
        self.model = SGDClassifier(loss='log_loss', random_state=42)
        self.classes_ = [0, 1] 

    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        """Executes traditional batch training for establishing model baselines."""
        self.model.fit(X, y)

    def incremental_train(self, X: np.ndarray, y: np.ndarray) -> None:
        """Performs step-wise incremental weight adjustments using real-time packet payloads."""
        self.model.partial_fit(X, y, classes=self.classes_)

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Generates raw calibrated class probabilities for severity assessment."""
        return self.model.predict_proba(X)

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> float:
        """Evaluates model performance against target matrices and returns the accuracy score."""
        preds = self.predict(X_test)
        print(classification_report(y_test, preds, target_names=["Normal (0)", "Attack (1)"]))
        return accuracy_score(y_test, preds)

    def save(self, filepath: str = 'SentinelAI/models/nids_model.pkl') -> None:
        joblib.dump(self, filepath)

    @classmethod
    def load(cls, filepath: str = 'SentinelAI/models/nids_model.pkl') -> 'NIDSClassifier':
        return joblib.load(filepath)
