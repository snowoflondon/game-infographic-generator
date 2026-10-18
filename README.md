# game-infographic-generator

A Python proof of concept for researching game metadata, validating it with
Pydantic, and rendering single-game portrait PNGs. Research is agent-driven;
the CLI validates and renders prepared local files.

## Workflows and architecture

The current implementation validates metadata and renders single-game portrait PNGs.
A first-pass personal top-ten rankings workflow is also implemented; its visual
output has not yet been generated or reviewed.

The current single-game iteration is a working POC baseline; its design is being
left in place for now.
See the [current snapshot](current_snapshot__2026-10-16T195014-0400.md) for the latest
review, verification results, and known limitations.

### Agent skills

| Skill | Purpose |
| --- | --- |
| [repo-understanding](skills/repo-understanding/SKILL.md) | Read-only repository refresher |
| [change-planner](skills/change-planner/SKILL.md) | Read-only change and impact investigation |
| [architecture-visualizer](skills/architecture-visualizer/SKILL.md) | Read-only architectural investigation with Mermaid output |
| [game-research](skills/game-research/SKILL.md) | Source-backed metadata research and validation |
| [infographic-design](skills/infographic-design/SKILL.md) | Single-game rendering, artwork discovery, and visual checks |
| [rankings-infographic](skills/rankings-infographic/SKILL.md) | Personal top-ten title checks and artwork-stripe rendering |

Invoke a helper by asking, for example, “Use architecture-visualizer to diagram
this repository.” The investigative helpers work independently and return their
findings in the response; saving a report requires an explicit request.

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

### Personal rankings infographic (first pass)

Supply a heading and exactly ten games in your personal order, starting with #1.
Codex checks each supplied title against an official game page or storefront,
correcting clear spelling/incomplete-title issues and reporting corrections. It
asks about ambiguous games or editions, then discovers verified artwork. These
checks can share the same source lookup. Rankings does not run `game-research`,
require GameMetadata JSON or use alternative titles. The Python CLI performs no
online title verification, research or downloads.

The separate rankings manifest has a nonblank `title` and a `games` array of
exactly ten objects, each containing nonblank `title` and `artwork_path` strings.
Paths resolve relative to the manifest, independently of your shell directory.
Array order is authoritative; no sorting, inferred rankings or explicit rank
fields are supported. Unexpected fields are rejected.

For example, one entry in the ten-entry array looks like this:

```json
{
  "title": "Persona 3 Reload",
  "artwork_path": "../../../assets/artwork/game/official_hero.jpg"
}
```

Use `rankings_models.py` for manifest validation and `rendering/rankings.py` with
independent `rankings.html.j2` / `rankings.css` templates. The existing dependencies
and packaged template configuration cover both workflows; no new installation step.

```sh
# Validate the manifest and local images; no browser or PNG:
game-infographic-generator rankings path/to/manifest.json output/rankings.png --check

# Export only when generation is wanted:
game-infographic-generator rankings path/to/manifest.json output/rankings.png
```

These command paths are illustrative; saved rankings manifests and previews are
indexed in [rankings validation runs](data/validation-runs/rankings/README.md). `--check` does not assess browser layout, crop suitability, semantic
accuracy or permissions. Normal rendering checks browser layout before capture.

The fixed 1200 × 1600 canvas matches the single-game 3:4 ratio. Ten equal-height
full-width artwork stripes fill the space between the heading and footer, with
#1 at the top and checked game titles in the bottom-left corner of each stripe.
No rank numbers are displayed. Alternative titles
are neither accepted in the manifest nor displayed.
Artwork is cropped proportionally with a consistent left-to-right dark gradient
that fades away over the right side. Titles occupy only the left half. The heading
preserves the user’s casing. The light editorial palette and 48px outer margins
unify header, artwork frame and footer; 6px off-white gaps separate equal-height cards with 8px rounded corners.
Artwork and gradients are clipped together; cards have no border or shadow. Each entry may supply
`"artwork_focal_point": {"x": 50, "y": 25}` (0–100 percentages, default center)
to adjust its crop, prioritizing character faces. Both the heading
and main game titles follow the single-game two-line policy: prefer a colon
break when it fits, otherwise use natural wrapping; unresolved overflow fails
explicitly without shrinking or truncating titles. No row,
title is silently omitted. Existing output is preserved on failure.

Shallow stripes need a different crop from a single-game 16:9 hero. Codex follows
shared [artwork guidance](skills/references/artwork-discovery.md) and checks the
final image when generation is authorized. Local fonts affect fit. Input/template and DOM-only layout tests cover this workflow; real PNG exports
and crop inspections are recorded with the saved examples. Shallow crops still
require visual judgment even with per-game focal controls.

Save rankings manifests and optional reports in `data/validation-runs/rankings/`,
PNGs in its `png/` subfolder, and reuse the shared artwork location. Record title
verification URLs in artwork provenance or optional reports. Neither research
metadata files nor condensed presentation JSON are needed for rankings.

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

The `single-game` and `rankings` commands render PNGs; rankings also offers `--check`.

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

## Architecture diagram exports (optional)

The `architecture-visualizer` skill returns Mermaid text without requiring a CLI.
To export that text as SVG, PNG, or PDF, use the official
[Mermaid CLI](https://github.com/mermaid-js/mermaid-cli). It is optional development
tooling, declared in `tools/mermaid/package.json` with an npm lockfile;
it is not a Python virtual-environment package.

Use Node.js 22.13+ within the 22.x line and npm (the tested version is recorded
in `tools/mermaid/.node-version`). On this workspace, a checksum-verified Node
runtime is installed in ignored `.tools/node/`. Enable it for the current shell:

```sh
export PATH="$PWD/.tools/node/bin:$PATH"
```

On a fresh checkout, install Node.js 22 from [Node.js](https://nodejs.org/en/download)
or your Node version manager first. From the repository root:

```sh
npm --prefix tools/mermaid ci
npm --prefix tools/mermaid run render -- --version
npm --prefix tools/mermaid run render -- -i "$PWD/architecture.mmd" -o "$PWD/architecture.svg"
```

Supply your own `.mmd` file; change the output extension to `.png` or `.pdf` as
needed. Installation also downloads the browser used by Mermaid CLI through
Puppeteer, independently of the Python renderer's Playwright Chromium. No npm
step is required to validate game metadata or render game infographics.

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
  data/validation-runs/game-research/genshin_impact__2026-10-14T192010-0400__game-research.json \
  output/genshin_impact.png
```

Without `--artwork`, the renderer shows full metadata (excluding sources) with
neutral fallback accents. Artwork is optional. When requested, provide both
`--artwork image.jpg` and `--presentation copy.json`. The image is mandatory for
that run; normal and compact layouts retain it or fail explicitly.

Presentation JSON is separate from research metadata:

```sh
game-infographic-generator single-game \
  data/validation-runs/game-research/yakuza_like_a_dragon__2026-10-14T192010-0400__game-research.json \
  output/yakuza_like_a_dragon.png \
  --artwork assets/artwork/yakuza_like_a_dragon/official_hero.jpg \
  --presentation data/validation-runs/infographic-design/baseline/yakuza_like_a_dragon__2026-10-14T210608-0400__infographic-design.presentation.json
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
factual metadata remains. Similar Games is retained unless compact mode still
overflows; only then is that entire section omitted, with a warning. Research
JSON is never rewritten. Main titles are limited to two lines: colon breaks are
preferred when they fit, otherwise natural wrapping is used. Titles that cannot
fit two lines at the compact font size fail explicitly. The
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
using proportional cropping without distortion. The frame controls image size
even for portrait source images. An artwork-mode failure never
triggers a typography-only substitute.

### Example artifacts

`data/validation-runs/game-research/` contains reusable research JSON.
Rendering artifacts are grouped by design round:

```text
data/validation-runs/
├── game-research/
└── infographic-design/
    ├── baseline/
    │   ├── png/
    │   └── earlier-iterations/png/
    ├── 01-title-and-similar-games/png/
    ├── 02-title-fit-and-overflow/png/
    └── 03-compact-platforms/png/
```

The [baseline](data/validation-runs/infographic-design/baseline/README.md)
preserves accepted PNGs and their presentation inputs; earlier iterations are
separate. The
[01-title-and-similar-games](data/validation-runs/infographic-design/01-title-and-similar-games/README.md)
folder records the first label/title refinements.
[02-title-fit-and-overflow](data/validation-runs/infographic-design/02-title-fit-and-overflow/README.md)
records the title-fit fallback policy. Current platform-display comparisons are in
[03-compact-platforms](data/validation-runs/infographic-design/03-compact-platforms/README.md).
Platform display groups iOS/Android as Mobile and shares console family prefixes
(for example, PlayStation 4 & 5); research lists and critic-score platform labels
remain unchanged.
Create a new named round for the next
meaningful design change, with a short README recording its purpose, starting
commit, and inputs used. No game or timestamp subfolders are needed.

Store only PNG images in each group’s `png/` subfolder; keep presentation JSON,
validation reports and the group README in the parent folder. Research-only
folders do not need an empty `png/` directory.

Validation-run filenames use
`<game_slug>__<timestamp>__<skill-name>.<extension>`. Artwork and its provenance
remain in `assets/artwork/`; research JSON retains source references that are
omitted from the infographic.

The saved examples contain 15 research records and 28 PNG iterations, including
Genshin Impact, Stellar Blade, Yakuza: Like a Dragon, Clair Obscur: Expedition 33,
The Legend of Zelda: Ocarina of Time, NieR:Automata, Shin Megami Tensei V: Vengeance,
Zenless Zone Zero, The First Descendant, original Atelier Ryza, Atelier Ryza 3 DX,
Persona 3 Reload, Honkai: Star Rail, THE FINALS and Crimson Desert.
Older iterations remain available as references. Some runs include a
`.validation.md` report; these reports are optional and are not currently required
by the skills. Research validation checks structure rather than factual truth;
player perspectives are sampled opinions and similar-game choices are editorial.

Release-date qualifications, artwork crops, layout omissions and source-access
limitations are documented in the corresponding round reports. Dates follow the
research skill’s earliest full-release rule across regions; timezone differences
can yield a local date before the advertised global launch day.
