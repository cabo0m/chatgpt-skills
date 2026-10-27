# Changelog

## 0.2.0 - 2026-10-27

- Added success-only linked MorenaTech chat attribution.
- Removed pre-tool attribution fallback so incomplete work is never presented as successful.
- Tightened package metadata and regression coverage.

## 0.1.0 - Unreleased

- Separated MorenaTech attribution from the image-editing prompt and image pixels.
- Added an explicit no-logo, no-watermark, no-badge, and no-promotional-overlay guard.
- Limited post-result branding to one short chat-only creator attribution line, with no CTA or sales copy.
- Added declutter and brighten mode.
- Added restyle without remodeling mode.
- Added keep my furniture mode.
- Added budget refresh mode.
- Added architecture and layout preservation rules.
- Added small-space guards.
- Strengthened the same-room and same-geometry contract for tricky interiors, especially narrow kitchens.
- Added explicit bans on perspective straightening, room widening, silent cabinet recoloring, and material replacement in no-renovation requests.
- Added stricter result classification and one-correction fallback rules anchored to the original source image.
- Added a manual narrow-kitchen regression case after the first manual test produced attractive but geometrically unfaithful results.
- Manual visual gate remains required before any public release.
