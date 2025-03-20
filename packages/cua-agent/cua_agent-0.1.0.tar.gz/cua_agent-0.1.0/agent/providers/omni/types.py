"""Type definitions for the Omni provider."""

from enum import StrEnum
from typing import Dict


class APIProvider(StrEnum):
    """Supported API providers."""

    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    GROQ = "groq"
    QWEN = "qwen"


# Default models for each provider
PROVIDER_TO_DEFAULT_MODEL: Dict[APIProvider, str] = {
    APIProvider.ANTHROPIC: "claude-3-7-sonnet-20250219",
    APIProvider.OPENAI: "gpt-4o",
    APIProvider.GROQ: "deepseek-r1-distill-llama-70b",
    APIProvider.QWEN: "qwen2.5-vl-72b-instruct",
}

# Environment variable names for each provider
PROVIDER_TO_ENV_VAR: Dict[APIProvider, str] = {
    APIProvider.ANTHROPIC: "ANTHROPIC_API_KEY",
    APIProvider.OPENAI: "OPENAI_API_KEY",
    APIProvider.GROQ: "GROQ_API_KEY",
    APIProvider.QWEN: "QWEN_API_KEY",
}
