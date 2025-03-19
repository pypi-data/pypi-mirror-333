from typing import Optional
from pydantic import BaseModel, Field, field_validator
import os


class EchoFireConfig(BaseModel):
    """Pydantic model for EchoFire configuration."""

    websocket_url: str = Field(
        default="ws://localhost:8000/ws",
        description="WebSocket URL for the server connection. Can be overridden with the WEBSOCKET_URL environment variable.",
    )

    pause_ms: int = Field(
        default=100, description="Pause duration in milliseconds", ge=0
    )

    play_audio: bool = Field(default=False, description="Whether to play audio")

    sample_rate: int = Field(default=16000, description="Audio sample rate in Hz", gt=0)

    channels: int = Field(default=1, description="Number of audio channels", gt=0)

    debug: bool = Field(default=False, description="Enable debug mode")

    tests_dir: str = Field(
        default="tests", description="Directory containing test files"
    )

    output_dir: str = Field(default="results", description="Directory for output files")

    system_prompt: Optional[str] = Field(
        default=None, description="System prompt for the LLM"
    )

    system_prompt_file: Optional[str] = Field(
        default="system_prompt.txt",
        description="File containing the system prompt for the LLM",
    )

    original_websocket_url: Optional[str] = Field(
        default=None, description="Original websocket URL from config file"
    )

    @field_validator("websocket_url", mode="before")
    def store_original_url(cls, v, info):
        """Store the original websocket URL before any modifications."""
        if (
            "original_websocket_url" not in info.data
            or info.data["original_websocket_url"] is None
        ):
            info.data["original_websocket_url"] = v
        # Check if the websocket_url contains environment variable placeholders
        # and replace them with their values
        if v and isinstance(v, str) and "{" in v and "}" in v:
            v = populate_template_variables_for_string(v)
        return v

    @field_validator("tests_dir", "output_dir")
    def validate_directory(cls, v):
        """Validate that directory paths are valid."""
        if not v:
            raise ValueError("Directory path cannot be empty")
        return v

    class Config:
        """Pydantic model configuration."""

        extra = "forbid"  # Prevent extra fields
        validate_assignment = True  # Validate values when assigned
        json_schema_extra = {
            "examples": [
                {
                    "websocket_url": "ws://localhost:8000/ws",
                    "pause_ms": 100,
                    "play_audio": False,
                    "sample_rate": 16000,
                    "channels": 1,
                    "debug": False,
                    "tests_dir": "tests",
                    "output_dir": "results",
                    "system_prompt_file": "system_prompt.txt",
                }
            ]
        }


def populate_template_variables_for_string(s: str) -> str:
    """
    Populate template variables in a string with their values from the environment.
    """
    for env_var in s.split("{"):
        if "}" in env_var:
            var_name = env_var.split("}")[0]
            if var_name in os.environ:
                s = s.replace(f"{{{var_name}}}", os.environ[var_name])
    return s
