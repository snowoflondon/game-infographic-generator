# Persona 3 Reload — research and artwork stress test

Starting commit: `5b6a05617133db50d35686410d008612659ce061` plus the existing uncommitted title/overflow/platform-display refinements. No application, schema or skill changes were made for this run.

## Inputs and output

- Research: `data/validation-runs/game-research/persona_3_reload__2026-10-16T194217-0400__game-research.json`
- Presentation: `data/validation-runs/infographic-design/03-compact-platforms/persona_3_reload__2026-10-16T194217-0400__infographic-design.presentation.json`
- Artwork: `assets/artwork/persona_3_reload/official_screenshot.jpg`
- Provenance: `assets/artwork/persona_3_reload/official_screenshot.provenance.json`
- PNG: `data/validation-runs/infographic-design/03-compact-platforms/png/persona_3_reload__2026-10-16T194217-0400__infographic-design.png`

## Validation and inspection

- All top-level research fields present; Pydantic CLI validation passed (exit 0).
- Presentation schema and artwork decode validated by the rendering CLI.
- Real Chromium export passed fixed-canvas, two-line-title and overflow checks (exit 0).
- Pillow decoded the resulting PNG and confirmed exactly 1200 × 1600 pixels.
- SHA-256 input checks: metadata, presentation and original artwork unchanged by rendering.
- Visual inspection: One-line title; Japanese alternative title readable. Full native 16:9 screenshot retained, including combat UI. Similar Games retained. Readable text, no observed clipping or missing glyphs. Displayed dates, scores and original-language titles match validated input; overview/themes match separate presentation copy.
- Renderer warnings: none.
- Platform display: `PlayStation 4 & 5 / Xbox One & Series X|S / PC / Nintendo Switch 2`.
- Actual validator and browser exports were exercised. No unit-suite rerun: application code was unchanged; the preceding implementation run reported 99 passing tests.

## Research qualifications

Reload remake only, excluding Episode Aigis DLC. Earliest local calendar release recorded as February 1, 2024 (North American Pacific PC storefront date); Steam shows February 1, while Atlus/Sega advertise February 2. Regional unlock reporting identifies 21:00 PST February 1 = February 2 elsewhere. This is a timezone distinction, not an early-access bonus. Nintendo Switch 2 followed October 23, 2025. Similar Games are editorial comparisons.

Sentiment comes from the opened platform-specific user-review page, using qualitative positive and negative themes rather than assuming consensus. User reports do not independently verify technical complaints. Critic values were read from the opened matching game/edition/platform listing; aggregates may change later. Source attribution is retained in JSON, not printed in the infographic. Artwork is for the recorded personal noncommercial local test scope; no general redistribution license is asserted.

## Sources and claim mapping

- [Sega Japan — original title, release and platforms](https://www.sega.jp/game/detail/p3re/)
- [Atlus — official February 2 launch date](https://atlus.com/persona-3-reload-and-persona-3-reload-expansion-pass-patch-notes-1-06-1-07/)
- [Steam — PC release date and developer/publisher](https://store.steampowered.com/app/2161700/Persona_3_Reload/)
- [VideoGamer — regional unlock timing](https://www.videogamer.com/news/persona-3-reload-release-time/)
- [Official game page — overview and artwork](https://www.playstation.com/en-us/games/persona-3-reload/)
- [Metacritic — edition and platform-specific critic score](https://www.metacritic.com/game/persona-3-reload/critic-reviews/?platform=pc)
- [Metacritic — sampled player reviews](https://www.metacritic.com/game/persona-3-reload/user-reviews/?platform=pc)

## Reproduce

```sh
.venv/bin/python -m game_infographic_generator single-game data/validation-runs/game-research/persona_3_reload__2026-10-16T194217-0400__game-research.json data/validation-runs/infographic-design/03-compact-platforms/png/persona_3_reload__2026-10-16T194217-0400__infographic-design.png --artwork assets/artwork/persona_3_reload/official_screenshot.jpg --presentation data/validation-runs/infographic-design/03-compact-platforms/persona_3_reload__2026-10-16T194217-0400__infographic-design.presentation.json
```
