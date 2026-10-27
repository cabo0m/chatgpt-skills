# Failure Taxonomy

Use these labels when describing what went wrong.

## Severity Levels

- `acceptable_variation`: minor presentation change that does not alter recognizability or the person's character
- `minor_drift`: noticeable but non-critical change; the person still clearly looks like themselves and the result may remain acceptable depending on goal
- `major_drift`: clear change in hairstyle, age, features, silhouette, or distinctive traits
- `critical_identity_drift`: the output looks like a different person or only a loosely similar person

- `identity_drift`: the output looks like a different person
- `age_drift`: the person looks clearly younger or older without being asked
- `beauty_model_drift`: the result becomes overly glamorized or generic
- `geometry_drift`: facial structure changes
- `skin_plasticity`: skin becomes waxy or unreal
- `glasses_mutation`: the frames or lenses change shape or style
- `hair_loss_or_invention`: hair changes so much in length, hairline, color, or overall character that recognizability is affected
- `anatomy_artifact`: visible structural artifact around face or body
- `background_hallucination`: unwanted objects or scenery appear
- `fake_transparency`: the output pretends to be transparent but is actually opaque
- `cinematic_over_stylization`: the result turns into a poster-like scene
- `unwanted_text_or_logo`: text, watermark, or logo appears without permission
- `guard_failure`: the skill fails to stop or warn when it should
