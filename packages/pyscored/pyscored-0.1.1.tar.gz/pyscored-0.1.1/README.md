# pyscored – Universal Plug-in-Play Scoring System

**pyscored** is a powerful, flexible, and easy-to-use Python library designed for universal scoring management. It seamlessly integrates into various applications, from game development frameworks to modern web applications, providing robust scoring functionalities through a secure sandbox environment and a versatile plugin architecture.

## Features

- **Universal Integration:** Compatible with game frameworks (e.g., Pygame, Pyglet) and web backends (e.g., FastAPI).
- **Plugin-Based Architecture:** Easily extend scoring logic with customizable plugins.
- **Sandbox Environment**: Ensures safe execution of dynamic scoring rules.
- **Flexible API**: Supports dynamic scoring configurations and rule management.

## Installation

Install pyscored easily using Poetry:

```bash
poetry add pyscored
```

## Quick Start

Here's a quick example to initialize and use the Scoring Engine:

```python
from pyscored.core.scoring_engine import ScoringEngine

engine = ScoringEngine()
engine.initialize_score("player1", initial_score=0)
engine.update_score("player1", 10)
print(f"Current score: {engine.get_score('player1')}")
```

## Features & Integrations

### Dynamic Rules
Easily define and apply dynamic scoring rules:

```python
engine.configure_rule("triple_points", lambda points: points * 3)
points_awarded = engine.apply_rule("triple_points", points=5)
print(f"Triple points awarded: {points_awarded}")
```

### Plugin System
Extend functionality using provided or custom plugins:

- **ComboBonusPlugin**: Bonus points for consecutive successful actions.
- **StreakRewardPlugin**: Special rewards for successful action streaks.

Example of registering plugins:

```python
from pyscored.plugins.combo_bonus_plugin import ComboBonusPlugin

combo_plugin = ComboBonusPlugin(name="combo_bonus", bonus_threshold=3, bonus_multiplier=1.5)
engine.register_plugin(combo_plugin)
```

### Framework Adapters

#### Game Development
Integrate with popular game frameworks:

```python
from pyscored.adapters.game_frameworks import GameFrameworkAdapter

adapter = GameFrameworkAdapter(engine)
adapter.setup_player("player1")
adapter.update_player_score("player1", 20)
```

### Web Applications
Easily implement gamification in web applications:

```python
from fastapi import FastAPI
from pyscored.adapters.web_frameworks import WebFrameworkAdapter

app = FastAPI()
web_adapter = WebFrameworkAdapter(engine)

@app.get("/score/{user_id}")
async def get_score(user_id: str):
    score = await web_adapter.get_user_score(user_id)
    return {"user_id": user_id, "score": score}
```

## Documentation

Detailed guides, API references, and usage examples are available in the [documentation](docs/API.md).

## Contributing

We welcome contributions! Please refer to our [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines on how to contribute effectively.

## License

pyscored is licensed under the [GNU License](LICENSE).

