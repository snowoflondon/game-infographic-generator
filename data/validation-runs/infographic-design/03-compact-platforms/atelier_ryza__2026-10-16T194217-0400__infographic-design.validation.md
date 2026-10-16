# Atelier Ryza: Ever Darkness & the Secret Hideout — research and artwork stress test

Starting commit: `5b6a05617133db50d35686410d008612659ce061` plus the existing uncommitted title/overflow/platform-display refinements. No application, schema or skill changes were made for this run.

## Inputs and output

- Research: `data/validation-runs/game-research/atelier_ryza__2026-10-16T194217-0400__game-research.json`
- Presentation: `data/validation-runs/infographic-design/03-compact-platforms/atelier_ryza__2026-10-16T194217-0400__infographic-design.presentation.json`
- Artwork: `assets/artwork/atelier_ryza/official_hero.jpg`
- Provenance: `assets/artwork/atelier_ryza/official_hero.provenance.json`
- PNG: `data/validation-runs/infographic-design/03-compact-platforms/png/atelier_ryza__2026-10-16T194217-0400__infographic-design.png`

## Validation and inspection

- All top-level research fields present; Pydantic CLI validation passed (exit 0).
- Presentation schema and artwork decode validated by the rendering CLI.
- Real Chromium export passed fixed-canvas, two-line-title and overflow checks (exit 0).
- Pillow decoded the resulting PNG and confirmed exactly 1200 × 1600 pixels.
- SHA-256 input checks: metadata, presentation and original artwork unchanged by rendering.
- Visual inspection: Two-line title with a preferred break after the colon. Japanese alternative title readable; native 16:9 promotional composition retains the four central characters. Compact mode still requires Similar Games omission; it remains in research JSON. Readable text, no observed clipping or missing glyphs. Displayed dates, scores and original-language titles match validated input; overview/themes match separate presentation copy.
- Renderer warnings: Similar Games omitted to fit the compact layout; input metadata is unchanged..
- Platform display: `PlayStation 4 / Nintendo Switch / PC`.
- Actual validator and browser exports were exercised. No unit-suite rerun: application code was unchanged; the preceding implementation run reported 99 passing tests.

## Research qualifications

Original 2019 game, explicitly not DX. Earliest release September 26, 2019 in Japan on PS4 and Nintendo Switch; the official Japanese news archive says released today on that date. PC followed October 29, 2019, as did the North American release. The original edition platform list excludes DX-only PS5/Switch 2 releases. Similar Games are editorial comparisons.

Sentiment comes from the opened platform-specific user-review page, using qualitative positive and negative themes rather than assuming consensus. User reports do not independently verify technical complaints. Critic values were read from the opened matching game/edition/platform listing; aggregates may change later. Source attribution is retained in JSON, not printed in the infographic. Artwork is for the recorded personal noncommercial local test scope; no general redistribution license is asserted.

## Sources and claim mapping

- [Koei Tecmo — original title, studio and platforms](https://www.koeitecmoamerica.com/games/atelier-ryza-ever-darkness-the-secret-hideout/)
- [Official Japanese site — original-language title](https://www.gamecity.ne.jp/atelier/ryza/)
- [Official Japanese launch news — September 26, 2019; PC followed October 29](https://www.gamecity.ne.jp/atelier/ryza/topics.html)
- [Official systems and story overview](https://www.koeitecmoamerica.com/ryza/)
- [Official game page — overview and artwork](https://www.playstation.com/en-vn/games/atelier-ryza-ever-darkness-and-the-secret-hideout/)
- [Metacritic — edition and platform-specific critic score](https://www.metacritic.com/game/atelier-ryza-ever-darkness-and-the-secret-hideout/critic-reviews/?platform=playstation-4)
- [Metacritic — sampled player reviews](https://www.metacritic.com/game/atelier-ryza-ever-darkness-and-the-secret-hideout/user-reviews/?platform=playstation-4)

## Reproduce

```sh
.venv/bin/python -m game_infographic_generator single-game data/validation-runs/game-research/atelier_ryza__2026-10-16T194217-0400__game-research.json data/validation-runs/infographic-design/03-compact-platforms/png/atelier_ryza__2026-10-16T194217-0400__infographic-design.png --artwork assets/artwork/atelier_ryza/official_hero.jpg --presentation data/validation-runs/infographic-design/03-compact-platforms/atelier_ryza__2026-10-16T194217-0400__infographic-design.presentation.json
```
