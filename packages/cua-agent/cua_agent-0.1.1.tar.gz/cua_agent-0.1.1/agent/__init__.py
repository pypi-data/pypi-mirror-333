"""CUA (Computer Use) Agent for AI-driven computer interaction."""

__version__ = "0.1.0"

from .core.factory import AgentFactory
from .core.agent import ComputerAgent
from .types.base import Provider, AgenticLoop
from .providers.omni.types import LLMProvider, LLM, Model, LLMModel, APIProvider

__all__ = ["AgentFactory", "Provider", "ComputerAgent", "AgenticLoop", "LLMProvider", "LLM", "Model", "LLMModel", "APIProvider"]
