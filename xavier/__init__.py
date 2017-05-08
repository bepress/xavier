import os
import sys

__version__ = "0.0.1"

# Add vendor directory to module search path
parent_dir = os.path.abspath(os.path.dirname(__file__))
vendor_dir = os.path.join(parent_dir, 'vendor')

sys.path.insert(1, vendor_dir)
