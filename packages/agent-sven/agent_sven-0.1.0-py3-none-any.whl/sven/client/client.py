"""
Command handler for the client that connects to the coder agent API.
"""

import argparse
import json
import os
import platform
import traceback
from pathlib import Path

import yaml
from langchain_core.load import dumpd, dumps
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from rich.console import Console
from rich.panel import Panel
from sven.client.api.client import ClientAPI
from sven.client.api.models import AgentCompletionRequest, Environment
from sven.client.components import MessageView
from sven.tools.ask_user_tool import AskUserTool
from sven.tools.file_edit_tool import FileEditTool
from sven.tools.file_read_tool import FileReadTool
from sven.tools.file_write_tool import FileWriteTool
from sven.tools.glob_tool import GlobTool
from sven.tools.grep_tool import GrepTool
from sven.tools.ls_tool import LSTool
from sven.tools.shell_tool import ShellTool


class SvenClient:
    def __init__(self, base_url: str, port: int):
        self.base_url = base_url
        self.port = port
        self.console = Console()
        self.working_directory = os.getcwd()
        self.model = "claude-3-7-sonnet-latest"
        self.persona = "default"

        # Try to load API key from config file
        api_key = None
        config_file = Path.home() / ".sven" / "config.json"
        if config_file.exists():
            try:
                with open(config_file) as f:
                    config = json.load(f)
                    api_key = config.get("api_key")
            except Exception as e:
                print(f"Error loading config: {str(e)}")

        # If API key is still not found, try environment variable
        if not api_key:
            api_key = os.getenv("SWE_API_KEY")

        self.client = ClientAPI(f"{base_url}:{port}", api_key)

        self.client_tools = [
            GlobTool(),
            GrepTool(),
            LSTool(),
            FileWriteTool(),
            FileEditTool(),
            FileReadTool(),
            ShellTool(),
            AskUserTool(),
        ]
        self.client_tools_by_name = {tool.name: tool for tool in self.client_tools}

        self.messages = []

    def load_messages_from_file(self, file_path: str):
        """Load messages from a YAML file containing human/AI message pairs."""

        with open(file_path) as f:
            data = yaml.safe_load(f)

            # Convert human/ai pairs to messages
            messages = []
            for k, v in data.items():
                if k == "human":
                    messages.append(HumanMessage(content=v))
                elif k == "ai":
                    messages.append(AIMessage(content=v))

            print(f"Loaded {len(messages)} messages from {file_path}")
            self.messages = messages

    def run(self, args: argparse.Namespace) -> int:
        """Run the client."""
        # Update instance variables from args
        if hasattr(args, "working_directory") and args.working_directory:
            self.working_directory = args.working_directory
        if hasattr(args, "model") and args.model:
            self.model = args.model
        if hasattr(args, "persona") and args.persona:
            self.persona = args.persona
        if hasattr(args, "messages") and args.messages:
            self.load_messages_from_file(args.messages)

        # Display welcome message
        self.console.print(
            Panel(
                f"[bold]Sven Agent Client[/bold]\n"
                f"Connecting to server at [cyan]{self.base_url}:{self.port}[/cyan]\n"
                f"Working directory: [cyan]{self.working_directory}[/cyan]\n"
                f"Model: [cyan]{self.model}[/cyan]\n"
                f"Persona: [cyan]{self.persona}[/cyan]",
                title="Welcome",
                border_style="green",
            )
        )

        self.console.print(
            "[bold]Type your messages below. Press Ctrl+C to exit.[/bold]"
        )

        def handle_command(user_message):
            command = user_message.strip().lower()
            if command in ["/exit", "/quit"]:
                raise KeyboardInterrupt()

            if command in ["/messages"]:
                with open("messages.txt", "w") as f:
                    f.write(dumps(self.messages))
                for message in self.messages:
                    self.console.print(MessageView(message))
                return 0

            if command in ["/clear"]:
                self.messages = []
                return 0

        def read_user_input():
            user_message = self.console.input("\n[bold blue]You:[/bold blue] ")

            if handle_command(user_message):
                return 0

            self.messages.append(HumanMessage(content=user_message))
            self.console.print(MessageView(self.messages[-1]))
            return 1

        def process_agent_messages(messages: list[BaseMessage]):
            for message in messages:
                self.console.print(MessageView(message, max_content_lines=4000))
                self.messages.append(message)

                if isinstance(message.content, list):
                    tool_id = 0
                    for content in message.content:
                        if isinstance(content, dict):
                            if content["type"] == "tool_use":
                                tool_call = message.tool_calls[tool_id]
                                self.execute_tool_locally(tool_call)
                                tool_id += 1

        def process_server_tool_messages(messages: list[BaseMessage]):
            for message in messages:
                self.messages.append(message)
                self.console.print(MessageView(message))

        def process_client_tool_messages(messages: list[BaseMessage]):
            for message in messages:
                self.messages.append(message)
                self.console.print(MessageView(message))

        def process_step(message):
            for source, data in message.items():
                if source == "agent":
                    process_agent_messages(data["messages"])
                elif source == "server_tools":
                    process_server_tool_messages(data["messages"])
                elif source == "client_tools":
                    process_client_tool_messages(data["messages"])
                else:
                    raise ValueError(f"Unknown source: {source}")

        try:
            while True:
                # Get user input
                if len(self.messages) == 0 or not isinstance(
                    self.messages[-1], ToolMessage
                ):
                    if not read_user_input():
                        continue

                # Send message and display streaming response
                for message_type, message in self.client.create_completion(
                    AgentCompletionRequest(
                        messages=[dumpd(message) for message in self.messages],
                        model=self.model,
                        persona=self.persona,
                        environment=Environment(
                            working_directory=self.working_directory,
                            platform=platform.system(),
                        ),
                    )
                ):
                    if message_type == "step":
                        process_step(message)
                    elif message_type == "status":
                        self.console.print(f"Status: {message}")
                    else:
                        raise ValueError(f"Unknown event type: {message_type}")

        except KeyboardInterrupt:
            self.console.print("\n[yellow]Session terminated by user[/yellow]")
        except Exception as e:
            traceback.print_exc()
            self.console.print(f"[bold red]Error during session: {str(e)}[/bold red]")
            return 1

        return 0

    def execute_tool_locally(self, tool_call):
        """Execute a tool locally and return the result."""
        tool_name = tool_call.get("name")
        tool_args = tool_call.get("args", {})
        tool_id = tool_call.get("id")

        self.console.print(f"\n[bold yellow]Tool call:[/bold yellow] {tool_name}")
        self.console.print(
            f"[yellow]Arguments:[/yellow] {json.dumps(tool_args, indent=2)}"
        )

        try:
            if tool_name in self.client_tools_by_name:
                tool = self.client_tools_by_name[tool_name]
                result = tool.invoke(tool_args)
                if not isinstance(result, str):
                    result = str(result)
                response = ToolMessage(
                    content=result,
                    name=tool_name,
                    tool_call_id=tool_id,
                )
                self.console.print(MessageView(response))
                self.messages.append(response)
        except Exception as e:
            response = ToolMessage(
                content=f"Error executing tool: {e}",
                name=tool_name,
                tool_call_id=tool_id,
            )
            self.console.print(MessageView(response))
            self.messages.append(response)
