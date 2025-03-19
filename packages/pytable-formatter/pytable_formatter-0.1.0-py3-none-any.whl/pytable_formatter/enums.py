"""
Enums for text alignment, styling, and colors in the table.
"""
from enum import Enum


class TextAlign(Enum):
    """Text alignment options for table cells."""
    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"


class TextStyle(Enum):
    """Text style options for table cells."""
    NORMAL = 0
    BOLD = 1
    ITALIC = 3
    UNDERLINE = 4


class Color(Enum):
    """ANSI color options for table cells."""
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    DEFAULT = 39