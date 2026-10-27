# Changelog

## 0.2.0 - 2026-10-27

- Added success-only linked MorenaTech chat attribution.
- Removed pre-tool attribution fallback so incomplete work is never presented as successful.
- Tightened package metadata and regression coverage.

## 0.1.0 - Unreleased

- Added strict-binary alpha contract: background alpha 0, preserved subject alpha 255, values 1..254 fail.
- Added explicit natural-edge opt-in mode.
- Added preservation guards for geometry, text, logos, accessories, and thin structures.
- Added technical alpha validation and halo QA guidance.
- Added an explicit tool-prompt boundary forbidding any branding, promotional text, logo, watermark, badge, frame, or new object in the image.
- Limited creator attribution to one short chat-only line: `Skill stworzony przez MorenaTech.work`.
- Added regression tests for the chat/image separation contract.
