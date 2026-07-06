import sys
import os
import types

# 1. Dynamically anchor the runtime environment to the root directory
root_dir = os.path.abspath(os.path.dirname(__file__))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# 2. Pre-import the loose folders so they exist in memory
import preprocessing
import preprocessing.preprocessor
import training
import training.model

# 3. THE PICKLE HACK: Inject a virtual 'SentinelAI' package map into sys.modules.
# This intercepts joblib/pickle loading requests and maps them to your root paths.
sentinel_mock = types.ModuleType('SentinelAI')
sys.modules['SentinelAI'] = sentinel_mock
sys.modules['SentinelAI.preprocessing'] = preprocessing
sys.modules['SentinelAI.preprocessing.preprocessor'] = preprocessing.preprocessor
sys.modules['SentinelAI.training'] = training
sys.modules['SentinelAI.training.model'] = training.model

# 4. Launch the dashboard safely now that the pickle trap is resolved
from dashboard.gradio_app import app

if __name__ == "__main__":
    app.launch()import sys
import os

# Ensure the root directory is in the path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Import directly from the dashboard folder since SentinelAI parent doesn't exist
from dashboard.gradio_app import app

if __name__ == "__main__":
    app.launch()
