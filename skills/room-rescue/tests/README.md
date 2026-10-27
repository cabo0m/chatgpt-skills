# Tests

This directory contains:

- `cases.json`: public text-only corpus T01-T14
- `case-schema.json`: lightweight schema document for the corpus
- `manual-results-template.md`: template for manual visual evaluation
- `static/`: deterministic unit tests for package validation

The public package intentionally ships without image assets.

## Manual Case TXX

`TXX Narrow Kitchen No Renovation`

Description:

- narrow kitchen
- brown cabinets
- dark marble-pattern countertops
- existing beige wall tiles
- parquet or tile-pattern floor
- small table in the center
- window at the end
- sink and stove on the right
- clutter on counters

User request example:

> Odswiez ta waska kuchnie bez remontu i bez wymiany mebli. Zachowaj uklad, proporcje pomieszczenia, brazowe szafki, ciemne blaty, plytki, podloge, stol, okno, zlew, kuchenke i okap. Usun tylko luzny balagan, lekko popraw swiatlo i nie zmieniaj perspektywy.

Expected:

- same geometry
- same cabinet color, count, and positions
- same countertops, floor, and wall tiles
- same table, window, lamp, sink, stove, and hood
- clutter reduced
- exposure improved

Reject if:

- room looks wider
- perspective is straightened
- cabinet color changes
- cabinets are replaced
- countertops, floor, or tiles are replaced
- appliances move
- layout changes
- result looks like a catalog renovation
