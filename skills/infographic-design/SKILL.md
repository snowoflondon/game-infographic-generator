---
name: infographic-design
description: Implement or refine the single-game portrait infographic renderer using Python, Pydantic, Jinja2, HTML/CSS, and Playwright Chromium. Use for rendering pipeline, template, export, and rendering tests; exclude game research and personal rankings.
---

# Infographic Design

## Objective and Scope

Render validated game metadata as a reusable, detailed portrait infographic PNG.
When asked to draft or review a design, return that design without implementing
the pipeline. Implement only when the user requests implementation.

- Preserve the existing research skill, JSON contract, Pydantic models, and
  validation workflow. Rendering must not research or rewrite game metadata;
  the agent may discover artwork through the separate procedure below.
- No hardcoded game metadata in this skill, renderer, templates, or styles.
  Game-specific values come exclusively from the supplied metadata. Existing
  fixtures may be used as test input, never as rendering defaults.
- Keep the single-game renderer separate from future rankings rendering.
  Share utilities only when concrete reuse warrants it; avoid base renderer
  classes, plugin systems, and premature abstractions.

## Stack and Data Flow

Use Python to orchestrate this pipeline:

```text
JSON file → existing GameMetadata validation → Jinja2 HTML + CSS
          → Playwright Python API + Chromium → PNG
```

Use Jinja2 for data injection and HTML/CSS for layout, typography, colors, and
spacing. Use the Python Playwright package; do not introduce React, a Node.js
application, npm tooling, or a frontend build pipeline. Playwright's packaged
runtime is an implementation detail, not a separate application stack.

## Implementation Procedure

1. Inspect repository guidance, `models.py`, the existing CLI and validation
   tests, the research contract, and sample JSON. Reuse the current validation
   behavior rather than creating a parallel schema.
2. Put rendering orchestration in `rendering/single_game.py`, with packaged
   template and stylesheet resources nearby. Prefer small typed functions and
   a renderer that accepts `GameMetadata` and an output path. Keep visual styling
   in CSS, separate from Python application logic, and template generation
   separately testable from browser capture.
3. Add a `single-game` subcommand to the existing CLI, accepting a metadata JSON path
   and an output PNG path. Preserve existing commands and readiness behavior.
   Validate before launching Chromium or creating the output image. Report
   invalid input, missing Chromium, and export failures clearly with nonzero
   exit status; release browser resources on success and failure.
4. Declare Jinja2 and Playwright as rendering dependencies in `pyproject.toml`
   when implementing. These are the requested stack; do not introduce additional
   frameworks. Include template/CSS resources in package distributions so
   rendering works independently of the current working directory.
5. Implement the layout and capture requirements below, then run relevant tests
   and inspect an actual exported PNG before reporting completion.

## Template and Visual Requirements

- Use a fixed 1200 × 1600 CSS-pixel canvas with a 3:4 portrait ratio. Do not
  expand the canvas, clip content, or introduce scroll containers. Wrap long
  titles and text without horizontal overflow. Fit content through layout and
  spacing adjustments while keeping text readable; if all content cannot fit,
  report the limitation rather than silently truncating or rewriting metadata.
- Use this section order, omitting unavailable content:
  1. Header: dominant game title, alternative titles beneath it, and release year
     plus primary genre when available. Derive the year from `release_date`;
     use the first supplied genre without inventing a classification.
  2. Full-width 16:9 hero artwork directly beneath the title when artwork mode
     is requested; artwork remains mandatory in that mode.
  3. Metadata: developer, publisher, full release date, genres, and platforms in
     a structured grid. Place metadata and critic scores in one two-column
     section with approximately 2:1 widths; use full width when one is absent.
  4. Critic scores: prominent values with source, platform, and original maximum
     together. Preserve values and scales; do not normalize or invent scores.
  5. Overview: supplied description, set for readability rather than density.
  6. Player sentiment: summary and positive/negative themes in balanced columns
     in subtle contrasting neutral panels, with equal column widths. Preserve qualifications and
     never imply that sampled opinions are a consensus.
  7. Similar games: a compact, readable list.
  8. Footer: minimal project branding.
- Omit sources entirely from the infographic: no sources section, reference
  notes, citation markers, or source URLs, including critic review links. Keep
  critic aggregator names and platforms as score labels. Retain all source data
  unchanged in the original research JSON for traceability.
- Make typography the primary visual element. Use a modern, minimal editorial
  aesthetic using a modern sans-serif typeface. At the fixed canvas width,
  use these CSS-pixel ranges as starting points: main title 64–80, bold; section
  headings 18–22, uppercase where the script supports case; body 24–28;
  metadata labels 16–20; critic score 72–96, bold. The title remains the dominant
  overall element even when scores use larger numerals. Set alternative titles
  below it at a subordinate but comfortably readable size. Keep line heights
  and letter spacing consistent by text role, adapting for multilingual scripts.
- Organize content through generous whitespace, consistent alignment, and
  spacing. Prioritize clarity, hierarchy, and readability over information
  density. Balance sections within the fixed canvas rather than crowding them
  or shrinking text excessively. Avoid unnecessary decorations, ornamental
  badges, and clutter. Avoid repeated horizontal dividers; use whitespace,
  typography, and panel backgrounds for hierarchy. Keep the footer in the
  content flow rather than pinning it to the bottom with a large empty gap.
- Keep background, primary/secondary text, neutral panels, and layout consistent
  across games. Extract accents automatically from supplied local artwork
  using Pillow, without recoloring the source image or modifying metadata.
  Use fixed sampling, stable ranking/tie-breaking, and a moderate-saturation
  filter. Select a distinctive candidate with at least 4.5:1 contrast against
  the background; otherwise use a fixed contrast-safe fallback. Invalid images
  must fail, not trigger a color fallback. Determinism is scoped to the same
  artwork and installed dependency versions.
- Pass theme colors through CSS variables. Use the accent for section headings,
  critic score card backgrounds, and a restrained decorative rule. Choose dark
  or light card text with at least 4.5:1 contrast against the accent. Keep the
  main title and body text neutral. No manual accent CLI option is provided.
- Default mode renders full metadata, excluding sources, without artwork. Artwork
  is opt-in through `--artwork`; use a fixed fallback accent when absent.
- Artwork mode requires an image and a separate `--presentation` JSON containing
  `overview` (one sentence or null), `highlights` and `criticisms` (short phrase
  arrays). Codex derives faithful condensed copy from the original description
  and positive/negative sentiment themes. Preserve uncertainty and mixed opinions;
  omit the long sentiment summary but label these as sampled player opinions.
  Keep similar games and all other factual fields. Never edit the research JSON
  or use string truncation as semantic summarization. Standalone CLI callers
  supply their own condensed copy; Python validates structure, not faithfulness.
- Artwork mode uses a full-width 16:9 hero beneath the title in both normal and
  compact layouts. Fit the source proportionally with `object-fit: cover` and a
  deliberate focal position (center by default). Inspect crops to preserve
  important subjects and embedded text; never stretch or distort the image.
  Preserve all existing display content and readable typography without further
  condensation or removal. Compact mode reduces spacing, not hero prominence.
  Try normal layout
  then compact with the full-width 16:9 hero retained; fail explicitly if neither fits. Never
  drop requested artwork or truncate content to force a successful export.
- Omit absent optional values and empty sections, including headings, dividers,
  or labels that would otherwise stand alone. Handle a title-only model cleanly.
  Do not display literal `None`/`null`, fabricated filler, or empty score cards.
- Preserve supplied Unicode text. Choose fonts/fallbacks covering Japanese,
  Korean, and Chinese and document installation or bundling requirements.
  Use local assets/fonts where possible for reliable, repeatable rendering.
- Enable Jinja2 HTML autoescaping. Treat metadata as text, not executable HTML
  or CSS; do not mark user content safe.

## Artwork Discovery

Artwork discovery is required only when the user requests artwork. If the user supplies an approved image, inspect and verify that asset
instead of searching for a replacement. Drafting or editing this skill does not
itself trigger discovery.

1. Confirm the exact game and edition from the input metadata.
2. Search for official promotional artwork, preferring developer/publisher
   media assets, then official cover artwork, then official gameplay screenshots.
   Open the source page and verify the image belongs to the specified edition;
   never invent URLs or rely on search thumbnails alone.
3. Select a high-resolution image suitable for the designated artwork region,
   preferably with room for controlled cropping. Avoid watermarks, unrelated
   imagery, and fan art without appropriate permission. Check the actual image
   for quality, proportions, and important subjects before selecting it.
4. Inspect any published usage terms. Official availability or appearance in
   search results does not establish permission to reuse an image. If the
   intended use is unclear or restricted, report the permission blocker rather than claiming reuse is authorized.
5. Download suitable, permitted artwork to `assets/artwork/<game_slug>/` in a
   renderer-supported format. Record the source page URL, direct image URL,
   retrieval date, local filename, and known usage terms or permission evidence
   in a sidecar provenance file. Keep this separate from the research JSON;
   do not add unsupported metadata fields or place provenance on the infographic.
6. Validate the downloaded file: check its format, decode it, verify positive
   dimensions, and visually confirm quality and the exact game/edition before
   rendering. A filename extension alone is not validation. Pass the local path
   through optional `--artwork` (which makes inclusion mandatory for that run). If discovery, permission,
   download, or decoding fails, report failure; do not generate a typography-only
   substitute for a requested artwork run. Missing requested artwork must fail before Chromium launches.

## PNG Capture

- Use headless Chromium through Playwright's Python API. Default device scale
  factor to 1 so the PNG is exactly 1200 × 1600 pixels.
- Wait for document layout, font loading, and any local images to finish before
  capture. Verify content fits within the fixed canvas before exporting it,
  without browser chrome, unexpected margins, or cropped content.
- Preserve any existing output PNG on every failure. Capture and verify the PNG
  first, then publish through a temporary file and atomic replacement.
- Avoid animation and remote asset dependencies. Use bounded readiness waits;
  report failures rather than silently exporting an incomplete image.

## Verification and Documentation

- Test template output with complete metadata, title-only metadata, partially
  populated nested objects, long text, Unicode alternative titles, and HTML-like
  text. Check meaningful behavior such as escaping and omitted empty sections.
- Test validation failure before rendering and preserve existing CLI tests.
- Add a Chromium integration test that generates a real PNG in a temporary
  directory and checks the PNG format, exact 1200 × 1600 dimensions, and absence
  of overflow. Test that source references are absent from rendered HTML while
  the original metadata and research JSON remain unchanged.
  Report browser-dependent tests separately if Chromium is unavailable; do not
  present a mocked screenshot as proof that export works.
- Before completion, verify successful PNG export and visually inspect it for
  title wrapping, legibility, missing glyphs, clipping, spacing, and alignment.
  Confirm displayed facts, dates, scores, and original-language titles match
  the validated JSON, allowing only faithful presentation formatting. Fix
  observed issues without changing metadata or adding unsupported claims.
- Test palette extraction, neutral/transparent fallback, deterministic selection,
  contrast, fixed neutral colors, CSS variables, and unchanged artwork bytes.
- Test both normal and compact artwork layouts, missing/corrupt artwork, and
  overflow failure. Verify artwork remains present in every successful artwork-mode export; test
  full text-only mode separately.
- Document rendering dependency installation, `python -m playwright install
  chromium`, any platform system/font prerequisites, the implemented CLI usage,
  output dimensions, and test commands in README. Clearly distinguish current
  functionality from the future rankings workflow.

## Completion Report

Report changed files, the implemented render command, output path and dimensions,
tests run/results, visual inspection findings, and any limitations or setup steps
that remain. For artwork-mode generation requests, include the artwork path, presentation
copy path, and provenance file, or explain the failure that prevented export. For draft-only requests, summarize the proposed design and open
decisions instead; do not install dependencies or claim rendering was tested.
