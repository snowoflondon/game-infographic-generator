# Crimson Desert — research and artwork stress test

Starting commit: `5b6a05617133db50d35686410d008612659ce061` plus the existing uncommitted title/overflow/platform-display refinements. No application, schema or skill changes were made for this run.

## Inputs and output

- Research: `data/validation-runs/game-research/crimson_desert__2026-10-16T194217-0400__game-research.json`
- Presentation: `data/validation-runs/infographic-design/03-compact-platforms/crimson_desert__2026-10-16T194217-0400__infographic-design.presentation.json`
- Artwork: `assets/artwork/crimson_desert/official_hero.jpg`
- Provenance: `assets/artwork/crimson_desert/official_hero.provenance.json`
- PNG: `data/validation-runs/infographic-design/03-compact-platforms/png/crimson_desert__2026-10-16T194217-0400__infographic-design.png`

## Validation and inspection

- All top-level research fields present; Pydantic CLI validation passed (exit 0).
- Presentation schema and artwork decode validated by the rendering CLI.
- Real Chromium export passed fixed-canvas, two-line-title and overflow checks (exit 0).
- Pillow decoded the resulting PNG and confirmed exactly 1200 × 1600 pixels.
- SHA-256 input checks: metadata, presentation and original artwork unchanged by rendering.
- Visual inspection: One-line title; Hangul title readable. Centered 16:9 crop retains Kliff and the foreground female character; rightmost background figure and dragon are partially cropped. Similar Games retained. Readable text, no observed clipping or missing glyphs. Displayed dates, scores and original-language titles match validated input; overview/themes match separate presentation copy.
- Renderer warnings: none.
- Platform display: `PlayStation 5 / Xbox Series X|S / PC / macOS`.
- Actual validator and browser exports were exercised. No unit-suite rerun: application code was unchanged; the preceding implementation run reported 99 passing tests.

## Research qualifications

Base Crimson Desert release, not DLC or a different Black Desert game. Earliest global launch March 19, 2026 at 15:00 PDT (22:00 UTC); Korea/Japan local date March 20 is the same instant. Platforms include native macOS from the official launch announcement; handheld Windows hardware is not a separate platform. Current PS page uses Enhanced branding, but selected March 2026 launch artwork matches the base game. Player opinions span patches; critic aggregate is specifically PC and captured from the opened listing. Similar Games are editorial comparisons.

Sentiment comes from the opened platform-specific user-review page, using qualitative positive and negative themes rather than assuming consensus. User reports do not independently verify technical complaints. Critic values were read from the opened matching game/edition/platform listing; aggregates may change later. Source attribution is retained in JSON, not printed in the infographic. Artwork is for the recorded personal noncommercial local test scope; no general redistribution license is asserted.

## Sources and claim mapping

- [Pearl Abyss — worldwide launch and platforms](https://www.pearlabyss.com/en-US/Board/Detail?_boardNo=14684)
- [Official Korean site — original title](https://crimsondesert.pearlabyss.com/ko-KR/Main)
- [Pearl Abyss — launch is live](https://crimsondesert.pearlabyss.com/en-us/News/Notice/Detail?_boardNo=70)
- [Official game page — overview and artwork](https://www.playstation.com/en-us/games/crimson-desert/)
- [Metacritic — edition and platform-specific critic score](https://www.metacritic.com/game/crimson-desert/critic-reviews/?platform=pc)
- [Metacritic — sampled player reviews](https://www.metacritic.com/game/crimson-desert/user-reviews/?platform=pc)

## Reproduce

```sh
.venv/bin/python -m game_infographic_generator single-game data/validation-runs/game-research/crimson_desert__2026-10-16T194217-0400__game-research.json data/validation-runs/infographic-design/03-compact-platforms/png/crimson_desert__2026-10-16T194217-0400__infographic-design.png --artwork assets/artwork/crimson_desert/official_hero.jpg --presentation data/validation-runs/infographic-design/03-compact-platforms/crimson_desert__2026-10-16T194217-0400__infographic-design.presentation.json
```
