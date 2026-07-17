"""Pytest configuration and fixtures."""
import sys
import os
import pytest

# Add backend directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))