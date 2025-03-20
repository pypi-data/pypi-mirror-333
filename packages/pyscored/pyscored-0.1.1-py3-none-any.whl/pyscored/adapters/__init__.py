"""
Adapters for integrating pyscored with various frameworks.

This package provides pre-built middleware for seamless integration with
game and web frameworks.
"""

from .game_frameworks import GameFrameworkAdapter
from .web_frameworks import WebFrameworkAdapter

__all__ = ["GameFrameworkAdapter", "WebFrameworkAdapter"]
