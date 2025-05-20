from types import ModuleType
from typing import Dict, Optional, List

from pydantic import BaseModel, ConfigDict
from strands import Agent


class AgentEntry(BaseModel):
    name: str
    agent: Agent
    skills: list[str]
    model_config = ConfigDict(extra='forbid', arbitrary_types_allowed=True)


class Registry:
    def __init__(self):
        self._registry: Dict[str, AgentEntry] = {}
        self._reverse_index: Dict[str, List[AgentEntry]] = {}

    def register(self, agent: AgentEntry):
        self._registry[agent.name] = agent
        for skill in agent.skills:
            if skill not in self._reverse_index:
                self._reverse_index[skill] = []
            self._reverse_index[skill].append(agent)

    def get(self, name: str) -> Optional[AgentEntry]:
        return self._registry.get(name, None)

    def find(self, skill: str) -> List[AgentEntry]:
        return self._reverse_index.get(skill, [])

    @property
    def agent_entries(self) -> List[AgentEntry]:
        return [entry for entry in self._registry.values()]

    @property
    def skills(self) -> List[str]:
        return [key for key in self._reverse_index.keys()]


def build_registry(discovered_plugins: Dict[str, ModuleType]) -> Registry:
    registry = Registry()
    for plugin_name, module in discovered_plugins.items():
        for agent_entry in module.build_agents():
            registry.register(agent_entry)
    return registry