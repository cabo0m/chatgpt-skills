# Quality Checklist

Run this review before finishing.

## Identity

- Does it still look like the same person?
- Does the result still feel like a better photograph of the same person?
- Would a person familiar with the subject immediately recognize them?
- Are facial proportions stable?
- Does the apparent age remain consistent?

## Features

- Are glasses unchanged except for the requested glare fix?
- Does the hairstyle remain recognizably the same in length, color, hairline, and overall character?
- Are distinctive marks still present unless the user explicitly requested removal?

## Texture And Anatomy

- Does the skin still look natural rather than plastic?
- Are presentation improvements subtle and believable?
- Has the model improved the photograph rather than redesigning the person?
- Are there anatomy artifacts around eyes, teeth, ears, hands, or shoulders?

## Background

- Does the background match the requested mode?
- Was text, logo, or decoration added without permission?
- For transparent output, is the background genuinely transparent?

## Severity

- Critical: different person, major age drift, broken guard behavior, fake transparency.
- Major: clear geometry drift, changed glasses, noticeably different hairstyle, unwanted wardrobe change.
- Minor: small halo, mild oversmoothing, small cleanup artifact, or non-critical presentation drift.

## Repair Rule

Allow at most one automatic correction, and always anchor the correction to the original source image.

If the problem is still present after that one repair, stop and explain the limitation.
