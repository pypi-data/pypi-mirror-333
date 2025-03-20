# pyscored/plugins/time_decay_plugin.py

from typing import Any
from pyscored.plugins.base_plugin import BasePlugin


class TimeDecayPlugin(BasePlugin):
    """Plugin that applies a time-based decay to player scores, useful for games with time-sensitive scoring."""

    def __init__(self, name: str, decay_rate: float):
        super().__init__(name)
        self.decay_rate = decay_rate

    def execute(self, player_id: str, elapsed_time: float) -> None:
        """Reduces the player's score based on elapsed time and configured decay rate."""
        current_score = self.engine.get_score(player_id)
        decay_amount = current_score * self.decay_rate(elapsed_time=elapsed_time)
        new_score = max(0, current_score - decay_amount)
        self.engine.update_score(player_id, new_score - current_score)

    def decay_rate(self, elapsed_time: float) -> float:
        """Determines the decay rate based on elapsed time. Customize this function as needed."""
        return self._decay_rate * elapsed_time

    def config(self) -> dict:
        base_config = super().config()
        base_config.update({"decay_rate": self.decay_rate})
        return base_config

    def execute(self, **kwargs) -> Any:
        elapsed_time = kwargs.get("elapsed_time", 0)
        player_id = kwargs["player_id"]
        return self.apply_decay(player_id, elapsed_time)

    def decay_rate(self, elapsed_time: float) -> float:
        """Calculates decay rate based on elapsed time."""
        # Example simple linear decay; override for custom behaviors
        return self.decay_rate_per_second * elapsed_time