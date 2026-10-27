# Quality Checklist

Run this review before finishing.

## Identity And Period

- Is the person still clearly recognizable?
- Is the apparent age from the time of the photograph preserved?
- Are expression, gaze direction, and head pose still consistent?
- Does the image still feel like it belongs to the same period?

## Restoration Fidelity

- Were scratches, dust, folds, and fading repaired without redesigning the face?
- Was any reconstruction limited and clearly signaled when necessary?
- Were unreadable details left uncertain instead of invented as facts?
- If the source was a photographed print, was the print itself normalized into a clean reproduction?
- Were border tint, tilt, and mild perspective problems removed when they were capture artifacts?

## Color Discipline

- If the user explicitly asked to colorize, did the first pass actually perform full colorization rather than warm-toned restoration?
- Are colors presented as estimated when they are not known?
- Do tones stay calm and believable?
- Was the original lighting logic respected?
- Does the result look naturally colorized rather than covered by a warm filter?
- Are skin, lips, eyes, hair, clothing, jewelry, and background chromatically distinct?
- Does skin contain believable local color variation?
- Are lips naturally distinct from surrounding skin?
- Are the sclera neutral rather than yellow, brown, or orange?
- Are dark hair and dark clothing visually separated?
- Are black, white, and gray areas still neutral where appropriate?
- Does jewelry retain believable metallic color and highlights?
- Are shadows free from excessive orange or yellow cast?
- Does the image avoid sepia-color-collapse?
- Would the result still look balanced after temporarily reducing saturation?

## Material And Presentation

- Does skin still look natural rather than waxy?
- Does hair still look natural rather than repainted?
- Were jewelry, clothing, and background preserved unless visible restoration justified a repair?
- Does the result look like a restored old photo rather than a modern beauty image?

## Severity

- Critical: different person, false certainty, major age drift, modern beauty conversion, broken guard behavior.
- Major: geometry drift, expression drift, gaze drift, invented clothing, invented jewelry, invented historical detail.
- Minor: mild oversharpening, small texture artifact, slight modernization that does not change identity.

## Repair Rule

Allow at most one automatic correction, always anchored to the original source image.

If the result still drifts after one correction, stop and explain the limitation.

If one automatic correction still produces a uniform warm cast, do not continue iterating. Return the attempt as unsuccessful and suggest changing colorization strength or adding reference data.

If an explicit colorization request still returns a sepia-like first pass, use the single automatic correction to complete the colorization instead of asking the user to repeat the request.
