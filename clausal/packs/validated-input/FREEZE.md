# Freeze of the rule pack "validated input", version 1 (plan node K1)

Committed before any target code (the toy parser `kvparse`, its book, its Lean words) was written, and before any
TDFLite file was read for this purpose. Source: `docs/studies/2026-11-12/packs.md`, sections 1, 2a, 4 and 5. The
sentence shapes were tried once against the compiler with words of the ledger fixture standing in for the slots
(every shape compiled except the draft of VI-7a, refused UNBOUND); no kvparse word existed.

What is frozen, all in `pack.yaml`:

1. **Template sentences**: 11 members (VI-1 to VI-10, VI-7 as 7a and 7b), 13 sentences and one draft once the variants
   are counted. They are the study's table rows, written in the live forms of the book (`is at most`, `accepted`).
2. **Slot list**: 18 slots. The study names 5; the other 13 are the project words its table rows use without naming them
   as slots (the number of fields of the result, the field limit, field of the input, known field, and so on).
3. **Variant list**: four axes: size (bounded, unbounded), unknown items (reject, ignore, preserve), duplicates (reject,
   first-wins, last-wins), canonical (canonical-only, lenient). Five choices have no sentence and say so.
4. **Adequacy expectation**: the instantiated suite must exclude reject-everything, accept-everything and
   return-a-default, each applied as a replacement of the project's parse.
5. **Seeded bug list**: the study's six; "length off by one" is applied in both directions, so seven mutants.

## How the results are counted (fixed here, before the run)

- **Member count** is 11. A member is *stated* on a target if its sentence for the chosen variant compiles; *workaround*
  members (VI-7b, VI-8 reject, VI-9) count as stated and are listed separately; a member is *cannot be stated* if its
  sentence is refused by the compiler or the pack has no sentence for the chosen variant; *not applicable* if the axis
  choice removes it (VI-4 and VI-5 for an unbounded format); *waived* if the project declines it, with a reason.
- **Stateability target**: at most a third of the members cannot be stated (at most 3 of 11). Counts against: more than
  a third, or any change to `clausebook/core.yaml` or `lean/Frames` made for the pack.
- **A mutant is shown false by a stated rule** if, in a pipeline run on the mutated crate, at least one pack rule that is
  not refuted on the unmutated crate gets the verdict REFUTED. Every such rule is reported per mutant, and the result is
  also reported with VI-10 left out, and with VI-10 and VI-7b left out (the two members that pin the value).
- **The main negative result** is a seeded bug or a trivial implementation that no stated pack rule shows false while the
  completeness line lists every member that could have shown it as stated. It is reported first if it happens.
- **Strip test**: the pack directory deleted, the bindings file deleted and the `@pack` tags stripped from the feature
  file; every verdict code of `out/graph.json` must be the same as with them.
- **Expected verdicts of the instantiated rules on the first target** are written to `kvparse/expected.json` and committed
  before the first pipeline run that includes them.

## Not frozen here, and why

- The words that fill the slots on a target: they are the target's book. The pack says what each must mean (`means:`).
- Which member shows which bug false: `by:` is the study's expectation, reported beside what the run gives.
