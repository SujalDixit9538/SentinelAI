import sys
import os

# Set the project root to the current directory
project_root = os.path.abspath(os.path.dirname(__file__))

# Add the project root to sys.path so 'SentinelAI' is importable
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Launch the app
try:
    from SentinelAI.dashboard.gradio_app import app
    app.launch()
except Exception as e:
    print(f"Failed to launch app: {e}")
    sys.exit(1)
