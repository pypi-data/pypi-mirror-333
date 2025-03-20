"""Unified computer agent implementation that supports multiple loops."""

import os
import logging
import asyncio
from typing import Any, AsyncGenerator, Dict, List, Optional, TYPE_CHECKING, Union, cast
from datetime import datetime

from computer import Computer

from ..types.base import Provider, AgenticLoop
from .base_agent import BaseComputerAgent

# Only import types for type checking to avoid circular imports
if TYPE_CHECKING:
    from ..providers.anthropic.loop import AnthropicLoop
    from ..providers.omni.loop import OmniLoop
    from ..providers.omni.parser import OmniParser

# Import the provider types
from ..providers.omni.types import LLMProvider, LLM, Model, LLMModel, APIProvider

logger = logging.getLogger(__name__)

# Default models for different providers
DEFAULT_MODELS = {
    LLMProvider.OPENAI: "gpt-4o",
    LLMProvider.ANTHROPIC: "claude-3-7-sonnet-20250219",
    LLMProvider.GROQ: "llama3-70b-8192",
}

# Map providers to their environment variable names
ENV_VARS = {
    LLMProvider.OPENAI: "OPENAI_API_KEY",
    LLMProvider.GROQ: "GROQ_API_KEY",
    LLMProvider.ANTHROPIC: "ANTHROPIC_API_KEY",
}


class ComputerAgent(BaseComputerAgent):
    """Unified implementation of the computer agent supporting multiple loop types.

    This class consolidates the previous AnthropicComputerAgent and OmniComputerAgent
    into a single implementation with configurable loop type.
    """

    def __init__(
        self,
        computer: Computer,
        loop_type: AgenticLoop = AgenticLoop.OMNI,
        model: Optional[Union[LLM, Dict[str, str], str]] = None,
        api_key: Optional[str] = None,
        save_trajectory: bool = True,
        trajectory_dir: Optional[str] = "trajectories",
        only_n_most_recent_images: Optional[int] = None,
        max_retries: int = 3,
        verbosity: int = logging.INFO,
        **kwargs,
    ):
        """Initialize the computer agent.

        Args:
            computer: Computer instance to control
            loop_type: The type of loop to use (Anthropic or Omni)
            model: LLM configuration. Can be:
                  - LLM object with provider and name
                  - Dict with 'provider' and 'name' keys
                  - String with model name (defaults to OpenAI provider)
                  - None (defaults based on loop_type)
            api_key: Optional API key (will use environment variable if not provided)
            save_trajectory: Whether to save screenshots and logs
            trajectory_dir: Directory to save trajectories (defaults to "trajectories")
            only_n_most_recent_images: Limit history to N most recent images
            max_retries: Maximum number of retry attempts for failed operations
            verbosity: Logging level (standard Python logging levels: logging.DEBUG, logging.INFO, etc.)
            **kwargs: Additional keyword arguments to pass to the loop
        """
        # Set up trajectory directories based on save_trajectory
        base_dir = trajectory_dir if save_trajectory else None
        # Don't create a redundant screenshots directory - directly use the timestamp folder
        screenshot_dir = None  # This was previously set to os.path.join(base_dir, "screenshots")
        log_dir = None

        super().__init__(
            max_retries=max_retries,
            computer=computer,
            screenshot_dir=screenshot_dir,
            log_dir=log_dir,
            **kwargs,
        )

        self.loop_type = loop_type
        self.save_trajectory = save_trajectory
        self.trajectory_dir = trajectory_dir
        self.only_n_most_recent_images = only_n_most_recent_images
        self.verbosity = verbosity
        self._kwargs = kwargs  # Keep this for loop initialization

        # Configure logging based on verbosity
        self._configure_logging(verbosity)

        # Process model configuration
        self.model_config = self._process_model_config(model, loop_type)
        
        # Get API key from environment if not provided
        if api_key is None:
            env_var = (
                ENV_VARS.get(self.model_config.provider) 
                if loop_type == AgenticLoop.OMNI 
                else "ANTHROPIC_API_KEY"
            )
            if not env_var:
                raise ValueError(
                    f"Unsupported provider: {self.model_config.provider}. Please use one of: {list(ENV_VARS.keys())}"
                )

            api_key = os.environ.get(env_var)
            if not api_key:
                raise ValueError(
                    f"No API key provided and {env_var} environment variable is not set.\n"
                    f"Please set the {env_var} environment variable or pass the api_key directly:\n"
                    f"  - Export in terminal: export {env_var}=your_api_key_here\n"
                    f"  - Add to .env file: {env_var}=your_api_key_here\n"
                    f"  - Pass directly: api_key='your_api_key_here'"
                )
        self.api_key = api_key

        # Initialize the appropriate loop based on loop_type
        self.loop = self._init_loop()
        
    def _process_model_config(
        self, model_input: Optional[Union[LLM, Dict[str, str], str]], loop_type: AgenticLoop
    ) -> LLM:
        """Process and normalize model configuration.
        
        Args:
            model_input: Input model configuration (LLM, dict, string, or None)
            loop_type: The loop type being used
            
        Returns:
            Normalized LLM instance
        """
        # Handle case where model_input is None
        if model_input is None:
            # Use Anthropic for Anthropic loop, OpenAI for Omni loop
            default_provider = (
                LLMProvider.ANTHROPIC if loop_type == AgenticLoop.ANTHROPIC else LLMProvider.OPENAI
            )
            return LLM(provider=default_provider)
            
        # Handle case where model_input is already a LLM or one of its aliases
        if isinstance(model_input, (LLM, Model, LLMModel)):
            return model_input
            
        # Handle case where model_input is a dict
        if isinstance(model_input, dict):
            provider = model_input.get("provider", LLMProvider.OPENAI)
            if isinstance(provider, str):
                provider = LLMProvider(provider)
            return LLM(
                provider=provider,
                name=model_input.get("name")
            )
            
        # Handle case where model_input is a string (model name)
        if isinstance(model_input, str):
            default_provider = (
                LLMProvider.ANTHROPIC if loop_type == AgenticLoop.ANTHROPIC else LLMProvider.OPENAI
            )
            return LLM(provider=default_provider, name=model_input)
            
        raise ValueError(f"Unsupported model configuration: {model_input}")

    def _configure_logging(self, verbosity: int):
        """Configure logging based on verbosity level."""
        # Use the logging level directly without mapping
        logger.setLevel(verbosity)
        logging.getLogger("agent").setLevel(verbosity)

        # Log the verbosity level that was set
        if verbosity <= logging.DEBUG:
            logger.info("Agent logging set to DEBUG level (full debug information)")
        elif verbosity <= logging.INFO:
            logger.info("Agent logging set to INFO level (standard output)")
        elif verbosity <= logging.WARNING:
            logger.warning("Agent logging set to WARNING level (warnings and errors only)")
        elif verbosity <= logging.ERROR:
            logger.warning("Agent logging set to ERROR level (errors only)")
        elif verbosity <= logging.CRITICAL:
            logger.warning("Agent logging set to CRITICAL level (critical errors only)")

    def _init_loop(self) -> Any:
        """Initialize the loop based on the loop_type.

        Returns:
            Initialized loop instance
        """
        # Lazy import OmniLoop and OmniParser to avoid circular imports
        from ..providers.omni.loop import OmniLoop
        from ..providers.omni.parser import OmniParser

        if self.loop_type == AgenticLoop.ANTHROPIC:
            from ..providers.anthropic.loop import AnthropicLoop

            # Ensure we always have a valid model name
            model_name = self.model_config.name or DEFAULT_MODELS[LLMProvider.ANTHROPIC]
            
            return AnthropicLoop(
                api_key=self.api_key,
                model=model_name,
                computer=self.computer,
                save_trajectory=self.save_trajectory,
                base_dir=self.trajectory_dir,
                only_n_most_recent_images=self.only_n_most_recent_images,
                **self._kwargs,
            )

        # Initialize parser for OmniLoop with appropriate device
        if "parser" not in self._kwargs:
            self._kwargs["parser"] = OmniParser()

        # Ensure we always have a valid model name
        model_name = self.model_config.name or DEFAULT_MODELS[self.model_config.provider]
        
        return OmniLoop(
            provider=self.model_config.provider,
            api_key=self.api_key,
            model=model_name,
            computer=self.computer,
            save_trajectory=self.save_trajectory,
            base_dir=self.trajectory_dir,
            only_n_most_recent_images=self.only_n_most_recent_images,
            **self._kwargs,
        )

    async def _execute_task(self, task: str) -> AsyncGenerator[Dict[str, Any], None]:
        """Execute a task using the appropriate loop.

        Args:
            task: Task description to execute

        Yields:
            Dict containing response content and metadata
        """
        try:
            # Format the messages based on loop type
            if self.loop_type == AgenticLoop.ANTHROPIC:
                # Anthropic format
                messages = [{"role": "user", "content": [{"type": "text", "text": task}]}]
            else:
                # Cua format
                messages = [{"role": "user", "content": task}]

            # Run the loop
            try:
                async for result in self.loop.run(messages):
                    if result is None:
                        break

                    # Handle error case
                    if "error" in result:
                        yield {
                            "role": "assistant",
                            "content": result["error"],
                            "metadata": {"title": "❌ Error"},
                        }
                        continue

                    # Extract content and metadata based on loop type
                    if self.loop_type == AgenticLoop.ANTHROPIC:
                        # Handle Anthropic format
                        if "content" in result:
                            content_text = ""
                            for content_block in result["content"]:
                                try:
                                    # Try to access the text attribute directly
                                    content_text += content_block.text
                                except (AttributeError, TypeError):
                                    # If it's a dictionary instead of an object
                                    if isinstance(content_block, dict) and "text" in content_block:
                                        content_text += content_block["text"]

                            yield {
                                "role": "assistant",
                                "content": content_text,
                                "metadata": result.get("parsed_screen", {}),
                            }
                        else:
                            yield {
                                "role": "assistant",
                                "content": str(result),
                                "metadata": {"title": "Screen Analysis"},
                            }
                    else:
                        # Handle Omni format
                        content = ""
                        metadata = {"title": "Screen Analysis"}

                        # If result has content (normal case)
                        if "content" in result:
                            content = result["content"]

                            # Ensure metadata has a title
                            if isinstance(content, dict) and "metadata" in content:
                                metadata = content["metadata"]
                                if "title" not in metadata:
                                    metadata["title"] = "Screen Analysis"

                            # For string content, convert to proper format
                            if isinstance(content, str):
                                content = content
                            elif isinstance(content, dict) and "content" in content:
                                content = content.get("content", "")

                        yield {"role": "assistant", "content": content, "metadata": metadata}
            except Exception as e:
                logger.error(f"Error running the loop: {str(e)}")
                yield {
                    "role": "assistant",
                    "content": f"Error running the agent loop: {str(e)}",
                    "metadata": {"title": "❌ Loop Error"},
                }

        except Exception as e:
            logger.error(f"Error in _execute_task: {str(e)}")
            yield {
                "role": "assistant",
                "content": f"Error: {str(e)}",
                "metadata": {"title": "❌ Error"},
            }
