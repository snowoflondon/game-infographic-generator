# Round 01 — title wrapping and Similar Games labels

PNG images are stored in `png/`; presentation JSON and reports remain here.

Starting commit: `5b6a05617133db50d35686410d008612659ce061`.
The refinements currently exist as uncommitted changes on top of that commit.

Purpose: compare individual wrapping Similar Games labels and preferred title
breaks after a colon against the [accepted baseline](../baseline/README.md).
Keep the fixed canvas, artwork behavior, readable typography, and research contract.

The first three comparison examples are recorded below. Save future PNGs, separate
presentation JSON, and optional validation reports here using
`<game_slug>__<timestamp>__infographic-design` filenames with the appropriate extension.

Reuse [research inputs](../../game-research/) and
[artwork with provenance](../../../../assets/artwork/). For each example, add a row
below identifying the exact inputs and code revision (or uncommitted changes).
Use the same inputs as a baseline example when comparing layout alone.

| Output | Research input | Presentation input | Artwork input | Code revision / notes |
| --- | --- | --- | --- | --- |
| [Atelier Ryza 3 DX — failed layout](atelier_ryza_3_dx__2026-10-16T184508-0400__infographic-design.validation.md) | [Metadata](../../game-research/atelier_ryza_3_dx__2026-10-16T184508-0400__game-research.json) | [Copy](atelier_ryza_3_dx__2026-10-16T184508-0400__infographic-design.presentation.json) | [Artwork](../../../../assets/artwork/atelier_ryza_3_dx/official_dx_screenshot.jpg) | `5b6a056` + current uncommitted title/label refinements; normal and compact overflow; no PNG |
| [genshin_impact](png/genshin_impact__2026-10-16T183955-0400__infographic-design.png) | [Metadata](../../game-research/genshin_impact__2026-10-14T192010-0400__game-research.json) | [Copy](genshin_impact__2026-10-16T183955-0400__infographic-design.presentation.json) | [Artwork](../../../../assets/artwork/genshin_impact/official_launch.jpg) | `5b6a056` + uncommitted title/label refinements and compact label padding fix |
| [nier_automata](png/nier_automata__2026-10-16T183955-0400__infographic-design.png) | [Metadata](../../game-research/nier_automata__2026-10-15T220607-0400__game-research.json) | [Copy](nier_automata__2026-10-16T183955-0400__infographic-design.presentation.json) | [Artwork](../../../../assets/artwork/nier_automata/official_promo.jpg) | `5b6a056` + uncommitted title/label refinements and compact label padding fix |
| [stellar_blade](png/stellar_blade__2026-10-16T183955-0400__infographic-design.png) | [Metadata](../../game-research/stellar_blade__2026-10-14T192010-0400__game-research.json) | [Copy](stellar_blade__2026-10-16T183955-0400__infographic-design.presentation.json) | [Artwork](../../../../assets/artwork/stellar_blade/official_hero.jpg) | `5b6a056` + uncommitted title/label refinements and compact label padding fix |

When rendering is requested, inspect title break points, complete label text,
wrapping and canvas overflow.

First comparison run: all three outputs exported at 1200 × 1600 using unchanged
baseline inputs (presentation copies are byte-identical). Each image was visually
inspected. Genshin initially exceeded the compact layout bottom limit by less than
two pixels; reducing compact label vertical padding from 6px to 5px resolved it
without removing content or changing font sizes. The full suite passed: 82 tests.
These titles fit on one line, so this run does not visually exercise a long
colon-separated title wrapping onto two lines. Research facts were reused, not
re-researched for this visual comparison.
