"""
SentinelAI Network Traffic Preprocessing Module.
Handles stateful feature scaling, robust categorical encoding, and target binarization.
"""

import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import joblib

class NIDSPreprocessor:
    """Stateful preprocessor for converting raw network packets into ML-compatible arrays."""
    
    def __init__(self):
        self.cat_cols = ['protocol_type', 'service', 'flag']
        self.num_cols = []
        self.preprocessor = None
        
    def fit_transform(self, df: pd.DataFrame, target_col: str = 'class') -> tuple[np.ndarray, np.ndarray]:
        """
        Fits transformers on baseline training data and returns processed features and binary targets.
        Normal traffic is encoded as 0, and any classification of anomaly/attack is encoded as 1.
        """
        X = df.drop(columns=[target_col])
        y_raw = df[target_col]
        
        y = (y_raw != 'normal').astype(int)
        self.num_cols = [col for col in X.columns if col not in self.cat_cols]
        
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), self.num_cols),
                ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), self.cat_cols)
            ])
        
        X_processed = self.preprocessor.fit_transform(X)
        return X_processed, y.values
        
    def transform(self, df: pd.DataFrame) -> np.ndarray:
        """Transforms streaming real-time data using the pre-configured baseline scales."""
        if isinstance(df, pd.Series):
            df = pd.DataFrame([df])
            
        return self.preprocessor.transform(df)
        
    def save(self, filepath: str = 'SentinelAI/models/preprocessor.pkl') -> None:
        """Serializes the initialized preprocessor state to disk."""
        joblib.dump(self, filepath)
        
    @classmethod
    def load(cls, filepath: str = 'SentinelAI/models/preprocessor.pkl') -> 'NIDSPreprocessor':
        """Deserializes a preprocessor state from disk."""
        return joblib.load(filepath)
