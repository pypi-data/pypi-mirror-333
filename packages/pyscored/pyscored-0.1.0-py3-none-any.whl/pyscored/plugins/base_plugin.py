# pyscored/plugins/base_plugin.py

from abc import ABC, abstractmethod
from typing import Any, Dict

class BasePlugin(ABC):
    """Abstract base class for plugins extending the Scoring Engine functionalities."""

    def __init__(self, name: str):
        self.name = name
        self.engine = None

    def initialize(self, engine: 'ScoringEngine') -> None:
        """Initializes the plugin with the given ScoringEngine instance."""
        self.engine = engine

    @abstractmethod
    def execute(self, **kwargs) -> Any:
        """Executes the plugin's core functionality. Must be implemented by subclasses."""
        pass

    def config(self) -> Dict[str, Any]:
        """Returns plugin-specific configuration details."""
        return {"name": self.name}
