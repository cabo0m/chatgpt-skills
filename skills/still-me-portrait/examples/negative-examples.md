# Negative Examples

## Example 1

User input:

> Make me look like a movie star.

Missing question:

> This is not a conservative retouch request. Do you want a different transformation workflow instead?

Internal contract:

```text
MUST PRESERVE
- none defined yet

MAY CHANGE
- unclear
```

Expected behavior:

- Do not pretend this is standard Still Me Portrait work.
- Flag it as stylization outside scope.

Why this fails if handled badly:

- The skill would drift into identity transformation.

## Example 2

User input:

> Here is half of my face. Make a full body corporate portrait.

Missing question:

> A full body result would require generating missing facial and body details. Do you want to proceed knowing fidelity may be low, or can you upload a wider source photo?

Internal contract:

```text
MUST PRESERVE
- visible facial identity

MAY CHANGE
- generated missing regions only with warning
```

Expected behavior:

- Warn before any edit.
- Prefer asking for a better source.

Why this fails if handled badly:

- Silent invention of missing anatomy breaks the identity promise.

## Example 3

User input:

> Fix this photo.

Missing question:

> What should improve here: light, background, crop, or glasses glare, and what must stay untouched?

Internal contract:

```text
MUST PRESERVE
- unspecified

MAY CHANGE
- unspecified
```

Expected behavior:

- Ask a narrow clarification instead of guessing.

Why this fails if handled badly:

- Vague prompts often invite over-editing and scope drift.

## Example 4

User input:

> Remove my glasses and make my jawline sharper.

Missing question:

> That request changes identity features and goes beyond conservative retouch. Should I route this to a different transformation workflow instead?

Internal contract:

```text
MUST PRESERVE
- identity features would be violated

MAY CHANGE
- not allowed in this skill by default
```

Expected behavior:

- Refuse to frame this as normal Still Me Portrait output.

Why this fails if handled badly:

- It directly violates the protected-feature contract.

## Example 5

User input:

> Make this a polished professional portrait, but keep me the same person.

Missing question:

> None, if the source image is usable and the scope is already clear.

Internal contract:

```text
MUST PRESERVE
- recognizable identity
- facial geometry
- apparent age
- hairstyle character

MAY CHANGE
- professional presentation only
```

Expected behavior:

- A small grooming improvement would be acceptable.
- A redesign is not.

Why this fails if handled badly:

- If the model significantly lengthens the hair, changes the hairstyle, makes the face younger, narrows the jaw, and creates a beauty-campaign look, it has redesigned the person rather than improving the photograph.

Difference to remember:

- Minor grooming means subtle tidying and believable presentation improvement.
- Redesign means visible identity drift, such as a noticeably different hairstyle, age, face shape, or overall glamorized persona.
