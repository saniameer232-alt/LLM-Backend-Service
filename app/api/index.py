
import sys
import os

# Root directory ko path mein add karna taake 'main.py' ya 'app' easily import ho sakay
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app