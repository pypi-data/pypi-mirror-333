"""
Cell class for individual table cells with styling and formatting.
"""
import os
from typing import Any, Optional, Callable
from .enums import TextAlign, TextStyle, Color


class Cell:
    """Represents a single cell in a table."""

    def __init__(
        self,
        value: Any,
        align: TextAlign = TextAlign.LEFT,
        style: Optional[TextStyle] = None,
        fg_color: Optional[Color] = None,
        bg_color: Optional[Color] = None,
        span: int = 1,
        formatter: Optional[Callable[[Any], str]] = None
    ):
        """
        Initialize a table cell with content and styling options.

        Args:
            value: The content of the cell.
            align: Text alignment within the cell (LEFT, RIGHT, CENTER).
            style: Text style (NORMAL, BOLD, ITALIC, UNDERLINE).
            fg_color: Foreground (text) color.
            bg_color: Background color.
            span: Number of columns this cell spans.
            formatter: Custom function to format the cell value.
        """
        self.value = value
        self.align = align
        self.style = style
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.span = span
        self.formatter = formatter or str

    def __str__(self) -> str:
        """Get the formatted string representation of the cell value."""
        content = self.formatter(self.value)

        # Apply ANSI styling if terminal supports it
        if os.name != 'nt' or os.environ.get('TERM'):
            parts = []

            # Add style codes
            if self.style:
                parts.append(f"\033[{self.style.value}m")

            # Add foreground color
            if self.fg_color:
                parts.append(f"\033[{self.fg_color.value}m")

            # Add background color
            if self.bg_color:
                bg_code = self.bg_color.value + 10  # Convert to background code
                parts.append(f"\033[{bg_code}m")

            # Add the content
            parts.append(content)

            # Reset all styles and colors
            if self.style or self.fg_color or self.bg_color:
                parts.append("\033[0m")

            return "".join(parts)

        return content