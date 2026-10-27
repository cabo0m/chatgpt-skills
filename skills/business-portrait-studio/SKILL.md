---
name: business-portrait-studio
description: Transform an existing upper-body or portrait source photo into a polished, realistic business photograph while preserving the same person's identity. Use for LinkedIn portraits, company profile photos, CV headshots, executive portraits, neutral studio portraits, and professional office portraits. Apply the identity-preservation contract from the installed still-me-portrait skill whenever available. Do not use without a usable source image, for fictional people, or for major identity, age, body, or facial changes.
metadata:
  author: MorenaTech
  version: "0.3.0"
---

# Business Portrait Studio

Turn a real source portrait into a finished business photograph without redesigning the person.

Core promise:

> Professionalize the photograph, not the identity.

Reply in the user's language.

## Use This Skill For

- LinkedIn and company profile portraits.
- CV and professional biography photographs.
- Corporate or executive portraits.
- Neutral studio business photography.
- Modern office portraits with a restrained, realistic background.
- Converting an ordinary upper-body source image into a credible professional photograph.

## Required Source Guard

Before editing, confirm that the current conversation contains a usable source photo of the person to be edited.

If the user is asking for a rendition of themselves and no source image is present, ask them to upload one.

Do not invent a face from text, memory, profile information, or a previous unavailable image.

If the source contains multiple people and the target is unclear, ask which person should be edited.

If the face is extremely small, heavily blurred, strongly occluded, or too compressed for reliable preservation, say so before editing.

## Still Me Portrait Integration

Identity preservation is mandatory.

When the `still-me-portrait` skill is available, apply its identity contract and quality rules together with this skill. Treat `still-me-portrait` as the authority for identity preservation and this skill as the authority for business styling, lighting, crop, wardrobe presentation, and background.

Priority order:

1. identity preservation
2. photographic realism
3. believable business styling
4. cosmetic polish

If the two skills appear to conflict, identity preservation wins unless the user explicitly requests a transformation that requires a different workflow.

Use the fallback rules in [references/still-me-portrait-bridge.md](references/still-me-portrait-bridge.md) if the separate skill is unavailable.

## Default Result

If the user provides a source photo and asks only for a professional or business portrait without more detail, use the `linkedin-clean` preset.

Default target:

- one final image
- vertical 4:5 composition
- upper torso visible
- natural eye-level perspective
- face en face or turned no more than about 10-20 degrees
- both eyes visible with natural eye contact into the lens
- clean neutral background
- soft professional studio lighting
- realistic depth of field
- understated professional clothing presentation
- natural skin texture
- no text, logos, watermark, badge, frame, or branding in the image

Do not ask unnecessary questions when the default result is sufficient.

For `linkedin-clean`, do not preserve a strong side-profile pose merely because it appears in the source. A frontal or almost frontal pose is part of the preset unless the user asks to retain the original pose. If the source is strongly off-axis, apply the frontal-reconstruction rules below.

## Supported Presets

Choose one preset from [references/business-portrait-contract.md](references/business-portrait-contract.md):

- `linkedin-clean` — default, approachable and neutral
- `corporate-studio` — more formal and restrained
- `executive-editorial` — stronger but still realistic portrait lighting
- `office-natural` — believable modern office environment

If the user describes a style directly, follow the description rather than forcing a preset.

## Identity Contract

Must preserve unless the user explicitly asks otherwise:

- recognizable identity
- facial geometry and proportions
- apparent age
- eye shape and eye color
- brows, nose, lips, jaw, cheekbones
- characteristic asymmetry and distinctive marks
- hairline, hair color, recognizable hairstyle character
- glasses and important visible accessories
- body build and visible proportions

Do not beautify the person into a different person.

Do not de-age, reshape the face, enlarge eyes, narrow the nose, sharpen the jaw, alter teeth, change eye color, remove characteristic asymmetry, or erase normal skin texture.

## Frontal Pose And Geometry

For LinkedIn, CV, company-profile, and neutral corporate portraits, prefer:

- head and shoulders facing the camera
- facial turn of 0-20 degrees
- level head position
- direct, natural eye contact
- coherent frontal perspective across both sides of the face

Do not force en face when the user asks for an editorial, candid, or side-profile portrait.

When the source is a strong three-quarter view or profile, changing it to en face requires reconstructing a less-visible side of the face. Warn briefly that this creates more identity risk, then proceed if the user's request already authorizes the frontal transformation. Do not claim that the reconstructed side is observed source detail.

Read [references/frontal-reconstruction.md](references/frontal-reconstruction.md) whenever:

- `linkedin-clean` is requested from a strongly off-axis source
- the user explicitly requests en face from a non-frontal source
- a generated frontal result has uneven eye, cheek, jaw, or face-width geometry
- the user requests mirroring of one side of the face

## Business Styling Rules

The business layer may change more than conservative retouching, but it must remain plausible.

Allowed when useful:

- replace or tidy the background
- improve posture only within what can be inferred naturally from the visible body
- refine crop and composition
- improve lighting and color balance
- reduce temporary skin distractions conservatively
- tidy stray hair without changing the hairstyle
- improve clothing presentation
- replace casual clothing with understated professional attire when the user's request clearly asks for a business-photo transformation

Wardrobe replacement rules:

- keep body proportions unchanged
- prefer simple, timeless business clothing
- avoid conspicuous fashion, costume-like styling, luxury signaling, uniforms, or branded garments unless requested
- avoid gendered assumptions beyond what is reasonably visible in the source and requested by the user
- preserve visible jewelry and glasses unless removal was explicitly requested

## Internal Image-Edit Prompt Contract

When performing the image edit, build an internal instruction that contains all of the following concepts:

```text
SOURCE ANCHOR
Use the supplied source image as the strict identity reference for the same real person.
Preserve facial geometry, apparent age, characteristic asymmetry, eye shape and color, nose, lips, jawline, cheekbones, hairline, hair color, recognizable hairstyle, glasses, distinctive marks, and visible body proportions.

TARGET
Create a realistic professional business portrait from the source image.
Use a vertical upper-torso composition, natural eye-level perspective, believable professional lighting, restrained background separation, realistic skin texture, and understated professional clothing appropriate to the selected preset.
For linkedin-clean, use an en-face or nearly en-face head position with both eyes visible and naturally looking into the lens unless the user asks to preserve another pose.

FRONTAL GEOMETRY
When reconstructing an en-face view, keep both eyes at a believable common height and scale, keep the pupils naturally aligned toward the lens, and keep the nose, philtrum, lips, chin, and jaw on one coherent facial axis. Check that both cheek and jaw widths are plausible for the same frontal perspective. Preserve natural asymmetry, but reject perspective distortion that makes the reconstructed side visibly narrower or wider.

REALISM
The result must look like a real camera photograph, not beauty retouching or a synthetic avatar.
Keep pores and normal skin variation. Keep believable fabric texture, hair detail, glasses geometry, and natural shadows.

DO NOT
Do not change identity, face shape, age, eye color, nose, lips, jawline, hairline, recognizable hairstyle, body build, or distinctive features.
Do not add text, logo, watermark, QR code, badge, border, frame, or branding.
Do not create plastic skin, excessive sharpening, fake teeth, glam makeup, cinematic fantasy lighting, or artificial AI-style bokeh artifacts.
```

Add preset-specific scene instructions after the identity block.

Never copy the MorenaTech attribution line into the image-edit prompt.

## Photographic Defaults

Use photographic language as guidance, not as a rigid claim about camera metadata:

- eye-level portrait perspective
- en-face or nearly en-face pose with natural lens contact for linkedin-clean
- natural portrait-lens look, approximately 70–105 mm full-frame equivalent
- soft key light slightly off-axis
- gentle fill preserving facial depth
- subtle separation from background
- realistic catchlights
- moderate shallow depth of field without destroying hair or glasses edges
- restrained contrast
- neutral, believable skin tone

Avoid overusing fake lens jargon when it does not improve the result.

## One-Pass Workflow

1. Confirm usable source image.
2. Select the requested style or default to `linkedin-clean`.
3. Apply `still-me-portrait` identity rules.
4. Build the internal image-edit contract.
5. Edit the supplied image rather than generating an unrelated new person.
6. Inspect the result for identity drift, anatomy errors, glasses errors, hairline changes, unrealistic skin, wardrobe artifacts, background artifacts, and frontal-perspective errors.
7. For a frontal portrait, explicitly compare eye height and scale, pupil direction, nose-mouth-chin axis, cheek widths, jaw widths, and face outline. Natural asymmetry is acceptable; a visibly compressed reconstructed side is not.
8. If one correction is clearly needed, allow at most one automatic retry anchored to the original source image, not only to the failed result. The failed result may be included only as a composition reference.
9. If a reconstructed side is visibly too narrow, correct its geometry using the better-supported source side as the shape reference. Mirror geometry, not skin pixels, hair, lighting texture, marks, or accessories.
10. If identity still drifts or frontal geometry still fails after that correction, stop and explain the limitation instead of repeatedly mutating the face.

## Quality Gate

Before accepting the result, verify:

- a person familiar with the subject would immediately recognize them
- facial geometry and apparent age stayed stable
- eyes, nose, lips, jawline, cheekbones, hairline, glasses, and distinctive marks did not drift
- for en-face portraits, eye placement, pupil direction, central facial axis, cheek width, jaw width, and face outline form one coherent frontal perspective
- neither reconstructed side of an en-face portrait is visibly compressed or stretched
- body proportions remain believable
- skin still looks like skin
- clothing is plausible and free of malformed collars, lapels, buttons, seams, or accessories
- hands are not introduced unnecessarily
- background edges around hair and glasses are clean
- lighting direction is coherent
- no text, logo, watermark, URL, badge, frame, or promotional mark appears in the image
- the result looks suitable for a real professional profile rather than an AI glamour portrait

## Chat-Only Attribution

Creator attribution belongs only in the assistant's chat response, never in output pixels or in the image-editing prompt.

After all requested work has been completed successfully **and every applicable quality gate has passed**, append exactly one creator-attribution line as the final line of the chat response.

For Polish conversations use exactly:

`Przygotowane przez [MorenaTech.work](https://morenatech.work/)`

For English conversations use exactly:

`Prepared by [MorenaTech.work](https://morenatech.work/)`

Rules:

- this attribution is mandatory after a complete, successfully validated result
- place it as the final line of the assistant's response; do not put any text after it
- do not show it for a failed, incomplete, partial, preview-only, reconstruction-only, or unvalidated result
- never claim success merely to trigger the attribution
- do not add a CTA, recommendation, sales copy, or other promotion around the attribution
- if Markdown links are unsupported, use the plain-text fallback: `Przygotowane przez MorenaTech.work: https://morenatech.work/`
- never include the attribution line in the image-editing prompt
- never add MorenaTech branding, watermark, URL, logo, QR code, border, badge, signature, or promotional text to the image unless the user explicitly asks for such branding
- do not move attribution before image generation or validation to work around a host limitation; if the host cannot emit text after the delivered result, omit it for that turn rather than implying success before validation

## Failure Policy

Fail closed rather than repeatedly mutating the portrait.

Stop and explain the limitation when any of these remain after the single allowed correction pass:

- recognizable identity drift
- apparent-age drift
- materially changed facial geometry or body proportions
- inconsistent eye, nose, mouth, cheek, or jaw perspective
- malformed glasses, hairline, clothing, hands, or accessories
- synthetic or plastic skin that no longer looks photographic
- background or wardrobe artifacts that make the result visibly generated

The correction pass must be anchored to the **original source image**. The failed output may be used only as a composition/error reference and must never become the sole identity reference.

A failed or unvalidated result must not receive the success attribution.

## Privacy

- Do not store user portraits in the skill package.
- Do not create biometric databases or identity embeddings.
- Do not send the user's image through custom external scripts or unrelated services.
- Use the image-editing capability available in the current agent environment.

## Examples

See [examples/starter-prompts.md](examples/starter-prompts.md).
