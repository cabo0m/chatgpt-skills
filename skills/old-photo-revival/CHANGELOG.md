# Changelog

## 0.2.0 - 2026-10-27

- Added success-only linked MorenaTech chat attribution.
- Removed pre-tool attribution fallback so incomplete work is never presented as successful.
- Tightened package metadata and regression coverage.

## 0.1.0 - Unreleased

- Separated MorenaTech attribution from the image-editing prompt and image pixels.
- Added an explicit no-logo, no-watermark, no-badge, and no-promotional-overlay guard.
- Limited post-result branding to one short chat-only creator attribution line, with no CTA or sales copy.
- Added print-normalization workflow before restoration and colorization when the source is a photographed physical print.
- Added single automatic colorization correction when a first-pass colorization still looks like sepia.
- Clarified that explicit colorization requests must complete actual colorization on the first workflow pass.
- Added print-normalization checks for borders, skew, and perspective artifacts.
- Added explicit protection against sepia color collapse.
- Changed default colorization strength to natural.
- Added local color separation and neutral balance requirements.
- Clarified conservative colorization versus uniform warm tinting.
- Added skin, lip, eye, hair, clothing, jewelry, and background color checks.
- Added the first failed manual faithful-colorization finding.
- Added the first internal alpha scaffold for Old Photo Revival.
- Added three modes: restore-only, faithful-colorization, and natural-revival.
- Added uncertainty and reconstruction guards.
- Added identity preservation and historical-character rules.
- Added deterministic package validation and read-only image inspection.
- Manual visual gate remains required before any public release.
