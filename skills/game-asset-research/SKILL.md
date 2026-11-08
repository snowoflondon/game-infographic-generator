---
name: game-asset-research
description: Find, verify and download official artwork for an exact video game and edition, or inspect supplied artwork, without researching metadata or rendering an infographic.
---

# Game Asset Research

## Invocation and scope

Use for requests such as “Find artwork for this game” or when an authorized
infographic request includes artwork. Accept a game title and edition, intended
use, and target crop (single-game 16:9 hero or shallow rankings stripe).
Validated metadata can establish identity but is not required. Correct obvious
title typos and report them; clarify genuinely ambiguous editions.

Do not run game-research, modify GameMetadata or research JSON, generate artwork,
or render an infographic. Drafting this skill does not authorize downloads.

## Selection criteria

Use only official developer/publisher artwork, such as promotional key art or
cover art. Exclude fan art and in-game screenshots, even screenshots published
by official accounts. Apply these restrictions to existing and supplied assets
as well as new discoveries; preserve historical files that no longer qualify.
Reject artwork containing the game title or title logo, including stylized or
original-language versions: the infographic already supplies the title. Find
an official title-free version instead. Do not erase, obscure or crop out a
title/logo to make an otherwise disallowed asset qualify.

Compare suitable candidates using these qualitative criteria:

- **Game identity:** Recognizable characters, setting, visual style or other
  distinctive elements that represent the exact game and edition.
- **Composition:** A clear focal point, balanced subjects and useful negative
  space; avoid distracting elements and embedded text that competes with the design.
- **Crop compatibility:** Important subjects survive the target aspect ratio.
  Consider the 16:9 single-game hero separately from shallow rankings stripes;
  account for title overlays and prioritize visible faces where present.
- **Technical quality:** Adequate resolution at the displayed size, clear detail,
  intact image data and no watermarks. An intact file alone does not establish
  visual quality.

Choose the strongest fit for both game identity and the intended design, rather
than simply the first downloadable image. Give a brief reason for the selection
and any material tradeoffs; do not assign confidence or numeric scores. If only
one suitable candidate is available, say so rather than implying a comparison.

## Procedure

1. Follow the shared [artwork discovery procedure](../references/artwork-discovery.md)
   for source priority, edition verification, usage terms, download location,
   provenance and image decoding. Use web search and open the actual supporting
   page and image; report unavailable tools or sources rather than inventing URLs.
2. Inspect existing assets and provenance before searching. Reuse an asset that still meets the selection criteria after
   reverification unless the user requests a replacement or a fresh download
   for comparison. For a comparison, download to a new filename; preserve the
   accepted original and its provenance. For replacement, do not delete assets
   referenced by earlier runs without explicit authorization.
3. Select using the criteria above and inspect the downloaded image visually.
   Preserve original bytes; do not stretch, recolor or embed titles. Report
   quality/crop limitations. Final rendered crop checks belong to the renderer.
4. Save a separate `.provenance.json` sidecar recording the checked game/edition,
   source page and direct image URLs, retrieval timestamp with timezone, local
   filename, actual format/dimensions, usage evidence, selection rationale and limitations.
   Include SHA-256 when comparing downloads; distinguish byte equality from
   equal decoded pixels and from merely depicting the same game.
5. If required artwork cannot be verified or obtained after checking suitable
   alternatives, stop and report the blocker; do not substitute another edition
   or an unrelated image, fan art or an in-game screenshot.

## Output

Return the checked game/edition, local image and provenance paths, source URL,
format/dimensions, selection rationale, intended crop suitability, and any
permission or access gaps.
Keep artwork in `assets/artwork/<game_slug>/`; never add it to metadata JSON.
For explicit validation runs, save a timestamped report under
`data/validation-runs/game-asset-research/` containing checks and comparison results.
Do not claim infographic generation or final crop validation for an asset-only run.
