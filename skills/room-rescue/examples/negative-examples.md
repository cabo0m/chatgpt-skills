# Negative Examples

## Example 1

Bad result:

- a narrow kitchen becomes visibly wider

Why FAIL:

- `space_expansion`
- `critical_geometry_drift`
- `room_width_drift`

## Example 2

Bad result:

- the window moves
- a door disappears

Why FAIL:

- `architecture_drift`

## Example 3

Bad result:

- a kitchen island appears in a space that cannot support it

Why FAIL:

- `impossible_furniture_fit`
- `circulation_blocked`

## Example 4

Bad result:

- the model changes viewpoint to hide the real room constraints

Why FAIL:

- `camera_viewpoint_drift`
- `perspective_correction_drift`

## Example 5

Bad result:

- a historical interior is turned into generic white luxury minimalism without consent

Why FAIL:

- `style_overreach`
- `catalog_redesign_drift`

## Example 6

Bad result:

- decluttering removes useful furniture and fixtures instead of random clutter

Why FAIL:

- `over_decluttering`
- `unwanted_remodel`

## Example 7

Bad result:

- brown kitchen cabinets become pale beige even though the user asked only for cleanup

Why FAIL:

- `cabinet_recolor_without_request`
- `renovation_overreach`

## Example 8

Bad result:

- old dark countertops are replaced with bright stone surfaces in a no-renovation request

Why FAIL:

- `renovation_overreach`
- `catalog_redesign_drift`

## Example 9

Bad result:

- the sink, stove, or hood changes model or position in a refresh-only request

Why FAIL:

- `fixed_fixture_replacement`
- `layout_drift`
