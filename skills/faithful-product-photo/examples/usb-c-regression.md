# USB-C Regression: Connector Ownership

## Source scenario

Retail photograph of a 3-pack of USB-C to USB-C cables:

- white cable
- black cable
- light gray cable
- printed retail card
- shop shelf and price strip in the surrounding scene

## Observed failure

A generated cleanup was visually convincing but changed component ownership around the white and black cable connectors.

The important bug was not simply "wrong connector count."

It was:

**the output no longer preserved which visible connector belonged to which cable.**

## Regression requirement

For repeated cables, validate each cable instance:

| Check | White | Black | Gray |
|---|---|---|---|
| color preserved | required | required | required |
| visible cable body preserved | required | required | required |
| visible connector type preserved | required | required | required |
| connector ownership preserved | required | required | required |
| cable ties preserved | required | required | required |

## Occlusion guard

If the source does not clearly show a second connector belonging to a cable, do not invent one to make the layout symmetric.

## Pass condition

The output can be called faithful only when the source/output comparison supports the same visible topology.
