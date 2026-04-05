"""Configuration management for ReRoom.

Reads environment variables (with .env file support) and validates
that all required Azure credentials are present.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass

from dotenv import load_dotenv

# Load .env file if present
load_dotenv()

@dataclass(frozen=True)
class Config:
    """Immutable application configuration."""

    azure_ai_foundry_endpoint: str
    azure_ai_foundry_api_key: str
    azure_openai_endpoint: str
    azure_openai_api_key: str

    # Model names (can be overridden via env vars)
    analysis_model: str = "gpt-4o"
    image_model: str = "gpt-image-1"
    image_size: str = "1024x1024"
    image_quality: str = "high"

_REQUIRED_VARS = [
    "AZURE_AI_FOUNDRY_ENDPOINT",
    "AZURE_AI_FOUNDRY_API_KEY",
    "AZURE_OPENAI_ENDPOINT",
    "AZURE_OPENAI_API_KEY",
]

def load_config() -> Config:
    """Load and validate configuration from environment variables.

    Returns:
        A validated Config instance.

    Raises:
        SystemExit: If any required environment variable is missing.
    """
    missing = [var for var in _REQUIRED_VARS if not os.getenv(var)]
    if missing:
        print(
            f"ERROR: Missing required environment variables: {', '.join(missing)}\n"
            "Please copy .env.example to .env and fill in your Azure credentials.",
            file=sys.stderr,
        )
        sys.exit(1)

    return Config(
        azure_ai_foundry_endpoint=os.environ["AZURE_AI_FOUNDRY_ENDPOINT"],
        azure_ai_foundry_api_key=os.environ["AZURE_AI_FOUNDRY_API_KEY"],
        azure_openai_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_openai_api_key=os.environ["AZURE_OPENAI_API_KEY"],
        analysis_model=os.getenv("REROOM_ANALYSIS_MODEL", "gpt-4o"),
        image_model=os.getenv("REROOM_IMAGE_MODEL", "gpt-image-1"),
        image_size=os.getenv("REROOM_IMAGE_SIZE", "1024x1024"),
        image_quality=os.getenv("REROOM_IMAGE_QUALITY", "high"),
    )
