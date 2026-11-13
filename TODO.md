# TODO

The plan is `docs/PLAN.md` ("Status after the wave of 2026-11-13" first); results are in `docs/RESULTS.md`; the state of everything is in `docs/HANDOFF.md`. This file is the short list.

## Internal priority

- [ ] **T9 `tdf-core`: TDFLite's decision core fully built and proved** (owner's top operational priority; north-star example).
  - [x] T9.1 ID-level spec; T9.2 Rust core; T9.3 32 statements; T9.4 bridge and Rust intake (18 + 2 statements); T9.6 three-way run, 0 unexplained; T9.7 first Clausal layer (20 of 26 sentences).
  - [ ] Move the crates, proofs and harness from `private/tdf-core` into `/Users/will/dev/TDFLite-Rust` (branch `rust/core`), with history.
  - [ ] Fold the must-fix findings into the ASCII-plane design (`TDFLite-Rust/docs/rust-core/03-critique-of-02.md`), then build the encoder with its injectivity proof.
  - [ ] T9.5 read permit owning the request; other verbs gated on it; the two key atoms (`rewrap`, `validate binding`).
  - [ ] The six blocked sentences: "or" between conditions; operations with more than one input.
  - [ ] T9.8 bundle verification and anti-rollback (read the scoped-generation design first); T9.9 hand-over.

## TDFLite: two tracks

- [ ] The plan for Go consolidation (policy-bundle work finished and tested end to end in Go first) and the Rust refactor in parallel, with its dependency graph, is in the TDFLite repository: `/Users/will/dev/TDFLite-Rust/docs/program/TWO-TRACK-PLAN.md` (branch `rust/core`). This repository's part is the Rust track's proofs and the Clausal layer.
- [ ] Open questions for the owner, consolidated: `private/QUESTIONS-2026-11-13.md` (git-ignored).

## Waiting on the owner (nothing here blocks work)

- [ ] Review a first slice of `clausebook/core` and record it as a person's attestation (H1): `clausal/clausebook/REVIEW-SHEET.md`. Nothing is reviewed by a person.
- [ ] Take the comprehension trial once its item bank exists; recruit two or three others (H2, Q7).
- [ ] The ten questions for the owner and Tim in `TDFLite-Rust/docs/rust-core/01-sentinel-docs-and-rust-direction.md` (edge profile or replacement; library or service).
- [ ] Register the names if wanted; send the five Aeneas reports, or not.
- [ ] Rename the local checkout directory when nothing is running.

## Next

- [ ] Repair the five stale mutation controls and the composer self-check; rerun the harness on a quiet machine.
- [ ] L1f a model as constrained, attested proposer; then L4r and L5 on fresh sentences.
- [ ] W-track: state "the verifier returns" in the assumption; W5 ranked "rests on" block tested on readers; W7 on the TDFLite key atoms.
- [ ] K1: widen the pack's search by default; second target (TDFLite label intake).
- [ ] Q7 trial with Q9 gate; Q10 README TDFLite rows; Q11.
- [ ] The 17 book-check violations: person review of proposed separations.
- [ ] R2 a real crate, R3 its history.
- [ ] H3 strict mode after H1.
- [ ] X4 housekeeping (disk; `docs/SCHEMA.md` with Route B); X6 mathematics strand to its own repository.

## Done

Waves of 2026-11-12 and 13: see `docs/RESULTS.md`.
