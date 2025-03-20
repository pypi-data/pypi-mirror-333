"""
Purpose: Reads file content from the filesystem.

How it works:
- Takes an absolute file path and optional offset/limit parameters.
- Returns the content of the file, with special handling for images and large files.
- Can display a subset of a file by specifying line ranges.

Example use case:
When the agent needs to understand the current content of a file before making
changes, or to examine specific parts of large files.

Tool description for the model:
Reads a file from the local filesystem. The file_path parameter must be an
absolute path, not a relative path. By default, it reads up to 2000 lines
starting from the beginning of the file. You can optionally specify a line
offset and limit (especially handy for long files), but it's recommended to read
the whole file by not providing these parameters. Any lines longer than 2000
characters will be truncated. For image files, the tool will display the image
for you. For Jupyter notebooks (.ipynb files), use the ReadNotebook instead.
"""

import base64
import mimetypes
import os
from typing import Type

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from rich.console import Console
from rich.panel import Panel
from rich.text import Text


class FileReadToolInput(BaseModel):
    file_path: str = Field(..., description="The absolute path to the file to read.")
    line_offset: int = Field(
        0, description="Line number to start reading from (0-indexed)."
    )
    line_limit: int = Field(2000, description="Maximum number of lines to read.")


class FileReadTool(BaseTool):
    name: str = "file_read"
    description: str = """
        When the agent needs to understand the current content of a file before making
        changes, or to examine specific parts of large files.

        Tool description for the model:
        Reads a file from the local filesystem. The file_path parameter must be an
        absolute path, not a relative path. By default, it reads up to 2000 lines
        starting from the beginning of the file. You can optionally specify a line
        offset and limit (especially handy for long files), but it's recommended to read
        the whole file by not providing these parameters. Any lines longer than 2000
        characters will be truncated. For image files, the tool will display the image
        for you. For Jupyter notebooks (.ipynb files), use the ReadNotebook instead.
    """
    args_schema: Type[BaseModel] = FileReadToolInput

    def _run(self, file_path: str, line_offset: int = 0, line_limit: int = 2000) -> str:
        """
        Read a file from the filesystem.
        """
        if not os.path.isabs(file_path):
            return f"Error: file_path must be an absolute path, got: {file_path}"

        if not os.path.exists(file_path):
            return f"Error: File not found: {file_path}"

        if not os.path.isfile(file_path):
            return f"Error: Not a file: {file_path}"

        # Create rich console
        console = Console()
        preview_text = ""

        # Get file preview (first 3 lines)
        try:
            with open(file_path, encoding="utf-8") as f:
                preview_lines = []
                for _ in range(3):
                    line = f.readline().strip()
                    if line:
                        preview_lines.append(line)
                preview_text = "\n".join(preview_lines)
        except Exception as e:
            preview_text = (
                f"[italic red]Unable to preview file contents: {str(e)}[/italic red]"
            )

        # Create and display the header panel
        panel_text = Text.from_markup(
            f"[bold blue]File Path:[/bold blue] {file_path}\n\n[bold green]Preview:[/bold green]\n{preview_text}"
        )
        console.print(Panel(panel_text, title="View File", border_style="blue"))

        # Check if it's an image file
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type and mime_type.startswith("image/"):
            try:
                with open(file_path, "rb") as f:
                    image_data = f.read()
                base64_data = base64.b64encode(image_data).decode("utf-8")
                return f"data:{mime_type};base64,{base64_data}"
            except Exception as e:
                return f"Error reading image file: {str(e)}"

        # Handle text files
        try:
            with open(file_path, encoding="utf-8") as f:
                # Skip lines if offset is provided
                for _ in range(line_offset):
                    if not f.readline():
                        break

                # Read the specified number of lines
                lines = []
                for _ in range(line_limit):
                    line = f.readline()
                    if not line:
                        break
                    # Truncate long lines
                    if len(line) > 2000:
                        line = line[:2000] + "... [truncated]"
                    lines.append(line)

                content = "".join(lines)

                # If we reached the line limit, add a note
                if f.readline():
                    content += f"\n... [truncated, showing {line_limit} lines starting from line {line_offset}]"

                return content
        except UnicodeDecodeError:
            return (
                "Error: File is not a text file or contains invalid Unicode characters."
            )
        except Exception as e:
            return f"Error reading file: {str(e)}"

    async def _arun(
        self, file_path: str, line_offset: int = 0, line_limit: int = 2000
    ) -> str:
        """Async implementation of the tool."""
        return self._run(file_path, line_offset, line_limit)
