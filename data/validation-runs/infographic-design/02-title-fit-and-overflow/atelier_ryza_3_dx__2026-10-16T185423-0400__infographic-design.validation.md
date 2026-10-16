# Atelier Ryza 3 DX — successful title-fit retry

Output: [png/atelier_ryza_3_dx__2026-10-16T185423-0400__infographic-design.png](png/atelier_ryza_3_dx__2026-10-16T185423-0400__infographic-design.png) — **1200 × 1600 PNG**.

- [Unchanged research input](../../game-research/atelier_ryza_3_dx__2026-10-16T184508-0400__game-research.json).
- [Presentation copy](atelier_ryza_3_dx__2026-10-16T185423-0400__infographic-design.presentation.json), byte-identical to round 01.
- [Official artwork](../../../../assets/artwork/atelier_ryza_3_dx/official_dx_screenshot.jpg) and
  [provenance](../../../../assets/artwork/atelier_ryza_3_dx/official_dx_screenshot.provenance.json).
- Code: `5b6a056` plus uncommitted title-fit and final overflow-fallback changes.

The original colon-grouped title required three lines. The renderer now measures
it after fonts load and chooses natural wrapping, preserving the full title in
two lines. Both normal and compact layouts still overflowed with Similar Games.
The last-resort compact attempt omitted only that section and exported successfully,
with a warning. The related titles remain unchanged in research JSON.

The final image was visually inspected: two readable title lines, Japanese title,
full-width 16:9 artwork, complete metadata, overview, both sentiment panels, and
footer. No clipping or distortion observed. PNG decoding/dimensions passed;
SHA-256 checks confirmed unchanged metadata, presentation, and artwork during export.

Research gaps from round 01 remain: no verified DX-specific aggregate critic score;
Steam lists November 12, 2025, while consoles list November 13. No new research was
performed and no facts or source JSON were changed to make the layout fit.
