"""
Purpose: Finds files by name patterns using glob syntax.

How it works:
- Supports glob patterns like **/*.js or src/**/*.ts.
- Returns matching file paths sorted by modification time.
- Allows for efficient file discovery based on name patterns.

Example use case:
When the agent needs to find all JavaScript files in a project, or all test
files matching a specific pattern.

Tool description for the model:
- Fast file pattern matching tool that works with any codebase size
- Supports glob patterns like "**/*.js" or "src/**/*.ts"
- Returns matching file paths sorted by modification time
- Use this tool when you need to find files by name patterns
- When you are doing an open ended search that may require multiple rounds of globbing and grepping, use the Agent tool instead
"""

import glob
import os
from typing import Type

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class GlobToolInput(BaseModel):
    pattern: str = Field(
        ...,
        description="The glob pattern to match files (e.g., '**/*.js', 'src/**/*.py').",
    )
    sort_by_modified: bool = Field(
        True, description="Whether to sort results by modification time (newest first)."
    )
    max_results: int = Field(100, description="Maximum number of results to return.")


class GlobTool(BaseTool):
    name: str = "glob"
    description: str = """
        - Fast file pattern matching tool that works with any codebase size
        - Supports glob patterns like "**/*.js" or "src/**/*.ts"
        - Returns matching file paths sorted by modification time
        - Use this tool when you need to find files by name patterns
        - When you are doing an open ended search that may require multiple rounds of globbing and grepping, use the Agent tool instead
    """
    args_schema: Type[BaseModel] = GlobToolInput

    def _run(
        self, pattern: str, sort_by_modified: bool = True, max_results: int = 100
    ) -> str:
        """Run the glob command with the specified pattern."""
        try:
            # Ensure the pattern is a string
            if not isinstance(pattern, str):
                return f"Error: Pattern must be a string, got {type(pattern)}"

            # Find all files matching the pattern
            try:
                matching_files = glob.glob(pattern, recursive=True)
            except Exception as e:
                return f"Error finding files with pattern '{pattern}': {str(e)}"

            # Filter out directories
            matching_files = [f for f in matching_files if os.path.isfile(f)]

            if not matching_files:
                return f"No files found matching pattern: {pattern}"

            # Get the total count before limiting
            total_count = len(matching_files)

            # Sort by modification time if requested
            if sort_by_modified:
                matching_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

            # Limit the number of results
            displayed_files = matching_files[:max_results]

            # Format the output
            result = f"Found {total_count} files matching pattern '{pattern}':\n\n"

            for file_path in displayed_files:
                # Get file size and modification time
                size = os.path.getsize(file_path)
                mod_time = os.path.getmtime(file_path)

                # Format size
                if size < 1024:
                    size_str = f"{size} bytes"
                elif size < 1024 * 1024:
                    size_str = f"{size / 1024:.1f} KB"
                else:
                    size_str = f"{size / (1024 * 1024):.1f} MB"

                # Format modification time
                from datetime import datetime

                mod_time_str = datetime.fromtimestamp(mod_time).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                result += f"{file_path} ({size_str}, modified: {mod_time_str})\n"

            return result

        except Exception as e:
            return f"Error finding files with pattern '{pattern}': {str(e)}"

    async def _arun(
        self, pattern: str, sort_by_modified: bool = True, max_results: int = 100
    ) -> str:
        """Run the glob command asynchronously."""
        return self._run(pattern, sort_by_modified, max_results)
