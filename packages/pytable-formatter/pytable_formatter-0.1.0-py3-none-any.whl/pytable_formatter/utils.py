"""
Utility functions for PyTable-Formatter.
"""
import shutil
import os


def get_terminal_width() -> int:
    """
    Get the current terminal width.

    Returns:
        int: The width of the terminal in columns, or 80 as a fallback.
    """
    try:
        return shutil.get_terminal_size().columns
    except (AttributeError, ValueError, OSError):
        return 80  # Default fallback width


def supports_ansi() -> bool:
    """
    Determine if the current terminal supports ANSI escape codes.

    Returns:
        bool: True if ANSI is supported, False otherwise.
    """
    # Check for Windows without ANSI support
    if os.name == 'nt' and not os.environ.get('TERM'):
        # Check if running in ANSICON or ConEmu
        return bool(os.environ.get('ANSICON') or
                    os.environ.get('ConEmuANSI') == 'ON')

    # Most Unix-like systems and Windows with proper terminals
    return True