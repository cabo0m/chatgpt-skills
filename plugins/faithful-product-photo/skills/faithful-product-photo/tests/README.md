# Tests

This package uses text-only test cases. No user product photo is bundled.

## Static validation

```text
python scripts/validate_package.py .
python -m unittest discover tests/static -v
```

## Behavioral/manual evaluation

`cases.json` describes the expected runtime behavior.

Generate a report template:

```text
python scripts/generate_test_report.py
```

Then review each case against the selected image-editing client.

Important: passing static tests does **not** prove visual fidelity. It only proves package consistency and policy coverage.
