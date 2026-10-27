# Colorization Guidelines

## Start With User Knowledge

Ask whether the user knows:

- eye color
- hair color
- skin tone
- clothing color
- jewelry color
- uniform or period attire details
- background color or material

## Use Reference Photos Carefully

Reference photos can help only when they plausibly belong to the same person and similar life period.

Use them for:

- likely hair color
- likely eye color
- clothing color if the garment is truly the same

Do not use them to:

- age-shift the person
- modernize grooming
- replace historical ambiguity with false certainty

## Preferred Color Character

- calm
- muted
- historically plausible
- respectful of the original light
- locally distinct
- balanced between warm, cool, pink, neutral, dark, and light regions where the image supports it

Muted and historically plausible colors must not collapse into a uniform sepia, beige, brown, yellow, or orange palette.

Conservative colorization means restrained saturation, not monochromatic warm tinting.

## Default Strength

Default strength is `natural`, not `conservative`.

- `conservative`: restrained saturation, but still requires local color separation and neutral tone retention
- `natural`: default, balanced and realistic
- `vivid`: somewhat stronger separation and saturation without beauty-styling

Avoid:

- bright blue or green eyes by default
- strong red lips
- white-glamour teeth
- visible modern makeup
- over-saturated skin tones
- uniform warm tint over the whole image
- yellow or brown sclera
- merging black hair and black clothing into one undifferentiated mass
- orange metallic jewelry

## Local Separation Requirements

Faithful colorization should preserve natural distinction between:

- skin
- lips
- sclera
- irises
- hair
- clothing
- jewelry
- background
- highlights
- shadows

Unknown color does not justify giving all of those areas the same warm tone.

When exact colors are unknown, select distinct, restrained, and plausible local colors. Do not replace uncertainty with uniform warm tinting.

## Skin

Require:

- subtle variation across warm, cool, pink, and neutral notes
- visible difference between cheeks, forehead, nose, and neck where supported
- natural texture
- no waxy mask
- no flat yellow-orange layer

## Lips

Require:

- natural separation from surrounding skin
- moderate believable color
- no modern lipstick look
- no merging into surrounding face color

## Eyes

Require:

- neutral sclera
- iris separation from sclera and pupil
- estimated iris color when unknown
- caution with blue and green defaults

## Hair And Dark Clothing

Require:

- tonal and textural separation
- neutral black, graphite, or natural dark brown handling
- preserved shadow detail
- no orange-brown flooding of dark regions

## Jewelry

Require:

- preserved shape and count
- believable metallic highlights
- estimated metal type when unknown
- no bright orange metal look

## Background

Require:

- a distinct tone from skin and hair
- a calm historically plausible color
- preserved original lighting logic
- no whole-image warm filter

## Do Not Overclaim

Never present estimated colors as exact or historically confirmed unless the user provides trustworthy supporting evidence.
