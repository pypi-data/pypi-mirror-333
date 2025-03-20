"""
Environment loading utilities for EchoFire.
"""

import os


def load_environment():
    """
    Load environment variables from .env file if available.
    This function should be called at the start of the application.
    """
    try:
        from dotenv import load_dotenv, find_dotenv

        # Load environment variables from .env file if it exists
        load_dotenv(find_dotenv(usecwd=True))
        return True
    except ImportError:
        # python-dotenv is not installed, continue without it
        return False


def get_api_key(key_name="FIREWORKS_API_KEY"):
    """
    Get API key from environment variables.

    Args:
        key_name: The name of the environment variable containing the API key

    Returns:
        The API key if found

    Raises:
        ValueError: If the API key is not found
    """
    # Ensure environment variables are loaded
    load_environment()

    # Get API key from environment variable
    api_key = os.environ.get(key_name)
    if not api_key:
        raise ValueError(
            f"{key_name} environment variable must be set in the environment or in a .env file"
        )
    return api_key


def is_ci():
    """
    Check if the application is running in a CI environment.
    """
    return os.environ.get("CI") == "true"
