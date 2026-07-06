import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from SentinelAI.dashboard.gradio_app import app

if __name__ == "__main__":
    app.launch()
