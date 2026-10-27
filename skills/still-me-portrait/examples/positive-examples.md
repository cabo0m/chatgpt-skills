# Positive Examples

## Example 1

User input:

> Prepare this for LinkedIn. Keep my glasses and make it look natural.

Missing question:

> Do you want a head-and-shoulders crop and a neutral background, or should I keep the original crop?

Internal contract:

```text
MUST PRESERVE
- facial geometry
- apparent age
- glasses
- hairline

MAY CHANGE
- crop
- exposure
- background
```

Expected behavior:

- Choose `professional-headshot`.
- Ask only the crop/background clarification.
- Produce one natural business portrait.

Why this succeeds:

- The scope is clear and identity protection stays explicit.

## Example 2

User input:

> Remove the background and give me a transparent PNG.

Missing question:

> None, unless the source is unclear or contains multiple people.

Internal contract:

```text
MUST PRESERVE
- person silhouette
- hair edges
- glasses

MAY CHANGE
- background only
```

Expected behavior:

- Choose `transparent-background`.
- Return one alpha-capable output.
- Avoid checkerboard fakery.

Why this succeeds:

- The request maps directly to a supported mode and a technical output requirement.

## Example 3

User input:

> Fix the glare on my glasses, but do not change how I look.

Missing question:

> If the eyes are heavily blocked, say that a faithful reconstruction may not be possible.

Internal contract:

```text
MUST PRESERVE
- glasses frame
- eye shape
- facial identity

MAY CHANGE
- glare intensity
```

Expected behavior:

- Choose `glasses-glare-fix`.
- Warn if the eyes are fully obscured.
- Keep the frames unchanged.

Why this succeeds:

- The mode is narrow, and the risk is acknowledged before editing.

## Example 4

User input:

> Clean up the photo a bit, but keep my age and skin texture.

Missing question:

> Which matters more here: better light, background cleanup, or both?

Internal contract:

```text
MUST PRESERVE
- apparent age
- skin texture
- facial geometry

MAY CHANGE
- light
- color
- background clutter
```

Expected behavior:

- Choose `natural-retouch` or a safe combination with `background-cleanup`.
- Avoid heavy smoothing.

Why this succeeds:

- The contract blocks common beauty-model drift before the edit starts.

## Example 5

User input:

> Make this into a professional headshot, but keep me clearly recognizable.

Missing question:

> Do you want a neutral background and a tighter professional crop, or should I keep the current framing?

Internal contract:

```text
MUST PRESERVE
- recognizable identity
- facial geometry
- apparent age
- glasses
- distinctive features

MAY CHANGE
- professional framing
- flattering but natural lighting
- skin presentation
- hair neatness
- minor grooming
```

Expected behavior:

- Choose `professional-headshot`.
- Allow slightly tidier hair, better light, and more polished presentation.
- Keep the face, age, and identity stable.
- Return a result that looks better, not redesigned.

Why this succeeds:

- Minor presentation improvements are acceptable because the person still looks unmistakably like themselves.
