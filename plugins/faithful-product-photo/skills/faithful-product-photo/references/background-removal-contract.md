# Background Removal Contract

## Default output

- PNG
- RGBA
- real alpha channel
- exterior scene removed
- subject retained

## Natural-edge alpha

Default for general product work.

- background exterior alpha = 0
- opaque subject interior alpha = 255
- intermediate alpha allowed only on antialiasing boundaries or genuinely translucent material

## Strict binary alpha

Use only when explicitly requested or when downstream tooling requires it.

Allowed alpha values:

`{0, 255}`

Binary alpha can damage glass, translucent plastic, fine fibers, motion blur, and antialiased curves. Do not silently switch to it.

## Never fake transparency

Invalid:

- white canvas presented as transparent
- checkerboard baked into RGB pixels
- blurred old background
- generated studio background claimed as removed background

## Scene shadow

A cast shadow belonging to the removed shelf/table/background is scene and should normally be removed.

A shadow or reflection physically printed on packaging is product evidence and must stay.

## Quality surfaces

Check the cutout on white, black, and a strong contrasting color.
