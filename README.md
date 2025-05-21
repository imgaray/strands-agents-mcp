# Strands Agent MCP

A Model Context Protocol (MCP) server for executing Strands agents. This project provides a simple way to integrate Strands agents with Amazon Q and other MCP-compatible systems.

> **IMPORTANT**: This project is currently in alpha stage and not yet published on PyPI.

## Overview

Strands Agent MCP is a bridge between the Strands agent framework and the Model Context Protocol (MCP). It allows you to:

- Register Strands agents as MCP tools
- Execute Strands agents through MCP
- Find agents by specific skills

The project uses a plugin architecture that makes it easy to add new agents without modifying the core code.

## Installation

> Note: This package is not yet available on PyPI. You'll need to install it from source.

```bash
# Clone the repository
git clone https://github.com/yourusername/strands-agent-mcp.git
cd strands-agent-mcp

# Install the package
pip install -e .
```

## Usage

### Starting the MCP Server

```bash
strands-agent-mcp
```

This will start the MCP server.

### Environment Variables

The server supports the following environment variables:

- `PLUGIN_PATH`: Custom path to look for plugins (default: ".")
- `PLUGIN_NAMESPACE`: Custom namespace prefix for plugins (default: 'sap_mcp_plugin')

### Creating Agent Plugins

To create a new agent plugin, create a Python package with a name that starts with `sap_mcp_plugin_` (sap stands for strands agent plugin). Your package should implement a `build_agents` function that returns a list of `AgentEntry` objects:

```python
from typing import List
from boto3 import Session
from strands import Agent
from strands.models import BedrockModel

from strands_agent_mcp.registry import AgentEntry

def build_agents() -> List[AgentEntry]:
    return [
        AgentEntry(
            name="my-agent",
            agent=Agent(
                model=BedrockModel(boto_session=Session(region_name="us-west-2"))
            ),
            skills=["general-knowledge", "coding"]
        )
    ]
```

### Using with Amazon Q

Once the MCP server is running, you can connect it to Amazon Q. Refer to the Amazon Q documentation for the correct connection parameters.

The following MCP tools will be available:

- `execute_agent`: Execute an agent with parameters `agent_name` and `prompt`
- `list_agents`: List all available agents

## Architecture

The project consists of three main components:

1. **Server**: The MCP server that exposes the agent execution API
2. **Registry**: A registry for managing available agents and their skills
3. **Plugins**: Dynamically discovered modules that register agents with the registry

The server automatically discovers all installed plugins that follow the naming convention and registers their agents.

## Dependencies

- `fastmcp>=2.3.4`: For implementing the MCP server
- `strands-agents>=0.1.1`: The core Strands agent framework
- `strands-agents-builder>=0.1.0`: Tools for building Strands agents
- `strands-agents-tools>=0.1.0`: Additional tools for Strands agents

## Development

This project uses [uv](https://github.com/astral-sh/uv) for dependency management. To set up a development environment:

1. Clone the repository
2. Install uv if you don't have it already: `pip install uv`
3. Create a virtual environment and install dependencies:
   ```bash
   uv venv
   uv sync
   ```

## Sample Plugin

The repository includes a sample plugin (`sap_mcp_plugin_simple`) that demonstrates how to create and register a simple agent:

```python
from typing import List
from boto3 import Session
from strands import Agent
from strands.models import BedrockModel

from strands_agent_mcp.registry import AgentEntry

def build_agents() -> List[AgentEntry]:
    return [
        AgentEntry(
            name="simple-agent",
            agent=Agent(
                model=BedrockModel(boto_session=Session(region_name="us-west-2"))
            ),
            skills=["general-knowledge"]
        )
    ]
```

## License

This project is licensed under the terms of the LICENSE file included in the repository.
