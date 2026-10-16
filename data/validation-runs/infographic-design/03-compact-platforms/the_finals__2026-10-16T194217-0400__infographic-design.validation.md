# THE FINALS — research and artwork stress test

Starting commit: `5b6a05617133db50d35686410d008612659ce061` plus the existing uncommitted title/overflow/platform-display refinements. No application, schema or skill changes were made for this run.

## Inputs and output

- Research: `data/validation-runs/game-research/the_finals__2026-10-16T194217-0400__game-research.json`
- Presentation: `data/validation-runs/infographic-design/03-compact-platforms/the_finals__2026-10-16T194217-0400__infographic-design.presentation.json`
- Artwork: `assets/artwork/the_finals/official_hero.jpg`
- Provenance: `assets/artwork/the_finals/official_hero.provenance.json`
- PNG: `data/validation-runs/infographic-design/03-compact-platforms/png/the_finals__2026-10-16T194217-0400__infographic-design.png`

## Validation and inspection

- All top-level research fields present; Pydantic CLI validation passed (exit 0).
- Presentation schema and artwork decode validated by the rendering CLI.
- Real Chromium export passed fixed-canvas, two-line-title and overflow checks (exit 0).
- Pillow decoded the resulting PNG and confirmed exactly 1200 × 1600 pixels.
- SHA-256 input checks: metadata, presentation and original artwork unchanged by rendering.
- Visual inspection: One-line title. Centered 16:9 crop retains the masked character’s face and weapon, while removing peripheral parts of the wide source. Similar Games retained. Readable text, no observed clipping or missing glyphs. Displayed dates, scores and original-language titles match validated input; overview/themes match separate presentation copy.
- Renderer warnings: none.
- Platform display: `PC / PlayStation 5 / Xbox Series X|S`.
- Actual validator and browser exports were exercised. No unit-suite rerun: application code was unchanged; the preceding implementation run reported 99 passing tests.

## Research qualifications

Earliest local release December 7, 2023, North American PS5 launch announcement; Steam/Xbox/PlayStation storefronts can show December 8 from regional timing. Sweden-origin Embark is the credited developer/publisher despite Nexon ownership; no distinct original-language title was verified, so alternative_titles is empty. Listed platforms are verified native releases from the opened current storefronts; no Xbox One or cloud-only device is inferred. Similar Games are editorial comparisons. Player complaints are attributed sampled opinions, not independently verified server or cheating claims.

Sentiment comes from the opened platform-specific user-review page, using qualitative positive and negative themes rather than assuming consensus. User reports do not independently verify technical complaints. Critic values were read from the opened matching game/edition/platform listing; aggregates may change later. Source attribution is retained in JSON, not printed in the infographic. Artwork is for the recorded personal noncommercial local test scope; no general redistribution license is asserted.

## Sources and claim mapping

- [Embark launch announcement — December 7 in North America](https://blog.playstation.com/2023/12/07/the-finals-launches-on-ps5-today/)
- [Steam — PC game and studio](https://store.steampowered.com/app/2073850/THE_FINALS/)
- [Xbox — developer, publisher and Series X|S](https://www.xbox.com/en-US/games/store/the-finals/9pgd71cmds0z)
- [Official game page — overview and artwork](https://www.playstation.com/en-us/games/the-finals/)
- [Metacritic — edition and platform-specific critic score](https://www.metacritic.com/game/the-finals/critic-reviews/?platform=pc)
- [Metacritic — sampled player reviews](https://www.metacritic.com/game/the-finals/user-reviews/?platform=pc)

## Reproduce

```sh
.venv/bin/python -m game_infographic_generator single-game data/validation-runs/game-research/the_finals__2026-10-16T194217-0400__game-research.json data/validation-runs/infographic-design/03-compact-platforms/png/the_finals__2026-10-16T194217-0400__infographic-design.png --artwork assets/artwork/the_finals/official_hero.jpg --presentation data/validation-runs/infographic-design/03-compact-platforms/the_finals__2026-10-16T194217-0400__infographic-design.presentation.json
```
