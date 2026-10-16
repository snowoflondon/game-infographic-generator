# Game Infographic Agent

## Project overview

Build a Python application that validates researched game metadata and generates
single-game portrait PNGs. Research is agent-driven through
[game-research](skills/game-research/SKILL.md); the Python CLI validates local JSON
and renders it. Personal rankings are future work and are not implemented.

## Tech stack

- Use Python 3.11+.
- Use Pydantic for structured data and validation, pytest for testing, and Git
  for version control.
- Use Jinja2 and HTML/CSS for templates, with Playwright's Python API and
  Chromium for PNG rendering, and Pillow for artwork accent extraction.

## Architecture

- Separate metadata retrieval from rendering, using structured models at the
  boundary.
- The research skill's JSON contract governs intentional schema development;
  existing Pydantic models govern runtime validation. Never change models merely
  to make generated research pass validation.
- Follow [infographic-design](skills/infographic-design/SKILL.md) for rendering.
  Preserve the 1200 × 1600 canvas and original research JSON. Artwork is optional;
  artwork mode requires a local image and separate condensed presentation JSON.
  Limit main titles to two lines without truncation. Requested artwork must
  remain present through normal and compact layouts; omit only Similar Games
  as the final compact fallback, then fail if content still cannot fit,
  preserving any existing output PNG.
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
