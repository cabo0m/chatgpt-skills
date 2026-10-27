# Edit Mode Contracts

## natural-retouch

Allowed:

- exposure correction
- white balance correction
- modest contrast tuning
- subtle cleanup of temporary blemishes
- minor stray hair cleanup
- subtle improvement in hair neatness
- natural-looking skin presentation improvement
- conservative crop improvement

Forbidden by default:

- face reshaping
- de-aging
- heavy smoothing
- strong makeup
- a noticeably different hairstyle
- hair color change
- teeth whitening beyond natural realism

Output:

- one edited portrait
- same person
- no text or logo

## background-cleanup

Allowed:

- removing clutter
- simplifying the background
- replacing the background with a neutral or explicitly requested one
- preserving or slightly improving clothing presentation if needed for a clean result

Forbidden by default:

- changing clothing
- changing pose
- dramatic relighting that changes the person
- adding logos, props, or decorations

Output:

- one edited portrait
- background matches request
- person remains intact

## transparent-background

Allowed:

- removing the background
- preserving fine edges like hair, glasses, and semi-transparent boundaries
- allowing minor presentation cleanup without changing recognizability

Forbidden by default:

- fake checkerboard backgrounds
- flattening to opaque output
- trimming away shoulders or hair to make segmentation easier

Output:

- one image
- real alpha channel
- format such as PNG

## professional-headshot

Allowed:

- neutral calm background
- conservative crop for head-and-shoulders or half body
- natural lighting refinement
- mild cleanup consistent with a business portrait
- slight hair neatness improvement
- subtle skin presentation improvement
- professional but natural framing
- small clothing-presentation cleanup when it does not redesign the subject

Forbidden by default:

- stock-photo glamor look
- wardrobe replacement
- dramatic cinematic styling
- changing profile view into a frontal face
- a noticeably different hairstyle
- age reduction
- face slimming or jaw narrowing

Output:

- one business-appropriate portrait
- natural, credible, still the same person
- presentation may be improved, but identity must remain unmistakable

## glasses-glare-fix

Allowed:

- reducing reflections
- restoring clarity if the eyes remain reasonably inferable from the source

Forbidden by default:

- inventing brand-new eyes
- changing frame style
- removing glasses entirely

Output:

- one portrait with glare reduced
- frames and eye area still consistent with the source

## Edge Cases

- If there are multiple people, ask which person to edit.
- If the source is too small or blurred, warn before editing.
- If the request needs missing body regions, say they will be generated and may drift.
