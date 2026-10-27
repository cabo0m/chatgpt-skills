# Restoration Modes

## Restore Only

Goal:

- repair technical damage
- preserve the original monochrome, sepia, or already-existing character
- avoid introducing new color or modern styling
- normalize photographed paper prints into clean reproductions when needed

Allowed:

- dust removal
- scratch removal
- small crack repair
- fold cleanup
- contrast and level correction
- paper discoloration reduction
- mild sharpening
- scan straightening
- gentle noise reduction
- crop away non-content paper border when it is a capture artifact
- straighten a tilted print
- correct mild perspective distortion from photographing the print

Forbidden by default:

- colorization
- face redesign
- skin beautification
- hairstyle change
- makeup
- clothing change
- modern studio conversion

Warnings:

- warn if the requested repair requires reconstructing large missing facial regions

Typical issues:

- over-sharpening
- waxy skin
- false face cleanup that changes age
- leaving phone-capture border, tilt, or paper cast untreated

Stop when:

- restoration would require guessing major facial structure or unreadable historical detail

## Faithful Colorization

Goal:

- preserve the photograph and the person
- add calm, plausible color
- clearly mark uncertain colors as estimated when references are absent
- produce natural local color separation rather than one warm global tint
- execute actual colorization on the first pass when the user explicitly asks to colorize

Strength levels:

- `conservative`: restrained saturation, full local color separation, neutral blacks, whites, and grays, no filter-like look
- `natural`: default; realistic color-photo feel with moderate saturation and clear but calm separation
- `vivid`: somewhat stronger separation and saturation, still period-respectful and never beauty-stylized

Allowed:

- user-informed color choices
- reference-photo-guided color estimation
- muted, believable tones
- color that respects the light structure of the original
- distinct but restrained local colors for skin, lips, eyes, hair, clothing, jewelry, and background
- natural separation between dark hair and dark clothing
- neutral sclera, believable metallic highlights, and preserved shadow detail

Forbidden by default:

- over-saturated eyes or lips
- white teeth glamour effects
- modern makeup
- claiming color certainty without evidence
- changing the age or era character
- uniform sepia, beige, brown, yellow, or orange tinting across most of the image
- brown sclera
- yellow-orange skin masks
- dark hair and black clothing merging into one flat area
- orange-plastic jewelry

Warnings:

- ask whether the user knows eye, hair, skin, clothing, jewelry, or uniform colors
- warn when colors are estimated rather than proven

Typical issues:

- false-color certainty
- beauty-model drift
- modernized skin or makeup
- sepia-color-collapse
- neutral-tone-loss
- local-color-separation-failure

Stop when:

- the user expects exact historical color without evidence
- one automatic correction still produces a uniform warm cast; stop and suggest a different strength level or reference data instead of iterating again

Automatic correction rule:

- if an explicit colorization request yields a result that still reads as sepia, beige-brown tinting, or partial colorization, perform one automatic correction anchored to the original source without asking the user to restate the request

## Natural Revival

Goal:

- create a natural restored version of an old portrait
- improve readability while preserving identity, age, expression, and era
- include print normalization when the source is a photographed paper print

Allowed:

- subtle tonal recovery
- careful cleanup of minor facial damage
- mild eye readability improvement
- natural skin and hair presentation
- reduction of harsh paper and scan artifacts

Forbidden by default:

- de-aging
- enlarged eyes
- reshaped nose, mouth, jaw, or cheeks
- symmetry perfection
- expression change
- modern fashion or beauty look
- clothing change
- hairstyle redesign
- new scenery

Warnings:

- warn before reconstructing large missing features
- warn when revival depends on estimation rather than visible evidence

Typical issues:

- modern studio conversion
- restoration overreach
- facial geometry drift

Stop when:

- the requested output becomes a reinterpretation instead of a restoration
