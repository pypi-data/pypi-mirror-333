"""
Utility module for custom confirmation prompts.

This module provides a reusable confirmation component that can be used
across different tools to get user confirmation with additional options.
"""

from typing import Optional, Union

from rich.console import Console
from rich.prompt import Prompt

# Custom confirmation choices
CONFIRM_CHOICES = [
    "Yes",
    "Yes, and don't ask again this session",
    "No, and tell Claude what to do differently",
]


def custom_confirmation(
    prompt: str, console: Optional[Console] = None
) -> Union[bool, str]:
    """
    Display a custom confirmation prompt with Yes/No/Don't ask again options.

    Args:
        prompt: The prompt text to display
        console: Optional console to use for display

    Returns:
        True if user confirms, False if they deny, "always" if they select don't ask again
    """
    if console is None:
        console = Console()

    for i, choice in enumerate(CONFIRM_CHOICES, 1):
        console.print(f"[bold]{i}[/bold]. {choice}")

    # Ask for user input
    while True:
        response = Prompt.ask(f"{prompt} (1-3)", default="1")
        try:
            choice_num = int(response)
            if 1 <= choice_num <= len(CONFIRM_CHOICES):
                if choice_num == 1:  # Yes
                    return True
                elif choice_num == 2:  # Yes and don't ask again
                    return "always"
                else:  # No
                    return False
            else:
                console.print("[red]Invalid choice number. Please try again.[/red]")
        except ValueError:
            # Handle text responses like "yes" or "no"
            if response.lower() in ("y", "yes"):
                return True
            elif response.lower() in ("n", "no"):
                return False
            else:
                console.print(
                    "[red]Invalid input. Please enter a number 1-3, 'yes', or 'no'.[/red]"
                )
