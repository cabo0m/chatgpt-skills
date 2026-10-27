# Business Portrait Studio

Portable ChatGPT/agent skill for producing credible professional portraits from an existing source photo while preserving the same person's identity.

Core promise:

> Professionalize the photograph, not the identity.

## Key safeguards

- usable-source guard
- explicit identity-preservation contract
- frontal-reconstruction rules for LinkedIn/CV portraits
- one correction pass anchored to the original source
- fail-closed identity and geometry gate
- no branding inside image pixels
- linked MorenaTech attribution only after a complete validated success

## Validation

From the skill root:

```text
python scripts/validate_package.py .
python -m unittest discover tests/static -v
```

Public tests are text-only and do not contain user portraits.
