# Positive Examples

## Example 1

Source:

- faded sepia portrait with light scratches

Mode:

- `restore-only`

MUST PRESERVE

- recognizable identity
- period character
- monochrome or sepia feel

MAY CHANGE

- fading
- dust
- scratches
- tonal balance

UNKNOWN OR ESTIMATED

- exact fabric colors

Expected behavior:

- repair physical damage
- improve readability
- keep the image uncolorized

Why correct:

- the skill restores visible damage without inventing new history

## Example 2

Source:

- black-and-white portrait with no reliable color reference

Mode:

- `faithful-colorization`

MUST PRESERVE

- identity
- age
- expression
- hairline

MAY CHANGE

- color presentation
- mild tonal cleanup

UNKNOWN OR ESTIMATED

- eye color
- exact clothing color
- jewelry tone

Expected behavior:

- ask for known colors
- use calm estimated colors if the user does not know
- say that the colors are estimated

Why correct:

- the skill adds plausible color without pretending certainty

## Example 3

Source:

- old portrait with a small damaged patch on the cheek

Mode:

- `natural-revival`

MUST PRESERVE

- identity
- age at the time
- expression
- gaze
- hairstyle

MAY CHANGE

- small facial damage
- paper harshness
- skin readability

UNKNOWN OR ESTIMATED

- none beyond the tiny reconstructed patch

Expected behavior:

- repair the cheek damage conservatively
- keep the face natural
- avoid modern glamour styling

Why correct:

- the restored image remains the same person from the same era, only more legible

## Example 4

Source:

- damaged portrait plus a second photo from a similar period

Mode:

- `faithful-colorization`

MUST PRESERVE

- main source composition
- main source age
- main source expression

MAY CHANGE

- estimated color informed by the second image

UNKNOWN OR ESTIMATED

- any color not truly confirmed by the reference photo

Expected behavior:

- use the second photo only to guide visible traits or likely colors
- avoid copying a different age or hairstyle into the main image

Why correct:

- the reference photo helps without replacing the historical source

## Example 5

Source:

- black-and-white portrait without reliable exact color references

Mode:

- `faithful-colorization`

MUST PRESERVE

- identity
- apparent age
- expression
- gaze
- facial geometry
- hairstyle
- jewelry
- clothing shape
- historical character
- original lighting direction

MAY CHANGE

- estimated skin tones
- estimated eye color
- estimated hair color
- estimated clothing color
- estimated background color
- local color separation
- neutral balance
- natural saturation

UNKNOWN OR ESTIMATED

- iris color
- exact hair color
- exact clothing color
- metal type of jewelry

Expected behavior:

- skin shows subtle local variation instead of one flat warm mask
- lips are gently distinct from the skin
- sclera stays neutral
- irises are readable and marked as estimated when unknown
- dark hair remains visibly distinct from dark clothing
- jewelry keeps believable metallic highlights
- the background gets a separate calm tone
- the image still looks like an old photograph

Why correct:

- the result is restrained but truly colorized, not merely warm-tinted

## Example 6

Source:

- phone photo of an old paper print with a yellow border, slight tilt, and mild perspective skew

Mode:

- `restore-only` or `faithful-colorization`

MUST PRESERVE

- image content
- identity
- historical character

MAY CHANGE

- print border artifacts
- tilt
- mild perspective distortion
- paper cast caused by photographing the print

UNKNOWN OR ESTIMATED

- none beyond the usual color uncertainty if colorization is requested

Expected behavior:

- normalize the photographed print before deeper restoration
- remove the accidental border and straighten the reproduction
- keep the historical image itself intact

Why correct:

- the workflow restores both the photograph and the capture of the photograph, without redesigning the source
