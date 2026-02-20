# Vercel looks for app at index.py, server.py, or app.py
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from backend.main import app
