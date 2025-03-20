"""
LSTool

Purpose: Lists files and directories in a given path.

How it works:
- Takes an absolute path and returns a list of files and directories.
- Helps the agent explore the codebase structure.
- Particularly useful when the agent needs to understand what files are available.

Example use case:
When agent needs to verify that a directory exists before creating a file in it,
or to understand the overall structure of a project.

Tool description for the model:
Lists files and directories in a given path. The path parameter must be an
absolute path, not a relative path. You should generally prefer the Glob and
Grep tools, if you know which directories to search.
"""

import os
from typing import Type

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class LSToolInput(BaseModel):
    path: str = Field(
        ..., description="The absolute path to list files and directories from."
    )


class LSTool(BaseTool):
    name: str = "ls"
    description: str = """
        Lists files and directories in a given path. The path parameter must be an
        absolute path, not a relative path. You should generally prefer the Glob and
        Grep tools, if you know which directories to search.
    """
    args_schema: Type[BaseModel] = LSToolInput

    def _run(self, path: str) -> str:
        """Run the ls command on the specified path."""
        try:
            if not os.path.isabs(path):
                return f"Error: '{path}' is not an absolute path. Please provide an absolute path."

            if not os.path.exists(path):
                return f"Error: Path '{path}' does not exist."

            if os.path.isfile(path):
                return f"Error: '{path}' is a file, not a directory."

            items = os.listdir(path)

            # Categorize items as files or directories
            files = []
            directories = []

            for item in items:
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    directories.append(f"{item}/")
                else:
                    files.append(item)

            # Sort alphabetically
            directories.sort()
            files.sort()

            # Format the output
            result = f"Contents of {path}:\n"

            if directories:
                result += "\nDirectories:\n"
                result += "\n".join(directories)

            if files:
                result += "\n\nFiles:\n"
                result += "\n".join(files)

            return result

        except Exception as e:
            return f"Error listing directory contents: {str(e)}"

    async def _arun(self, path: str) -> str:
        """Run the ls command asynchronously."""
        return self._run(path)
