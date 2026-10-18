# Katsuya's List — first rankings validation run

Branch: feature/personal-rankings; existing uncommitted first-pass rankings implementation.

- Heading: `Katsuya's List`, preserved exactly.
- Manifest: [katsuyas_list__2026-10-18T142424-0400__rankings-infographic.json](katsuyas_list__2026-10-18T142424-0400__rankings-infographic.json)
- Output: [1200 × 1600 PNG](png/katsuyas_list__2026-10-18T142424-0400__rankings-infographic.png)
- CLI `--check`: passed; all ten existing local artwork files decoded.
- Real Chromium CLI export: passed; fixed-canvas, equal-stripe and two-line-title layout checks passed.
- Pillow independently decoded output and confirmed PNG format and 1200 × 1600 dimensions.
- Manifest and all ten original images: SHA-256 hashes unchanged after rendering.
- No full game-research runs or GameMetadata files were used to prepare this manifest.
- Unit tests were not rerun for this artifact-only generation; prior rankings implementation validation reported 18 passing tests.

## Input interpretation

Rank order is exactly the supplied sequence; #1 is Zenless Zone Zero and #10 is
The First Descendant. Corrected the clear spelling error “The First Descandent”.
Expanded “Atelier Ryza 1” to “Atelier Ryza: Ever Darkness & the Secret Hideout”,
the original 2019 game, not DX. NieR: Automata punctuation follows the official
publisher-authored PlayStation post. No alternative titles are rendered.

## Visual review and limitations

All ten numbered titles are present, readable and fit on one line in this run.
The header/footer and all ten equal-height artwork bands fit the fixed canvas.
No text clipping or distortion was observed. This run does not exercise two-line
wrapping because none of these titles needs it at the current width/font size.

This is a first-pass design preview, not approval of the artwork composition.
The current overlay darkens the artwork heavily, especially the Clair Obscur and
Stellar Blade rows. Reused 16:9/wide hero assets are not consistently suitable for
these shallow stripes: the Honkai: Star Rail, Stellar Blade and Persona 3 Reload
crops omit or cut faces; NieR shows mainly scenery. The current renderer has no
per-image focal-position control, so no hand-tuned crop was applied. Artwork is
present in every row but its visual prominence and recognizability need review.
No renderer/style changes were made to conceal or fix these first-pass findings.

Existing artwork provenance documents the personal noncommercial local POC scope.
Official hosting is not a general commercial/public redistribution license.
Some title-check URLs were unavailable to the page reader; official publisher
PlayStation blog posts and the PlayStation Direct storefront supplied accessible
fallbacks. All chosen image identities also have existing provenance records.

## Inputs and title checks

| Rank | Checked title | Local artwork | Verification |
| --- | --- | --- | --- |
| 1 | Zenless Zone Zero | [Artwork](../../../assets/artwork/zenless_zone_zero/official_hero.jpg) / [provenance](../../../assets/artwork/zenless_zone_zero/official_hero.provenance.json) | [Official title check](https://www.playstation.com/en-us/games/zenless-zone-zero/) |
| 2 | Honkai: Star Rail | [Artwork](../../../assets/artwork/honkai_star_rail/official_hero.jpg) / [provenance](../../../assets/artwork/honkai_star_rail/official_hero.provenance.json) | [Official title check](https://www.playstation.com/en-us/games/honkai-star-rail/) |
| 3 | Genshin Impact | [Artwork](../../../assets/artwork/genshin_impact/official_launch.jpg) / [provenance](../../../assets/artwork/genshin_impact/official_launch.provenance.json) | [Official title check](https://blog.playstation.com/?p=341471) |
| 4 | Stellar Blade | [Artwork](../../../assets/artwork/stellar_blade/official_hero.jpg) / [provenance](../../../assets/artwork/stellar_blade/official_hero.provenance.json) | [Official title check](https://direct.playstation.com/en-us/buy-games/stellar-blade-ps5) |
| 5 | NieR: Automata | [Artwork](../../../assets/artwork/nier_automata/official_promo.jpg) / [provenance](../../../assets/artwork/nier_automata/official_promo.provenance.json) | [Official title check](https://blog.playstation.com/2016/12/22/nier-automata-demo-out-today-on-playstation-store/) |
| 6 | Clair Obscur: Expedition 33 | [Artwork](../../../assets/artwork/clair_obscur_expedition_33/official_hero.jpg) / [provenance](../../../assets/artwork/clair_obscur_expedition_33/official_hero.provenance.json) | [Official title check](https://blog.playstation.com/2024/10/16/introducing-the-cast-of-clair-obscur-expedition-33/) |
| 7 | Persona 3 Reload | [Artwork](../../../assets/artwork/persona_3_reload/official_screenshot.jpg) / [provenance](../../../assets/artwork/persona_3_reload/official_screenshot.provenance.json) | [Official title check](https://www.playstation.com/en-us/games/persona-3-reload/) |
| 8 | Atelier Ryza: Ever Darkness & the Secret Hideout | [Artwork](../../../assets/artwork/atelier_ryza/official_hero.jpg) / [provenance](../../../assets/artwork/atelier_ryza/official_hero.provenance.json) | [Official title check](https://www.koeitecmoamerica.com/games/atelier-ryza-ever-darkness-the-secret-hideout/) |
| 9 | Crimson Desert | [Artwork](../../../assets/artwork/crimson_desert/official_hero.jpg) / [provenance](../../../assets/artwork/crimson_desert/official_hero.provenance.json) | [Official title check](https://www.playstation.com/en-us/games/crimson-desert/) |
| 10 | The First Descendant | [Artwork](../../../assets/artwork/the_first_descendant/official_hero.jpg) / [provenance](../../../assets/artwork/the_first_descendant/official_hero.provenance.json) | [Official title check](https://www.playstation.com/en-us/games/the-first-descendant/) |

## Reproduce

```sh
.venv/bin/python -m game_infographic_generator rankings data/validation-runs/rankings/katsuyas_list__2026-10-18T142424-0400__rankings-infographic.json data/validation-runs/rankings/png/katsuyas_list__2026-10-18T142424-0400__rankings-infographic.png
```
