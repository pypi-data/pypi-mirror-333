import json
import os
from pathlib import Path
from typing import Optional, Tuple

import yaml
from rich.console import Console

from echofire.models.config_model import EchoFireConfig

console = Console()


def find_config_file(directory: str = None) -> Optional[Path]:
    """
    Find a configuration file in the specified directory.

    Args:
        directory: Directory to search in, defaults to current directory

    Returns:
        Path to the configuration file, or None if not found
    """
    search_dir = Path(directory or os.getcwd())

    # Look for config files in the following order
    config_files = [
        "echofire.yaml",
        "echofire.yml",
        "echofire.json",
        ".echofire.yaml",
        ".echofire.yml",
        ".echofire.json",
    ]

    for config_file in config_files:
        config_path = search_dir / config_file
        if config_path.exists():
            return config_path

    return None


def load_config(
    config_path: Optional[Path] = None, raise_if_not_found: bool = False
) -> Tuple[EchoFireConfig, Path]:
    """
    Load configuration from a file.

    Args:
        config_path: Path to the configuration file, or None to search
        raise_if_not_found: If True, raise an error when config file is not found

    Returns:
        Tuple of (Configuration object, Path to the config file)

    Notes:
        - If the WEBSOCKET_URL environment variable is set, it will override the websocket_url in the config file
        - Environment variables in the format {VAR_NAME} in the websocket_url will be replaced with their values
    """
    # Find the config file if not specified
    if not config_path:
        config_path = find_config_file()

    # If still not found, return default config or raise error
    if not config_path:
        if raise_if_not_found:
            raise FileNotFoundError("No configuration file found")
        console.print("[yellow]No configuration file found, using defaults")
        return EchoFireConfig(), Path(os.getcwd())

    # Load the config file
    try:
        with open(config_path, "r") as f:
            if config_path.suffix.lower() in [".yaml", ".yml"]:
                config_dict = yaml.safe_load(f)
            else:
                config_dict = json.load(f)

        # Validate with Pydantic model
        config = EchoFireConfig(**config_dict)

        if config.system_prompt is None and config.system_prompt_file is not None:
            with open(config.system_prompt_file, "r") as f:
                config.system_prompt = f.read()

        if config.system_prompt is None:
            # set a default system prompt
            config.system_prompt = "You are a helpful assistant."

        # Check for WEBSOCKET_URL environment variable and use it if available
        websocket_url_env = os.environ.get("WEBSOCKET_URL")
        if websocket_url_env:
            # Save the original websocket URL from environment variable
            config.original_websocket_url = websocket_url_env
            config.websocket_url = websocket_url_env
            if config.debug:
                console.print(
                    "[green]Using websocket URL from WEBSOCKET_URL environment variable"
                )
        else:
            # Save the original websocket URL from config file
            config.original_websocket_url = config.websocket_url

        # if websocket_url is not set, raise an error
        if config.websocket_url is None:
            raise ValueError("websocket_url is not set")

        console.print(f"[green]Loaded configuration from {config_path}")
        return config, config_path
    except Exception as e:
        console.print(f"[red]Error loading configuration: {e}")
        console.print("[yellow]Using default configuration")
        return EchoFireConfig(), config_path


def create_default_config():
    """
    Create a default configuration file.

    Args:
        output_path: Path to write the configuration file to
    """
    default_config = EchoFireConfig().model_dump()

    try:
        with open("echofire.yaml", "w") as f:
            yaml.dump(default_config, f, default_flow_style=False)

        console.print(f"[green]Created default configuration at echofire.yaml")
    except Exception as e:
        console.print(f"[red]Error creating default configuration: {e}")
