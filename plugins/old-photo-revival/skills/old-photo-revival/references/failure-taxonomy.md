# Failure Taxonomy

## Severity Classes

- `acceptable_variation`: small restoration change that does not alter identity, age, expression, or historical character
- `minor_drift`: noticeable but non-critical drift; the result may still be usable with caution
- `major_drift`: clear change in identity cues, age, expression, gaze, clothing, jewelry, or historical character
- `critical_identity_drift`: the output looks like a different person or a loose reinterpretation

## Failure Labels

- `identity_drift`: the output looks like a different person
- `age_drift`: the person looks clearly younger or older than in the source period
- `expression_drift`: the facial expression changes materially
- `gaze_drift`: gaze direction changes materially
- `face_geometry_drift`: facial structure changes
- `beauty_model_drift`: the result looks glamorized or model-like
- `modern_makeup_drift`: contemporary makeup cues appear
- `hairstyle_invention`: hairstyle is changed beyond restoration
- `jewelry_invention`: new jewelry appears or visible jewelry is reimagined
- `clothing_invention`: clothing is invented or materially changed
- `background_invention`: background details are created without support
- `historical_detail_invention`: insignia, medals, text, or other historical details are invented
- `false_color_certainty`: estimated colors are presented as certain
- `sepia_color_collapse`: color technically exists, but most of the image collapses into one warm sepia, beige, brown, yellow, or orange palette instead of natural colorization
- `neutral_tone_loss`: blacks, whites, or grays are pushed into yellow, brown, or orange when they should remain neutral
- `local_color_separation_failure`: important elements are not chromatically distinct enough for believable colorization
- `incomplete_colorization_first_pass`: a direct colorization request returns mostly tinted restoration instead of full colorization on the first pass
- `print_normalization_failure`: the person may be restored, but the photographed paper print still looks skewed, bordered, yellowed, or phone-captured
- `over_sharpening`: restoration creates harsh digital sharpness
- `waxy_skin`: skin becomes plasticky or unreal
- `fake_texture`: synthetic or painted texture replaces photographic material
- `face_asymmetry_removal`: characteristic asymmetry is erased
- `excessive_eye_enlargement`: eyes become unnaturally larger
- `modern_studio_conversion`: the old photograph becomes a contemporary studio portrait
- `restoration_overreach`: repair goes beyond supported restoration and redesigns the image

## Colorization Failure Notes

### sepia_color_collapse

Symptoms:

- skin, background, jewelry, and shadows share nearly the same warm palette
- lips barely separate from the skin
- sclera looks yellow or brown
- hair and clothing merge
- metal looks orange and plastic
- the whole image reads as tinted sepia rather than natural colorization

Severity:

- `minor_drift` when only a small region is affected
- `major_drift` when most of the image collapses into one warm cast

For `faithful-colorization`, major sepia-color-collapse is an automatic fail even if identity is preserved.

### neutral_tone_loss

Definition:

Neutral blacks, whites, and grays lose neutrality and shift into warm tinting.

### local_color_separation_failure

Definition:

Skin, lips, eyes, hair, clothing, jewelry, and background are not sufficiently separated in color for believable natural colorization.
