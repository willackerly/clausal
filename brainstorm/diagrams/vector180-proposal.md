# Proposal: native arrowheads and diamonds for Vector180

For the owner to consider for the office180 repository. Proposal text only; nothing there was changed. Written 2026-11-10 from experiments with the `vector180` CLI on PATH.

## What 0.1 does today (measured, not read from the docs)

| Construct | `validate` | `resolve` | `compile` to PPTX |
|---|---|---|---|
| Native `rect`, `ellipse`, `text`, `line`, untransformed or translated `g` | yes | yes | yes |
| Arrowhead as two short native `line`s (open chevron) | yes | yes | yes, as three connectors |
| Diamond or hexagon as four or six native `line`s (outline only, no fill) | yes | yes | yes, as four or six connectors |
| Right-angle route as several native `line`s | yes | yes | yes, one connector per segment |
| Pill as a stroke-less `rect` plus two stroke-less `circle`s of the same fill (filled, no outline) | yes | yes | yes, as three shapes |
| A native `line` with no `data-vector180-from`/`-to` (used for the head strokes and polygon edges above) | yes | yes | yes |
| Native geometry that is not a whole or half unit (for example 15.6 or 490.69 from computed offsets) | yes | yes | **refused** ("does not map exactly by factor 7620") |
| `rect` with `rx`/`ry` | yes | yes | **refused** ("Rounded rectangle ... outside the bounded C9 native subset") |
| Asset group (`role="asset"`, `export="svg"`, `data-vector180-bounds`) containing `polygon`, `path` (curves included), `polyline`, `defs` + `marker` + `marker-end`, gradients, `stroke-dasharray`, `stroke-linejoin`, inner `transform="rotate(..)"`, `use` of a same-document id | yes | yes | **refused**: one asset anywhere fails the whole atom ("the bounded C9 slice admits native objects only") |
| Asset group with no bounds, or with a `transform` on the group itself | yes | refused | refused |
| Asset nested inside a translated native group | yes | yes | refused |
| Native `polygon` or `path` with `role="shape"`; `line` with `role="shape"` | refused | | |
| Native `polyline` connector | yes | refused (outside C6) | refused |
| `marker-end`, `stroke-dasharray` or `stroke-linecap` on a native `line` | yes | refused | refused |
| `opacity` other than 1 on a native object | yes | yes | refused |
| A `class` attribute, an external `href`, or `script`, even inside an asset | refused | | |

Three things worth knowing that the authoring card does not say:

1. **`validate` is much more permissive than `resolve`.** Several constructs that pass `validate` cannot be resolved. An author who runs only `validate` gets a false green. The card should say "validate and resolve", or `validate` should warn.
2. **Asset bounds are declared, not checked.** A bounds box of `0 0 5 5` around a 100 by 60 polygon passes. That is consistent with "the tool never measures", but it means a wrong box is silent until someone opens the PPTX.
3. **Text inside an asset is invisible to `text-fit`** (it reported 0 lines). Labels must stay as native text objects on top of the asset.

4. **`compile` wants geometry that lands exactly on the EMU grid.** Whole and half units were accepted; values such as 15.6 were refused. Worth one line in the card ("prefer integers" is there, but not that anything else can fail the compile).

So in 0.1 the honest choice is: draw with lines only and keep the PPTX path, or use assets and get a figure that renders well everywhere but cannot be compiled at all. There is no middle.

The lines-only route goes further than expected. `chain-v2a` and `chain-v2b` in this folder use open-chevron arrowheads, right-angle routes, outline diamonds and filled pills, contain no asset, and compile (146 and 129 native objects). Quick Look's rendering of the compiled PPTX matched the SVG; it was not opened in PowerPoint. What the route costs:

- An arrow is three objects (five for an elbow), and the count of objects roughly triples. In PowerPoint the head does not follow the shaft unless the group is moved as one, and resizing the group distorts the head.
- Corners and tips are butt-capped strokes meeting, so each bend needs a half-stroke overlap to avoid a notch, and diamond vertices show a hairline notch at high zoom.
- A diamond cannot be filled, so it cannot hide anything behind it and its colour can only be carried by the stroke.
- An outlined pill or rounded box is impossible; a pill can be filled or it can be compiled, not outlined.
- All of this is only practical from a generator. Nobody should hand-edit 146 objects.

## Proposed additions, in order of value for effort

### 1. Arrowheads on native connectors

Source syntax: two attributes on a native `line`.

```xml
<line id="a-to-b" data-vector180-role="connector" data-vector180-export="native"
      data-vector180-from="a" data-vector180-to="b"
      data-vector180-end="triangle"
      x1="100" y1="130" x2="200" y2="130"
      stroke="#576b64" stroke-width="3"
      marker-end="url(#v180.end.triangle.576b64)"/>
```

- `data-vector180-start` and `data-vector180-end` take a closed vocabulary: `none`, `triangle`, `open`, `dot`. These map one to one onto DrawingML `a:headEnd` / `a:tailEnd` types `triangle`, `arrow`, `oval` (note DrawingML's naming: `headEnd` is the start of the line, `tailEnd` is the end).
- Size is fixed at DrawingML `med`/`med`, which is three stroke widths long and wide. SVG `markerUnits="strokeWidth"` gives the same proportions, so one marker definition renders the same in a browser and in PowerPoint without measuring anything.
- The atom must still render with no runtime, so the SVG `marker-end` reference stays in the source, pointing at a marker in a root `<defs>` whose content is **fixed by the profile**. The validator checks that each referenced marker is byte-identical to the canonical template for its type and colour, and that the `data-` attribute and the `marker-` attribute agree. Anything else is refused. (Root `<defs>` with a `<marker>` already validates, resolves and compiles today; it is simply ignored.)
- Colour: one canonical marker per stroke colour, id `v180.end.<type>.<hex>`. `fill="context-stroke"` would avoid the per-colour copies, but I am not sure every renderer GitHub readers use supports it, so I would not rely on it.
- Round trip: `reconcile` reads `headEnd`/`tailEnd` back into the two attributes. A size or type PowerPoint offers that the vocabulary lacks is reported, not approximated.

- `open` is the type the lean-rosette figures want (a thin open chevron); it is DrawingML `arrow`.

This is the single most useful addition. Every diagram that shows flow needs it, and today's alternatives are a dot at the end of the line (the current figures; reads as "joined", not "goes to") or three separate objects.

### 2. Compile `rx`/`ry` rectangles

The resolver already parses `rx`/`ry`; only the compiler refuses. Map to `prstGeom prst="roundRect"` with the adjust value `rx / min(width, height)`, require `rx == ry`, refuse otherwise. Smallest change on this list.

### 3. A closed set of preset polygons, diamond first

```xml
<polygon id="check.proof" data-vector180-role="shape" data-vector180-export="native"
         data-vector180-geometry="diamond"
         data-vector180-bounds="700 400 200 110"
         points="800,400 900,455 800,510 700,455"
         fill="#e4f2ec" stroke="#24735d" stroke-width="3"/>
```

- `data-vector180-geometry` names a preset; `data-vector180-bounds` gives its box; `points` must equal the canonical points computed from the box (and one optional adjust number), or validation fails. The author never gets a free polygon in the native set, so the "no silent approximation" rule holds.
- Start with `diamond` (DrawingML `diamond`), `hexagon` (`hexagon`), `pentagon-arrow` (`homePlate`), `triangle`. (The pill used for tools in `chain-v2a` and `chain-v2b` needs no preset: it is item 2 with `rx` equal to half the height.) Each is a preset PowerPoint users can restyle, resize and retype natively.
- Text stays a separate native text object grouped with the shape, as with rectangles. Optional later refinement: `text-fit` could compute capacity from the shape's width at the baseline instead of the frame, which matters for diamonds, where a second line has much less room than the first.

### 4. Compile opaque SVG assets as pictures

The profile already promises this ("atomic vector picture with declared bounds"). Until it lands, one decorative polygon makes an atom uncompilable, which pushes authors away from assets entirely. Emit the subtree as an SVG picture part with a PNG fallback at the declared bounds. This also covers every shape that is not worth a preset.

### 5. Elbow connectors

Accept a native `polyline` connector whose segments are axis-aligned, and map it to `bentConnector2/3`. The "bracket" that ties a check to the two artifacts it compares costs three lines today (see `chain-v2a` and `chain-v2b`); it is one object in PowerPoint.

### 6. Dashed strokes

`stroke-dasharray` from a closed vocabulary (`dash`, `dot`) mapping to `a:prstDash`. Wanted here for "assumed, nothing checks this" links. Lowest priority.

## What I would not do

- Free `path` or free `polygon` as native shapes. Custom geometry in PowerPoint is editable only point by point, and it breaks the property that a native object is something an ordinary user can restyle.
- Auto-routing or connectors that follow a moved shape. The profile's stance that explicit endpoints are authoritative is right; arrowheads do not need it.
- Arrowhead sizes beyond one. Every added size is another thing to keep identical across two renderers.

## Open questions for the owner

- Is PPTX round trip actually wanted for the lean-rosette figures? If they are only ever shown on GitHub, nothing here blocks that repository: the lines-only route already draws what it needs. Items 1 to 3 would cut the object count by about two thirds and make the result editable by a person; item 4 is what would allow filled diamonds.
- Is a profile-fixed marker in `<defs>` acceptable, given the "no theme, no shared definitions" stance for atoms? The alternative is an arrowhead with no SVG rendering at all, which fails the "renders anywhere" goal.
