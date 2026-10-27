# Still Me Portrait Bridge



This skill is designed to work together with the MorenaTech `still-me-portrait` skill.



## Responsibility Split



`still-me-portrait` owns:



- identity preservation

- face geometry stability

- apparent age stability

- hairline and hairstyle continuity

- glasses and distinctive-feature protection

- conservative realism checks



`business-portrait-studio` owns:



- business-photo composition

- business wardrobe presentation

- professional lighting

- neutral studio or office background

- profile-photo suitability



Identity preservation always has higher priority than styling.



## Fallback Identity Contract



If `still-me-portrait` is not available in the current agent environment, enforce this minimum contract:



Preserve:



- recognizable identity

- facial geometry and proportions

- apparent age

- characteristic asymmetry

- eye shape and eye color

- eyebrow shape

- nose, lips, jawline, and cheekbones

- distinctive marks

- hairline, hair color, and recognizable hairstyle character

- glasses and important accessories

- visible body build and proportions



Do not:



- de-age or age-progress

- reshape the face

- change eye color

- replace the nose, lips, jaw, or cheekbones

- erase characteristic asymmetry

- replace glasses without explicit instruction

- move or redesign the hairline

- create a visibly different hairstyle

- smooth skin into a plastic texture

- reshape the body



## Retry Rule

If identity drift appears, retry at most once and anchor the correction to the original source image. Do not use a drifted generated result as the sole identity reference.

For an en-face reconstruction, the original source remains the identity authority. A failed frontal result may be reused only for crop, pose, and background continuity. If one side is visibly compressed, copy the better-supported side's geometry rather than its pixels or skin texture. Stop after one correction if identity or anatomy still drifts.
