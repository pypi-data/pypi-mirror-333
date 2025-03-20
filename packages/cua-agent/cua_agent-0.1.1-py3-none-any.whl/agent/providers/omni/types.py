"""Type definitions for the Omni provider."""

from enum import StrEnum
from typing import Dict, Optional
from dataclasses import dataclass


class LLMProvider(StrEnum):
    """Supported LLM providers."""

    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    GROQ = "groq"
    QWEN = "qwen"


# For backward compatibility
APIProvider = LLMProvider


@dataclass
class LLM:
    """Configuration for LLM model and provider."""
    
    provider: LLMProvider
    name: Optional[str] = None
    
    def __post_init__(self):
        """Set default model name if not provided."""
        if self.name is None:
            self.name = PROVIDER_TO_DEFAULT_MODEL.get(self.provider)


# For backward compatibility
LLMModel = LLM
Model = LLM


# Default models for each provider
PROVIDER_TO_DEFAULT_MODEL: Dict[LLMProvider, str] = {
    LLMProvider.ANTHROPIC: "claude-3-7-sonnet-20250219",
    LLMProvider.OPENAI: "gpt-4o",
    LLMProvider.GROQ: "deepseek-r1-distill-llama-70b",
    LLMProvider.QWEN: "qwen2.5-vl-72b-instruct",
}

# Environment variable names for each provider
PROVIDER_TO_ENV_VAR: Dict[LLMProvider, str] = {
    LLMProvider.ANTHROPIC: "ANTHROPIC_API_KEY",
    LLMProvider.OPENAI: "OPENAI_API_KEY",
    LLMProvider.GROQ: "GROQ_API_KEY",
    LLMProvider.QWEN: "QWEN_API_KEY",
}
