"""
Authentication command parser and handler for the Sven CLI.
"""

import subprocess
import sys
from pathlib import Path
from typing import Any


def handle_auth(args: Any) -> int:
    """Handle the auth command by calling the standalone auth CLI script."""
    # Get the path to the auth_cli.py script
    script_path = Path(__file__).parent.parent.parent / "auth_cli.py"

    # Build the command
    cmd = [sys.executable, str(script_path), "--url", args.url]

    # Run the command
    result = subprocess.run(cmd)

    return result.returncode


def add_auth_parser(subparsers: Any) -> None:
    """Add the auth parser to the subparsers."""
    auth_parser = subparsers.add_parser(
        "auth",
        help="Authenticate with the server",
        description="Authenticate with the server to access the API",
    )

    auth_parser.add_argument(
        "--url",
        type=str,
        required=True,
        help="Base URL for the API",
    )
