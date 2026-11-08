# Honkai: Star Rail — selected-artwork single-game preview

- Starting commit: `ddc44d3b10345d0a69651d7aaf69fe6cf7cd3e5b`; existing uncommitted skill/documentation work retained.
- [PNG](png/honkai_star_rail__2026-11-07T203747-0500__infographic-design.png) — 1200 × 1600.
- [Research JSON](../../game-research/honkai_star_rail__2026-10-16T194217-0400__game-research.json)
- [Presentation copy](honkai_star_rail__2026-11-07T203747-0500__infographic-design.presentation.json)
- [Artwork](../../../../assets/artwork/honkai_star_rail/keyart__2026-11-07T203520-0500__game-asset-research.jpg) / [provenance](../../../../assets/artwork/honkai_star_rail/keyart__2026-11-07T203520-0500__game-asset-research.provenance.json)

## Validation and visual inspection

Existing metadata passed the CLI Pydantic validator. Used byte-identical copies
of the prior condensed presentation JSON; no new facts or research were added.
Actual Chromium export passed the renderer's image decoding, font readiness,
two-line title, canvas and overflow checks. Pillow decoded the final PNG and
confirmed exact dimensions. Visually inspected the PNG: artwork is present,
alternative titles render, and Similar Games remains visible. No existing PNG
was overwritten. Metadata, artwork, provenance and presentation hashes were
verified unchanged after rendering. No application code changed or unit suite rerun.

Version 4.2 key art is byte-identical to the earlier accepted hero. Both faces survive the native 16:9 frame. It is update-specific art, not a launch illustration.

Existing limitations: some metadata columns have cramped horizontal spacing,
particularly Honkai publisher/developer and adjacent release-date/genre values;
no layout fix was included in this artwork-only run. Research facts and date
qualifications are reused from the prior validation records, not freshly verified.

## Command

```sh
.venv/bin/python -m game_infographic_generator single-game data/validation-runs/game-research/honkai_star_rail__2026-10-16T194217-0400__game-research.json data/validation-runs/infographic-design/04-official-artwork/png/honkai_star_rail__2026-11-07T203747-0500__infographic-design.png --artwork assets/artwork/honkai_star_rail/keyart__2026-11-07T203520-0500__game-asset-research.jpg --presentation data/validation-runs/infographic-design/04-official-artwork/honkai_star_rail__2026-11-07T203747-0500__infographic-design.presentation.json
```
