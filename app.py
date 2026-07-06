import sys
import os

# Ensure the root directory is in the path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Import directly from the dashboard folder since SentinelAI parent doesn't exist
from dashboard.gradio_app import app

if __name__ == "__main__":
    app.launch()
