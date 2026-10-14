# Game Infographic Agent

## Project overview

Build a Python application that retrieves video game metadata and generates
portrait infographics. The repository currently contains a minimal scaffold;
metadata retrieval and infographic rendering are not yet implemented.

## Tech stack

- Target Python 3.11+. The scaffold currently declares Python 3.9+ in
  `pyproject.toml` and `README.md`; align these when updating runtime support.
- Use Pydantic for structured data and validation, pytest for testing, and Git
  for version control.

## Architecture

- Separate metadata retrieval from rendering, using structured models at the
  boundary.
- Keep modules small and testable, and external API integrations modular.
- Add type hints to public functions.
- Prefer existing dependencies and the standard library. Ask before adding
  major dependencies.

## Development workflow

- Inspect relevant code and repository instructions before making changes.
- For onboarding or a current-state investigation, use
  [repo-understanding](skills/repo-understanding/SKILL.md). For investigating
  a proposed change and its impact, use
  [change-planner](skills/change-planner/SKILL.md). Both are read-only; use them
  when their investigation is useful rather than requiring both for every edit.
- Keep changes scoped to the request and explain significant architectural
  decisions.
- Write meaningful tests for new functionality and run relevant tests after
  code changes, normally with `python -m pytest`. Report results and any checks
  that could not be run.
- Never commit changes unless explicitly asked.

## Security

- Never hardcode API keys or secrets. Read credentials from environment
  variables and keep `.env` files out of version control.
- Ask before destructive commands.

## Project priorities

Use this order when making tradeoffs:

1. Correctness and reliable metadata.
2. Simplicity and maintainability.
3. Low operating costs.
4. Visual quality of generated infographics.
