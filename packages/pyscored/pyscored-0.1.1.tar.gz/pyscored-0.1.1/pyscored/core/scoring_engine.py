# pyscored/core/scoring_engine.py

from typing import Dict, Any, Callable, Optional
from pyscored.core.sandbox import Sandbox
from pyscored.plugins.base_plugin import BasePlugin

class ScoringEngine:
    """Core scoring engine that manages scoring logic within a sandboxed environment."""

    def __init__(self, sandbox: Optional[Sandbox] = None):
        self._scores: Dict[str, float] = {}
        self._sandbox = sandbox if sandbox else Sandbox()
        self._plugins: Dict[str, BasePlugin] = {}

    def initialize_score(self, player_id: str, initial_score: float = 0.0) -> None:
        """Initializes the score for a new player or resets an existing player's score."""
        self._scores[player_id] = initial_score

    def update_score(self, player_id: str, points: float) -> None:
        """Updates the score of a player by a given number of points."""
        if player_id not in self._scores:
            raise ValueError(f"Player ID '{player_id}' has not been initialized.")
        self._scores[player_id] += points

    def get_score(self, player_id: str) -> float:
        """Retrieves the current score of a player."""
        return self._scores.get(player_id, 0.0)

    def reset_score(self, player_id: str) -> None:
        """Resets the score of a specified player."""
        if player_id in self._scores:
            self._scores[player_id] = 0.0

    def configure_rule(self, rule_name: str, rule_logic: Callable[..., Any]) -> None:
        """Dynamically configures scoring rules within the sandbox."""
        self._sandbox.add_rule(rule_name, rule_logic)

    def apply_rule(self, rule_name: str, **kwargs) -> Any:
        """Applies a configured scoring rule within the sandbox."""
        return self._sandbox.execute_rule(rule_name, **kwargs)

    def register_plugin(self, plugin: BasePlugin) -> None:
        """Registers a plugin to extend scoring functionalities."""
        self._plugins[plugin.name] = plugin
        plugin.initialize(self)

    def execute_plugin(self, plugin_name: str, **kwargs) -> Any:
        """Executes a plugin by its name."""
        if plugin_name not in self._plugins:
            raise ValueError(f"Plugin '{plugin_name}' is not registered.")
        return self._plugins[plugin_name].execute(**kwargs)

