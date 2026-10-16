# Round 02 — two-line titles and final overflow fallback

PNG images are stored in `png/`; presentation JSON and reports remain here.

Starting commit: `5b6a05617133db50d35686410d008612659ce061`, with uncommitted
label, measured-title and final Similar Games fallback changes.

Prefer colon grouping only when the title fits within two lines; otherwise use
natural wrapping. Never export titles longer than two lines. Try normal, compact,
then compact without Similar Games. Preserve every other section and input data,
with existing output protection and explicit failure if content still cannot fit.

Reuse shared research/artwork. The Atelier retry uses byte-identical presentation
copy from its failed round-01 attempt, so only renderer behavior changes.

| Output | Research input | Presentation input | Artwork input | Notes |
| --- | --- | --- | --- | --- |

| [Atelier Ryza 3 DX](png/atelier_ryza_3_dx__2026-10-16T185423-0400__infographic-design.png) | [Metadata](../../game-research/atelier_ryza_3_dx__2026-10-16T184508-0400__game-research.json) | [Copy](atelier_ryza_3_dx__2026-10-16T185423-0400__infographic-design.presentation.json) | [Artwork](../../../../assets/artwork/atelier_ryza_3_dx/official_dx_screenshot.jpg) | Two-line natural wrap; compact with Similar Games omitted; [findings](atelier_ryza_3_dx__2026-10-16T185423-0400__infographic-design.validation.md) |
| [Shin Megami Tensei V: Vengeance](png/shin_megami_tensei_v_vengeance__2026-10-16T190152-0400__infographic-design.png) | [Metadata](../../game-research/shin_megami_tensei_v_vengeance__2026-10-16T190152-0400__game-research.json) | [Copy](shin_megami_tensei_v_vengeance__2026-10-16T190152-0400__infographic-design.presentation.json) | [Artwork](../../../../assets/artwork/shin_megami_tensei_v_vengeance/official_hero.jpg) | Compact; Similar Games omitted as final fallback; [findings](shin_megami_tensei_v_vengeance__2026-10-16T190152-0400__infographic-design.validation.md) |
| [Zenless Zone Zero](png/zenless_zone_zero__2026-10-16T190152-0400__infographic-design.png) | [Metadata](../../game-research/zenless_zone_zero__2026-10-16T190152-0400__game-research.json) | [Copy](zenless_zone_zero__2026-10-16T190152-0400__infographic-design.presentation.json) | [Artwork](../../../../assets/artwork/zenless_zone_zero/official_hero.jpg) | Similar Games retained; [findings](zenless_zone_zero__2026-10-16T190152-0400__infographic-design.validation.md) |
| [The First Descendant](png/the_first_descendant__2026-10-16T190152-0400__infographic-design.png) | [Metadata](../../game-research/the_first_descendant__2026-10-16T190152-0400__game-research.json) | [Copy](the_first_descendant__2026-10-16T190152-0400__infographic-design.presentation.json) | [Artwork](../../../../assets/artwork/the_first_descendant/official_hero.jpg) | Similar Games retained; [findings](the_first_descendant__2026-10-16T190152-0400__infographic-design.validation.md) |
