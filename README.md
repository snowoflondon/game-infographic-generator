# game-infographic-generator

A Python proof of concept for researching game metadata, validating it with
Pydantic, and rendering single-game portrait PNGs. Research is agent-driven;
the CLI validates and renders prepared local files.

## Workflows and architecture

The current implementation validates metadata and renders single-game portrait PNGs.
Personal rankings remain future work.

### Single-game infographic

```text
One game title → Codex + game-research → metadata JSON
             → GameMetadata validation → detailed portrait renderer
```

Codex follows [game-research](skills/game-research/SKILL.md) using research tools
and saves JSON. The skill's contract governs intentional schema development;
the existing Pydantic models govern runtime validation. Research is an
agent-driven step, separate from the Python CLI and rendering code.

Keep `GameMetadata` and its nested models in
`src/game_infographic_generator/models.py`. Rendering is implemented in
`rendering/single_game.py` with
`render_single_game(metadata, output_path, artwork=None, presentation=None)`.
The CLI loads and validates the
JSON before passing the model to the renderer. The renderer owns presentation;
it does not research games or change metadata. PNG export uses Python, Jinja2, HTML/CSS, and Playwright Chromium.

### Personal rankings infographic (future)

```text
Ordered game titles → separate RankingsInput validation
                    → minimal rankings renderer
```

The input order represents the user's personal ranking and must be preserved;
positions come directly from that order. The initial implementation will need
no LLM research and will not require full `GameMetadata` records.

When this workflow is implemented, add `rankings_models.py` for its Pydantic
input model and `rendering/rankings.py` for its independent layout. Extract
common utilities into `rendering/common.py` only when both renderers need them,
for example text wrapping, font loading, colors, or export. Prefer plain
functions; introduce abstractions only when actual duplication warrants them.
Rankings models, commands, and rendering modules are not implemented yet.

## Setup

Requires Python 3.11 or newer.

```sh
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
```

This installs the package in editable mode with Pydantic, Jinja2, Playwright, Pillow,
and the pytest development extra. Substitute another Python 3.11+ interpreter
if needed. An existing Python 3.9 virtual environment must be replaced with one
created using a supported interpreter; changing project configuration does not
upgrade that environment. Deactivate and rename the old `.venv` outside the
repository before creating the new one if you want to preserve it.

### Chromium setup

Inside the activated environment, install the browser matching Playwright:

```sh
python -m playwright install chromium
```

Re-run this command after upgrading Playwright. On supported Linux systems,
`python -m playwright install --with-deps chromium` also installs required OS
libraries and may require administrator privileges. See the
[Playwright system requirements](https://playwright.dev/python/docs/intro#system-requirements)
for supported operating systems. No npm setup or separate Node.js application
is required. Fonts with Japanese, Korean, and Chinese coverage will be needed
for multilingual output; the renderer uses local system font fallbacks.

To check Python dependency consistency:

```sh
python -m pip check
```

The `single-game` command renders PNGs; `rankings` is not implemented.

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
python -m game_infographic_generator validate tests/fixtures/game_metadata.json
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
Although runtime validation accepts omitted optional fields, the research skill
requires every top-level field in generated JSON, using `null` or `[]` as appropriate.
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
provided the project dependencies and pytest are available in the active environment.

## Render a single game

```sh
source .venv/bin/activate
game-infographic-generator single-game \
  data/validation-runs/genshin_impact__2026-10-14T192010-0400__game-research.json \
  output/genshin_impact.png
```

Without `--artwork`, the renderer shows full metadata (excluding sources) with
neutral fallback accents. Artwork is optional. When requested, provide both
`--artwork image.jpg` and `--presentation copy.json`. The image is mandatory for
that run; normal and compact layouts retain it or fail explicitly.

Presentation JSON is separate from research metadata:

```sh
game-infographic-generator single-game \
  data/validation-runs/yakuza_like_a_dragon__2026-10-14T192010-0400__game-research.json \
  output/yakuza_like_a_dragon.png \
  --artwork assets/artwork/yakuza_like_a_dragon/official_hero.jpg \
  --presentation data/validation-runs/yakuza_like_a_dragon__2026-10-14T210608-0400__infographic-design.presentation.json
```

```json
{
  "overview": "A faithful one-sentence overview of the supplied description.",
  "highlights": ["Brief positive theme"],
  "criticisms": ["Brief critical theme"]
}
```

Codex condenses the source text; the standalone CLI does not summarize it.
Use `null` for the overview only when the source description is absent, and `[]`
for themes only when the corresponding source sentiment list is empty. Artwork mode replaces
only the overview and sentiment presentation, omitting the long sentiment summary;
similar games and factual metadata remain. Research JSON is never rewritten. The
output is fixed at 1200 × 1600 pixels (3:4). Content that cannot fit after
spacing adjustments produces an error rather than clipping or truncation.
Source references and URLs are omitted from the image and retained unchanged
in the research JSON. Critic aggregator names remain visible.
It keeps neutral backgrounds and body text, extracting restrained accents from
artwork with Pillow for headings, score cards, and a decorative rule. Accent
text and score-card text meet a 4.5:1 contrast threshold; unsuitable palettes use
a fixed fallback. Extraction is deterministic for identical artwork and dependency
versions, does not recolor artwork, and has no manual CLI override.
It uses local system fonts. Install Noto Sans CJK fonts on
Linux; macOS fallbacks include PingFang SC, Hiragino Sans, and Apple SD Gothic
Neo. Font availability can affect line wrapping between machines.

`python -m game_infographic_generator single-game ...` is equivalent. Invalid
metadata is rejected before browser launch; rendering errors exit with status 1.
Output directories are created automatically. An existing output PNG is replaced
atomically only after successful rendering; failures preserve its contents.
Image signatures and Pillow decoding are checked before browser launch;
Chromium also decodes the image before layout/capture. Missing, corrupt, or
undecodable artwork fails explicitly.

Run all tests with `python -m pytest`. Browser integration tests require Chromium
and permission to launch it. The renderer blocks network requests, escapes input
text, and does not emit source reference links.

### Codex discovery vs. standalone CLI

When Codex follows [infographic-design](skills/infographic-design/SKILL.md), it discovers
and verifies requested artwork for the exact game/edition (or inspects the
approved image you supply). It prefers
official promotional assets, then official covers, then official screenshots,
checks suitability and usage terms, and stores the local image and provenance in
`assets/artwork/<game_slug>/`. It prepares separate condensed presentation copy,
then invokes the CLI with `--artwork` and `--presentation`.

The standalone Python CLI only validates metadata, reads any requested local
artwork, and renders it. It does not search, download, establish permissions, or
verify which game an image depicts. That verification is the agent/user's job.
Both normal and compact layouts retain a full-width 16:9 hero beneath the title,
using proportional cropping without distortion. An artwork-mode failure never
triggers a typography-only substitute.

### Example artifacts

`data/validation-runs/` contains research JSON, condensed `.presentation.json`
sidecars, and rendered PNGs for the example games. Validation-run filenames use
`<game_slug>__<timestamp>__<skill-name>.<extension>`. Artwork and its provenance
remain in `assets/artwork/`; research JSON retains source references that are
omitted from the infographic.
