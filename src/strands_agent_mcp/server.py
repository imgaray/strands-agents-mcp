import importlib
import pkgutil
from typing import List, Annotated
from pydantic import Field

from fastmcp import FastMCP

from strands_agent_mcp.registry import build_registry

mcp = FastMCP(name="strands_agent_mcp")

discovered_plugins = {
    name: importlib.import_module(name)
    for finder, name, ispkg
    in pkgutil.iter_modules()
    # sap stands for strands agent plugin
    if name.startswith('sap_mcp_plugin')
}

agent_registry = build_registry(discovered_plugins)


@mcp.tool(description="Execute an agent with a given prompt")
def execute_agent(agent: Annotated[str, Field(description="The name of the agent to execute")],
                  prompt: Annotated[str, Field(description="The prompt to execute the agent with")]) -> str:
    """
    Execute an agent with the provided name and prompt, return its response
    """
    result = agent_registry.find(agent)(prompt)
    return str(result.message)


@mcp.tool(description="list all available agents")
def list_agents() -> List[str]:
    """
    List all registered agents
    """
    return agent_registry.agents


if __name__ == "__main__":
    mcp.run()
