# Quality Gate

A result passes only if all relevant gates pass.

## 1. Fidelity gate

- same visible product count
- same visible component count
- same component ownership
- same colors
- same visible text / logo geometry
- same package geometry
- no invented hidden detail

## 2. Background gate

- no shelf
- no price strip
- no neighboring merchandise
- no wall/table/floor
- no fake checkerboard
- no generated studio scene when transparent output was requested

## 3. Alpha gate

When transparent output is requested and local inspection is available:

- PNG
- alpha channel present
- transparent pixel count > 0
- opaque pixel count > 0
- intermediate alpha accepted only in natural-edge mode

## 4. Edge gate

Inspect over white, black, and high-contrast color.

Reject:

- white/dark/color halo
- clipped corners
- lost cable ties
- missing thin metal pieces
- residual background islands
- unintended interior holes

## 5. Honesty gate

Never use these claims without evidence:

- pixel validated
- exact preservation
- faithful cutout

If machine validation was unavailable, say so.
