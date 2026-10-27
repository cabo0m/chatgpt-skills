# Positive Examples

## Example 1

Input:

> Refresh this kitchen without renovation. Keep the layout, cabinets, window, sink, cooker, floor, and room size. Tidy the counters, improve the light, and make it feel calmer.

Chosen mode:

- `declutter-and-brighten`

MUST PRESERVE

- room geometry
- camera viewpoint
- exact framing
- wide-angle distortion
- window
- cabinetry layout
- cabinet color
- sink position
- cooker position
- floor
- countertops
- wall tiles
- circulation width

MAY CHANGE

- clutter
- lighting
- small decor
- countertop organization
- white balance

MUST NOT ADD

- island
- extra window
- moved sink
- wider room
- straightened perspective
- cabinet recolor
- new countertops
- new floor

Expected result:

- cleaner counters
- calmer room
- better light
- same cabinet color and same materials
- same kitchen

Why PASS:

- the room is improved without inventing space or changing the layout
- it still looks like the same phone photo, not a redesigned showroom

## Example 2

Input:

> Design this living room around my sofa and dining table. Keep both.

Chosen mode:

- `keep-my-furniture`

MUST PRESERVE

- sofa
- dining table
- room geometry
- circulation

MAY CHANGE

- rug
- lamp
- wall color
- accessories

MUST NOT ADD

- oversized replacement furniture
- blocked walkways

Expected result:

- updated styling around the protected pieces

Why PASS:

- the protected furniture remains clearly the same and still fits naturally

## Example 3

Input:

> Odswiez waska kuchnie bez remontu i bez wymiany mebli. Zachowaj uklad, brazowe szafki, ciemne blaty, plytki, stol, okno, zlew, kuchenke i proporcje pomieszczenia. Usun tylko luzny balagan i delikatnie popraw swiatlo.

Chosen mode:

- `declutter-and-brighten`

MUST PRESERVE

- same room width and depth
- same framing
- same perspective
- same brown cabinets
- same dark countertops
- same tiles and floor
- same table
- same window
- same sink and stove

MAY CHANGE

- loose clutter
- small accessories
- exposure
- white balance

MUST NOT ADD

- wider room
- straightened geometry
- lighter cabinets
- replacement counters
- replacement appliances
- catalog makeover

Expected result:

- visibly cleaner narrow kitchen
- modest lighting improvement
- no renovation cues

Why PASS:

- every protected structural and material cue remains intact while the clutter is reduced
