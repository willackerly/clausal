# Fixes after the adversarial review of the ledger: what was rerun

| File | What it is |
|---|---|
| `before_fix_reviewer_mutants.log` | the reviewer's mutants `r1`..`r5` run through the harness on a snapshot of the tree BEFORE any fix: `r1`, `r2`, `r3`, `r5` change no example row and give the search nothing (lost proofs only); `r4` is caught by one row. Reproduces the review. |
| `r3_reproved_after_fix_run.log` | the reviewer's own patch (`../loops/r3_survivor_reproved.diff`: mutant `r3` plus a lemma and two proofs rewritten to fit it) applied to the fixed tree: `./run.sh` exits 1, with a counterexample to `whole_rejected_unchanged` replayed on the compiled Rust. Before the fix the same patch gave exit 0. |
| `mutation_run_after_fix.log` | console output of the full harness on the fixed tree (45 mutants, 15 controls). Results: `../../mutation/results.md`. |

The account of the fixes is in `../../DESIGN.md` section 12.8.
