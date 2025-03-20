# autogen-agentai

[![PyPI version](https://img.shields.io/pypi/v/autogen-agentai.svg)](https://pypi.org/project/autogen-agentai/)
[![Python versions](https://img.shields.io/pypi/pyversions/autogen-agentai.svg)](https://pypi.org/project/autogen-agentai/)
[![License](https://img.shields.io/github/license/meepolabs/autogen-agentai.svg)](https://github.com/meepolabs/autogen-agentai/blob/main/LICENSE)
[![Documentation Status](https://readthedocs.org/projects/autogen-agentai/badge/?version=latest)](https://autogen-agentai.readthedocs.io/en/latest/?badge=latest)

An extension for Microsoft AutoGen that allows running agents from [agent.ai](https://agent.ai/).

## Overview

autogen-agentai is a Python package that serves as an extension for Microsoft's AutoGen framework, enabling the use of agent.ai agents within AutoGen. It enables developers to:

- **Agent Integration**: Seamlessly integrate agent.ai agents into AutoGen workflows
- **Agent Communication**: Enable communication between AutoGen agents and agent.ai agents
- **Simplified API**: Provide a simple interface to configure and use agent.ai services
- **Extensibility**: Extend AutoGen's capabilities with agent.ai's specialized AI agents

## Key Features (Planned)

- **Agent Interoperability**
  - Connect AutoGen's agent ecosystem with agent.ai's specialized agents
  - Enable cross-platform agent communication
  - Maintain agent context across different platforms
  - Synchronize agent states and knowledge

- **Configuration Management**
  - Simple configuration for agent.ai API connections
  - Credential management for agent.ai services
  - Environment-based configuration options
  - Persistent configuration storage

- **Workflow Integration**
  - Integrate agent.ai agents into existing AutoGen workflows
  - Create hybrid workflows combining agents from both platforms
  - Enable task delegation between different agent types
  - Support for complex multi-agent scenarios

- **Developer Tools**
  - Debugging utilities for agent interactions
  - Logging and monitoring capabilities
  - Testing utilities for agent.ai integration
  - Documentation and examples

## Installation

```bash
pip install autogen-agentai
```

Or with Poetry:

```bash
poetry add autogen-agentai
```

## Quick Example

```python
from autogen_agentai import AgentAIExtension
import autogen

# Initialize the extension
agent_ai_extension = AgentAIExtension(api_key="your_agentai_api_key")

# Create an AutoGen agent with agent.ai capabilities
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={"config_key": "config_value"},
    extensions=[agent_ai_extension]
)

# Use the agent normally in AutoGen workflows
# The agent will have access to agent.ai capabilities
```

## Documentation

For detailed documentation, visit [autogen-agentai.readthedocs.io](https://autogen-agentai.readthedocs.io).

The documentation includes:
- Getting Started Guide
- API Reference
- Examples and Tutorials
- FAQ

## Contributing

We welcome contributions! Please check out our [contributing guidelines](CONTRIBUTING.md) for details on:
- Setting up your development environment
- Running tests
- Submitting pull requests

## License

This project is licensed under the [GNU General Public License v3.0 (GPLv3)](LICENSE).
