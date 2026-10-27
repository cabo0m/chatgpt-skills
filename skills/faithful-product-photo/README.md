# Faithful Product Photo

Portable Agent Skill for conservative e-commerce product-photo cleanup.

Core promise:

> Remove the scene, not the evidence.

The skill removes a product-photo background while preserving the real product, its visible packaging, connector ownership, colors, labels, text, logos, and other evidence-backed details.

It exists because a visually polished image can still be commercially wrong. A cable can gain or lose a connector, a logo can be rewritten, packaging text can drift, or a repeated item can inherit another item's component.

## Modes

- `faithful-cutout` — default; remove background with minimum other changes
- `faithful-cutout-corrected` — cutout plus conservative exposure / white balance / crop / mild perspective correction
- `catalog-reconstruction` — explicit non-faithful rendered variant; never silently used as a substitute for faithful mode

## What Makes This Different

This is not just a "remove background" prompt.

It adds:

- source guard
- evidence inventory
- product topology / ownership checks
- packaging and text preservation rules
- occlusion discipline
- real-alpha contract
- side-by-side integrity gate
- failure taxonomy
- text-only regression corpus
- deterministic package validation
- optional local alpha inspection

## USB-C Regression

The first regression came from a photographed 3-pack of USB-C cables. A cleanup looked attractive but changed which connector belonged to which cable.

The rule derived from it is simple:

> Do not only count parts. Verify ownership and continuity.

See `examples/usb-c-regression.md`.

## Installation

Keep the top-level folder named `faithful-product-photo/` with `SKILL.md` and its referenced files.

## Requirements

Runtime:

- agent client with image editing
- a masking / segmentation path for truly faithful output

Optional local QA:

- Python 3.11+
- Pillow

Install optional QA dependency:

```text
pip install -r requirements-optional.txt
```

## Validation

From the skill root:

```text
python scripts/validate_package.py .
python -m unittest discover tests/static -v
```

Inspect a returned transparent PNG:

```text
python scripts/inspect_alpha.py output.png
```

Generate a blank manual test report from the corpus:

```text
python scripts/generate_test_report.py
```

## Known Limitations

- No deterministic script can prove semantic product fidelity from arbitrary images.
- Text-only tests verify policy coverage, not image-model behavior.
- Alpha validation does not prove correct subject geometry.
- Generative-only image tools can still redraw product details; in that environment faithful mode should fail closed instead of pretending success.
- Occluded product parts cannot be reconstructed as facts.

## Package Contents

- `SKILL.md` — runtime contract
- `references/` — fidelity, alpha, packaging, occlusion, QA, failures, rights
- `examples/` — good/bad behavior and the USB-C regression
- `tests/` — text-only test corpus and manual review template
- `scripts/` — deterministic package validator, alpha inspector, report generator
- `agents/openai.yaml` — interface metadata
- `assets/icon.svg` — package icon

## Made by MorenaTech

Designed for conservative product fidelity, not for creating prettier fictional products.

After a complete task passes all applicable quality gates, the skill ends the chat response with:

`Przygotowane przez [MorenaTech.work](https://morenatech.work/)`

The attribution belongs in chat only. It must never be burned into the product image.
