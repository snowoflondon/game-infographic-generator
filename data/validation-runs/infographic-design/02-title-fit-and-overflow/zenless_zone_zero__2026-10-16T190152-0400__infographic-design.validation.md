# Zenless Zone Zero — artwork validation run

Starting commit: `5b6a05617133db50d35686410d008612659ce061` plus current round-02 working-tree changes. No renderer, template or schema changes were made for this example.

- Research input: `data/validation-runs/game-research/zenless_zone_zero__2026-10-16T190152-0400__game-research.json`
- Presentation input: `data/validation-runs/infographic-design/02-title-fit-and-overflow/zenless_zone_zero__2026-10-16T190152-0400__infographic-design.presentation.json`
- Artwork: `assets/artwork/zenless_zone_zero/official_hero.jpg`
- Artwork provenance: `assets/artwork/zenless_zone_zero/official_hero.provenance.json`
- Output: `data/validation-runs/infographic-design/02-title-fit-and-overflow/png/zenless_zone_zero__2026-10-16T190152-0400__infographic-design.png`
- Pydantic CLI validation: passed (exit 0).
- Chromium CLI export: passed (exit 0); Pillow decoded PNG and confirmed 1200 × 1600.
- Research, presentation and artwork SHA-256 hashes unchanged by rendering: True.
- Layout: Similar Games retained. All main titles fit one line at the resulting compact size; these examples do not exercise two-line wrapping.
- Visual review: artwork present in a full-width 16:9 region without distortion; central subjects retained; original-language titles readable; dates, platform-specific scores and presentation copy match inputs; no text clipping observed. Wide source artwork for Zenless Zone Zero and The First Descendant loses peripheral content through centered proportional cropping; no claim is made that the entire source composition is retained.
- Checks were the actual metadata validators and three real browser exports; the unit suite was not rerun because application code was unchanged.

## Research qualifications

Earliest full global release: July 4, 2024, on PC, mobile and PS5; Xbox followed later. Publisher uses the official storefront legal credit COGNOSPHERE; developer uses HoYoverse branding from the producer. Critic score is specifically PS5, not the PC score. Sentiment explicitly describes a launch-era sample, not current-version consensus. Artwork is the official page’s later live-service promotional image, not a launch image. Similar Games are editorial comparisons.

Supporting source URLs are retained in the research JSON. Artwork URLs and personal/noncommercial usage scope are retained separately in provenance. Official hosting does not grant a general redistribution license.

## Reproduce

```sh
.venv/bin/python -m game_infographic_generator single-game data/validation-runs/game-research/zenless_zone_zero__2026-10-16T190152-0400__game-research.json data/validation-runs/infographic-design/02-title-fit-and-overflow/png/zenless_zone_zero__2026-10-16T190152-0400__infographic-design.png --artwork assets/artwork/zenless_zone_zero/official_hero.jpg --presentation data/validation-runs/infographic-design/02-title-fit-and-overflow/zenless_zone_zero__2026-10-16T190152-0400__infographic-design.presentation.json
```
