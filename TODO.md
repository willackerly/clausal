# TODO

Phase 1 is closed. The plan for phase 2 is in `docs/PLAN.md`; the state of everything is in `docs/HANDOFF.md`. This file is the short list.

Names: Clausal (the language), the Clausebook (the library), the Clausal compiler. Code still says `slice`, `slicegen` and `vocabulary.yaml` until the rename (X5).

## Waiting on the owner

- [x] Decide name, form and first audience: Clausal, language first (2026-11-11, `DECISIONS.md`).
- [ ] Register the names if wanted (crates `clausal`, `cargo-clausal`, `clausebook`; domains). Nothing is registered.
- [ ] Sign `clausebook/core`, the 53 shared frames and modifiers, once C1 has split them out: `cd slice && python3 -m clausal review <entry-id|all> --reviewer NAME` (H1).
- [ ] Take the meaning trial once its new item bank exists, and recruit two or three others (H2).
- [ ] Send the five Aeneas reports, or not (`census/fork/upstream/`). Blocks nothing.
- [ ] TDFLite: read `private/tdflite-pilot/t2/AFTER-REVIEW.md` and `t3r/README.md`; say when `tdf-core` (T9) should start.
- [ ] Say whether to track `tdflite-ideas/` and `docs/TDFLITE.md` now that TDFLite can be discussed publicly.
- [ ] Decide whether the mathematics strand gets its own repository (recommended; frees about 150 GB here).
- [ ] Say when the repository rename may happen (X5).

## Phase 2, first wave (can start now, in parallel)

- [ ] L2 add the missing Clausebook pieces, each with one canonical sentence form.
- [ ] L3 separating inputs for pairs of candidate readings.
- [ ] L1 `clausal compose`, suggest mode, first version on today's pieces.
- [ ] C1 split the catalogue into `clausebook/core`, `clausebook/ledger` and local fixture bindings (before or with L2: same file).
- [ ] R1 wire the patched translator into the pipeline.
- [ ] E2 flag rules larger than every size tried.
- [ ] X4 housekeeping: prune disk (about 170 GB here), update `docs/SCHEMA.md` including Route B, redraw the pipeline figure.

Not in this wave, on purpose: synonyms or alternative phrasings in the static grammar.

## Then

- [ ] L4 the 48 frozen sentences, strict and through `compose`.
- [ ] H1 sign-off, then H3 strict mode on.
- [ ] H2 meaning trial on canonical sentences and separating inputs.
- [ ] R2 a real crate end to end and T9 TDFLite `tdf-core`, both on the same unmodified core; R3 replay history.
- [ ] L5 fresh sentences from new authors.
- [ ] M10, M11, T8 as capacity allows.
- [ ] X5 the rename, one commit, nothing else running.
