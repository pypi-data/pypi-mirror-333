from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator, model_validator
import os


class EchoFireConfig(BaseModel):
    """Pydantic model for EchoFire configuration."""

    websocket_url: Optional[str] = Field(
        default=None,
        description="WebSocket URL for the server connection. Can be overridden with the WEBSOCKET_URL environment variable, and takes highest precedence when set via --url flag where available.",
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
    if not s:
        return s
    for env_var in s.split("{"):
        if "}" in env_var:
            var_name = env_var.split("}")[0]
            if var_name in os.environ:
                s = s.replace(f"{{{var_name}}}", os.environ[var_name])
    return s
