import asyncio
import os
import sys
import re
from pathlib import Path
from typing import List, Literal, Optional
import importlib.metadata

import typer
from rich.console import Console

from echofire.core.interactive import start_interactive_session
from echofire.core.testing import execute_all_tests
from echofire.core.report import generate_html_report
from echofire.utils.config import (
    create_default_config,
    find_config_file,
    load_config,
)
from echofire.utils.env import load_environment

# Load environment variables at the start of the application
load_environment()

app = typer.Typer(
    name="echofire",
    help="EchoFire - Realistic Voice Agent Testing",
)

console = Console()


def version_callback(value: bool):
    """Print version and exit."""
    if value:
        try:
            # Get version from package metadata
            version = importlib.metadata.version("echofire")
            console.print(f"EchoFire v{version}")
        except importlib.metadata.PackageNotFoundError:
            console.print(
                "[red]Error: Package not installed. Please install the package or run from the project root.[/red]"
            )
        except Exception as e:
            console.print(f"[red]Error reading version: {e}[/red]")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        callback=version_callback,
        help="Show version and exit",
    ),
):
    """EchoFire CLI for testing voice agents."""
    pass


@app.command("init")
def init():
    """Initialize a new EchoFire project with a default configuration file."""

    # Check if config file already exists
    config_path = find_config_file()
    if config_path:
        console.print(f"[red]Configuration file already exists at {config_path}")
        console.print(
            "[yellow]Remove existing config file or use 'echofire talk' to start a session"
        )
        raise typer.Exit(1)

    create_default_config()

    # Create a sample system prompt file
    system_prompt_file = "system_prompt.txt"
    with open(system_prompt_file, "w") as f:
        f.write(
            """You are a helpful voice assistant. Your responses should be concise and conversational.
When speaking, use a natural tone and keep your responses brief but informative.
Avoid unnecessary verbosity and focus on providing clear, direct answers to the user's questions.
"""
        )
    console.print(f"[green]Created sample system prompt file at {system_prompt_file}")

    # Create a sample .env file
    env_file = Path(".env")
    if not env_file.exists():
        with open(env_file, "w") as f:
            f.write(
                """# API Keys and Configuration for EchoFire
# Uncomment and add your keys/settings below

# FIREWORKS_API_KEY=your-fireworks-api-key
# WEBSOCKET_URL=ws://localhost:8000/ws
"""
            )
        console.print(f"[green]Created sample .env file at {env_file}")

    # Create a .gitignore file
    gitignore_file = Path(".gitignore")
    if not gitignore_file.exists():
        with open(gitignore_file, "w") as f:
            f.write(
                """# Ignore environment variables
.env

# macOS
.DS_Store
"""
            )
        console.print(f"[green]Created .gitignore file at {gitignore_file}")

    console.print("[green]Initialized EchoFire project")


@app.command("talk")
def talk(
    websocket_url: str = typer.Option(
        None, "--url", "-u", help="WebSocket URL for the voice agent"
    ),
    config_file: str = typer.Option(
        None, "--config", "-c", help="Path to configuration file"
    ),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug output"),
    sample_rate: int = typer.Option(
        None, "--sample-rate", "-sr", help="Sample rate for audio capture"
    ),
    mode: str = typer.Option(
        "interactive",
        "--mode",
        "-m",
        help="Display mode: 'raw' prints JSON structures directly, 'interactive' renders them as a conversation (choices: raw, interactive; default: raw)",
    ),
    channels: int = typer.Option(
        None, "--channels", "-ch", help="Number of audio channels"
    ),
    device: Optional[int] = typer.Option(
        None, "--device", "-dev", help="Audio device to use"
    ),
    save_test: Optional[str] = typer.Option(
        None,
        "--save-test",
        "-st",
        help="Save audio chunks as a test with the specified name in the tests directory",
    ),
    system_prompt_file: Optional[str] = typer.Option(
        None,
        "--system-prompt-file",
        "-spf",
        help="Path to a file containing the system prompt to send to the LLM",
    ),
):
    """Start an interactive conversation with the voice agent."""

    # Load configuration
    config, config_path = load_config(
        websocket_url,
        Path(config_file) if config_file else None,
        raise_if_not_found=True,
        debug=debug,
    )

    if sample_rate:
        config.sample_rate = sample_rate
    if channels:
        config.channels = channels

    # Run the interactive session
    try:
        asyncio.run(
            start_interactive_session(
                config=config,
                mode=mode,
                device=device,
                save_test=save_test,
                config_path=config_path,
            )
        )
    except KeyboardInterrupt:
        console.print("[yellow]Interrupted by user")
    except Exception as e:
        console.print(f"[red]Error: {e}")
        if config.debug:
            import traceback

            console.print(traceback.format_exc())
        sys.exit(1)


@app.command("test")
def test(
    tests_dir: str = typer.Option(
        None, "--tests-dir", "-d", help="Directory containing test directories"
    ),
    websocket_url: str = typer.Option(
        None, "--url", "-u", help="WebSocket URL for the voice agent"
    ),
    config_file: str = typer.Option(
        None, "--config", "-c", help="Path to configuration file"
    ),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug output"),
    pause_ms: int = typer.Option(
        None, "--pause", "-p", help="Pause between audio files in milliseconds"
    ),
    play_audio: bool = typer.Option(
        None, "--play", "-a", help="Play audio files while streaming"
    ),
    output_dir: str = typer.Option(
        None, "--output", "-o", help="Directory to save results in"
    ),
    repeat: int = typer.Option(
        5, "--repeat", "-n", help="Number of times to repeat each test"
    ),
    test_name: str = typer.Option(
        None, "--test", "-t", help="Run a single test by name"
    ),
    system_prompt: str = typer.Option(
        None, "--system-prompt", "-sp", help="System prompt to send to the LLM"
    ),
    system_prompt_file: str = typer.Option(
        None,
        "--system-prompt-file",
        "-spf",
        help="Path to a file containing the system prompt to send to the LLM",
    ),
):
    """Run all tests in a directory."""

    # Load configuration
    config, _ = load_config(
        websocket_url,
        Path(config_file) if config_file else None,
        raise_if_not_found=True,
        debug=debug,
    )

    if pause_ms is not None:
        config.pause_ms = pause_ms
    if play_audio is not None:
        config.play_audio = play_audio
    if output_dir:
        config.output_dir = output_dir
    if system_prompt:
        config.system_prompt = system_prompt
    if system_prompt_file:
        config.system_prompt_file = system_prompt_file

    # Use the tests_dir from config if not specified
    if not tests_dir:
        tests_dir = config.tests_dir

    # Run all tests
    asyncio.run(
        execute_all_tests(
            config=config,
            tests_dir=tests_dir,
            repeat=repeat,
            test_name=test_name,
        )
    )


@app.command("report")
def report(
    csv_file: str = typer.Option(
        None, "--csv", "-c", help="Path to the CSV file containing test results"
    ),
    output_file: str = typer.Option(
        None, "--output", "-o", help="Path where the HTML report will be saved"
    ),
    tests_dir: str = typer.Option(
        None, "--tests-dir", "-d", help="Directory containing test directories"
    ),
    config_file: str = typer.Option(
        None, "--config", "-cf", help="Path to configuration file"
    ),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug output"),
):
    """Generate an HTML report from test results CSV file."""

    # Load configuration
    config, _ = load_config(
        None,
        Path(config_file) if config_file else None,
        raise_if_not_found=True,
        raise_if_websocket_url_not_set=False,
        debug=debug,
    )

    # Use the tests_dir from config if not specified
    if not tests_dir:
        tests_dir = config.tests_dir

    # Default CSV file path if not specified
    if not csv_file:
        csv_file = os.path.join(tests_dir, "test-runs.csv")

    # Default output file path if not specified
    if not output_file:
        output_file = os.path.join(tests_dir, "test-report.html")

    # Generate the HTML report
    generated_path = generate_html_report(csv_file, output_file)

    if generated_path:
        console.print(
            f"[green]Report generated successfully at: [bold]{generated_path}[/bold]"
        )
        # Try to open the report in the default browser, but only if not in CI environment
        is_ci = (
            os.environ.get("CI") == "true" or os.environ.get("GITHUB_ACTIONS") == "true"
        )
        if not is_ci:
            try:
                import typer

                typer.launch(f"file://{os.path.abspath(generated_path)}")
                console.print("[green]Report opened in your default browser.[/green]")
            except Exception as e:
                console.print(
                    f"[yellow]Could not open the report automatically: {str(e)}[/yellow]"
                )
                console.print(
                    f"[yellow]Please open it manually at: {os.path.abspath(generated_path)}[/yellow]"
                )
        else:
            console.print(
                "[yellow]Running in CI environment, not opening browser.[/yellow]"
            )
    else:
        console.print("[red]Failed to generate report.[/red]")
        sys.exit(1)


if __name__ == "__main__":
    app()
