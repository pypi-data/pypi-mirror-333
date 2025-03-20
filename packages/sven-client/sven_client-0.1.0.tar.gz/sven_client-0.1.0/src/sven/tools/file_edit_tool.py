"""
Tool for making targeted edits to files.

This tool provides functionality to make precise, single-instance text replacements in files.
It is designed for small, targeted edits where the exact text to be replaced can be uniquely
identified within the file.

Key features:
- Makes a single text replacement at a time
- Requires exact matching of text including whitespace
- Validates file paths and replacement uniqueness
- Provides diff preview of changes
- Works with any text file format except Jupyter notebooks

Usage notes:
- For moving/renaming files, use the Bash tool with 'mv' instead
- For larger edits, use the Write tool to overwrite files
- For Jupyter notebooks (.ipynb), use NotebookEditCell instead
- Always verify file contents and paths before editing
- Include sufficient context (3-5 lines) before and after edit points

"""

import difflib
import os
from typing import Type

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from sven.tools.util.confirmation import custom_confirmation


class FileEditToolInput(BaseModel):
    file_path: str = Field(..., description="The absolute path to the file to modify.")
    old_string: str = Field(
        ...,
        description="The text to replace (must be unique within the file and match exactly, including whitespace).",
    )
    new_string: str = Field(
        ..., description="The edited text to replace the old_string with."
    )


class FileEditTool(BaseTool):
    name: str = "file_edit"
    description: str = """
        This is a tool for editing files. For moving or renaming files, you should
        generally use the Bash tool with the 'mv' command instead. For larger edits, use
        the Write tool to overwrite files. For Jupyter notebooks (.ipynb files), use the
        NotebookEditCell instead.

        Before using this tool:

        1. Use the View tool to understand the file's contents and context

        2. Verify the directory path is correct (only applicable when creating new files):
        - Use the LS tool to verify the parent directory exists and is the correct location

        To make a file edit, provide the following:
        1. file_path: The absolute path to the file to modify (must be absolute, not relative)
        2. old_string: The text to replace (must be unique within the file, and must match the file contents exactly, including all whitespace and indentation)
        3. new_string: The edited text to replace the old_string

        The tool will replace ONE occurrence of old_string with new_string in the specified file.

        CRITICAL REQUIREMENTS FOR USING THIS TOOL:

        1. UNIQUENESS: The old_string MUST uniquely identify the specific instance you want to change. This means:
        - Include AT LEAST 3-5 lines of context BEFORE the change point
        - Include AT LEAST 3-5 lines of context AFTER the change point
        - Include all whitespace, indentation, and surrounding code exactly as it appears in the file

        2. SINGLE INSTANCE: This tool can only change ONE instance at a time. If you need to change multiple instances:
        - Make separate calls to this tool for each instance
        - Each call must uniquely identify its specific instance using extensive context

        3. VERIFICATION: Before using this tool:
        - Check how many instances of the target text exist in the file
        - If multiple instances exist, gather enough context to uniquely identify each one
        - Plan separate tool calls for each instance

        WARNING: If you do not follow these requirements:
        - The tool will fail if old_string matches multiple locations
        - The tool will fail if old_string doesn't match exactly (including whitespace)
        - You may change the wrong instance if you don't include enough context

        When making edits:
        - Ensure the edit results in idiomatic, correct code
        - Do not leave the code in a broken state
        - Always use absolute file paths (starting with /)

        If you want to create a new file, use:
        - A new file path, including dir name if needed
        - An empty old_string
        - The new file's contents as new_string
    """
    args_schema: Type[BaseModel] = FileEditToolInput

    def _create_diff_display(
        self, old_content: str, new_content: str, start_line: int = 1
    ) -> Panel:
        """
        Create a rich panel displaying the diff between old and new content with line numbers.

        Args:
            old_content: The original content
            new_content: The new content
            start_line: The starting line number for the diff (default: 1)

        Returns:
            A rich Panel containing the diff with color highlighting and line numbers
        """
        # Split content into lines if they aren't already lists
        if isinstance(old_content, str):
            old_lines = old_content.splitlines()
        else:
            old_lines = old_content

        if isinstance(new_content, str):
            new_lines = new_content.splitlines()
        else:
            new_lines = new_content

        # Generate the diff
        diff = difflib.SequenceMatcher(None, old_lines, new_lines)

        # Create a text object with colored diff lines and line numbers
        diff_text = Text()

        line_num = start_line

        # Process each diff block
        for tag, i1, i2, j1, j2 in diff.get_opcodes():
            if tag == "equal":
                # Lines are the same - regular display with line numbers
                for line_idx in range(i1, i2):
                    line_txt = f"{line_num:4d} | {old_lines[line_idx]}\n"
                    diff_text.append(line_txt)
                    line_num += 1

            elif tag == "replace":
                # Lines were replaced - show old lines (red) and new lines (green)
                for line_idx in range(i1, i2):
                    line_txt = f"{line_num:4d} | {old_lines[line_idx]}\n"
                    diff_text.append(line_txt, style="black on red")
                    line_num += 1

                # Reset line number for new lines (they're at the same position)
                temp_line_num = start_line + i1
                for line_idx in range(j1, j2):
                    line_txt = f"{temp_line_num:4d} | {new_lines[line_idx]}\n"
                    diff_text.append(line_txt, style="black on green")
                    temp_line_num += 1

            elif tag == "delete":
                # Lines were deleted - red background
                for line_idx in range(i1, i2):
                    line_txt = f"{line_num:4d} | {old_lines[line_idx]}\n"
                    diff_text.append(line_txt, style="black on red")
                    line_num += 1

            elif tag == "insert":
                # Lines were inserted - green background
                for line_idx in range(j1, j2):
                    line_txt = f"{line_num:4d} | {new_lines[line_idx]}\n"
                    diff_text.append(line_txt, style="black on green")
                    line_num += 1

        # Return a panel containing the styled diff
        return Panel(diff_text, title="File Changes", border_style="yellow")

    # Track if user has selected "don't ask again" option
    _always_confirm = False

    def _confirm_changes(self, diff_panel: Panel, file_path: str) -> bool:
        """
        Ask the user to confirm the changes.

        Args:
            diff_panel: The panel displaying the diff.
            file_path: The path to the file being modified.

        Returns:
            True if the user confirms, False otherwise.
        """
        if self.__class__._always_confirm:
            return True

        console = Console()
        console.print(Panel(f"Modifying file: {file_path}", border_style="blue"))
        console.print(diff_panel)

        # Use our custom prompt for confirmation
        prompt_text = f"Do you want to modify {os.path.basename(file_path)}?"

        result = custom_confirmation(prompt_text, console)

        # If user selected "Yes and don't ask again"
        if result == "always":
            self.__class__._always_confirm = True
            return True

        # Convert string result to boolean
        return result is True

    def _run(self, file_path: str, old_string: str, new_string: str) -> str:
        """
        Edit a file by replacing old_string with new_string.

        Args:
            file_path: The absolute path to the file to modify.
            old_string: The text to replace (must be unique within the file).
            new_string: The edited text to replace the old_string with.

        Returns:
            A message indicating success or failure.
        """
        console = Console()

        # Make file path absolute if it's not already
        if not os.path.isabs(file_path):
            file_path = os.path.abspath(file_path)

        # Handle new file creation
        if old_string == "" and not os.path.exists(file_path):
            try:
                # Ensure the directory exists
                directory = os.path.dirname(file_path)
                if not os.path.exists(directory):
                    os.makedirs(directory, exist_ok=True)

                # Use the same diff display mechanism as for editing
                empty_content = ""
                diff_panel = self._create_diff_display(empty_content, new_string)
                diff_panel.title = "New File Content"
                diff_panel.border_style = "green"

                console.print(
                    Panel(f"Creating new file: {file_path}", border_style="blue")
                )
                console.print(diff_panel)

                # Use our custom prompt for confirmation
                prompt_text = f"Do you want to create {os.path.basename(file_path)}?"

                result = custom_confirmation(prompt_text, console)

                # Handle "Yes and don't ask again" option
                if result == "always":
                    self.__class__._always_confirm = True
                    proceed = True
                else:
                    proceed = result is True

                if proceed:
                    # Create the new file
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_string)
                    return f"Successfully created new file: {file_path}"
                else:
                    return "File creation cancelled by user."
            except Exception as e:
                return f"Error creating file: {str(e)}"

        # Handle file editing
        if not os.path.exists(file_path):
            return f"Error: File not found: {file_path}"

        if not os.path.isfile(file_path):
            return f"Error: Not a file: {file_path}"

        try:
            # Read the file content
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            # Check if old_string exists in the file
            if old_string not in content:
                return "Error: The specified text was not found in the file."

            # Check if old_string appears multiple times
            occurrences = content.count(old_string)
            if occurrences > 1:
                return f"Error: The specified text appears {occurrences} times in the file. Please provide more context to uniquely identify the instance to change."

            # Find line number of the change for proper context
            start_line = 1
            if old_string in content:
                lines_before = content.split(old_string)[0]
                if lines_before:
                    start_line = lines_before.count("\n") + 1

            # Create a panel showing the full file diff
            new_content = content.replace(old_string, new_string, 1)
            diff_panel = self._create_diff_display(content, new_content, start_line)

            console.print(Panel(f"Editing file: {file_path}", border_style="blue"))
            console.print(diff_panel)

            # Show diff and ask for confirmation
            # if self._confirm_changes(diff_panel, file_path):
            if custom_confirmation("Would you like to make these edits?", console):
                # Write the modified content back to the file
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)

                return f"Successfully edited file: {file_path}"
            else:
                return "Edit cancelled by user."

        except UnicodeDecodeError:
            return (
                "Error: File is not a text file or contains invalid Unicode characters."
            )
        except Exception as e:
            return f"Error editing file: {str(e)}"

    async def _arun(self, file_path: str, old_string: str, new_string: str) -> str:
        """
        Async implementation of the edit file tool.

        This simply calls the synchronous implementation as the UI interactions
        are inherently synchronous.
        """
        return self._run(file_path, old_string, new_string)


# For backward compatibility with existing code and tests
FileEditTool = FileEditTool

# Alias for test_file_write.py
EditTool = FileEditTool
