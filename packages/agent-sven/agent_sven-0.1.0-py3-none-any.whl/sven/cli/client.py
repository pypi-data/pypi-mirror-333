"""
Client command parser and handler for the Sven CLI.
"""

import json
import time
from argparse import Namespace
from pathlib import Path
from typing import Any

import requests
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt
from sven.client.client import SvenClient


def add_client_parser(subparsers: Any) -> None:
    """Register the 'client' command with the argument parser."""
    parser = subparsers.add_parser("client", help="Connect to a coder agent API server")

    # Create subparsers for client subcommands
    client_subparsers = parser.add_subparsers(
        dest="client_command", help="Client subcommands"
    )

    # Register client subcommands
    add_register_parser(client_subparsers)
    add_login_parser(client_subparsers)

    # Add general client arguments
    parser.add_argument(
        "--url",
        type=str,
        default="https://api.swedishembedded.com",
        help="Base URL of the API server (default: https://api.swedishembedded.com)",
    )

    # Add port
    parser.add_argument(
        "--port",
        type=int,
        default=443,
        help="Port of the API server (default: 443)",
    )

    parser.add_argument(
        "--working-directory",
        type=str,
        help="Working directory for the agent (default: current directory)",
    )

    parser.add_argument(
        "--messages",
        type=str,
        help="Path to a YAML file containing human/AI message pairs",
    )

    parser.add_argument(
        "--model",
        type=str,
        default="claude-3-7-sonnet-latest",
        choices=[
            "claude-3-7-sonnet-latest",
            "claude-3-5-sonnet-latest",
            "claude-3-opus-latest",
            "claude-3-haiku-latest",
            "fake",
        ],
        help="Model to use (default: claude-3-7-sonnet-latest)",
    )

    parser.add_argument(
        "--persona",
        type=str,
        default="blogger",
        choices=[
            "blogger",
            "ceo",
            "coder",
            "assistant",
        ],
        help="Persona to use (default: coder)",
    )

    parser.set_defaults(command="client")


def add_register_parser(subparsers: Any) -> None:
    """Register the 'register' subcommand for the client command."""
    parser = subparsers.add_parser("register", help="Register a new user with email")

    parser.add_argument(
        "--email",
        type=str,
        required=True,
        help="Email address to register with",
    )

    parser.add_argument(
        "--url",
        type=str,
        required=True,
        help="Base URL of the API server (e.g., http://localhost:8000)",
    )


def add_login_parser(subparsers: Any) -> None:
    """Register the 'login' subcommand for the client command."""
    parser = subparsers.add_parser("login", help="Login with email")

    parser.add_argument(
        "--email",
        type=str,
        help="Email address to login with",
    )

    parser.add_argument(
        "--url",
        type=str,
        default="https://api.swedishembedded.com",
        help="Base URL of the API server (default: https://api.swedishembedded.com)",
    )


def handle_client(args: Namespace) -> int:
    """Handle the 'client' command to connect to the coder agent API."""
    # Check if a client subcommand was specified
    if hasattr(args, "client_command") and args.client_command:
        if args.client_command == "register":
            return handle_client_register(args)
        elif args.client_command == "login":
            return handle_client_login(args)

    # Default client behavior
    client = SvenClient(args.url, args.port)
    client.run(args)

    return 0


def handle_client_register(args: Namespace) -> int:
    """Handle the 'client register' command to register a new user."""
    console = Console()

    # Get the base URL and email from args
    base_url = args.url.rstrip("/")
    email = args.email

    # Make the registration request
    try:
        response = requests.post(
            f"{base_url}/auth/register", params={"email": email, "base_url": base_url}
        )

        if response.status_code == 201:
            console.print(
                Panel(
                    f"[green]Registration initiated![/green]\n\n"
                    f"A verification email has been sent to [bold]{email}[/bold].\n"
                    f"Please check your email and click the verification link to complete registration.",
                    title="Registration",
                )
            )
            return 0
        else:
            console.print(
                Panel(
                    f"[red]Registration failed![/red]\n\n"
                    f"Error: {response.json().get('detail', 'Unknown error')}",
                    title="Registration Error",
                )
            )
            return 1
    except Exception as e:
        console.print(
            Panel(
                f"[red]Registration failed![/red]\n\n" f"Error: {str(e)}",
                title="Registration Error",
            )
        )
        return 1


def handle_client_login(args: Namespace) -> int:
    """Handle the 'client login' command to login a user and get an API key."""
    console = Console()

    # Get the base URL from args
    base_url = args.url.rstrip("/")

    # If email is not provided, prompt for it
    email = args.email
    if not email:
        email = Prompt.ask("Enter your email address")

    # Make the login request
    try:
        response = requests.post(
            f"{base_url}/auth/login", params={"email": email, "base_url": base_url}
        )

        if response.status_code == 200:
            console.print(
                Panel(
                    f"[green]Login initiated![/green]\n\n"
                    f"A verification email has been sent to [bold]{email}[/bold].\n"
                    f"Please check your email and click the verification link.",
                    title="Login",
                )
            )

            # Ask if the user wants to wait for verification
            wait_for_verification = Prompt.ask(
                "Do you want to wait for email verification?",
                choices=["y", "n"],
                default="y",
            )

            if wait_for_verification.lower() == "y":
                # First, we need to get the verification token
                # This is a bit of a hack, but we'll prompt the user to enter the token from the URL
                console.print(
                    "\nAfter clicking the verification link, please copy the token from the URL."
                )
                console.print("The token is the part after '/auth/verify/' in the URL.")
                token = Prompt.ask("Enter the verification token")

                # Poll the server for verification status
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=console,
                ) as progress:
                    task = progress.add_task(
                        "Waiting for email verification...", total=None
                    )

                    # Now poll for verification status
                    max_attempts = 60  # 5 minutes (5 seconds * 60)
                    for _ in range(max_attempts):
                        try:
                            status_response = requests.get(
                                f"{base_url}/auth/verification-status/{token}"
                            )
                            status_data = status_response.json()

                            if status_data.get("verified", False):
                                # Verification successful, save the API key
                                api_key = status_data.get("api_key")
                                user_id = status_data.get("user_id")

                                if api_key:
                                    # Create config directory if it doesn't exist
                                    config_dir = Path.home() / ".sven"
                                    config_dir.mkdir(exist_ok=True)

                                    # Save API key to config file
                                    config_file = config_dir / "config.json"

                                    # Load existing config if it exists
                                    config = {}
                                    if config_file.exists():
                                        with open(config_file) as f:
                                            try:
                                                config = json.load(f)
                                            except json.JSONDecodeError:
                                                pass

                                    # Update config with new API key
                                    config["api_key"] = api_key
                                    config["user_id"] = user_id
                                    config["base_url"] = base_url

                                    # Save config
                                    with open(config_file, "w") as f:
                                        json.dump(config, f, indent=2)

                                    progress.update(task, completed=True)
                                    console.print(
                                        Panel(
                                            f"[green]Login successful![/green]\n\n"
                                            f"API key saved to [bold]{config_file}[/bold]",
                                            title="Login",
                                        )
                                    )
                                    return 0
                                else:
                                    progress.update(task, completed=True)
                                    console.print(
                                        Panel(
                                            "[red]Login failed![/red]\n\n"
                                            "No API key received from server.",
                                            title="Login Error",
                                        )
                                    )
                                    return 1

                            # Wait before polling again
                            time.sleep(5)
                        except Exception as e:
                            progress.update(task, completed=True)
                            console.print(
                                Panel(
                                    f"[red]Login failed![/red]\n\n" f"Error: {str(e)}",
                                    title="Login Error",
                                )
                            )
                            return 1

                    # If we get here, verification timed out
                    progress.update(task, completed=True)
                    console.print(
                        Panel(
                            "[red]Login verification timed out![/red]\n\n"
                            "Please try again later.",
                            title="Login Error",
                        )
                    )
                    return 1
            else:
                console.print(
                    Panel(
                        "[yellow]Login initiated but not verified.[/yellow]\n\n"
                        "Please check your email and click the verification link to complete login.",
                        title="Login",
                    )
                )
                return 0
        else:
            console.print(
                Panel(
                    f"[red]Login failed![/red]\n\n"
                    f"Error: {response.json().get('detail', 'Unknown error')}",
                    title="Login Error",
                )
            )
            return 1
    except Exception as e:
        console.print(
            Panel(
                f"[red]Login failed![/red]\n\n" f"Error: {str(e)}",
                title="Login Error",
            )
        )
        return 1
