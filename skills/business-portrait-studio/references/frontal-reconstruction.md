# Frontal Reconstruction

Use this contract only when a business portrait must be en face or nearly en face and the source is strongly off-axis, or when a first frontal result has perspective distortion.

## Source Roles

When correcting a failed frontal result:

- the original photograph is the authority for identity, apparent age, facial character, hair, skin, body proportions, and accessories
- the failed frontal result may be used only for pose, crop, clothing, lighting, and background continuity
- never use the failed result as the sole identity reference

State these roles explicitly in the image-edit instruction.

## Frontal Geometry Contract

Require one coherent frontal perspective:

- both eyes sit at a believable common height and scale for the head position
- pupils look naturally toward the lens
- the nose is centered consistently between the eyes
- philtrum, lips, chin, and jaw follow the same facial center line
- distances from the nose center to the outer eye corners are plausible
- cheekbone, temple, jaw, and face-outline widths are plausible on both sides
- the reconstructed side is not visibly compressed, stretched, or flattened

Natural human asymmetry should remain. Do not demand perfect mathematical symmetry during the first pass.

## Narrow-Side Correction

If one reconstructed side is visibly narrower because the model compressed the unobserved geometry:

1. Anchor the correction to the original photograph.
2. Identify which side is better supported by visible source evidence.
3. Use that side as the shape reference for the other side's eye spacing, cheek width, jaw width, and face outline.
4. Mirror geometry across the facial center line only as much as needed to remove the perspective defect.
5. Keep skin pores, fine lines, marks, lighting texture, hair, gray-streak placement, jewelry, and accessories naturally non-mirrored.
6. Preserve a seamless center line without repeated texture.

If the user explicitly asks to mirror the left or right side, treat left and right as image-space directions unless they clearly say anatomical left or right. State that assumption briefly before editing when confusion is likely.

## Stop Rule

Allow one targeted correction. If identity, anatomy, or frontal geometry still fails, stop and explain that the source angle does not provide enough evidence for a reliable en-face reconstruction. Recommend a frontal source photograph rather than repeatedly mutating the face.
