---
name: rankings-infographic
description: Prepare and render a personal top-ten game rankings infographic using checked game titles and verified artwork, preserving the user's supplied order.
---

# Rankings Infographic

## Invocation and boundaries

Invoke with “Use rankings-infographic for this heading and these ten games,
in order from #1 to #10.” Obtain a user-provided heading and exactly ten ordered
entries before rendering. Never invent, sort or deduplicate the user's order;
position alone determines rank. Resolve ambiguous game editions with the user.
Draft/review requests do not authorize research, downloads or infographic export.

## Preparation

1. Inspect project guidance, `rankings_models.py` and `rendering/rankings.py`.
2. Perform a lightweight title/edition check against an official developer,
   publisher or storefront page, ideally while finding artwork. Correct a clear
   spelling error or incomplete title only when the intended game is unambiguous;
   report the correction. Ask when multiple games/editions could match. Preserve
   each entry’s position. Do not invoke game-research, collect full metadata, or
   look up alternative titles. Existing records may help identify a game but
   are never required. Record verification URLs in artwork provenance or an
   optional report, outside the manifest.
3. Follow [artwork discovery](../references/artwork-discovery.md) for every
   game. Artwork is required. Select for shallow horizontal stripes and check
   that central subjects survive cropping; a good 16:9 hero may be unsuitable.
4. Create a separate manifest containing a nonblank `title` and `games`, an
   array of exactly ten objects, each with nonblank `title` and `artwork_path`
   strings. An optional `artwork_focal_point` object accepts `x` and `y` percentages
   from 0 to 100, each defaulting to 50 (center). Use these as CSS object-position
   controls; inspect the resulting crop and prioritize visible character faces.
   Artwork paths resolve relative to the manifest. Reject extra fields,
   including old `metadata_path` and `alternative_titles` fields. Keep order
   exactly as supplied, #1 first; no rank fields or presentation summaries.

## Design and rendering

- Use Python, Pydantic, Jinja2, HTML/CSS and Playwright Chromium; no new framework.
- Keep the rankings renderer and template separate from single-game rendering.
  Preserve GameMetadata, research JSON and original artwork bytes.
- Fixed 1200 × 1600 canvas (3:4). Align header, wide artwork strips and footer
  within consistent 48px horizontal margins. Reserve header/footer space and
  nine 6px vertical gaps revealing the warm off-white background, then divide the remaining height equally among
  ten stripes spanning the inner frame. Do not vary stripe heights or omit entries.
- Use the light editorial palette: background #f5f3ed, main heading #252b2b,
  secondary labels/footer #5d6969, and white game titles over the existing artwork
  gradients. Each card has 8px rounding on all four corners, clipping both artwork
  and overlay; add no borders, shadows or separate card backgrounds.
- Use modern sans-serif typography, restrained neutral header/footer, consistent
  bottom-left title alignment and readable white text. Do not show rank numerals;
  vertical order alone communicates ranking. Apply the same left-to-right dark
  gradient to every stripe: softly shaded but contrast-safe behind the left-half
  white title (at least 4.5:1 even over bright art), fading to transparent over
  right-side artwork. Do not uniformly darken the whole
  image or use separate title boxes. Reserve the left half for title text with
  consistent bottom-left insets; never extend titles into the right half.
  Crop proportionally without stretching and apply per-game focal settings to
  prioritize faces. Choose different artwork if positioning cannot yield a
  suitable crop. Keep a consistent identity across stripes.
- Preserve the user-provided heading’s original casing in the manifest and
  rendered title; do not force uppercase or automatically recase game titles.
- Each stripe displays only the checked game title and its artwork.
  Do not display alternative titles, scores, descriptions, sources or sentiment.
  The user’s heading and minimal project footer remain outside the stripes.
- Apply the single-game title policy to the user heading and every game title:
  keep one line when it fits; prefer a break after a colon (including `：`)
  only when the grouped phrases fit within two lines. If grouping exceeds that
  limit, use natural word/script wrapping across the whole title. Measure after
  fonts load. Keep readable fixed sizes and CJK fallbacks; fail if natural
  wrapping still exceeds two lines. Never clamp, clip, truncate, shrink text
  below its defined size or alter equal stripe heights to force success.
- Run `game-infographic-generator rankings manifest.json output.png --check`
  to validate local inputs without a browser/export. When export is requested,
  omit `--check`. The CLI performs no research or downloads. Check-only mode
  cannot establish visual fit, semantic correctness or artwork permissions.
- Before PNG capture, wait for fonts and images, verify equal stripe heights,
  title limits and overflow. Preserve existing output on every failure.

## Verification and output

Test schema/count/order, manifest-relative paths, title escaping, Unicode,
missing/corrupt artwork, unexpected manifest fields, equal stripe heights and overflow.
Do not capture images when the user requests validation without generation;
DOM-only browser checks are allowed. Real PNG export and visual crop inspection
remain necessary before calling a generated example complete.

Save ranking manifests, optional reports and PNGs under `data/validation-runs/rankings/`, using a `png/`
subfolder for images. Retain descriptive slug, timestamp and skill in filenames.
Report exact inputs/output, checks performed, any unverified crops or limitations,
and failures. The CLI validates structure and image decoding, not title correctness, edition
identity or artwork permissions; those checks belong to the agent/user.
