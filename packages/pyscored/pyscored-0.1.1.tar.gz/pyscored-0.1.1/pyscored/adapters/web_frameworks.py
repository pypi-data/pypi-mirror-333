# pyscored/adapters/web_frameworks.py

from typing import Any, Dict
from pyscored.core.scoring_engine import ScoringEngine


class WebFrameworkAdapter:
    """Adapter for integrating the ScoringEngine with modern web frameworks like FastAPI."""

    def __init__(self, engine: ScoringEngine):
        self.engine = engine

    async def setup_user(self, user_id: str, initial_score: float = 0.0) -> None:
        """Asynchronously sets up initial scoring for a new user in a web application."""
        self.engine.initialize_score(user_id, initial_score)

    async def update_user_score(self, user_id: str, points: float) -> None:
        """Asynchronously updates the user's score based on web interactions."""
        self.engine.update_score(user_id, points)

    async def get_user_score(self, user_id: str) -> float:
        """Asynchronously retrieves the current score of a user."""
        return self.engine.get_score(user_id)

    async def apply_web_rule(self, rule_name: str, **kwargs) -> Any:
        """Asynchronously applies web-specific scoring rules dynamically."""
        return self.engine.apply_rule(rule_name, **kwargs)

    async def execute_plugin_feature(self, plugin_name: str, **kwargs) -> Any:
        """Asynchronously executes additional features provided by registered plugins."""
        return self.engine.execute_plugin(plugin_name, **kwargs)

