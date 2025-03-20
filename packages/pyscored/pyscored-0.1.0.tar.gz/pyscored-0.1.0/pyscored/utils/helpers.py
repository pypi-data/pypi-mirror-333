# pyscored/utils/helpers.py

from typing import Any, Dict, Type, Optional

def validate_score(score: float) -> bool:
    """Validates that the score is a non-negative number."""
    return isinstance(score, (int, float)) and score >= 0

def merge_config(default_config: Dict[str, Any], custom_config: Dict[str, Any]) -> Dict[str, Any]:
    """Merges custom configuration settings into default configuration."""
    merged_config = default_config.copy()
    merged_config.update(custom_config)
    return merged_config

def clamp_score(score: float, min_score: float = 0.0, max_score: float = float('inf')) -> float:
    """Clamps the score within specified minimum and maximum bounds."""
    return max(min(score, max_score), min_score)

def format_score(score: float, decimals: int = 2) -> str:
    """Formats the score to a fixed number of decimal places."""
    return f"{score:.{decimals}f}"

def safe_cast(value: Any, to_type: Type, default: Optional[Any] = None) -> Any:
    """Safely casts a value to a specified type, returning a default if casting fails."""
    try:
        return to_type(value)
    except (ValueError, TypeError):
        return default