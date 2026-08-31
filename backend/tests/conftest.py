import sys
import os

# Add backend and root to sys.path for pytest
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root_dir = os.path.dirname(backend_dir)

sys.path.insert(0, backend_dir)
sys.path.insert(0, root_dir)
