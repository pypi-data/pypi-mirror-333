"""
Tools for the Sven CLI.
"""

from typing import Dict, List, Type

from langchain_core.tools import BaseTool

# Import tools
from sven.tools.ask_user_tool import AskUserTool
from sven.tools.file_edit_tool import FileEditTool
from sven.tools.file_read_tool import FileReadTool
from sven.tools.file_write_tool import FileWriteTool
from sven.tools.glob_tool import GlobTool
from sven.tools.grep_tool import GrepTool
from sven.tools.ls_tool import LSTool
from sven.tools.shell_tool import ShellTool

# Export tools
__all__ = [
    "AskUserTool",
    "FileEditTool",
    "FileReadTool",
    "FileWriteTool",
    "GlobTool",
    "GrepTool",
    "LSTool",
    "ShellTool",
]

# Tool registry
TOOLS: Dict[str, Type[BaseTool]] = {
    "ask_user": AskUserTool,
    "file_edit": FileEditTool,
    "file_read": FileReadTool,
    "file_write": FileWriteTool,
    "glob": GlobTool,
    "grep": GrepTool,
    "ls": LSTool,
    "shell": ShellTool,
}


def get_available_tools() -> List[str]:
    """Get a list of available tool names."""
    return list(TOOLS.keys())


def get_tool_by_name(name: str) -> Type[BaseTool]:
    """Get a tool class by name."""
    if name not in TOOLS:
        raise ValueError(f"Unknown tool: {name}")
    return TOOLS[name]
