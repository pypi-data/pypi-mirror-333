"""
Auto ML Processor
----------------

A Python package for automated machine learning preprocessing and model training.
"""

__version__ = '0.1.2'

# Import the main class to make it available at the package level
from .processor import AutoMLProcessor

# Define what should be available when doing "from auto_ml_processor import *"
__all__ = ['AutoMLProcessor']