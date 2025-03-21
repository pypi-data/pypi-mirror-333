"""CUA (Computer Use) Agent for AI-driven computer interaction."""

__version__ = "0.1.0"

from .core.factory import AgentFactory
from .core.agent import ComputerAgent
from .providers.omni.types import LLMProvider, LLM
from .types.base import Provider, AgentLoop

__all__ = ["AgentFactory", "Provider", "ComputerAgent", "AgentLoop", "LLMProvider", "LLM"]
