# Honkai: Star Rail — research and artwork stress test

Starting commit: `5b6a05617133db50d35686410d008612659ce061` plus the existing uncommitted title/overflow/platform-display refinements. No application, schema or skill changes were made for this run.

## Inputs and output

- Research: `data/validation-runs/game-research/honkai_star_rail__2026-10-16T194217-0400__game-research.json`
- Presentation: `data/validation-runs/infographic-design/03-compact-platforms/honkai_star_rail__2026-10-16T194217-0400__infographic-design.presentation.json`
- Artwork: `assets/artwork/honkai_star_rail/official_hero.jpg`
- Provenance: `assets/artwork/honkai_star_rail/official_hero.provenance.json`
- PNG: `data/validation-runs/infographic-design/03-compact-platforms/png/honkai_star_rail__2026-10-16T194217-0400__infographic-design.png`

## Validation and inspection

- All top-level research fields present; Pydantic CLI validation passed (exit 0).
- Presentation schema and artwork decode validated by the rendering CLI.
- Real Chromium export passed fixed-canvas, two-line-title and overflow checks (exit 0).
- Pillow decoded the resulting PNG and confirmed exactly 1200 × 1600 pixels.
- SHA-256 input checks: metadata, presentation and original artwork unchanged by rendering.
- Visual inspection: One-line title; Traditional Chinese title readable. Native 16:9 version 4.2 artwork retains both faces without the problematic crop from the rejected wider hero. Similar Games retained. Readable text, no observed clipping or missing glyphs. Displayed dates, scores and original-language titles match validated input; overview/themes match separate presentation copy.
- Renderer warnings: none.
- Platform display: `PC / Mobile / PlayStation 5`.
- Actual validator and browser exports were exercised. No unit-suite rerun: application code was unchanged; the preceding implementation run reported 99 passing tests.

## Research qualifications

Earliest local calendar date April 25, 2023 for PC/mobile in the Americas: the publisher launch timestamp April 26 10:00 UTC+8 converts to April 25 19:00 PDT. The globally advertised date is April 26; the model has no timezone field, so this interpretation is documented here. PS5 released later. Official news pages are JavaScript-heavy: their launch/platform text was available in indexed results but not the page reader; the launch timestamp could not be re-extracted from rendered page text. Traditional Chinese title is copied from the official regional page. Artwork depicts a later live-service update; sentiment spans versions. Similar Games are editorial comparisons.

Sentiment comes from the opened platform-specific user-review page, using qualitative positive and negative themes rather than assuming consensus. User reports do not independently verify technical complaints. Critic values were read from the opened matching game/edition/platform listing; aggregates may change later. Source attribution is retained in JSON, not printed in the infographic. Artwork is for the recorded personal noncommercial local test scope; no general redistribution license is asserted.

## Sources and claim mapping

- [HoYoverse — version 1.0 went live April 26 at 10:00 UTC+8](https://hsr.hoyoverse.com/en-us/news/111258)
- [HoYoverse — PC, iOS, Android and PS5 platform announcement](https://www.hoyoverse.com/en-us/news/123644)
- [Official Chinese-language PlayStation page — original title](https://www.playstation.com/zh-hant-tw/games/honkai-star-rail/)
- [Official game page — overview and artwork](https://www.playstation.com/en-us/games/honkai-star-rail/)
- [Metacritic — edition and platform-specific critic score](https://www.metacritic.com/game/honkai-star-rail/critic-reviews/?platform=pc)
- [Metacritic — sampled player reviews](https://www.metacritic.com/game/honkai-star-rail/user-reviews/?platform=pc)

## Reproduce

```sh
.venv/bin/python -m game_infographic_generator single-game data/validation-runs/game-research/honkai_star_rail__2026-10-16T194217-0400__game-research.json data/validation-runs/infographic-design/03-compact-platforms/png/honkai_star_rail__2026-10-16T194217-0400__infographic-design.png --artwork assets/artwork/honkai_star_rail/official_hero.jpg --presentation data/validation-runs/infographic-design/03-compact-platforms/honkai_star_rail__2026-10-16T194217-0400__infographic-design.presentation.json
```
