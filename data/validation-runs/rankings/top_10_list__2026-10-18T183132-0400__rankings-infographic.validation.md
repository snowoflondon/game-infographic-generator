# Top 10 List. — rankings validation

- Manifest: [top_10_list__2026-10-18T183132-0400__rankings-infographic.json](top_10_list__2026-10-18T183132-0400__rankings-infographic.json)
- Output: [PNG](png/top_10_list__2026-10-18T183132-0400__rankings-infographic.png), 1200 × 1600.
- Used the current light editorial layout: ten equal rounded artwork cards, 6px gaps, bottom-left white titles, and existing gradients. No renderer, schema, skill or research JSON changes.
- Preserved the supplied order exactly. Rankings uses lightweight official title/edition checks, not full game-research.

## Title checks

Normalized “Metaphor Refantazio” to **Metaphor: ReFantazio** and expanded “NieR Replicant ver. 1.22” to **NieR Replicant ver.1.22474487139…**. The terminal ellipsis belongs to the official title; it is not renderer truncation. Verified the Director's Cut edition of Yakuza 0 and the remake Trails in the Sky 1st Chapter. Final Fantasy VII Remake artwork comes from its original PS4 page, not Intergrade.

## Artwork

Downloaded nine official assets and reused the previously verified NieR: Automata promotional landscape. Source pages, direct image URLs, retrieval times, decoded format/dimensions and usage notes are recorded beside each downloaded asset in `assets/artwork/`.

Persona 3 Reload uses a newly downloaded official base-game cover image, replacing the old screenshot selection in this manifest. The previous screenshot remains available solely to preserve historical previews and manifests; it was not deleted or overwritten. Episode Aigis artwork was excluded.

## Checks and findings

- CLI `rankings ... --check` passed for all ten entries and decoded local artwork.
- Actual Chromium export passed the renderer's font/image readiness, equal card heights, title two-line limits, and canvas/text overflow checks.
- Pillow decoded the final PNG and confirmed 1200 × 1600 dimensions.
- Visually inspected the final PNG. Adjusted focal points before export to keep major faces visible where the source composition allows. NieR Replicant title wraps naturally to two lines.
- No export errors or clipping detected. No previous output PNG was overwritten.
- Some candidate image requests returned HTTP 403/404; selected working official alternatives. This did not block export.
- Crop limitation: NieR: Automata's reused landscape has a small, back-facing 2B. NieR Replicant's landscape also gives less face detail than character close-ups. Embedded logos remain in some official promotional art, particularly Persona 3 Reload; original artwork bytes were preserved.
- Artwork is recorded for this local personal/noncommercial preview; no public redistribution or commercial reuse license is asserted.

## Official verification sources

- [Final Fantasy VII Rebirth](https://www.playstation.com/en-us/games/final-fantasy-vii-rebirth/)
- [Persona 5 Royal](https://www.playstation.com/en-us/games/persona-5-royal/)
- [Yakuza 0 Director's Cut](https://www.playstation.com/en-us/games/yakuza-0-directors-cut/)
- [NieR: Automata](https://blog.playstation.com/2016/12/22/nier-automata-demo-out-today-on-playstation-store/)
- [Persona 3 Reload](https://www.playstation.com/en-us/games/persona-3-reload/)
- [Metaphor: ReFantazio](https://www.playstation.com/en-us/games/metaphor-refantazio/)
- [Final Fantasy VII Remake](https://www.playstation.com/en-us/games/final-fantasy-vii-remake/)
- [Trails in the Sky 1st Chapter](https://www.playstation.com/en-us/games/trails-in-the-sky-1st-chapter/)
- [Yakuza Kiwami 2](https://www.playstation.com/en-us/games/yakuza-kiwami-2/)
- [NieR Replicant ver.1.22474487139…](https://www.playstation.com/en-us/games/nier-replicant-ver-1-22474487139/)
