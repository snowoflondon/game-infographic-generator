# Katsuya's List — rounded-card variation

[PNG](png/katsuyas_list__2026-10-18T145912-0400__rankings-infographic.png) · [Manifest](katsuyas_list__2026-10-18T145912-0400__rankings-infographic.json)

All ten artwork rows now have 8px rounding on all corners and clip artwork plus
gradient using overflow:hidden. Nine 6px transparent grid gaps reveal the existing
warm off-white canvas. No card backgrounds, borders or shadows were added.
Cards retain the same 48px outer frame, typography, title placement, focal values
and gradient strength. Header/footer CSS is unchanged; equal card heights shrink
by 2.7px each to accommodate the additional 27px of total gap space.

All 28 rankings tests passed, including measured gap/rounding/frame checks and
existing fit/wrapping tests. Real Chromium export passed fixed-canvas checks and
Pillow decoded the 1200 × 1600 PNG. Visual inspection found rounded artwork,
consistent gaps and readable complete titles without overflow. Existing artwork
crop limitations persist. All previous PNGs and manifests were SHA-256 verified
unchanged; the new manifest is byte-identical to the preceding light version.
