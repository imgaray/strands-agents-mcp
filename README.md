# Strands Agent MCP

A Model Context Protocol (MCP) server for executing Strands agents. This project provides a simple way to integrate Strands agents with Amazon Q and other MCP-compatible systems.

<a href="https://glama.ai/mcp/servers/@imgaray/strands-agents-mcp">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@imgaray/strands-agents-mcp/badge" alt="Strands Agent MCP server" />
</a>

## Overview

Strands Agent MCP is a bridge between the Strands agent framework and the Model Context Protocol (MCP). It allows you to:

- Register Strands agents as MCP tools
- Execute Strands agents through MCP
- Discover and list available agents

The project uses a plugin architecture that makes it easy to add new agents without modifying the core code.

## Installation

```bash
pip install strands-agent-mcp
```

## Usage

### Starting the MCP Server

```bash
strands-agent-mcp
```

This will start the MCP server on the default port.

### Creating Agent Plugins

To create a new agent plugin, create a Python package with a name that starts with `sap_mcp_plugin_` (sap stands for strands agent plugin). Your package should implement a `register_plugin` function that registers one or more agents with the provided registry:

```python
from strands import Agent
from strands.models import BedrockModel
from strands_agent_mcp.registry import Registry

def register_plugin(registry: Registry) -> None:
    registry.register("my-agent", Agent(
        model=BedrockModel(boto_session=Session(region_name="us-west-2")))
    )
```

### Using with Amazon Q

Once the MCP server is running, you can use the agents with Amazon Q:

```bash
q chat --mcp-server http://localhost:8000
```

Then you can use the following commands in your chat:

- List available agents: `strands___list_agents`
- Execute an agent: `strands___execute_agent` with parameters `agent` (agent name) and `prompt` (the prompt to send to the agent)

## Architecture

The project consists of three main components:

1. **Server**: The MCP server that exposes the agent execution API
2. **Registry**: A simple registry for managing available agents
3. **Plugins**: Dynamically discovered modules that register agents with the registry

The server automatically discovers all installed plugins that follow the naming convention and registers their agents.

## Dependencies

- `fastmcp`: For implementing the MCP server
- `strands-agents`: The core Strands agent framework
- `strands-agents-builder`: Tools for building Strands agents
- `strands-agents-tools`: Additional tools for Strands agents

## Development

To set up a development environment:

1. Clone the repository
2. Create a virtual environment: `python -m venv .venv`
3. Activate the virtual environment: `source .venv/bin/activate` (Linux/Mac) or `.venv\Scripts\activate` (Windows)
4. Install development dependencies: `pip install -e ".[dev]"`

## Creating a Test Plugin

The repository includes a sample plugin (`sap_mcp_plugin_test`) that demonstrates how to create and register a simple agent called "simple-agent":

```python
from boto3 import Session
from strands import Agent
from strands.models import BedrockModel

from strands_agent_mcp.registry import Registry


def register_plugin(registry: Registry) -> None:
    registry.register("simple-agent", Agent(
        model=BedrockModel(boto_session=Session(region_name="us-west-2")))
    )
```

## License

[Add license information here]