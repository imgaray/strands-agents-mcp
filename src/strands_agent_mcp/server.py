import importlib
import pkgutil
from typing import List, Annotated
from pydantic import Field
import os

from fastmcp import FastMCP

from strands_agent_mcp.registry import build_registry

mcp = FastMCP(name="strands_agent_mcp")


plugin_path = os.environ.get("PLUGIN_PATH", None)

# sap stands for strands agent plugin
plugin_namespace = os.environ.get("PLUGIN_NAMESPACE", 'sap_mcp_plugin')


discovered_plugins = {
    name: importlib.import_module(name)
    for finder, name, ispkg
    in pkgutil.iter_modules(plugin_path)
    if name.startswith(plugin_namespace)
}

agent_registry = build_registry(discovered_plugins)


@mcp.tool(description="Execute an agent with a given prompt")
def execute_agent(agent_name: Annotated[str, Field(description="The name of the agent to execute")],
                  prompt: Annotated[str, Field(description="The prompt to execute the agent with")]) -> str:
    """
    Execute an agent with the provided name and prompt, return its response
    """
    agent = agent_registry.get(agent_name)
    result = agent.agent(prompt)
    return str(result.message)


@mcp.tool(description="list all available agents")
def list_agents() -> List[str]:
    """
    List all registered agents
    """
    return [agent.name for agent in agent_registry.agent_entries]

@mcp.tool(description="list all available skills for agents")
def list_skills() -> List[str]:
    """
    List all registered skills
    """
    return [skill for skill in agent_registry.skills]


if __name__ == "__main__":
    mcp.run()
