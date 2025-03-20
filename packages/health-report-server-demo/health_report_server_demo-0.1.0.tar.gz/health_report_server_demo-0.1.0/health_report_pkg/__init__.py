# health_report_pkg/__init__.py

"""
Health Report Package
=====================
A Django-based health report system.

This package provides functionalities to monitor and generate reports for system health.
"""

__version__ = "0.1.0"

# Import necessary modules for easier access when the package is imported
from .cli import main

# Define what gets imported when using `from health_report_pkg import *`
__all__ = ["main"]
