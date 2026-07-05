import pandas as pd
import time

class PacketStreamer:
    def __init__(self, filepath):
        self.filepath = filepath
        
    def stream(self, batch_size=1, delay=0.0):
        """
        Yields data chunks to simulate a real-time network stream.
        
        Parameters:
        - batch_size: Number of rows to yield at a time (1 = single packet).
        - delay: Artificial delay in seconds between packets to mimic network latency.
        """
        # chunksize enables memory-safe iterative reading
        for chunk in pd.read_csv(self.filepath, chunksize=batch_size):
            if delay > 0:
                time.sleep(delay)
            yield chunk
