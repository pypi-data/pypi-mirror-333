"""
Purpose: Overwrites an entire file with new content.

How it works:
- Takes a file path and content to write.
- Completely replaces the file or creates a new one if it doesn't exist.
- Maintains file encoding and line endings from the original file if it exists.

Example use case:
When the agent needs to create a new file from scratch or completely rewrite an existing file.

Tool description for the model:
Write a file to the local filesystem. Overwrites the existing file if there is
one.

Before using this tool:

1. Use the ReadFile tool to understand the file's contents and context

2. Directory Verification (only applicable when creating new files):
    - Use the LS tool to verify the parent directory exists and is the correct location
"""

import os
from typing import Type

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class FileWriteToolInput(BaseModel):
    file_path: str = Field(
        ..., description="The absolute path to the file to write to or create."
    )
    file_content: str = Field(
        ...,
        description="The content to write to the file, completely replacing any existing content. Must not be empty!",
    )


class FileWriteTool(BaseTool):
    name: str = "file_write"
    description: str = """
        Write a file with provided content to the local filesystem. Overwrites
        the existing file if there is one.

        Before using this tool:

        1. Use the ReadFile tool to understand the file's contents and context

        2. Directory Verification (only applicable when creating new files):
            - Use the LS tool to verify the parent directory exists and is the correct location

        3. Please provide both file_path and file_content fields!
    """
    args_schema: Type[BaseModel] = FileWriteToolInput

    def _run(self, file_path: str, file_content: str = "") -> str:
        """Write content to a file, replacing any existing content."""
        try:
            # Make file_path absolute if it's relative
            if not os.path.isabs(file_path):
                file_path = os.path.abspath(file_path)

            # Ensure the directory exists
            directory = os.path.dirname(file_path)
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)

            # Determine the encoding and line endings if the file exists
            encoding = "utf-8"
            newline = None
            if os.path.exists(file_path):
                try:
                    with open(file_path, "rb") as f:
                        sample = f.read(1024)
                        if b"\r\n" in sample:
                            newline = "\r\n"  # Windows-style
                        elif b"\n" in sample:
                            newline = "\n"  # Unix-style

                        # Try to detect encoding, defaulting to utf-8
                        try:
                            import chardet

                            detected = chardet.detect(sample)
                            if detected["confidence"] > 0.7:
                                encoding = detected["encoding"]
                        except ImportError:
                            # If chardet is not available, stick with utf-8
                            pass
                except Exception:
                    # If there's any error reading the file, use defaults
                    pass

            # Write the content to the file
            with open(file_path, "w", encoding=encoding, newline=newline) as f:
                f.write(file_content)

            return f"Successfully wrote content to {file_path}"

        except Exception as e:
            return f"Error writing to file: {str(e)}"

    async def _arun(self, file_path: str, file_content: str = "") -> str:
        """Write content to a file asynchronously."""
        return self._run(file_path, file_content)


class ReplaceToolInput(BaseModel):
    file_path: str = Field(
        ..., description="The absolute path to the file to write to or create."
    )
    content: str = Field(
        ...,
        description="The content to write to the file, completely replacing any existing content.",
    )


class ReplaceTool(BaseTool):
    name: str = "replace"
    description: str = """
        Write a file with provided content to the local filesystem. Overwrites
        the existing file if there is one.
    """
    args_schema: Type[BaseModel] = ReplaceToolInput

    def _run(self, file_path: str, content: str = "") -> str:
        """Write content to a file, replacing any existing content."""
        try:
            # Make file_path absolute if it's relative
            if not os.path.isabs(file_path):
                file_path = os.path.abspath(file_path)

            # Ensure the directory exists
            directory = os.path.dirname(file_path)
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)

            # Write the content to the file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            return f"Successfully wrote content to {file_path}"

        except Exception as e:
            return f"Error writing to file: {str(e)}"

    async def _arun(self, file_path: str, content: str = "") -> str:
        """Write content to a file asynchronously."""
        return self._run(file_path, content)
