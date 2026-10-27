# Quality Checklist

Run this review before finishing.

## Identity

- Is this clearly the same room?
- Does it still look like an edit of the source photo, not a new inspirational room?
- Are the same width and depth preserved?
- Are the walls, windows, doors, ceiling, and floor geometry preserved?
- Is the camera viewpoint preserved?
- Is the original framing preserved?
- Is the perspective preserved instead of being straightened into a different-looking room?
- Is the room still the same visible size?

## Layout

- Are fixed installations still in the same places?
- Are cabinet count, positions, and proportions preserved?
- Are countertop lengths preserved?
- Are circulation paths usable?
- Can doors, drawers, appliances, and cabinets still open?
- Do new objects realistically fit?

## Scope

- Were only allowed elements changed?
- Were cabinet colors preserved when the user did not ask to recolor them?
- Were countertops, tiles, and floor preserved when no material change was requested?
- Were only loose clutter and small movable items removed?
- Did the edit improve the room without inventing extra space?
- Does the result look achievable without structural remodeling?
- Is the room visually calmer without being emptied of useful items?
- Does it avoid looking like a full catalog renovation?

## Style And Realism

- Are lighting and colors believable?
- Does the room avoid a generic luxury-showroom appearance?
- Does the result still respect the room's original function and character?

## Classification

- `PASS_FAITHFUL_RESCUE`: same room, same geometry, same protected materials and fixtures, only allowed cleanup or styling changes
- `MINOR_CONTENT_DRIFT`: same room and geometry, but a small unrequested loose-item or decor change went a bit too far
- `MAJOR_STYLE_DRIFT`: same room, but the result acts like a redesign, recolor, or catalog makeover
- `MAJOR_GEOMETRY_DRIFT`: same room identity is weakened by changed perspective, width, depth, layout, or cabinet proportions
- `CRITICAL_STRUCTURE_DRIFT`: fixed architecture, cabinetry, or fixtures changed so much that it is no longer a faithful edit
- `INSPIRATION_ONLY`: attractive image, but not an acceptable edit of the provided room

## Repair Rule

Allow at most one automatic correction, always anchored to the original source image.

If the result still has geometry or structure drift after one correction, stop and label it `INSPIRATION_ONLY`.
