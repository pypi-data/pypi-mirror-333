"""
PyTable-Formatter: Advanced Table Formatting for Terminal Output

A Python library that provides enhanced table formatting capabilities for command-line applications
with support for nested tables, cell styling, and interactive elements.

Author: Biswanath Roul (authorbiswanath@gmail.com)
"""

from .enums import TextAlign, TextStyle, Color
from .cell import Cell
from .table import Table

__version__ = '0.1.0'
__all__ = ['Table', 'Cell', 'TextAlign', 'TextStyle', 'Color']

def demo():
    """Run a demonstration of PyTable-Formatter capabilities."""
    from .table import demo as table_demo
    table_demo()