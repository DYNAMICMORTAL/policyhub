import sys
import os

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Vercel expects a handler function
def handler(request):
    return app(request.environ, lambda status, headers: None)

# For compatibility
application = app

if __name__ == "__main__":
    app.run()
