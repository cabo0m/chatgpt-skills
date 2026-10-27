# QA checklist

Before accepting a cutout:

- confirm the file is PNG with real alpha
- confirm the foreground subject is the original subject, not a regenerated substitute
- check hair, fur, fingers, wires, handles, straps, glass rims, and other thin structures
- check for missing subject fragments and trapped background islands
- inspect for visible fringe or halo on white, black, and a strong contrast color
- in strict-binary mode confirm zero alpha values in 1..254
- confirm no fake checkerboard or solid background is baked into the output
- confirm no new logo, watermark, badge, URL, text, signature, frame, promotional overlay, or unrelated visual element was added
- confirm creator attribution exists only in chat text, never in image pixels or the image-tool prompt
