# TODO

Ordered by what unblocks the most. Tick items off and move finished work into `docs/EXPERIMENTS.md`.

## Waiting on the owner

- [ ] Read the 14 glossary entries in `slice/out/report.md` and sign them: `cd slice && python3 -m slicegen review all --reviewer NAME`. Until then every "proved" rests on an unreviewed reading of the English.
- [ ] Confirm `_to_delete/` can be deleted.
- [ ] Decide whether to put the repo under git (nothing is recoverable today; agents have already deleted superseded files).
- [ ] Rule on D1–D6 in `tdflite-ideas/` when ready; a pilot can start without them (see `docs/TDFLITE.md`).
- [ ] Say whether a mathematician is available to rate outlines; all readability ratings so far are from one model reader.

## In flight (collect results, then update README and EXPERIMENTS)

- [ ] Machine-corpus run: review and fix phases for experiments 9–11.
- [ ] Slice with loops (experiment 12): cost table and viability verdict.
- [ ] Friction census and packet experiment (experiment 13).
- [ ] Write `out/corpus/FINDINGS.md` once the above land (agents cannot create it).

## Next, maths side

- [ ] **Definition-centred outline.** Experiment 10 says the content is in definitions. Build the outline from structures and definitions (fields shown, or the paper's prose for them), with lemmas grouped under the concepts they are about.
- [ ] **Context-relative statements.** Print a lifted or outline statement relative to its parent: shared variables and local definitions stated once. Needed for analysis proofs (experiment 5).
- [ ] **Use the surface cues that worked.** Docstrings and naming predicted blueprint membership as well as the graph did; combine them with reachability for a "what to read" ranking, and test on a third blueprint project.
- [ ] **Compare with the paper.** Align the Navier–Stokes outline with the proof strategy described in the repository's own documentation; list stated steps the outline misses.
- [ ] Follow whatever the reuse and friction runs point to (general lemmas, bundles as structures).
- [ ] Have `Rosette` emit the refinement graph directly (`docs/SCHEMA.md`, open questions 1 and 2), including a structural hash for lifted lemmas.
- [ ] Get ratings from a second reader, ideally a human analyst, on a sampled (not hand-picked) set.

## Next, software side

- [ ] Act on the loops result: if proofs need hand-written invariants, try an agent writing them in the loop and measure success rate and cost.
- [ ] Random sampling in the counterexample search and in the two-readings comparison, so a bug away from boundaries yields a failing input.
- [ ] Multi-step scenarios (more than one When), if the loops run did not settle it.
- [ ] Make `./run.sh --strict` the default once the glossary is signed.
- [ ] A node kind for narrative claims that have no scenario.
- [ ] Try hax alongside plain Aeneas (TDFLite's plan prefers hax contracts).

## TDFLite (see `docs/TDFLITE.md`)

- [ ] Pilot: Lean model of the decision as it behaves today, guarantees 1–5 and D1–D6 as scenarios, expected verdicts recorded. No production code touched.
- [ ] "Model target" mode for the scenario generator (bind to a hand-written Lean model, not Aeneas output).
- [ ] Differential oracle recorded as `tested` evidence in the graph.

## Housekeeping

- [ ] Extend `.gitignore` before the first commit (done for the large directories; recheck).
- [ ] `bench/run_reuse.sh` has only been run step by step, never as a script.
- [ ] `Rosette.Bench` keeps its own copy of the enumerator; reconcile with `Rosette.Candidates`.
- [ ] Building `Rosette` runs Tests and Demo at compile time (1.5 minutes, rewrites files under `out/`); split them out of the default target.
- [ ] Disk: about 55 GB in this directory plus four Lean toolchains; prune corpora not in use.
- [ ] Lean library in `slice/` is still called `Wallet` though it now also holds the ledger.
