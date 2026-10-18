# Katsuya's List — dark cinematic frame

- [PNG](png/katsuyas_list__2026-10-18T144909-0400__rankings-infographic.png); [manifest](katsuyas_list__2026-10-18T144909-0400__rankings-infographic.json).
- Original heading casing restored: Katsuya's List. Manifest and focal values copied byte-for-byte from the previous run; all earlier manifests and PNGs verified unchanged by SHA-256.
- Background #151719; heading #F3F2ED; secondary #A5AFB0; footer #8E989A.
- Header, 1104px-wide artwork frame and footer align at 48px outer margins.
- Nine 3px #292D30 gaps separate ten equal-height artwork rows.
- Softer shared gradient: 78% black at left, 64% at midpoint, 6% at 78%, transparent at right. White text on the left half retains at least 4.5:1 contrast even over pure-white source art.
- Two-line colon-to-natural wrapping and per-game focal controls retained. Original Atelier Ryza wraps naturally to two lines in the narrower frame.
- 28 rankings tests passed, including palette/frame/separator, contrast and existing layout/failure regressions.
- Real Chromium export passed layout checks; Pillow decoded the PNG at exactly 1200 × 1600.
- Visually inspected all rows: no text clipping, consistent margins, subtle separators, readable titles and preserved order. Prior shallow-crop limitations remain: group subjects and the Clair Obscur close-up cannot all fit fully.
- No single-game renderer changes, metadata research, new artwork or dependency changes.

```sh
.venv/bin/python -m game_infographic_generator rankings data/validation-runs/rankings/katsuyas_list__2026-10-18T144909-0400__rankings-infographic.json data/validation-runs/rankings/png/katsuyas_list__2026-10-18T144909-0400__rankings-infographic.png
```
