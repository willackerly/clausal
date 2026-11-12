# Second target, written down in advance: TDFLite label intake

Written at the freeze, before the first target (`kvparse`) existed and without reading any TDFLite code, the private
pilot or the private planning notes. Its only source is the tracked study (`docs/studies/2026-11-12/packs.md`, sections
2a and 3), so it is a prediction made from that study's mapping table: the later measurement on TDFLite is a recall
check contaminated by that table (the study says so), and this file adds no contamination from the first target.

| Slot | Predicted fill | Sure? |
|---|---|---|
| `parse` | the operation that takes one label as written and answers its parts ("parse of a label") | yes |
| `well_formed` | "the label is well-formed": exactly the segments the format names and nothing after the value | yes; the whole content of VI-2 is here |
| `not_well_formed` | its negated form | yes |
| `length`, `limit` | none predicted: the study names no size limit for a label | axis `size`: unbounded unless the owner rules a limit |
| `count`, `count_limit` | not applicable under `size: unbounded` | – |
| `encoding`, `input_value` | "the written form of the result", "the label" | yes if intake is canonical-only; the owner's ruling on trailing segments decides the axis `canonical` |
| `field`, `is_known` | "label of the resource", "resolves in the snapshot" (one level up: the operation is then intake of a resource's labels, a second instantiation with its own `parse`) | predicted |
| `unknown_differs` | "the labels differ only in labels that do not resolve" | only if the owner chooses `ignore` |
| `unknown_field`, `extra_field` | none predicted | only if the owner chooses `preserve` |
| `key`, `is_repeated` | "hierarchy level of the claim", "is repeated in the claim" | predicted; a third instantiation (intake of a claim) |
| `reference` | "the reference engine's reading of the label" | predicted; needs a signed definition |
| `encode` | none | VI-7a is not stateable anyway |

Predicted axis choices are the owner's, not this file's: `unknown` and `duplicates` are exactly the rulings the study
says the pack should force into the open.

Predicted difficulties, to be checked against the measurement and not corrected afterwards:

1. One pack instantiation has one `parse`. Label intake looks like three operations (a label, the labels of a resource,
   a claim), so "the second target" may be two or three instantiations, each using a part of the pack.
2. A condition that compares two parts known before the call ("the namespace of the label is a namespace of the policy")
   is not a slot of this pack. It would be a second `only if` sentence written by hand, or a part of `well_formed`.
3. Matching without regard to case has no member of its own: the study maps it to VI-8 `ignore` with a case variation or
   to VI-10. If the owner's ruling is "case matters", the bug is shown false only through `well_formed` or `reference`.
4. If intake is over strings, the extracted model has axioms for string operations; the first exercise would be against
   the pilot's Lean model, where this pack's sentences are about a model and not about extracted Rust.
