# Katsuya's List — visible artwork and bottom-left titles

- [PNG](png/katsuyas_list__2026-10-18T143023-0400__rankings-infographic.png); [manifest](katsuyas_list__2026-10-18T143023-0400__rankings-infographic.json).
- Original preview preserved byte-for-byte (SHA-256 `f0f649690a0b485fdae308b41576d01c93a73b44abaa96e5a3f113694dcd14d9`).
- Same ordered titles and original local artwork; manifest is a byte-identical copy of the first run.
- Removed visible numbering; ordered list semantics and user order remain intact.
- Removed the full-stripe dark overlay. Original image brightness is retained except beneath localized translucent title backings.
- Positioned all titles at the bottom-left with consistent inset; retained ten equal stripes, two-line title policy and 1200 × 1600 canvas.
- 19 rankings tests passed, including DOM checks of alignment, absent numbering/overlay, image opacity/filter, title wrapping and equal heights.
- Actual Chromium PNG export succeeded; Pillow confirmed PNG decoding and 1200 × 1600 dimensions.
- Visually inspected the new output: titles readable, no observed clipping, artwork substantially more visible, all ten games in the original order.
- Existing center-crop limitations persist (notably Honkai, Stellar Blade and Persona faces). No focal-position or artwork substitution changes were requested or made.
- No changes to single-game rendering. See the first run report for artwork provenance and title checks.
