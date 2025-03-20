# pyscored/adapters/game_frameworks.py

from typing import Any
from pyscored.core.scoring_engine import ScoringEngine


class GameFrameworkAdapter:
    """Adapter for integrating the ScoringEngine with traditional Python game frameworks like Pygame and Pyglet."""

    def __init__(self, engine: ScoringEngine):
        self.engine = engine

    def setup_player(self, player_id: str, initial_score: float = 0.0) -> None:
        """Sets up initial scoring for a new player in the game."""
        self.engine.initialize_score(player_id, initial_score)

    def update_player_score(self, player_id: str, points: float) -> None:
        """Updates the player's score during gameplay."""
        self.engine.update_score(player_id, points)

    def get_player_score(self, player_id: str) -> float:
        """Retrieves the current score of a player for display."""
        return self.engine.get_score(player_id)

    def apply_game_rule(self, rule_name: str, **kwargs) -> Any:
        """Applies specific game scoring rules dynamically."""
        return self.engine.apply_rule(rule_name, **kwargs)

    def execute_plugin_feature(self, plugin_name: str, **kwargs) -> Any:
        """Executes additional features provided by registered plugins."""
        return self.engine.execute_plugin(plugin_name, **kwargs)

