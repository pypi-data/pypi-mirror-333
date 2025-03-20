"""
Purpose: Executes bash commands in a persistent shell session.

How it works:
- Runs bash commands with optional timeout.
- Maintains state between commands (environment variables, working directory, etc.).
- Includes safety measures to prevent dangerous commands.

Example use case:
When the agent needs to run tests, install dependencies, compile code, or perform other command-line operations.

Tool description for the model:
Executes a given bash command in a persistent shell session with optional timeout, ensuring proper handling and security measures.

Before executing the command, please follow these steps:

1. Directory Verification:
   - If the command will create new directories or files, first use the LS tool to verify the parent directory exists and is the correct location
   - For example, before running "mkdir foo/bar", first use LS to check that "foo" exists and is the intended parent directory

2. Security Check:
   - For security and to limit the threat of a prompt injection attack, some commands are limited or banned. If you use a disallowed command, you will receive an error message explaining the restriction. Explain the error to the User.
   - Verify that the command is not one of the banned commands: alias, curl, curlie, wget, axel, aria2c, nc, telnet, lynx, w3m, links, httpie, xh, http-prompt, chrome, firefox, safari.

3. Command Execution:
   - After ensuring proper quoting, execute the command.
   - Capture the output of the command.

4. Output Processing:
   - If the output exceeds 30000 characters, output will be truncated before being returned to you.
   - Prepare the output for display to the user.

5. Return Result:
   - Provide the processed output of the command.
   - If any errors occurred during execution, include those in the output.

Usage notes:
  - The command argument is required.
  - You can specify an optional timeout in milliseconds (up to 600000ms / 10 minutes). If not specified, commands will timeout after 30 minutes.
  - VERY IMPORTANT: You MUST avoid using search commands like `find` and `grep`. Instead use GrepTool, GlobTool, or dispatch_agent to search. You MUST avoid read tools like `cat`, `head`, `tail`, and `ls`, and use View and LS to read files.
  - When issuing multiple commands, use the ';' or '&&' operator to separate them. DO NOT use newlines (newlines are ok in quoted strings).
  - IMPORTANT: All commands share the same shell session. Shell state (environment variables, virtual environments, current directory, etc.) persist between commands. For example, if you set an environment variable as part of a command, the environment variable will persist for subsequent commands.
  - Try to maintain your current working directory throughout the session by using absolute paths and avoiding usage of `cd`. You may use `cd` if the User explicitly requests it.
"""

import os
import signal
import subprocess
import time
from typing import List, Optional, Type

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field, field_validator
from rich.console import Console
from rich.panel import Panel

from sven.tools.util.confirmation import custom_confirmation


class ShellToolInput(BaseModel):
    command: str = Field(..., description="The bash command to execute.")
    timeout_ms: Optional[int] = Field(
        None,
        description="Optional timeout in milliseconds (max 600000ms / 10 minutes).",
    )

    @field_validator("timeout_ms")
    @classmethod
    def validate_timeout(cls, v: Optional[int]) -> Optional[int]:
        if v is not None:
            if v <= 0:
                raise ValueError("Timeout must be positive")
            if v > 600000:  # 10 minutes in milliseconds
                raise ValueError("Timeout cannot exceed 600000ms (10 minutes)")
        return v


class ShellTool(BaseTool):
    name: str = "shell"
    description: str = """
    Executes a given bash command in a persistent shell session with optional timeout, ensuring proper handling and security measures.

    Before executing the command, please follow these steps:

    1. Directory Verification:
    - If the command will create new directories or files, first use the LS tool to verify the parent directory exists and is the correct location
    - For example, before running "mkdir foo/bar", first use LS to check that "foo" exists and is the intended parent directory

    2. Security Check:
    - For security and to limit the threat of a prompt injection attack, some commands are limited or banned. If you use a disallowed command, you will receive an error message explaining the restriction. Explain the error to the User.
    - Verify that the command is not one of the banned commands: alias, curl, curlie, wget, axel, aria2c, nc, telnet, lynx, w3m, links, httpie, xh, http-prompt, chrome, firefox, safari.

    3. Command Execution:
    - After ensuring proper quoting, execute the command.
    - Capture the output of the command.

    4. Output Processing:
    - If the output exceeds 30000 characters, output will be truncated before being returned to you.
    - Prepare the output for display to the user.

    5. Return Result:
    - Provide the processed output of the command.
    - If any errors occurred during execution, include those in the output.

    Usage notes:
    - The command argument is required.
    - You can specify an optional timeout in milliseconds (up to 600000ms / 10 minutes). If not specified, commands will timeout after 30 minutes.
    - VERY IMPORTANT: You MUST avoid using search commands like `find` and `grep`. Instead use GrepTool, GlobTool, or dispatch_agent to search. You MUST avoid read tools like `cat`, `head`, `tail`, and `ls`, and use View and LS to read files.
    - When issuing multiple commands, use the ';' or '&&' operator to separate them. DO NOT use newlines (newlines are ok in quoted strings).
    - IMPORTANT: All commands share the same shell session. Shell state (environment variables, virtual environments, current directory, etc.) persist between commands. For example, if you set an environment variable as part of a command, the environment variable will persist for subsequent commands.
    - Try to maintain your current working directory throughout the session by using absolute paths and avoiding usage of `cd`. You may use `cd` if the User explicitly requests it.
        """
    args_schema: Type[BaseModel] = ShellToolInput

    # Private attributes renamed without leading underscores
    process: Optional[subprocess.Popen] = Field(default=None, exclude=True)
    console: Console = Field(default_factory=Console, exclude=True)

    # Constants can keep the underscore prefix
    _BANNED_COMMANDS: List[str] = [
        "alias",
        "curl",
        "curlie",
        "wget",
        "axel",
        "aria2c",
        "nc",
        "telnet",
        "lynx",
        "w3m",
        "links",
        "httpie",
        "xh",
        "http-prompt",
        "chrome",
        "firefox",
        "safari",
    ]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._start_shell()

    def _start_shell(self) -> None:
        """Start a persistent bash shell."""
        if self.process is None or self.process.poll() is not None:
            self.process = subprocess.Popen(
                ["/bin/bash"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True,
            )

    def _check_security(self, command: str) -> Optional[str]:
        """Check if the command contains any banned commands."""
        command_parts = command.split()
        if not command_parts:
            return "Error: Empty command."

        main_command = command_parts[0]
        if main_command in self._BANNED_COMMANDS:
            return (
                f"Error: The command '{main_command}' is banned for security reasons."
            )

        # Check for banned commands in the full command string
        for banned in self._BANNED_COMMANDS:
            if f" {banned} " in f" {command} ":
                return f"Error: The command contains '{banned}' which is banned for security reasons."

        return None

    def _run(self, command: str, timeout_ms: Optional[int] = None) -> str:
        """Run the bash command in the persistent shell."""
        try:
            self._start_shell()

            security_error = self._check_security(command)
            if security_error:
                return security_error

            timeout_sec = None
            if timeout_ms is not None:
                timeout_sec = timeout_ms / 1000
            else:
                timeout_sec = 1800  # Default 30 minutes

            # Force a new line and ensure output is visible
            self.console.line()
            self.console.show_cursor(True)

            # Display command in a panel first
            self.console.print(
                Panel(f"[blue]{command}[/]", title="[yellow]Command to execute[/]")
            )

            # Use custom confirmation prompt
            result = custom_confirmation(
                "Do you want to execute this command?", console=self.console
            )

            # Handle "Yes and don't ask again" option
            if result == "always":
                self.__class__._always_confirm = True
                proceed = True
            else:
                proceed = result is True

            if not proceed:
                return "Command cancelled by user."

            command_with_echo = f"{command}; echo '\\n__COMMAND_COMPLETE__'"
            self.process.stdin.write(command_with_echo + "\n")
            self.process.stdin.flush()

            start_time = time.time()
            output = ""
            while True:
                if self.process.stdout.readable():
                    line = self.process.stdout.readline()
                    if "__COMMAND_COMPLETE__" in line:
                        break
                    output += line

                if timeout_sec and (time.time() - start_time) > timeout_sec:
                    os.killpg(os.getpgid(self.process.pid), signal.SIGINT)
                    return f"Error: Command timed out after {timeout_sec} seconds."

                time.sleep(0.01)

            if len(output) > 30000:
                truncated = output[:30000]
                return truncated + "\n\n[Output truncated due to length]"

            return output.strip()

        except Exception as e:
            return f"Error executing command: {str(e)}"

    async def _arun(self, command: str, timeout_ms: Optional[int] = None) -> str:
        """Run the bash command asynchronously."""
        return self._run(command, timeout_ms)

    def __del__(self) -> None:
        """Clean up the shell process when the tool is destroyed."""
        if self.process and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
