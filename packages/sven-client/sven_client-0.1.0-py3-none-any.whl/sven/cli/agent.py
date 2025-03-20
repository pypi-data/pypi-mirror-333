"""
Agent command parser and handler for the Sven CLI.
"""

import argparse
from typing import Any


def handle_agent(args: argparse.Namespace) -> int:
    """Handle the agent command."""
    # Check if an agent type was specified
    if not hasattr(args, "agent_type") or not args.agent_type:
        print("Error: No agent type specified")
        return 1

    # In the client, we don't actually run the agent directly
    # Instead, we send a request to the server to run the agent
    print(f"Requesting server to run agent: {args.agent_type}")
    print(f"Using model: {args.model}")
    print("This functionality is handled by the client command.")
    print(
        "Please use 'aa client --persona {args.agent_type} --model {args.model}' instead."
    )

    return 0


def add_agent_parser(subparsers: Any) -> None:
    """Add the agent parser to the subparsers."""
    parser = subparsers.add_parser(
        "agent",
        help="Run various AI agents",
        description="Run various AI agents for specific tasks",
    )

    # Add subparsers for different agent types
    agent_subparsers = parser.add_subparsers(dest="agent_type", help="Agent types")

    # Add CEO agent parser
    agent_subparsers.add_parser(
        "ceo",
        help="Run the CEO Agent to help with educational entrepreneurship strategies",
        description="Run the CEO Agent to help with educational entrepreneurship strategies",
    )

    # Add the coder parser to the subparsers.
    agent_subparsers.add_parser(
        "coder",
        help="Start an interactive coder agent that responds to user tasks",
        description="Start an interactive coder agent that responds to user tasks",
    )

    # Add the blogger parser to the subparsers.
    agent_subparsers.add_parser(
        "blogger",
        help="Start an interactive blogger agent that helps with creating a blog post",
        description="Start an interactive blogger agent that helps with creating a blog post",
    )

    # Add the assistant parser to the subparsers.
    agent_subparsers.add_parser(
        "assistant",
        help="Start an interactive assistant agent that helps with creating a blog post",
        description="Start an interactive assistant agent that helps with creating a blog post",
    )

    # Add the info-entrepreneur parser to the subparsers.
    agent_subparsers.add_parser(
        "info-entrepreneur",
        help="Start an interactive info-entrepreneur agent that helps with creating a blog post",
        description="Start an interactive info-entrepreneur agent that helps with creating a blog post",
    )

    # Add model argument
    parser.add_argument(
        "--model",
        type=str,
        default="claude-3-7-sonnet-latest",
        help="The model to use for the agent (default: claude-3-7-sonnet-latest)",
    )

    return parser
