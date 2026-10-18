# Katsuya's List — gradient, half-width titles and focal positioning

- [PNG](png/katsuyas_list__2026-10-18T143916-0400__rankings-infographic.png); [manifest](katsuyas_list__2026-10-18T143916-0400__rankings-infographic.json).
- Fixed 1200 × 1600 canvas; ten equal full-width stripes and original order.
- Heading displayed uppercase via CSS; original manifest heading unchanged.
- All game titles bottom-left within the left half. No numbering or title boxes.
- Consistent gradient: 82% black on the left, 70% at the midpoint, fading to transparent at the right edge; white text remains on the dark half.
- Added optional validated `artwork_focal_point` x/y percentages (0–100, default 50/50). Values are CSS object-position alignment percentages, not normalized source-image face coordinates. Source proportions and artwork bytes are unchanged.
- CLI check and real Chromium export passed; Pillow confirmed dimensions and decoding. All previous manifests/PNGs were SHA-256 verified unchanged.
- Visual review: no title clipping, heading uppercase, all titles in left half. Original Atelier Ryza uses two-line natural wrapping; colon grouping would exceed that budget. Faces are visible in Honkai, Stellar Blade, Persona and Crimson Desert where prior centered crops omitted them.
- Limits: shallow crops still omit secondary group faces and parts of close-ups (especially Clair Obscur); NieR's character remains small in the original landscape. Gradient intentionally darkens the left area but retains right-side artwork visibility. No artwork was generated, recolored or replaced.

## Focal settings

| Game | x | y |
| --- | --- | --- |
| Zenless Zone Zero | 50 | 55 |
| Honkai: Star Rail | 50 | 18 |
| Genshin Impact | 50 | 48 |
| Stellar Blade | 50 | 80 |
| NieR: Automata | 50 | 95 |
| Clair Obscur: Expedition 33 | 50 | 25 |
| Persona 3 Reload | 50 | 18 |
| Atelier Ryza: Ever Darkness & the Secret Hideout | 50 | 36 |
| Crimson Desert | 50 | 25 |
| The First Descendant | 50 | 20 |

## Reproduce

```sh
.venv/bin/python -m game_infographic_generator rankings data/validation-runs/rankings/katsuyas_list__2026-10-18T143916-0400__rankings-infographic.json data/validation-runs/rankings/png/katsuyas_list__2026-10-18T143916-0400__rankings-infographic.png
```

Original title-check evidence and artwork permissions are retained in the first
run report and the artwork provenance sidecars. No full game-research was run.
