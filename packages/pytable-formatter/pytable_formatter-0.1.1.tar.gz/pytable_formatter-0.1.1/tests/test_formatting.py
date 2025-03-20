"""
Tests for formatting functionality in PyTable-Formatter.
"""
import unittest
from pytable_formatter import Table, Cell, TextAlign, TextStyle, Color


class TestFormatting(unittest.TestCase):
    """Test cases for table formatting functionality."""

    def test_cell_alignment(self):
        """Test that cell alignment is applied correctly."""
        # Create a table with cells using different alignments
        table = Table(
            data=[
                [
                    Cell("Left", align=TextAlign.LEFT),
                    Cell("Center", align=TextAlign.CENTER),
                    Cell("Right", align=TextAlign.RIGHT)
                ]
            ]
        )

        # Get the formatted cells directly for testing
        left_cell = table._format_cell(table.rows[0][0], 15)
        center_cell = table._format_cell(table.rows[0][1], 15)
        right_cell = table._format_cell(table.rows[0][2], 15)

        # Remove padding to check alignment
        left_content = left_cell.strip()
        center_content = center_cell.strip()
        right_content = right_cell.strip()

        # Check that left alignment starts with content
        self.assertTrue(left_content.startswith("Left"))
        # Check that center alignment has spaces on both sides
        self.assertTrue(center_content.startswith(" ") and center_content.endswith(" "))
        # Check that right alignment ends with content
        self.assertTrue(right_content.endswith("Right"))

    def test_cell_truncation(self):
        """Test that long cell content is truncated correctly."""
        long_content = "This is a very long string that should be truncated"
        cell = Cell(long_content)
        table = Table()

        # Format the cell to a width that's shorter than the content
        formatted = table._format_cell(cell, 20)

        # Check that the content was truncated and has ellipsis
        self.assertLess(len(formatted), len(long_content))
        self.assertTrue("..." in formatted)

    def test_multiline_cell_content(self):
        """Test handling of multiline cell content."""
        multiline_content = "First line\nSecond line\nThird line"
        cell = Cell(multiline_content)
        table = Table()

        # Format the cell
        formatted = table._format_cell(cell, 20)

        # Check that newlines are preserved
        self.assertEqual(formatted.count("\n"), 2)
        self.assertIn("First line", formatted)
        self.assertIn("Second line", formatted)
        self.assertIn("Third line", formatted)

    def test_custom_formatter(self):
        """Test that custom formatters are applied correctly."""
        # Create a cell with a currency formatter
        currency_cell = Cell(
            1234.56,
            formatter=lambda x: f"${x:,.2f}"
        )

        # Create a cell with a percentage formatter
        percentage_cell = Cell(
            0.7525,
            formatter=lambda x: f"{x:.2%}"
        )

        table = Table()

        # Format the cells
        formatted_currency = table._format_cell(currency_cell, 15)
        formatted_percentage = table._format_cell(percentage_cell, 15)

        # Check that formatters were applied
        self.assertIn("$1,234.56", formatted_currency)
        self.assertIn("75.25%", formatted_percentage)

    def test_border_styles(self):
        """Test different border styles."""
        # Default border style
        default_table = Table(
            headers=["Header"],
            data=[["Data"]]
        )
        default_rendered = default_table.render()

        # Custom border style (ASCII only)
        ascii_table = Table(
            headers=["Header"],
            data=[["Data"]],
            border_style="| + + + + + + + + + -"
        )
        ascii_rendered = ascii_table.render()

        # Check that the rendered tables use different border characters
        self.assertNotEqual(default_rendered[0], ascii_rendered[0])


if __name__ == '__main__':
    unittest.main()