"""
Tests for the Table class.
"""
import unittest
import re
from pytable_formatter import Table, Cell, TextAlign, TextStyle, Color


class TestTable(unittest.TestCase):
    """Test cases for the Table class."""

    def test_table_initialization(self):
        """Test that a table can be properly initialized."""
        # Empty table
        table = Table()
        self.assertEqual(table.rows, [])
        self.assertEqual(table.headers, [])

        # Table with headers
        headers = ["Name", "Age", "Country"]
        table = Table(headers=headers)
        self.assertEqual(len(table.headers), 3)
        self.assertEqual(table.headers[0].value, "Name")

        # Table with data
        data = [
            ["John", 30, "USA"],
            ["Mary", 25, "Canada"]
        ]
        table = Table(data=data)
        self.assertEqual(len(table.rows), 2)
        self.assertEqual(table.rows[0][0].value, "John")

        # Table with title and footer
        table = Table(
            headers=headers,
            data=data,
            title="Test Table",
            footer="Test Footer"
        )
        self.assertEqual(table.title, "Test Table")
        self.assertEqual(table.footer, "Test Footer")

    def test_add_row(self):
        """Test adding rows to a table."""
        table = Table()

        # Add a row with simple values
        table.add_row(["John", 30, "USA"])
        self.assertEqual(len(table.rows), 1)
        self.assertEqual(table.rows[0][0].value, "John")

        # Add a row with cell objects
        table.add_row([
            Cell("Mary", style=TextStyle.BOLD),
            Cell(25, align=TextAlign.RIGHT),
            Cell("Canada", fg_color=Color.GREEN)
        ])
        self.assertEqual(len(table.rows), 2)
        self.assertEqual(table.rows[1][0].value, "Mary")
        self.assertEqual(table.rows[1][0].style, TextStyle.BOLD)

    def test_calculate_column_widths(self):
        """Test the column width calculation."""
        # Table with fixed content
        table = Table(
            headers=["Name", "Age", "Country"],
            data=[
                ["John Doe", 30, "United States of America"],
                ["Mary Smith", 25, "Canada"]
            ]
        )

        col_widths = table._calculate_column_widths()

        # Check that we have 3 columns
        self.assertEqual(len(col_widths), 3)

        # Check that the widths are appropriate
        # Name column should be at least wide enough for "John Doe" plus padding
        self.assertGreaterEqual(col_widths[0], len("John Doe") + table.padding * 2)

        # Country column should be wide enough for "United States of America" plus padding
        self.assertGreaterEqual(col_widths[2], len("United States of America") + table.padding * 2)

    def test_render_empty_table(self):
        """Test rendering an empty table."""
        table = Table()
        rendered = table.render()
        self.assertEqual(rendered, "")

    def test_render_table_with_content(self):
        """Test rendering a table with content."""
        table = Table(
            headers=["Name", "Age"],
            data=[
                ["John", 30],
                ["Mary", 25]
            ],
            title="Test Table"
        )

        rendered = table.render()

        # Check that the rendered output is a string
        self.assertIsInstance(rendered, str)

        # Check that it contains the title
        self.assertIn("Test Table", rendered)

        # Check that it contains the headers
        self.assertIn("Name", rendered)
        self.assertIn("Age", rendered)

        # Check that it contains the data
        self.assertIn("John", rendered)
        self.assertIn("30", rendered)
        self.assertIn("Mary", rendered)
        self.assertIn("25", rendered)

    def test_render_table_with_styled_cells(self):
        """Test rendering a table with styled cells."""
        table = Table(
            headers=[
                Cell("Name", style=TextStyle.BOLD),
                Cell("Age", style=TextStyle.BOLD)
            ],
            data=[
                [
                    Cell("John", fg_color=Color.GREEN),
                    Cell(30, align=TextAlign.RIGHT)
                ],
                [
                    Cell("Mary", fg_color=Color.BLUE),
                    Cell(25, align=TextAlign.RIGHT)
                ]
            ]
        )

        rendered = table.render()
        self.assertIsInstance(rendered, str)

        # We can't easily test the ANSI codes here since they may be disabled in test environment
        # So we just check that the content is present
        self.assertIn("John", rendered)
        self.assertIn("30", rendered)
        self.assertIn("Mary", rendered)
        self.assertIn("25", rendered)

    def test_render_table_with_footer(self):
        """Test rendering a table with a footer."""
        table = Table(
            headers=["Name", "Age"],
            data=[
                ["John", 30],
                ["Mary", 25]
            ],
            footer="Total: 2 people"
        )

        rendered = table.render()
        self.assertIn("Total: 2 people", rendered)


if __name__ == '__main__':
    unittest.main()