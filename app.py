import sys
import os

# Get the absolute path of the directory containing app.py (/app)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Inject both the root directory and the SentinelAI subdirectory into Python's search path
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

sentinel_path = os.path.join(current_dir, "SentinelAI")
if os.path.exists(sentinel_path) and sentinel_path not in sys.path:
    sys.path.insert(0, sentinel_path)

# Safe relative import execution
try:
    from SentinelAI.dashboard.gradio_app import app
except ModuleNotFoundError:
    # Fallback if the folder structure was flattened during the git push
    from dashboard.gradio_app import app

if __name__ == "__main__":
    app.launch()
