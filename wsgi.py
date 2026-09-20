"""
WSGI entrypoint for DBERT Internship Portal
Used by production WSGI servers:
- Gunicorn (Linux): gunicorn -w 4 -b 127.0.0.1:5000 wsgi:app
- Waitress (Windows): waitress-serve --listen=127.0.0.1:5000 wsgi:app
"""
import os
import sys

# Ensure current directory is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

if __name__ == "__main__":
    app.run()
