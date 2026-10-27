# Old Photo Revival

Old Photo Revival is a portable Agent Skill for conservative restoration, colorization, and natural revival of old photographs.

Core promise:

> Restore what is visible. Clearly distinguish what was reconstructed or estimated.

It is designed for users who want an old image repaired and clarified without turning it into a modern beauty portrait or a historically overconfident reconstruction.

## Three Modes

- `restore-only`
- `faithful-colorization`
- `natural-revival`

## Restoration, Reconstruction, Estimation

- Restoration means repairing what is visibly supported by the source.
- Reconstruction means cautiously filling a small missing area from surrounding evidence.
- Estimation means choosing a plausible but uncertain detail such as color when the source does not prove it.

The skill is expected to tell the user when it moves from restoration into reconstruction or estimation.

## Workflow Priority

When the source is a photographed paper print rather than a clean scan, the workflow should first normalize the print capture itself:

- inspect the source
- normalize the print
- restore the image
- colorize or revive it
- run a quality gate
- allow at most one automatic correction

That means the skill should correct accidental border tint, tilt, and mild perspective issues before deeper portrait work.

## Example Requests

- "Usun rysy i zagniecenia, ale pozostaw zdjecie czarno-biale."
- "Colorize the photograph naturally. Treat eye color and clothing color as estimated unless I provide references."
- "Odnów portret, zachowujac wiek, mimike, fryzure i bizuterie."
- "Repair only the paper damage. Do not beautify the face."
- "Use the second photo only as a reference for hair color."
- "Do not reconstruct the damaged eye without warning me first."

## Installation

Install this package as a portable Agent Skill in a client that supports Skills and image editing.

The exact installation interface may change across products and workspaces, so this package does not assume one fixed UI flow. The important part is that the top-level folder remains `old-photo-revival/` and contains `SKILL.md` with the referenced materials.

## Requirements

- An agent client with image-editing support
- Python 3.11 or newer for local package validation
- Pillow only if you want to use local image inspection

## Validation

From the skill root, run:

```text
python scripts/validate_package.py .
python -m unittest discover tests/static -v
```

Optional local inspection:

```text
python scripts/inspect_image.py input.jpg
```

## Privacy And Rights

- This package ships without user photos.
- Scripts do not upload images.
- Public test cases use `input_asset: null`.
- Do not add private or rights-unclear photos to the repository, examples, or promo materials.
- Photos found on Facebook, Instagram, or similar services are not valid public corpus material without explicit rights and permission.

## Known Limitations

- The skill cannot guarantee exact reconstruction of missing details.
- Color choices may be estimated unless the user provides trustworthy references.
- The package cannot prove visual identity preservation automatically.
- Large missing facial regions, unreadable text, or destroyed insignia require explicit warnings and may remain uncertain.
- The skill does not guarantee historical accuracy without evidence.

## Package Contents

- `SKILL.md` for runtime instructions
- `references/` for restoration rules, identity protection, uncertainty handling, and colorization discipline
- `examples/` for prompts, uncertainty messages, and behavior examples
- `tests/` for text-only corpus and manual review templates
- `scripts/` for deterministic package validation and read-only image inspection

## Made by MorenaTech

Built as a careful scaffold for manual visual testing of old-photo restoration workflows, not as a promise of automatic historical truth.
