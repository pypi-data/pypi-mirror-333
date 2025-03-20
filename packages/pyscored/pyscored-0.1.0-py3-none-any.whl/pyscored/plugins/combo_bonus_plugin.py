# pyscored/plugins/combo_bonus_plugin.py

from typing import Any
from pyscored.plugins.base_plugin import BasePlugin


class ComboBonusPlugin(BasePlugin):
    """Plugin that awards bonus points for consecutive successful actions or combos, beneficial for gaming scenarios."""

    def __init__(self, name: str, bonus_threshold: int, bonus_multiplier: float):
        super().__init__(name)
        self.bonus_threshold = bonus_threshold
        self.bonus_multiplier = bonus_multiplier
        self.combo_counts = {}

    def execute(self, player_id: str, action_successful: bool, base_points: float) -> None:
        """Applies bonus points based on consecutive successful actions."""
        if action_successful:
            self.combo_counts[player_id] = self.combo_counts.get(player_id, 0) + 1
        else:
            self.combo_counts[player_id] = 0

        if self.combo_counts[player_id] >= self.bonus_threshold:
            bonus_points = base_points * self.bonus_multiplier
            self.engine.update_score(player_id, bonus_points)

    def config(self) -> dict:
        base_config = super().config()
        base_config.update({
            "bonus_threshold": self.bonus_threshold,
            "bonus_multiplier": self.bonus_multiplier
        })
        return base_config


class StreakRewardPlugin(BasePlugin):
    """Plugin that awards special rewards when a player reaches a specific streak of successful actions."""

    def __init__(self, name: str, reward_streak: int, reward_points: float):
        super().__init__(name)
        self.reward_streak = reward_streak
        self.reward_points = reward_points
        self.streak_counts = {}

    def execute(self, player_id: str, action_successful: bool) -> None:
        """Awards special reward points based on achieving a successful action streak."""
        if action_successful:
            self.streak_counts[player_id] = self.streak_counts.get(player_id, 0) + 1
        else:
            self.streak_counts[player_id] = 0

        if self.streak_counts[player_id] == self.reward_streak:
            self.engine.update_score(player_id, self.reward_points)
            self.streak_counts[player_id] = 0  # reset streak after reward

    def config(self) -> dict:
        base_config = super().config()
        base_config.update({
            "reward_streak": self.reward_streak,
            "reward_points": self.reward_points
        })
        return base_config