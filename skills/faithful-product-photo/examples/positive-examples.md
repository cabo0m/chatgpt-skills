# Positive Examples

## Example 1 - Shop shelf cleanup

User:
> Usuń tło, półkę i cenówkę. Zostaw całe opakowanie.

Correct behavior:

- retains package card and its own hanger geometry
- removes shop price strip and neighboring merchandise
- preserves product colors and visible text
- exports real transparent PNG
- compares source and output before claiming success

## Example 2 - Repeated cable pack

User:
> Wytnij zestaw trzech kabli.

Correct behavior:

- tracks white, black, and gray cable separately
- traces visible connectors to the correct cable
- does not force visual symmetry
- treats occluded cable ends as unknown
- rejects the result if any plug changes ownership

## Example 3 - White background

User:
> Potrzebuję białego tła na Allegro.

Correct behavior:

1. create/validate transparent cutout
2. composite the validated cutout over pure white
3. do not redraw the product to create a cleaner studio rendering
