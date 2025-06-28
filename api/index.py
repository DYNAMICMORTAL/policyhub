import sys
import os

# Add the parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the Flask app
from app import app

# Vercel expects this handler
def handler(request):
    return app(request)

# For compatibility
application = app

if __name__ == "__main__":
    app.run()
