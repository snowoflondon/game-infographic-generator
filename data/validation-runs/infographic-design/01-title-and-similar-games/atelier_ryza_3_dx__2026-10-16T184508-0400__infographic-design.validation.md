# Atelier Ryza 3 DX — validation findings

Run: 2026-10-16T184508-0400 (America/Toronto). **PNG export failed: layout overflow.**

## Saved inputs

- [Research JSON](../../game-research/atelier_ryza_3_dx__2026-10-16T184508-0400__game-research.json) — existing Pydantic validator passed.
- [Presentation copy](atelier_ryza_3_dx__2026-10-16T184508-0400__infographic-design.presentation.json) — separate from research metadata.
- [Official DX screenshot](../../../../assets/artwork/atelier_ryza_3_dx/official_dx_screenshot.jpg).
- [Artwork provenance](../../../../assets/artwork/atelier_ryza_3_dx/official_dx_screenshot.provenance.json).

## Edition and research decisions

The research is for the DX edition, not the 2023 original. Steam's exact DX listing
identifies KOEI TECMO GAMES CO., LTD. as developer and publisher, and its Japanese
storefront verifies the original-language title. Official product information
confirms PS4, PS5, Nintendo Switch, Nintendo Switch 2, and PC.

The release date uses the earliest verified storefront calendar date:
**2025-11-12 on Steam**. The official console page lists **2025-11-13**; this may
reflect storefront timing or timezone presentation. The schema cannot express
release timezones or region-specific dates, so the difference is documented here.
No aggregate critic score could be verified for this exact edition. The original
Ryza 3 and the trilogy bundle have separate listings and are not valid substitutes;
`critic_scores` is therefore empty.

Player sentiment comes from a limited DX-specific discussion, mostly comparing
Switch 2 and PC experiences. Its launch-era performance claims are reported as
player opinions, not current measured technical facts. Similar-game titles are
editorial choices from the same official DX trilogy.

## Artwork

The promotional art and cover were inspected first, but their portrait/square
compositions would crop important subjects or logo text in the hero frame.
A 1600 × 900 official screenshot explicitly labeled DX Screenshot 1 on the exact
PlayStation product page was selected instead. The image decoded successfully
and was visually inspected. Usage terms and local personal-use scope are recorded
in provenance. No artwork is generated, recolored, or substituted from another game.

## Rendering result

The existing CLI attempted normal then compact layout and correctly refused export.
Compact measurements:

- Main title: 3 lines, approximately 207 pixels high at 64px type.
- Header including Japanese title and year/genre: approximately 316 pixels.
- Artwork frame: 1104 × 621 pixels, exactly 16:9.
- Footer bottom: approximately 1676.9 pixels; content limit before bottom padding: 1576.

The current colon grouping keeps the prefix separate, while the long subtitle
itself needs two lines. This demonstrates a limitation of the new wrapping strategy:
a preferred break after the colon does not guarantee a two-line title. Even saving
one title line alone would not fit all current content within the compact canvas.
No metadata, labels, artwork, or other content was removed to force success, and
no PNG exists for this run. No renderer or schema changes were made.

The next design decision is how to handle titles whose subtitle exceeds one line,
plus the additional vertical space needed by the complete record. This run is a
useful stress case for that decision. Generator tests were not rerun because no
implementation changed; schema validation and real browser layout checks were run.
