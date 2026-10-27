# Negative Examples

## Wrong: "Looks right"

A result contains the same total number of connectors as the source, so the assistant calls it faithful.

Why wrong:

One connector moved from the white cable to the black cable. Total count is insufficient.

## Wrong: retyping package

The source logo is slightly blurred. The edit replaces it with clean text.

Why wrong:

The output contains newly generated typography rather than preserved evidence.

## Wrong: checkerboard

The output shows a gray checkerboard but the PNG has no alpha channel.

Why wrong:

Transparency was simulated.

## Wrong: product completion

Only one cable end is clearly visible. The model draws a second end because "all cables have two ends."

Why wrong:

The hidden detail was inferred and presented as fact.

## Wrong: silent render fallback

The tool cannot mask source pixels, so it generates a clean 3D packshot and calls it background removal.

Why wrong:

That is `catalog-reconstruction`, not `faithful-cutout`.
