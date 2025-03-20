"""
Rich components for displaying messages in the terminal.
"""

import json

from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from rich.console import Console, ConsoleOptions, RenderResult
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table


class MessageView:
    """
    Rich component for displaying LangChain messages in the terminal.

    Supports various message types including HumanMessage, AIMessage, ToolMessage, etc.
    Ensures display is between 3-15 lines for readability.
    """

    def __init__(
        self, message: BaseMessage, max_content_lines: int = 10, max_width: int = 100
    ):
        """
        Initialize the message view.

        Args:
            message: The LangChain message to display
            max_content_lines: Maximum number of lines to show for content
            max_width: Maximum width for content display
        """
        self.message = message
        self.max_content_lines = max_content_lines
        self.max_width = max_width

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        """
        Render the message for Rich console output.
        """
        # Create a table for the message content
        table = Table(show_header=False, box=None, padding=(0, 1), expand=True)
        table.add_column("Content", ratio=1)

        # Get message type and style based on message class
        if isinstance(self.message, HumanMessage):
            title = "Human"
            style = "bold blue"
        elif isinstance(self.message, AIMessage):
            title = "AI"
            style = "bold green"
        elif isinstance(self.message, ToolMessage):
            title = (
                f"Tool: {self.message.name}"
                if hasattr(self.message, "name")
                else "Tool"
            )
            style = "bold yellow"
        elif isinstance(self.message, SystemMessage):
            title = "System"
            style = "bold magenta"
        else:
            title = self.message.__class__.__name__
            style = "bold"

        # Format the content based on message type
        if (
            isinstance(self.message, AIMessage)
            and hasattr(self.message, "content")
            and isinstance(self.message.content, list)
        ):
            # Handle structured content in AIMessage
            self._add_structured_content(table)
        elif isinstance(self.message, ToolMessage):
            # Handle tool message content
            self._add_tool_content(table)
        else:
            # Handle regular text content
            self._add_text_content(table)

        # Add metadata if available
        if (
            hasattr(self.message, "additional_kwargs")
            and self.message.additional_kwargs
        ):
            self._add_metadata_row(table)

        # Add tool calls if available (for AIMessage)
        if (
            isinstance(self.message, AIMessage)
            and hasattr(self.message, "tool_calls")
            and self.message.tool_calls
        ):
            self._add_tool_calls_row(table)

        # Create the panel with the table
        panel = Panel(
            table,
            title=title,
            title_align="left",
            border_style=style,
            padding=(0, 1),
        )

        yield panel

    def _add_structured_content(self, table: Table) -> None:
        """Add structured content from an AIMessage to the table."""
        for item in self.message.content[:3]:  # Limit to first 3 items for brevity
            if isinstance(item, dict):
                if item.get("type") == "text":
                    text = self._truncate_text(item.get("text", ""))
                    table.add_row(text)
                elif item.get("type") == "tool_use":
                    tool_name = item.get("name", "unknown")
                    tool_input = json.dumps(item.get("input", {}), indent=2)
                    tool_text = f"[bold]Tool Use:[/bold] {tool_name}\n"
                    tool_text += self._truncate_text(tool_input)
                    table.add_row(tool_text)
                else:
                    table.add_row(self._truncate_text(str(item)))
            else:
                table.add_row(self._truncate_text(str(item)))

        if len(self.message.content) > 3:
            table.add_row(
                f"[dim]...and {len(self.message.content) - 3} more items[/dim]"
            )

    def _add_tool_content(self, table: Table) -> None:
        """Add content from a ToolMessage to the table."""
        content = str(self.message.content)

        # Check if content is JSON or code-like
        if content.startswith("{") and content.endswith("}"):
            try:
                parsed = json.loads(content)
                content = json.dumps(parsed, indent=2)
                syntax = Syntax(content, "json", theme="monokai", line_numbers=False)
                table.add_row(syntax)
                return
            except json.JSONDecodeError:
                pass

        # Regular text content
        table.add_row(self._truncate_text(content))

        # Add tool call ID if available
        if hasattr(self.message, "tool_call_id") and self.message.tool_call_id:
            table.add_row(f"[dim]Tool Call ID: {self.message.tool_call_id}[/dim]")

    def _add_text_content(self, table: Table) -> None:
        """Add regular text content to the table."""
        if hasattr(self.message, "content"):
            content = str(self.message.content)
            table.add_row(self._truncate_text(content))
        else:
            table.add_row("[italic]No content[/italic]")

    def _add_metadata_row(self, table: Table) -> None:
        """Add metadata information to the table."""
        metadata = self.message.additional_kwargs

        # Create a compact representation of metadata
        metadata_items = []
        for key, value in list(metadata.items())[:3]:  # Limit to 3 items
            if isinstance(value, dict) and len(value) > 2:
                value = f"{{{len(value)} items}}"
            metadata_items.append(f"{key}: {value}")

        if metadata_items:
            metadata_text = "[dim]Metadata: " + ", ".join(metadata_items)
            if len(metadata) > 3:
                metadata_text += f" ...and {len(metadata) - 3} more[/dim]"
            else:
                metadata_text += "[/dim]"
            table.add_row(metadata_text)

    def _add_tool_calls_row(self, table: Table) -> None:
        """Add tool calls information to the table."""
        tool_calls = self.message.tool_calls

        if tool_calls:
            tool_calls_text = "[bold]Tool Calls:[/bold] "
            tool_names = [f"{tc.get('name', 'unknown')}" for tc in tool_calls[:2]]
            tool_calls_text += ", ".join(tool_names)

            if len(tool_calls) > 2:
                tool_calls_text += f" ...and {len(tool_calls) - 2} more"

            table.add_row(tool_calls_text)

    def _truncate_text(self, text: str) -> str:
        """Truncate text to fit within max_content_lines."""
        lines = text.split("\n")

        if len(lines) > self.max_content_lines:
            displayed_lines = lines[: self.max_content_lines - 1]
            displayed_lines.append(
                f"[dim]...and {len(lines) - self.max_content_lines + 1} more lines[/dim]"
            )
            return "\n".join(displayed_lines)

        return text
