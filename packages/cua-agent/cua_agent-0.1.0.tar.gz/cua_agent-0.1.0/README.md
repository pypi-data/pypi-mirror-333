<div align="center">
<h1>
  <div class="image-wrapper" style="display: inline-block;">
    <picture>
      <source media="(prefers-color-scheme: dark)" alt="logo" height="150" srcset="../../img/logo_white.png" style="display: block; margin: auto;">
      <source media="(prefers-color-scheme: light)" alt="logo" height="150" srcset="../../img/logo_black.png" style="display: block; margin: auto;">
      <img alt="Shows my svg">
    </picture>
  </div>

  [![Python](https://img.shields.io/badge/Python-333333?logo=python&logoColor=white&labelColor=333333)](#)
  [![macOS](https://img.shields.io/badge/macOS-000000?logo=apple&logoColor=F0F0F0)](#)
  [![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?&logo=discord&logoColor=white)](https://discord.com/invite/mVnXXpdE85)
  [![PyPI](https://img.shields.io/pypi/v/cua-computer?color=333333)](https://pypi.org/project/cua-computer/)
</h1>
</div>

**Agent** is a Computer Use (CUA) framework for running multi-app agentic workflows targeting macOS and Linux sandbox, supporting local (Ollama) and cloud model providers (OpenAI, Anthropic, Groq, DeepSeek, Qwen). The framework integrates with Microsoft's OmniParser for enhanced UI understanding and interaction.

### Get started with Agent

There are two ways to use the agent: with OmniParser for enhanced UI understanding (recommended) or with basic computer control.

#### Option 1: With OmniParser (Recommended)

<div align="center">
    <img src="../../img/agent.png"/>
</div>

```python
from agent.providers.omni import OmniComputerAgent, APIProvider

# Set your API key
export OPENAI_API_KEY="your-openai-api-key"

# Initialize agent with OmniParser for enhanced UI understanding
agent = OmniComputerAgent(
    provider=APIProvider.OPENAI,
    model="gpt-4o",
    start_omniparser=True  # Automatically starts OmniParser server
)

task = """
1. Search the ai-gradio repo on GitHub.
2. Clone it to the desktop.
3. Open the repo with the Cursor app.
4. Work with Cursor to add a new provider for Cua.
"""

async with agent:  # Ensures proper cleanup
    async for result in agent.run(task):
        print(result)
```

#### Option 2: Basic Computer Control

```python
from agent.computer_agent import ComputerAgent
from agent.base.types import Provider

# Set your API key (supports any provider)
export OPENAI_API_KEY="your-openai-api-key"  # or other provider keys

# Initialize basic agent
agent = ComputerAgent(
    provider=Provider.OPENAI,  # or ANTHROPIC, GROQ, etc.
)

task = """
1. Open Chrome and navigate to github.com
2. Search for 'trycua/cua'
3. Star the repository
"""

async with agent:
    async for result in agent.run(task):
        print(result)
```

## Install

### cua-agent

```bash
# Basic installation with Anthropic
pip install cua-agent[anthropic]

# Install with OmniParser (recommended)
# Includes all provider dependencies (OpenAI, Anthropic, etc.)
pip install cua-agent[omni]

# Install with all features and providers
pip install cua-agent[all]
```

## Features

### OmniParser Integration
- Enhanced UI understanding with element detection
- Automatic bounding box detection for UI elements
- Improved accuracy for complex UI interactions
- Support for icon and text element recognition

### Basic Computer Control
- Direct keyboard and mouse control
- Window and application management
- Screenshot capabilities
- Basic UI element detection

### Provider Support
- OpenAI (GPT-4V) - Recommended for OmniParser integration
- Anthropic (Claude) - Strong general performance
- Groq - Fast inference with Llama models
- DeepSeek - Alternative model provider
- Qwen - Alibaba's multimodal model

## Run

Refer to these notebooks for step-by-step guides on how to use the Computer-Use Agent (CUA):

- [Getting Started with OmniParser](../../notebooks/omniparser_nb.ipynb) - Enhanced UI understanding
- [Basic Computer Control](../../notebooks/basic_agent_nb.ipynb) - Simple computer interactions
- [Advanced Usage](../../notebooks/agent_nb.ipynb) - Complete examples and workflows

# Computer Agent Library

A Python library for controlling computer interactions with AI agents.

## Introduction

This library provides a unified interface for AI-powered computer interaction agents, allowing applications to automate UI interactions through various AI providers.

## Key Features

- **Unified Agent**: Single `ComputerAgent` class with configurable loop types
- **Multiple AI providers**: Support for OpenAI, Anthropic, Groq, and other providers
- **Screen analysis**: Intelligent screen parsing and element identification
- **Tool execution**: Execute tools and commands to interact with the computer
- **Trajectory saving**: Option to save screenshots and logs for debugging and analysis

## Installation

To install the library along with its dependencies:

```bash
pip install -e .
```

## Usage

Here's a simple example of how to use the ComputerAgent:

```python
import asyncio
from computer import Computer
from agent.core.agent import ComputerAgent
from agent.types.base import AgenticLoop
from agent.providers.omni.types import APIProvider

async def main():
    # Initialize the computer interface
    computer = Computer()
    
    # Create a computer agent
    agent = ComputerAgent(
        computer=computer,
        loop_type=AgenticLoop.OMNI,  # Use OMNI loop
        provider=APIProvider.OPENAI,  # With OpenAI provider
        model="gpt-4o",               # Specify the model
        save_trajectory=True,         # Save logs and screenshots
    )
    
    # Use the agent with a context manager
    async with agent:
        # Run a task
        async for result in agent.run("Open Safari and navigate to github.com"):
            # Process the result
            title = result["metadata"].get("title", "Screen Analysis")
            content = result["content"]
            print(f"\n{title}")
            print(content)

if __name__ == "__main__":
    asyncio.run(main())
```

## Components

The library consists of several components:

- **Core**
  - `ComputerAgent`: Unified agent class supporting multiple loop types
  - `BaseComputerAgent`: Abstract base class for computer agents
  
- **Providers**
  - `Anthropic`: Implementation for Anthropic Claude models
  - `Omni`: Implementation for multiple providers (OpenAI, Groq, etc.)

- **Loops**
  - `AnthropicLoop`: Loop implementation for Anthropic
  - `OmniLoop`: Generic loop supporting multiple providers

## Configuration

The agent can be configured with various parameters:

- **loop_type**: The type of loop to use (ANTHROPIC or OMNI)
- **provider**: AI provider to use with the loop
- **model**: The AI model to use
- **save_trajectory**: Whether to save screenshots and logs
- **only_n_most_recent_images**: Only keep a specific number of recent images

See the [Core README](./agent/core/README.md) for more details on the unified agent.