# Room Rescue

Room Rescue is a portable Agent Skill for refreshing a real room without pretending it is bigger, emptier, or architecturally different than it really is.

Core rule:

> Improve the room without inventing extra space.

This skill is for practical visual makeovers, not for architectural plans.

## Four Modes

- `declutter-and-brighten`
- `restyle-without-remodeling`
- `keep-my-furniture`
- `budget-refresh`

## What It Is Good At

- cleaning up visual clutter
- making a room calmer and brighter
- changing colors, finishes, and decor without structural work
- designing around furniture the user wants to keep
- improving style while respecting real layout constraints

## Example Requests

- "Odswiez te kuchnie bez remontu i bez zmiany ukladu."
- "Usun balagan z blatow, ale nie zmieniaj wyposazenia."
- "Zaprojektuj pokoj wokol tej sofy i stolu."
- "Pokaz budzetowa wersje metamorfozy."
- "Zmien kolory frontow i zaslony, ale nie przesuwaj szafek."
- "Zachowaj podloge, okno i kaloryfer."

## Important Limitations

- The result is a visualization, not a construction guarantee.
- The skill does not promise structural feasibility.
- It should preserve room geometry, perspective, installations, and circulation unless the user explicitly asks for a conceptual remodel.
- It should preserve framing, wide-angle distortion, cabinetry proportions, and visible materials in no-renovation requests.
- It should not invent extra space, hidden rooms, or impossible furniture fit.

## Same Room Contract

For cleanup and no-renovation requests, the skill should:

- edit the provided photo only
- keep the same framing and perspective
- keep the same room width and depth
- keep cabinet count, positions, and proportions
- keep cabinet, countertop, tile, and floor color unless the user explicitly asks to change them
- remove only loose clutter by default

If a result looks like a prettier but different room, it should fail the quality gate.

## Installation

Install this as a portable Agent Skill in a client that supports Skills and image editing.

The exact installation UI may vary by product and workspace. The important part is that the top-level folder remains `room-rescue/` and contains `SKILL.md` with the referenced materials.

## Validation

From the skill root, run:

```text
python scripts/validate_package.py .
python -m unittest discover tests/static -v
```

## Privacy

- This package ships without room photos from users.
- Do not add private interior photos to the repo, tests, README, or promo materials.
- Do not use images from social media as public examples without explicit rights and permission.

## Made by MorenaTech

Built as a friendly, reality-aware room-refresh scaffold for manual visual testing.

The first manual narrow-kitchen test produced attractive but geometrically unfaithful outputs, so this package now adds a stricter same-room quality gate.
