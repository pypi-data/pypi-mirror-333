"""
AskUserTool

Purpose: Allows the agent to request additional input or clarification from the user.

How it works:
- Takes a question or prompt and presents it to the user
- Returns the user's response back to the agent
- Helps facilitate interactive dialogue when the agent needs more information

Example use cases:
- Clarifying ambiguous requirements
- Getting preferences or choices from the user
- Confirming whether to proceed with an action
- Requesting missing information needed to complete a task
"""

from typing import Type

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class AskUserInput(BaseModel):
    question: str = Field(
        ..., description="The question or prompt to present to the user"
    )


class AskUserTool(BaseTool):
    name: str = "ask_user"
    description: str = """
        Use this tool when you need additional input or clarification from the user.
        Present a clear question or prompt and the user will provide a response.
        Only use this when you cannot proceed without more information from the user.
    """
    args_schema: Type[BaseModel] = AskUserInput

    def _run(self, question: str) -> str:
        """Present the question to the user and return their response."""
        print("\nAgent Question:", question)
        response = input("Your response: ")
        return response
