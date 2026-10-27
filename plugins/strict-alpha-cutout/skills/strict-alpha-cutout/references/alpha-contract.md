# Alpha contract

## strict-binary

A strict pass requires a real alpha-capable PNG with only two alpha values:

- background: 0
- preserved foreground: 255

Any alpha value 1..254 is a failure.

A white, black, checkerboard, blurred, or background-colored fill is not transparency.

Do not describe a result as technically validated unless the actual output file was inspected.

## natural-edge

Intermediate alpha is permitted only after explicit user opt-in and only on justified edge structures such as hair, fur, glass, smoke, or motion blur.

The background itself remains fully transparent.

## preservation

Alpha cleanup must not become subject redesign. Preserve geometry, identity, color, labels, existing logos, text, accessories, and thin structures that belong to the foreground subject.
