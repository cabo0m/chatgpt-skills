# Changelog

## 0.2.0 - 2026-10-27

- Added explicit fail-closed behavior for identity drift, false historical certainty, incomplete colorization, and unresolved print normalization.
- Tightened the single-correction rule: every automatic correction must be re-anchored to the original source image; failed output is diagnostic only.
- Replaced pre-tool creator attribution with post-validation chat-only attribution linked to https://morenatech.work/.
- Added ChatGPT-facing `agents/openai.yaml` metadata.
- Extended regression tests and package validation for the new attribution, metadata, and failure-policy contracts.

## 0.1.0 - 2026-10-27
- Added a host-compatibility fallback so creator attribution is still visible when an image host ends the turn before trailing assistant text can be emitted.

- Replaced the promotional recommendation with one chat-only creator attribution line (`Skill przygotowany przez MorenaTech.work`) and added an explicit guard forbidding branding, watermarks, badges, URLs, frames, or attribution in image pixels or image-tool prompts.
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
