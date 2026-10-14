# game-infographic-generator

A minimal proof of concept for a game infographic agent. Includes a Python
package, a Pydantic game model, and a CLI readiness message.

## Setup

Requires Python 3.9 or newer.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
```

This installs the package in editable mode with Pydantic and pytest.

## Run

```sh
game-infographic-generator
# Game Infographic Agent ready
```

You can also run `python -m game_infographic_generator` after installation.

## Test

```sh
python -m pytest
```

Tests can also run directly from the repository before installing the package,
provided pytest and Pydantic are available in the active environment.
