# NieR:Automata validation run

Run: 2026-10-15T220607-0400 (America/Toronto).

## Inputs and outputs

- Research: [metadata](../../game-research/nier_automata__2026-10-15T220607-0400__game-research.json).
- Presentation: [condensed copy](nier_automata__2026-10-15T220607-0400__infographic-design.presentation.json).
- Result: [1200 × 1600 PNG](png/nier_automata__2026-10-15T220607-0400__infographic-design.png).
- Artwork: [official image](../../../../assets/artwork/nier_automata/official_promo.jpg).
- Attribution and terms: [provenance](../../../../assets/artwork/nier_automata/official_promo.provenance.json).

## Scope and research decisions

This record represents the original 2017 release. The earliest verified full
release is February 23, 2017, on PlayStation 4 in Japan, from the
[Japanese developer page](https://www.platinumgames.co.jp/works/nier-automata).
The same source verifies the Japanese title, developer, publisher, and genre.
PS4 and PC are listed for this edition; Xbox and Switch packages have distinct
edition names and are deliberately excluded. The platform list does not imply
simultaneous release. No PS5-native edition is inferred from compatibility.

The [platform-specific Metacritic page](https://www.metacritic.com/game/nier-automata/critic-reviews/?platform=playstation-4)
verifies the original PS4 score of 88/100. No score is borrowed from a later edition.
The English developer page has apparent year errors for the later Game of the
YoRHa Edition; those dates were not used. Current storefronts also emphasize
later editions, so the original-release entry was used for this test.

Player perspectives summarize two linked discussions in the research JSON,
including praise and disagreement; the sample is qualitative and not representative.
Similar games are editorial suggestions based on series connections and shared
action design, not an objective or validated similarity ranking.

## Artwork and presentation

The official 1280 × 720 image comes from a launch-era Square Enix-authored
PlayStation Blog post. It shows 2B and Pod overlooking a desert city. Its native
16:9 ratio fits the hero without material cropping or upscaling. Usage terms and
personal-use scope are recorded in provenance; no publication license is asserted.
The image was decoded and inspected before export, and remains unmodified.

Condensed copy is stored separately. The one-sentence overview preserves the
premise and mechanics, and the short sentiment phrases preserve mixed opinions.
Sources remain in research JSON and are omitted from the image as designed.

## Checks and result

- Existing CLI metadata validator: passed.
- All top-level contract fields supplied; no schema changes.
- Actual Chromium PNG export: passed on the first attempt, including built-in fit checks.
- PNG decoded with Pillow: PNG format, exactly 1200 × 1600.
- Research JSON SHA-256 unchanged during rendering: `100b59925cabe775c9a20c60535bb378c59e5e6670b82ec54b9a0c3daa1f4261`.
- Extracted accent: `#182828`; contrast against background: 13.79:1;
  white score-card text contrast: 15.30:1 (both exceed 4.5:1).
- Visual inspection: readable English/Japanese text, visible artwork subject,
  no observed clipping, aligned metadata and critic card, all expected sections present.
- Full test suite: **75 passed in 9.97 seconds**.

No implementation, schema, template, or skill changes were needed for this run.
Remaining limits are research judgment, sampled sentiment, subjective similar-game
selection, and the existing system-font dependence. Pydantic validates structure,
not factual accuracy or semantic faithfulness. This is a successful baseline example,
not proof that every game's content will fit the fixed canvas.
