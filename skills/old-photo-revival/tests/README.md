# Tests

This directory contains:

- `cases.json`: public text-only corpus T01-T14
- `case-schema.json`: lightweight schema document for the corpus
- `manual-results-template.md`: template for manual visual evaluation
- `static/`: deterministic unit tests for validation and read-only image inspection

The public package intentionally ships without image assets.

For `faithful-colorization`, preserving identity alone is not enough. Manual review must also verify local color separation, neutral balance, skin-color naturalness, and freedom from sepia-color-collapse.

For photographed paper prints, manual review must also verify print normalization: border cleanup, straightening, mild perspective correction, and removal of the "phone photo of a print" look when that look is accidental.
