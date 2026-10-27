# Negative Examples

## Example 1

Source:

- old portrait with soft eyes and light damage

Bad outcome:

- eyes become much larger
- jaw becomes slimmer
- face looks younger

Why wrong:

- this is identity drift and beauty-model drift, not restoration

## Example 2

Source:

- black-and-white portrait for colorization

Bad outcome:

- bright blue eyes
- strong red lips
- glossy modern makeup
- colors described as original

Why wrong:

- estimated color was turned into false historical certainty and modernized appearance

## Example 3

Source:

- portrait with visible simple earrings

Bad outcome:

- new jewelry is invented
- clothing is redesigned
- background becomes decorative

Why wrong:

- the skill must preserve visible details, not add new fashionable ones

## Example 4

Source:

- damaged old portrait

Bad outcome:

- hairstyle changes materially
- modern studio lighting appears
- skin looks airbrushed

Why wrong:

- the image was converted into a contemporary portrait instead of restored as an old photograph

## Example 5

Source:

- heavily damaged face with one eye largely missing

Bad outcome:

- the skill reconstructs a full new face without warning

Why wrong:

- a major missing feature requires explicit warning because it is reconstruction, not recovery

## Example 6

Source:

- old portrait of a woman

Bad outcome:

- identity and age are preserved
- the entire image shifts into beige-brown warm tinting
- skin, lips, eyes, hair, clothing, and background are poorly separated
- the result looks like toned sepia rather than natural colorization
- the same output might be acceptable as `restore-only`, but not as `faithful-colorization`

Why wrong:

- this is `major_drift` caused by `sepia_color_collapse`, not successful faithful colorization

## Example 7

Source:

- phone photo of an old printed portrait

Bad outcome:

- the face is restored
- color may even be improved
- but the yellow paper border remains
- the print stays slightly crooked
- mild perspective skew is still visible
- the result still looks like a phone snapshot of a paper print

Why wrong:

- this is `print_normalization_failure`; the subject was edited, but the photographed print itself was not properly normalized
