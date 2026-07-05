"""
SentinelAI Lightweight Streaming Analytics Environment Guard.
Monitors system metric variances dynamically using O(1) mathematical bounds checking.
"""

import numpy as np

class DriftDetector:
    """Validates structural vector invariants on scaled elements using Z-score boundaries."""
    
    def __init__(self, window_size: int = 50, drift_threshold: float = 2.5):
        self.window_size = window_size
        self.drift_threshold = drift_threshold
        self.buffer = []
        
    def check_drift(self, X_stream: np.ndarray, num_features_count: int) -> bool:
        """Evaluates scaled vector components to verify baseline operational parameter integrity rules."""
        packet_features = X_stream[0] if X_stream.ndim > 1 else X_stream
        num_features = packet_features[:num_features_count]
        
        self.buffer.append(num_features)
        if len(self.buffer) > self.window_size:
            self.buffer.pop(0)
            
        if len(self.buffer) == self.window_size:
            window_mean = np.mean(self.buffer, axis=0)
            max_deviation = np.max(np.abs(window_mean))
            
            if max_deviation > self.drift_threshold:
                self.buffer.clear()
                return True
                
        return False
