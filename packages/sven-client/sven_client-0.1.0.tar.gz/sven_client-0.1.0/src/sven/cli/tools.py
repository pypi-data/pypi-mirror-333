"""
Tool command parser and handler for the Sven CLI.
"""

import json
from argparse import Namespace
from typing import Any

from rich.console import Console
from rich.table import Table


def add_tool_parser(subparsers: Any) -> None:
    """Add the tool command parser to the subparsers."""
    tool_parser = subparsers.add_parser("tools", help="Tool operations")
    tool_subparsers = tool_parser.add_subparsers(
        dest="tool_command", help="Tool commands"
    )

    # Add list command
    list_parser = tool_subparsers.add_parser("list", help="List available tools")
    list_parser.add_argument(
        "--format",
        choices=["table", "json"],
        default="table",
        help="Output format (default: table)",
    )


def handle_tool(args: Namespace) -> int:
    """Handle the tool command."""
    if not hasattr(args, "tool_command") or not args.tool_command:
        print("Error: No tool command specified")
        print("Available commands: list")
        return 1

    if args.tool_command == "list":
        return handle_tool_list(args)

    print(f"Error: Unknown tool command: {args.tool_command}")
    return 1


def handle_tool_list(args: Namespace) -> int:
    """Handle the tool list command."""
    # Define the available tools
    tools = [
        {
            "name": "file_read",
            "description": "Read the contents of a file",
            "category": "File Operations",
        },
        {
            "name": "file_write",
            "description": "Write content to a file",
            "category": "File Operations",
        },
        {
            "name": "file_edit",
            "description": "Edit the contents of a file",
            "category": "File Operations",
        },
        {
            "name": "glob",
            "description": "Find files matching a pattern",
            "category": "File Operations",
        },
        {
            "name": "grep",
            "description": "Search for patterns in files",
            "category": "File Operations",
        },
        {
            "name": "ls",
            "description": "List directory contents",
            "category": "File Operations",
        },
        {
            "name": "shell",
            "description": "Execute shell commands",
            "category": "System Operations",
        },
        {
            "name": "ask_user",
            "description": "Ask the user for input",
            "category": "User Interaction",
        },
    ]

    # Output in the requested format
    if args.format == "json":
        print(json.dumps(tools, indent=2))
    else:  # table format
        console = Console()
        table = Table(title="Available Tools")
        table.add_column("Name", style="cyan")
        table.add_column("Category", style="green")
        table.add_column("Description")

        for tool in tools:
            table.add_row(tool["name"], tool["category"], tool["description"])

        console.print(table)

    return 0
