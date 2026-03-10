import sys
import os
from pathlib import Path

# Add the project directory to sys.path so app.py can import local modules
current_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(current_dir))

# Import the Flask app object from the main app.py
from app import app

# This allows running locally via this file if needed
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
