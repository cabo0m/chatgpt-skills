# Failure Taxonomy

## F01 - Source missing

No usable source image is present.

## F02 - Background residue

Shelf, price strip, neighboring product, wall, table, or other scene material remains.

## F03 - Fake transparency

White/checkerboard/generated background is presented as transparency.

## F04 - Alpha defect

PNG has no alpha, has invalid alpha for selected mode, or is technically empty.

## F05 - Product instance drift

Product count changes.

## F06 - Component count drift

A visible connector, cap, handle, cable tie, label, or other component appears or disappears.

## F07 - Component ownership drift

A component exists but is transferred to another product instance.

## F08 - Connector/type drift

Connector type or orientation materially changes.

## F09 - Color drift

Product or packaging color changes beyond conservative color correction.

## F10 - Text/logo drift

Visible brand, label, code, symbol, or printed claim changes.

## F11 - Packaging geometry drift

Package outline, hanger, blister, cutout, or structural fold is redrawn.

## F12 - Occlusion invention

Hidden detail is generated and presented as source fact.

## F13 - Edge erosion

Thin subject structures or corners are lost.

## F14 - Halo / color fringe

Removed background contaminates the edge.

## F15 - Over-retouch

Visible product wear, deformation, or real imperfection is silently removed.

## F16 - False validation claim

The response claims machine/pixel validation that was not performed.

## F17 - Reconstruction mislabeled as faithful

A generative redraw is presented as a faithful source-preserving edit.
