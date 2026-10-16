# Round 03 — compact platform labels

PNG images are stored in `png/`; presentation JSON and reports remain here.

Starting commit: `5b6a05617133db50d35686410d008612659ce061` plus existing working-tree title/overflow refinements and this display-only platform formatter.

Group supplied iOS/Android as Mobile and share known console family prefixes.
Research JSON, schema, artwork, critic-score platform labels and presentation copy
are unchanged. Previous outputs remain in their original design rounds.
No research was refreshed for these visual comparisons.

Verification: **99 tests passed in 16.25s** with Chromium access. All six inputs
passed CLI metadata validation, all six real browser exports passed the existing
canvas/title/overflow checks, and Pillow confirmed 1200 × 1600 PNGs. All six were
visually inspected for platform labels, artwork, Unicode, readable text and clipping.
Similar Games is retained in every output, including SMT V: Vengeance, where it
was omitted in round 02. SHA-256 checks confirmed metadata, presentation and artwork
were unchanged by rendering; presentation copies are byte-identical to prior runs.
The skill validator script could not run because its PyYAML dependency is absent;
the narrow skill edit was reviewed manually without adding a dependency.

| Output | Research | Presentation | Artwork / provenance | Displayed platforms |
| --- | --- | --- | --- | --- |
| [Zenless Zone Zero](png/zenless_zone_zero__2026-10-16T190859-0400__infographic-design.png) | [JSON](../../game-research/zenless_zone_zero__2026-10-16T190152-0400__game-research.json) | [Copy](zenless_zone_zero__2026-10-16T190859-0400__infographic-design.presentation.json) | [Image](../../../../assets/artwork/zenless_zone_zero/official_hero.jpg) / [provenance](../../../../assets/artwork/zenless_zone_zero/official_hero.provenance.json) | PC / Mobile / PlayStation 5 / Xbox Series X&#124;S |
| [Shin Megami Tensei V: Vengeance](png/shin_megami_tensei_v_vengeance__2026-10-16T190859-0400__infographic-design.png) | [JSON](../../game-research/shin_megami_tensei_v_vengeance__2026-10-16T190152-0400__game-research.json) | [Copy](shin_megami_tensei_v_vengeance__2026-10-16T190859-0400__infographic-design.presentation.json) | [Image](../../../../assets/artwork/shin_megami_tensei_v_vengeance/official_hero.jpg) / [provenance](../../../../assets/artwork/shin_megami_tensei_v_vengeance/official_hero.provenance.json) | Nintendo Switch / PlayStation 4 & 5 / Xbox One & Series X&#124;S / PC |
| [NieR:Automata](png/nier_automata__2026-10-16T190859-0400__infographic-design.png) | [JSON](../../game-research/nier_automata__2026-10-15T220607-0400__game-research.json) | [Copy](nier_automata__2026-10-16T190859-0400__infographic-design.presentation.json) | [Image](../../../../assets/artwork/nier_automata/official_promo.jpg) / [provenance](../../../../assets/artwork/nier_automata/official_promo.provenance.json) | PlayStation 4 / PC |
| [Stellar Blade](png/stellar_blade__2026-10-16T190859-0400__infographic-design.png) | [JSON](../../game-research/stellar_blade__2026-10-14T192010-0400__game-research.json) | [Copy](stellar_blade__2026-10-16T190859-0400__infographic-design.presentation.json) | [Image](../../../../assets/artwork/stellar_blade/official_hero.jpg) / [provenance](../../../../assets/artwork/stellar_blade/official_hero.provenance.json) | PlayStation 5 / PC |
| [Genshin Impact](png/genshin_impact__2026-10-16T190859-0400__infographic-design.png) | [JSON](../../game-research/genshin_impact__2026-10-14T192010-0400__game-research.json) | [Copy](genshin_impact__2026-10-16T190859-0400__infographic-design.presentation.json) | [Image](../../../../assets/artwork/genshin_impact/official_launch.jpg) / [provenance](../../../../assets/artwork/genshin_impact/official_launch.provenance.json) | PC / Mobile / PlayStation 5 / Xbox Series X&#124;S |
| [Clair Obscur: Expedition 33](png/clair_obscur_expedition_33__2026-10-16T190859-0400__infographic-design.png) | [JSON](../../game-research/clair_obscur_expedition_33__2026-10-14T193235-0400__game-research.json) | [Copy](clair_obscur_expedition_33__2026-10-16T190859-0400__infographic-design.presentation.json) | [Image](../../../../assets/artwork/clair_obscur_expedition_33/official_hero.jpg) / [provenance](../../../../assets/artwork/clair_obscur_expedition_33/official_hero.provenance.json) | PlayStation 5 / Xbox Series X&#124;S / PC |

| [The Legend of Zelda: Ocarina of Time](png/the_legend_of_zelda_ocarina_of_time__2026-10-16T193441-0400__infographic-design.png) | [JSON](../../game-research/the_legend_of_zelda_ocarina_of_time__2026-10-15T214718-0400__game-research.json) | [Copy](the_legend_of_zelda_ocarina_of_time__2026-10-16T193441-0400__infographic-design.presentation.json) | [Image](../../../../assets/artwork/the_legend_of_zelda_ocarina_of_time/official_link_ganondorf.webp) / [provenance](../../../../assets/artwork/the_legend_of_zelda_ocarina_of_time/official_link_ganondorf.provenance.json) | Nintendo 64 |
| [Atelier Ryza 3: Alchemist of the End & the Secret Key DX](png/atelier_ryza_3_dx__2026-10-16T193441-0400__infographic-design.png) | [JSON](../../game-research/atelier_ryza_3_dx__2026-10-16T184508-0400__game-research.json) | [Copy](atelier_ryza_3_dx__2026-10-16T193441-0400__infographic-design.presentation.json) | [Image](../../../../assets/artwork/atelier_ryza_3_dx/official_dx_screenshot.jpg) / [provenance](../../../../assets/artwork/atelier_ryza_3_dx/official_dx_screenshot.provenance.json) | PlayStation 4 & 5 / Nintendo Switch & Switch 2 / PC |

| [Persona 3 Reload](png/persona_3_reload__2026-10-16T194217-0400__infographic-design.png) | [JSON](../../game-research/persona_3_reload__2026-10-16T194217-0400__game-research.json) | [Copy](persona_3_reload__2026-10-16T194217-0400__infographic-design.presentation.json) | [Image](../../../../assets/artwork/persona_3_reload/official_screenshot.jpg) / [provenance](../../../../assets/artwork/persona_3_reload/official_screenshot.provenance.json) | PlayStation 4 & 5 / Xbox One & Series X&#124;S / PC / Nintendo Switch 2 |
| [Atelier Ryza: Ever Darkness & the Secret Hideout](png/atelier_ryza__2026-10-16T194217-0400__infographic-design.png) | [JSON](../../game-research/atelier_ryza__2026-10-16T194217-0400__game-research.json) | [Copy](atelier_ryza__2026-10-16T194217-0400__infographic-design.presentation.json) | [Image](../../../../assets/artwork/atelier_ryza/official_hero.jpg) / [provenance](../../../../assets/artwork/atelier_ryza/official_hero.provenance.json) | PlayStation 4 / Nintendo Switch / PC |
| [Honkai: Star Rail](png/honkai_star_rail__2026-10-16T194217-0400__infographic-design.png) | [JSON](../../game-research/honkai_star_rail__2026-10-16T194217-0400__game-research.json) | [Copy](honkai_star_rail__2026-10-16T194217-0400__infographic-design.presentation.json) | [Image](../../../../assets/artwork/honkai_star_rail/official_hero.jpg) / [provenance](../../../../assets/artwork/honkai_star_rail/official_hero.provenance.json) | PC / Mobile / PlayStation 5 |
| [THE FINALS](png/the_finals__2026-10-16T194217-0400__infographic-design.png) | [JSON](../../game-research/the_finals__2026-10-16T194217-0400__game-research.json) | [Copy](the_finals__2026-10-16T194217-0400__infographic-design.presentation.json) | [Image](../../../../assets/artwork/the_finals/official_hero.jpg) / [provenance](../../../../assets/artwork/the_finals/official_hero.provenance.json) | PC / PlayStation 5 / Xbox Series X&#124;S |
| [Crimson Desert](png/crimson_desert__2026-10-16T194217-0400__infographic-design.png) | [JSON](../../game-research/crimson_desert__2026-10-16T194217-0400__game-research.json) | [Copy](crimson_desert__2026-10-16T194217-0400__infographic-design.presentation.json) | [Image](../../../../assets/artwork/crimson_desert/official_hero.jpg) / [provenance](../../../../assets/artwork/crimson_desert/official_hero.provenance.json) | PlayStation 5 / Xbox Series X&#124;S / PC / macOS |

Reproduce any row with:

```sh
.venv/bin/python -m game_infographic_generator single-game <research.json> <output.png> --artwork <artwork> --presentation <presentation.json>
```

Existing research limitations and artwork usage terms remain applicable; platform formatting does not add missing releases or establish current platform availability. Clair Obscur reuses the existing 1088 × 612 hero with slight upscaling.

## Additional Zelda and Atelier run

Both existing research inputs passed CLI validation and both real Chromium exports
passed canvas/overflow checks at 1200 × 1600. Visually inspected both PNGs: artwork
is present, Japanese titles are readable, and text has no observed clipping.
Zelda keeps its one-line title and Similar Games; Atelier uses a two-line natural
title wrap and still requires compact mode with Similar Games omitted. Its
research JSON retains Similar Games unchanged. Atelier has no verified critic
score in its existing metadata, so no score card appears. Zelda’s existing
525 × 700 artwork remains visibly soft after cropping and enlargement.
Input metadata, artwork and presentation hashes were unchanged by rendering;
presentation files are byte-identical copies of prior inputs. No code changed
and no unit-suite rerun was needed; the earlier 99-test result above still refers
to the implementation check, not a new test run.

## Five new research stress tests

Persona 3 Reload, original Atelier Ryza (2019, not DX), Honkai: Star Rail,
THE FINALS and Crimson Desert received fresh source-backed research JSON and
separate presentation copy. All five metadata validations and real browser exports
passed at 1200 × 1600, with input hashes unchanged. Each PNG was visually
inspected. Original Atelier Ryza uses two title lines and omits Similar Games as
the final compact fallback; the other four retain it. Earlier statements about
all examples retaining Similar Games refer only to the first six-example batch.

Per-run reports record source mappings, artwork provenance, crops and research
limitations:

- [Persona 3 Reload](persona_3_reload__2026-10-16T194217-0400__infographic-design.validation.md)
- [Atelier Ryza: Ever Darkness & the Secret Hideout](atelier_ryza__2026-10-16T194217-0400__infographic-design.validation.md)
- [Honkai: Star Rail](honkai_star_rail__2026-10-16T194217-0400__infographic-design.validation.md)
- [THE FINALS](the_finals__2026-10-16T194217-0400__infographic-design.validation.md)
- [Crimson Desert](crimson_desert__2026-10-16T194217-0400__infographic-design.validation.md)

Date qualification: Persona 3 Reload uses February 1, 2024 (North American
Pacific unlock/storefront date) and Honkai: Star Rail uses April 25, 2023
(Americas date converted from the publisher’s April 26 10:00 UTC+8 launch
timestamp), following the existing earliest-local-date interpretation. Their
advertised dates are February 2 and April 26 respectively. HoYoverse’s dynamic
news bodies could not be extracted by the page reader, so indexed official text
was used for those launch/platform claims and this evidence limitation is
recorded in the Honkai report. No schema or date policy changes were made.
