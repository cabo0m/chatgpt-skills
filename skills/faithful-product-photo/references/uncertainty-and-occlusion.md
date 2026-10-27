# Uncertainty And Occlusion

## Core rule

Occluded does not mean absent and does not mean known.

Classify details as:

- `visible-confirmed`
- `partially-visible`
- `occluded-unproven`
- `unreadable`

## Editing rule

Only `visible-confirmed` evidence may be treated as factual geometry.

Partially visible material may be continued only when a non-generative geometric transform preserves the same pixels.

Do not use model priors to complete:

- hidden connector
- cable end
- label text
- package back
- cap underside
- internal product content

## Communication

If the requested result requires reconstructing an occluded edge, say that faithful certainty is not possible.

A preview may still be offered as reconstruction if the user wants one, but it is not a faithful cutout.
