"""
Purpose: Searches file contents using regular expressions.

How it works:
- Searches through file contents using regular expression patterns.
- Can be filtered to specific file types using the include parameter.
- Returns matching files sorted by modification time.
- Respects .gitignore patterns to exclude files from search.

Example use case:
When the agent needs to find where a specific function is defined, or where a
particular string or pattern appears in the codebase.

Tool description for the model:
- Fast content search tool that works with any codebase size
- Searches file contents using regular expressions
- Supports full regex syntax (eg. "log.*Error", "function\\s+\\w+", etc.)
- Filter files by pattern with the include parameter (eg. "*.js", "*.{ts,tsx}")
- Returns matching file paths sorted by modification time
- Respects .gitignore patterns to exclude files from search
- Use this tool when you need to find files containing specific patterns
- When you are doing an open ended search that may require multiple rounds of globbing and grepping, use the Agent tool instead
"""

import fnmatch
import glob
import os
import re
from datetime import datetime
from typing import List, Type

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class GrepToolInput(BaseModel):
    pattern: str = Field(
        ..., description="The regex pattern to search for in file contents."
    )
    include: str = Field(
        "**/*",
        description="Glob pattern to filter which files to search (e.g., '**/*.js', 'src/**/*.py').",
    )
    case_sensitive: bool = Field(
        False, description="Whether the search should be case sensitive."
    )
    max_results: int = Field(50, description="Maximum number of results to return.")
    max_matches_per_file: int = Field(
        5, description="Maximum number of matches to show per file."
    )
    respect_gitignore: bool = Field(
        True, description="Whether to respect .gitignore patterns."
    )


class GrepTool(BaseTool):
    name: str = "grep"
    description: str = """
        - Fast content search tool that works with any codebase size
        - Searches file contents using regular expressions
        - Supports full regex syntax (eg. "log.*Error", "function\\s+\\w+", etc.)
        - Filter files by pattern with the include parameter (eg. "*.js", "*.{ts,tsx}")
        - Returns matching file paths sorted by modification time
        - Respects .gitignore patterns to exclude files from search
        - Use this tool when you need to find files containing specific patterns
        - When you are doing an open ended search that may require multiple rounds of globbing and grepping, use the Agent tool instead
    """
    args_schema: Type[BaseModel] = GrepToolInput

    def __init__(self) -> None:
        super().__init__()
        self._gitignore_patterns = self._load_gitignore_patterns()

    def _load_gitignore_patterns(self) -> List[str]:
        """Load patterns from .gitignore files."""
        patterns = []

        # Start with the root .gitignore
        gitignore_path = os.path.join(os.getcwd(), ".gitignore")
        if os.path.exists(gitignore_path):
            with open(gitignore_path, encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comments
                    if line and not line.startswith("#"):
                        # Normalize patterns
                        if line.startswith("/"):
                            line = line[1:]
                        if line.endswith("/"):
                            line = line + "**"
                        patterns.append(line)

        return patterns

    def _is_ignored(self, file_path: str) -> bool:
        """Check if a file should be ignored based on .gitignore patterns."""
        if not self._gitignore_patterns:
            return False

        # Convert to relative path from current working directory
        rel_path = os.path.relpath(file_path, os.getcwd())

        # Normalize path separators
        rel_path = rel_path.replace(os.sep, "/")

        for pattern in self._gitignore_patterns:
            # Handle directory patterns
            if pattern.endswith("**"):
                if fnmatch.fnmatch(rel_path + "/", pattern):
                    return True
            # Handle standard patterns
            elif fnmatch.fnmatch(rel_path, pattern):
                return True
            # Handle patterns that should match at any level
            elif "/" not in pattern and fnmatch.fnmatch(
                os.path.basename(rel_path), pattern
            ):
                return True

        return False

    def _run(
        self,
        pattern: str,
        include: str = "**/*",
        case_sensitive: bool = False,
        max_results: int = 50,
        max_matches_per_file: int = 5,
        respect_gitignore: bool = True,
    ) -> str:
        """Run the grep command with the specified pattern."""
        try:
            # Ensure the pattern is a string
            if not isinstance(pattern, str):
                return f"Error: Pattern must be a string, got {type(pattern)}"

            # Compile the regex pattern
            try:
                if case_sensitive:
                    regex = re.compile(pattern)
                else:
                    regex = re.compile(pattern, re.IGNORECASE)
            except re.error as e:
                return f"Error compiling regex pattern '{pattern}': {str(e)}"

            # Find all files matching the include pattern
            try:
                matching_files = glob.glob(include, recursive=True)
            except Exception as e:
                return f"Error finding files with pattern '{include}': {str(e)}"

            # Filter out directories
            matching_files = [f for f in matching_files if os.path.isfile(f)]

            # Filter out files that match .gitignore patterns if requested
            if respect_gitignore:
                matching_files = [f for f in matching_files if not self._is_ignored(f)]

            if not matching_files:
                return f"No files found matching pattern: {include}"

            # Sort by modification time (newest first)
            matching_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

            # Search for the pattern in each file
            results = []
            total_matches = 0

            for file_path in matching_files:
                try:
                    with open(file_path, encoding="utf-8", errors="replace") as f:
                        content = f.read()

                    # Find all matches in the file
                    file_matches = []
                    lines = content.splitlines()
                    for i, line in enumerate(lines, 1):
                        match = regex.search(line)
                        if match:
                            # Get match and surrounding context
                            match_start = match.start()
                            match_end = match.end()

                            # Calculate the match length
                            match_length = match_end - match_start

                            # Calculate how much context we can include (total 80 chars max)
                            available_context = 80 - match_length
                            context_before = min(20, available_context // 2)
                            context_after = min(20, available_context - context_before)

                            # Adjust context boundaries
                            context_start = max(0, match_start - context_before)
                            context_end = min(len(line), match_end + context_after)

                            # If we still have room, expand context evenly
                            total_length = context_end - context_start
                            if total_length < 80:
                                extra_space = 80 - total_length
                                extra_before = min(context_start, extra_space // 2)
                                extra_after = min(
                                    len(line) - context_end, extra_space - extra_before
                                )
                                context_start -= extra_before
                                context_end += extra_after

                            # Extract context with match
                            context = line[context_start:context_end]
                            if context_start > 0:
                                context = "..." + context
                            if context_end < len(line):
                                context += "..."

                            # Ensure final context is no more than 80 chars
                            if len(context) > 80:
                                context = context[:77] + "..."

                            file_matches.append((i, context))
                            if len(file_matches) >= max_matches_per_file:
                                break

                    if file_matches:
                        results.append((file_path, file_matches))
                        total_matches += len(file_matches)

                        # Stop if we've reached the maximum number of results
                        if len(results) >= max_results:
                            break
                except Exception:
                    # Skip files that can't be read
                    continue
            # Format the output
            if not results:
                return f"No matches found for pattern '{pattern}' in files matching '{include}'"

            output = f"Found {total_matches} matches for pattern '{pattern}' in {len(results)} files:\n\n"

            for file_path, matches in results:
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
                mod_time_str = datetime.fromtimestamp(mod_time).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                output += f"{file_path} ({size_str}, modified: {mod_time_str}):\n"

                for line_num, line_content in matches:
                    output += f"  Line {line_num}: {line_content}\n"

                output += "\n"

            return output

        except Exception as e:
            return f"Error searching for pattern '{pattern}': {str(e)}"

    async def _arun(
        self,
        pattern: str,
        include: str = "**/*",
        case_sensitive: bool = False,
        max_results: int = 50,
        max_matches_per_file: int = 5,
        respect_gitignore: bool = True,
    ) -> str:
        """Run the grep command asynchronously."""
        return self._run(
            pattern,
            include,
            case_sensitive,
            max_results,
            max_matches_per_file,
            respect_gitignore,
        )
