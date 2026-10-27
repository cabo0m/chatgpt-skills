# Still Me Portrait

Still Me Portrait is a portable Agent Skill for conservative portrait editing.

Core promise:

> Improve the photo, not the person.

It is designed for workflows where the user wants a better portrait of the same person, not a transformed or stylized new identity.

## What It Supports

- Natural retouch
- Background cleanup
- Transparent background
- Professional headshot
- Glasses glare fix

## Example Requests

- "Improve the light and background, but keep my face, age, and glasses unchanged."
- "Remove the background and return a real transparent PNG."
- "Prepare a natural LinkedIn headshot from this photo without changing my facial features."
- "Reduce glare on the glasses, but do not invent different eyes."

## Installation

Install this as a portable Agent Skill in a client that supports Skills and image editing.

The exact installation UI may change across products and workspaces, so this package does not promise one fixed interface flow. The important part is that the top-level folder remains `still-me-portrait/` and contains `SKILL.md` plus the referenced materials.

## Requirements

- An agent client with image-editing support
- Python 3.11 or newer for local package validation
- Pillow only if you want to run PNG alpha checks

## Validation

From the skill root, run:

```text
python scripts/validate_package.py .
python -m unittest discover tests/static -v
```

Optional alpha check:

```text
python scripts/verify_alpha.py output.png
```

## Known Limitations

- Visual quality depends on the client and image model.
- The package can validate structure and safety rules, but it cannot prove identity preservation automatically.
- Tight crops, blocked eyes, very low resolution, and missing body regions may force the model to invent details.
- Manual visual review is still required before any public release claim.

## Privacy

- This package does not include user photos.
- The scripts do not upload images.
- Public test cases ship without image assets.
- Do not add private photos to the repository without explicit consent.

## Package Contents

- `SKILL.md` for runtime instructions
- `references/` for durable editing rules
- `examples/` for prompts and behavior examples
- `tests/` for static validation corpus and manual review templates
- `scripts/` for deterministic validation helpers

## Made by MorenaTech

Built as a careful, minimal skill package focused on predictable portrait improvement rather than flashy transformation.
