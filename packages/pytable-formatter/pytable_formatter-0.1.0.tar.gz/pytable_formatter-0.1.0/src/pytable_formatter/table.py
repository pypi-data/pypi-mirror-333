"""
Table class for creating and rendering formatted tables.
"""
from typing import List, Optional, Union, Any
from .cell import Cell
from .enums import TextAlign, TextStyle, Color
from .utils import get_terminal_width


class Table:
    """Represents a formatted table with customizable styles and layouts."""

    def __init__(
        self,
        headers: Optional[List[Union[str, Cell]]] = None,
        data: Optional[List[List[Union[Any, Cell]]]] = None,
        title: Optional[str] = None,
        footer: Optional[str] = None,
        min_width: Optional[int] = None,
        max_width: Optional[int] = None,
        padding: int = 1,
        border_style: str = "│ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼ ─"
    ):
        """
        Initialize a table with headers, data, and styling options.

        Args:
            headers: List of column headers (strings or Cell objects)
            data: List of rows, each containing cells (values or Cell objects)
            title: Optional title to display above the table
            footer: Optional footer to display below the table
            min_width: Minimum width for the table (in characters)
            max_width: Maximum width for the table (in characters)
            padding: Number of spaces to add around cell content
            border_style: String containing border characters separated by spaces
        """
        self.title = title
        self.footer = footer
        self.min_width = min_width
        self.max_width = max_width or get_terminal_width()
        self.padding = padding
        self.border_chars = border_style.split(" ")

        # Process headers
        self.headers = []
        if headers:
            for header in headers:
                if isinstance(header, Cell):
                    self.headers.append(header)
                else:
                    self.headers.append(Cell(header, style=TextStyle.BOLD))

        # Process data
        self.rows = []
        if data:
            for row in data:
                processed_row = []
                for cell in row:
                    if isinstance(cell, Cell):
                        processed_row.append(cell)
                    else:
                        processed_row.append(Cell(cell))
                self.rows.append(processed_row)

    def add_row(self, row: List[Union[Any, Cell]]) -> None:
        """
        Add a row to the table.

        Args:
            row: List of values or Cell objects
        """
        processed_row = []
        for cell in row:
            if isinstance(cell, Cell):
                processed_row.append(cell)
            else:
                processed_row.append(Cell(cell))
        self.rows.append(processed_row)

    def _calculate_column_widths(self) -> List[int]:
        """
        Calculate the optimal width for each column based on content.

        Returns:
            List[int]: List of column widths
        """
        all_rows = [self.headers] + self.rows if self.headers else self.rows
        if not all_rows:
            return []

        # Get the maximum number of columns
        max_columns = max(len(row) for row in all_rows)

        # Initialize column widths with minimum width of 1
        col_widths = [1] * max_columns

        # Calculate width needed for each column
        for row in all_rows:
            for i, cell in enumerate(row):
                # Skip if beyond the maximum columns
                if i >= max_columns:
                    break

                # Get the string representation of the cell value
                content = str(cell.value)
                lines = content.split('\n')
                max_line_length = max(len(line) for line in lines)

                # Add padding to the width
                width_needed = max_line_length + (self.padding * 2)

                # Update column width if this cell requires more space
                if width_needed > col_widths[i]:
                    col_widths[i] = width_needed

        # Adjust column widths to fit within max_width
        total_width = sum(col_widths) + len(col_widths) + 1  # Include border chars
        if total_width > self.max_width:
            # Distribute the excess width proportionally
            excess = total_width - self.max_width
            for i in range(len(col_widths)):
                proportion = col_widths[i] / sum(col_widths)
                col_widths[i] = max(1, col_widths[i] - int(excess * proportion))

        return col_widths

    def _format_cell(self, cell: Cell, width: int) -> str:
        """
        Format a cell's content to fit the column width.

        Args:
            cell: The Cell object to format
            width: The column width to fit the cell content into

        Returns:
            str: The formatted cell content
        """
        content = str(cell.value)
        lines = content.split('\n')

        # Adjust for padding
        usable_width = width - (self.padding * 2)

        formatted_lines = []
        for line in lines:
            # Truncate if too long
            if len(line) > usable_width:
                line = line[:usable_width - 3] + "..."

            # Apply alignment
            if cell.align == TextAlign.RIGHT:
                line = line.rjust(usable_width)
            elif cell.align == TextAlign.CENTER:
                line = line.center(usable_width)
            else:  # LEFT or default
                line = line.ljust(usable_width)

            # Add padding
            padded_line = " " * self.padding + line + " " * self.padding
            formatted_lines.append(padded_line)

        return "\n".join(formatted_lines)

    def render(self) -> str:
        """
        Render the table as a string.

        Returns:
            str: The formatted table as a string
        """
        if not self.rows and not self.headers:
            return ""

        col_widths = self._calculate_column_widths()
        if not col_widths:
            return ""

        # Border characters
        v, tl, tr, bl, br, lm, rm, tm, bm, mm, h = self.border_chars

        # Calculate table width
        table_width = sum(col_widths) + len(col_widths) + 1

        # Build the table
        lines = []

        # Add title
        if self.title:
            title_line = f" {self.title} ".center(table_width - 2, h)
            lines.append(tl + title_line + tr)
        else:
            # Top border
            top_border = tl
            for i, width in enumerate(col_widths):
                top_border += h * width
                top_border += tm if i < len(col_widths) - 1 else tr
            lines.append(top_border)

        # Add headers
        if self.headers:
            header_line = v
            for i, (header, width) in enumerate(zip(self.headers, col_widths)):
                header_line += self._format_cell(header, width) + v
            lines.append(header_line)

            # Add separator after headers
            sep_line = lm
            for i, width in enumerate(col_widths):
                sep_line += h * width
                sep_line += mm if i < len(col_widths) - 1 else rm
            lines.append(sep_line)

        # Add data rows
        for row in self.rows:
            row_lines = []
            max_height = 1

            # Format each cell and determine the maximum height
            formatted_cells = []
            for i, cell in enumerate(row):
                if i < len(col_widths):
                    formatted = self._format_cell(cell, col_widths[i])
                    cell_height = formatted.count('\n') + 1
                    max_height = max(max_height, cell_height)
                    formatted_cells.append(formatted.split('\n'))

            # Create row lines with proper vertical alignment
            for j in range(max_height):
                line = v
                for i, cell_lines in enumerate(formatted_cells):
                    if j < len(cell_lines):
                        line += cell_lines[j] + v
                    else:
                        # Empty space for cells with fewer lines
                        line += " " * col_widths[i] + v
                row_lines.append(line)

            lines.extend(row_lines)

        # Add footer
        if self.footer:
            # Add separator before footer
            sep_line = lm
            for i, width in enumerate(col_widths):
                sep_line += h * width
                sep_line += mm if i < len(col_widths) - 1 else rm
            lines.append(sep_line)

            footer_line = f" {self.footer} ".center(table_width - 2, h)
            lines.append(bl + footer_line + br)
        else:
            # Bottom border
            bottom_border = bl
            for i, width in enumerate(col_widths):
                bottom_border += h * width
                bottom_border += bm if i < len(col_widths) - 1 else br
            lines.append(bottom_border)

        return "\n".join(lines)

    def __str__(self) -> str:
        """Return the rendered table."""
        return self.render()


def demo():
    """Demonstrate the capabilities of PyTable-Formatter."""
    # Create a simple table
    headers = ["Name", "Age", "Country", "Occupation"]

    data = [
        ["John Doe", 28, "United States", "Software Engineer"],
        ["Jane Smith", 34, "Canada", "Data Scientist"],
        ["Alice Johnson", 45, "United Kingdom", "Project Manager"],
        ["Bob Brown", 52, "Australia", "CEO"]
    ]

    # Create a styled table
    table = Table(
        headers=headers,
        data=data,
        title="Sample Personnel Data",
        footer="4 entries displayed",
        padding=1
    )

    print("\nSimple Table Example:")
    print(table)

    # Create a more advanced table with styling
    headers = [
        Cell("Product", style=TextStyle.BOLD, fg_color=Color.WHITE, bg_color=Color.BLUE, align=TextAlign.CENTER),
        Cell("Quantity", style=TextStyle.BOLD, fg_color=Color.WHITE, bg_color=Color.BLUE, align=TextAlign.CENTER),
        Cell("Price ($)", style=TextStyle.BOLD, fg_color=Color.WHITE, bg_color=Color.BLUE, align=TextAlign.CENTER),
        Cell("Total ($)", style=TextStyle.BOLD, fg_color=Color.WHITE, bg_color=Color.BLUE, align=TextAlign.CENTER)
    ]

    data = [
        [
            Cell("Laptop", fg_color=Color.CYAN),
            Cell(5, align=TextAlign.RIGHT),
            Cell(1200.00, align=TextAlign.RIGHT, formatter=lambda x: f"{x:,.2f}"),
            Cell(6000.00, align=TextAlign.RIGHT, fg_color=Color.GREEN, formatter=lambda x: f"{x:,.2f}")
        ],
        [
            Cell("Smartphone", fg_color=Color.CYAN),
            Cell(10, align=TextAlign.RIGHT),
            Cell(800.00, align=TextAlign.RIGHT, formatter=lambda x: f"{x:,.2f}"),
            Cell(8000.00, align=TextAlign.RIGHT, fg_color=Color.GREEN, formatter=lambda x: f"{x:,.2f}")
        ],
        [
            Cell("Monitor", fg_color=Color.CYAN),
            Cell(3, align=TextAlign.RIGHT),
            Cell(350.00, align=TextAlign.RIGHT, formatter=lambda x: f"{x:,.2f}"),
            Cell(1050.00, align=TextAlign.RIGHT, fg_color=Color.GREEN, formatter=lambda x: f"{x:,.2f}")
        ]
    ]

    styled_table = Table(
        headers=headers,
        data=data,
        title="Sales Report",
        footer="Total: $15,050.00",
        padding=1
    )

    print("\nStyled Table Example:")
    print(styled_table)

    # Example with a nested table
    nested_data = [
        [
            Cell("Department", style=TextStyle.BOLD),
            Cell("Quarterly Sales", style=TextStyle.BOLD)
        ],
        [
            "Electronics",
            Table(
                headers=["Q1", "Q2", "Q3", "Q4"],
                data=[
                    [15000, 17500, 16000, 19000]
                ],
                border_style="| + + + + + + + + + -"
            )
        ],
        [
            "Clothing",
            Table(
                headers=["Q1", "Q2", "Q3", "Q4"],
                data=[
                    [12000, 14500, 13000, 15000]
                ],
                border_style="| + + + + + + + + + -"
            )
        ]
    ]

    nested_table = Table(
        data=nested_data,
        title="Annual Sales Report by Department",
        padding=1
    )

    print("\nNested Table Example:")
    print(nested_table)


if __name__ == "__main__":
    demo()