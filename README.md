# game-infographic-generator

A minimal proof of concept for a game infographic agent. Includes a Python
package, nested Pydantic metadata models, and a CLI for validating research JSON.

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

## Validate metadata

```sh
game-infographic-generator validate tests/fixtures/game_metadata.json
# Or:
python -m game_infographic_generator validate data/persona_5_royal.json
```

Before editable installation, use the existing environment from the repository root:

```sh
PYTHONPATH=src .venv/bin/python -m game_infographic_generator validate tests/fixtures/game_metadata.json
```

The validator prints success and exits with status 0 for valid JSON. Invalid
JSON, schema violations, and unreadable files produce an error on stderr and
exit status 1; command usage errors exit with status 2.

`GameMetadata` lives in `src/game_infographic_generator/models.py`. Only `title`
is required. Unknown optional scalars and `player_sentiment` default to `null`;
list fields default to `[]`. A supplied sentiment object can omit its fields.
Critic entries require `source`, integer `score`, positive integer `max_score`,
and `platform`; source entries require `name`. Their URLs are optional strings.
Scores must fall between zero and their maximum. Dates use `YYYY-MM-DD`.
Unexpected fields and implicit scalar type coercions are rejected at every level.

The sample fixture copies the illustrative Persona 5 Royal example in
`skills/game-research/SKILL.md`; it is not verified research. Schema validation
does not verify facts or URL reachability. Research outputs need verified URLs.

## Test

```sh
python -m pytest
# With the existing repository environment:
.venv/bin/python -m pytest
```

Tests can also run directly from the repository before installing the package,
provided pytest and Pydantic are available in the active environment.
