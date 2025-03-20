#!/usr/bin/env python3
"""
Sven CLI - A command line utility for agent automation.
"""

import argparse
import logging
import sys
import warnings
from typing import List, Optional

import langchain
from dotenv import load_dotenv
from sven.cli.agent import add_agent_parser, handle_agent
from sven.cli.auth import add_auth_parser, handle_auth
from sven.cli.client import add_client_parser, handle_client
from sven.cli.tools import add_tool_parser, handle_tool

# Configure logging
logging.basicConfig(level=logging.ERROR)

# Suppress specific loggers
for logger_name in ["httpx", "httpcore", "langchain", "langchain_core"]:
    logging.getLogger(logger_name).setLevel(logging.ERROR)

# Suppress LangChain beta warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Ensure langchain debugging is disabled
langchain.debug = False

load_dotenv()


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the application."""
    if args is None:
        args = sys.argv[1:]

    # Create the main parser with all subparsers
    parser = create_main_parser()

    # Parse arguments
    parsed_args = parser.parse_args(args)

    # Handle version command
    if hasattr(parsed_args, "version") and parsed_args.version:
        from sven import __version__

        print(f"Sven version {__version__}")
        return 0

    # If no command was specified, show help
    if not hasattr(parsed_args, "command") or not parsed_args.command:
        parser.print_help()
        return 1

    # Import the command handler
    if parsed_args.command == "tools":
        return handle_tool(parsed_args)
    elif parsed_args.command == "client":
        return handle_client(parsed_args)
    elif parsed_args.command == "agent":
        return handle_agent(parsed_args)
    elif parsed_args.command == "auth":
        return handle_auth(parsed_args)
    else:
        parser.print_help()
        return 1


class DotNotationArgumentParser(argparse.ArgumentParser):
    """Custom argument parser that supports dot notation for commands."""

    def parse_args(self, args=None, namespace=None):
        # Check for dot notation in the first argument
        if args and len(args) > 0 and "." in args[0] and not args[0].startswith("-"):
            # Split the dot notation into parts
            parts = args[0].split(".")

            # Replace the dot notation with separate arguments
            new_args = parts + args[1:]
            return super().parse_args(new_args, namespace)

        return super().parse_args(args, namespace)


def create_main_parser() -> DotNotationArgumentParser:
    """Create the main parser with all subparsers."""
    parser = DotNotationArgumentParser(
        prog="aa",
        description="Sven CLI - A command line utility for agent automation.",
    )

    # Add version argument
    parser.add_argument(
        "--version", action="store_true", help="Show version information and exit"
    )

    # Add subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Add parsers for each command
    add_tool_parser(subparsers)
    add_agent_parser(subparsers)
    add_client_parser(subparsers)
    add_auth_parser(subparsers)

    return parser


if __name__ == "__main__":
    sys.exit(main())
