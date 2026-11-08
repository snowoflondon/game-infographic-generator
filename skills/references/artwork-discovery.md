# Artwork discovery for game infographics

Shared procedure owned by [game-asset-research](../game-asset-research/SKILL.md).

1. Confirm the exact title and edition: use validated GameMetadata for single-game
   mode, or the checked supplied title for rankings. Inspect an
   approved supplied image instead of searching for a replacement.
2. Use only official developer/publisher promotional artwork or cover art.
   Exclude fan art, in-game screenshots and artwork containing the game title
   or title logo, including officially published versions.
   Open the source page and actual image;
   verify edition and quality. Never invent URLs or rely on search thumbnails.
3. Apply the selection criteria in game-asset-research. Preserve proportions
   and important subjects; avoid unrelated placeholders and watermarks.
   Inspect the final crop.
4. Inspect published usage terms. Official availability is not a reuse license.
   Record known permissions and restrictions; report a permission blocker when
   intended use is unclear or restricted rather than claiming authorization.
5. Save the original image to `assets/artwork/<game_slug>/` and record source
   page, direct URL, retrieval date, filename and usage evidence in a separate
   provenance sidecar. Never add artwork fields to GameMetadata.
6. Decode the downloaded file and verify its actual format, positive dimensions
   and exact game/edition visually. Supported formats are PNG, JPEG and WebP.
   Missing, corrupt or unavailable required artwork is an explicit failure;
   do not silently substitute typography-only output.

Single-game artwork is opt-in. Rankings requires an image for every game and
must evaluate the much shallower stripe crop rather than assuming an existing
single-game hero image is suitable. Existing assets may be reused after review.
