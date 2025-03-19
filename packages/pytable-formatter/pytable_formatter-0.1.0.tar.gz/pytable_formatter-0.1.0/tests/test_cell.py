"""
Tests for the Cell class.
"""
import unittest
from pytable_formatter import Cell, TextAlign, TextStyle, Color


class TestCell(unittest.TestCase):
    """Test cases for the Cell class."""

    def test_cell_initialization(self):
        """Test that a cell can be properly initialized with different values."""
        # Test with default values
        cell = Cell("test")
        self.assertEqual(cell.value, "test")
        self.assertEqual(cell.align, TextAlign.LEFT)
        self.assertIsNone(cell.style)
        self.assertIsNone(cell.fg_color)
        self.assertIsNone(cell.bg_color)
        self.assertEqual(cell.span, 1)

        # Test with custom values
        cell = Cell(
            value=123,
            align=TextAlign.RIGHT,
            style=TextStyle.BOLD,
            fg_color=Color.GREEN,
            bg_color=Color.BLACK,
            span=2,
            formatter=lambda x: f"${x}"
        )

        self.assertEqual(cell.value, 123)
        self.assertEqual(cell.align, TextAlign.RIGHT)
        self.assertEqual(cell.style, TextStyle.BOLD)
        self.assertEqual(cell.fg_color, Color.GREEN)
        self.assertEqual(cell.bg_color, Color.BLACK)
        self.assertEqual(cell.span, 2)
        self.assertEqual(cell.formatter(123), "$123")

    def test_cell_string_representation(self):
        """Test the string representation of a cell with no styling."""
        # Simple value
        cell = Cell("test")
        self.assertEqual(str(cell), "test")

        # Numeric value
        cell = Cell(123)
        self.assertEqual(str(cell), "123")

        # Custom formatter
        cell = Cell(123, formatter=lambda x: f"${x:,.2f}")
        self.assertEqual(str(cell), "$123.00")

    def test_cell_with_custom_formatter(self):
        """Test a cell with a custom formatter function."""
        # Price formatter
        price_formatter = lambda x: f"${x:,.2f}"
        cell = Cell(1234.5, formatter=price_formatter)
        self.assertEqual(str(cell), "$1,234.50")

        # Percentage formatter
        pct_formatter = lambda x: f"{x:.1f}%"
        cell = Cell(75.5, formatter=pct_formatter)
        self.assertEqual(str(cell), "75.5%")


if __name__ == '__main__':
    unittest.main()