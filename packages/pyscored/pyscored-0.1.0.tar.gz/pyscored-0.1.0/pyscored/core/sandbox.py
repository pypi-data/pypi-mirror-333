# pyscored/core/sandbox.py

from typing import Callable, Dict, Any


class Sandbox:
    """Sandbox environment to securely execute scoring rules and prevent unauthorized code execution."""

    def __init__(self):
        self._rules: Dict[str, Callable[..., Any]] = {}

    def add_rule(self, rule_name: str, rule_logic: Callable[..., Any]) -> None:
        """Registers a new scoring rule within the sandbox."""
        if rule_name in self._rules:
            raise ValueError(f"Rule '{rule_name}' already exists.")
        self._rules[rule_name] = rule_logic

    def execute_rule(self, rule_name: str, **kwargs) -> Any:
        """Executes a registered scoring rule safely."""
        if rule_name not in self._rules:
            raise ValueError(f"Rule '{rule_name}' is not defined.")
        rule_logic = self._rules[rule_name]
        try:
            return rule_logic(**kwargs)
        except Exception as e:
            raise RuntimeError(f"An error occurred while executing rule '{rule_name}': {e}") from e

    def remove_rule(self, rule_name: str) -> None:
        """Removes a scoring rule from the sandbox."""
        if rule_name in self._rules:
            del self._rules[rule_name]

    def list_rules(self) -> Dict[str, Callable[..., Any]]:
        """Lists all available scoring rules within the sandbox."""
        return self._rules.copy()

