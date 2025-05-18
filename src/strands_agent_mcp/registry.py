from types import ModuleType
from typing import Dict, Optional, List

from strands import Agent


class Registry:
    def __init__(self):
        self._registry = {}

    def register(self, name: str, agent: Agent):
        self._registry[name] = agent

    def find(self, name: str) -> Optional[Agent]:
        return self._registry.get(name, None)

    @property
    def agents(self) -> List[str]:
        return [key for key in self._registry.keys()]


def build_registry(discovered_plugins: Dict[str, ModuleType]) -> Registry:
    registry = Registry()
    for plugin_name, module in discovered_plugins.items():
        module.register_plugin(registry)
    return registry