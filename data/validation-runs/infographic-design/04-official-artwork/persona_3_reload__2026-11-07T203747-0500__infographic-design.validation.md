# Persona 3 Reload — title-free artwork revision

The user authorized overwriting this run's prior branded-art PNG. Filename and
output path are retained; the source metadata and presentation copy are unchanged.

- [PNG](png/persona_3_reload__2026-11-07T203747-0500__infographic-design.png) — 1200 × 1600.
- [Research JSON](../../../../data/validation-runs/game-research/persona_3_reload__2026-10-16T194217-0400__game-research.json)
- [Presentation copy](persona_3_reload__2026-11-07T203747-0500__infographic-design.presentation.json)
- [Selected artwork](../../../../assets/artwork/persona_3_reload/official_title_free_hero__2026-11-07T204422-0500__game-asset-research.jpg) / [provenance](../../../../assets/artwork/persona_3_reload/official_title_free_hero__2026-11-07T204422-0500__game-asset-research.provenance.json)

## Asset selection and test

Rejected the former branded illustration because it repeats the game's title.
Official portrait character art has poor centered 16:9 compatibility; the release
commemorative poster also contains title text. The official moon background has
weaker game identity. Selected the 1920 × 1080 Hero profile illustration linked
from the Persona 3 Reload publisher storefront's Points Shop section. It depicts
the protagonist and butterflies, contains no game title/logo, is not a gameplay
screenshot and has no third-party watermark. A decorative numeral 3 remains; it
is not the game title or title logo. Dark shading is baked into the original.

Pillow decoding passed. Actual Chromium export passed the renderer's image/font,
canvas, title-limit and overflow checks. Visually inspected the final PNG: no
repeated game title in the artwork, face remains visible, native 16:9 framing
requires no material crop, Similar Games retained, alternative title readable.
Confirmed exact 1200 × 1600 PNG dimensions and unchanged metadata, presentation,
artwork and provenance hashes. Previous PNG replaced only after successful capture.
No renderer or schema edits; no unit-suite rerun needed for these skill changes.

Original branded source artwork and historical reports were preserved.
Official source availability does not establish public redistribution/commercial
reuse permission. This remains a user-requested local visual preview.

## Command

```sh
.venv/bin/python -m game_infographic_generator single-game data/validation-runs/game-research/persona_3_reload__2026-10-16T194217-0400__game-research.json data/validation-runs/infographic-design/04-official-artwork/png/persona_3_reload__2026-11-07T203747-0500__infographic-design.png --artwork assets/artwork/persona_3_reload/official_title_free_hero__2026-11-07T204422-0500__game-asset-research.jpg --presentation data/validation-runs/infographic-design/04-official-artwork/persona_3_reload__2026-11-07T203747-0500__infographic-design.presentation.json
```
