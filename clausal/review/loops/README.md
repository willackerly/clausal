# Adversarial review of the ledger (loops) slice: evidence

Everything here was produced in scratch copies of `slice/` (made with `mutation/workcopy.sh`); the real tree was only read.

| File | What it is |
|---|---|
| `baseline_run.log` | `./run.sh` on an unmodified scratch copy: exit 0, 31 scenarios, regenerated `Generated/*.lean` and `Statements.lean` byte-identical to the builder's tree |
| `ReviewLoops.lean`, `ReviewLoops.out` | reviewer's Lean file and its output: type + axioms of all 17 ledger proofs; which model constants each statement reaches (only `Generated.Ledger`, never the hand-written `runN`); kernel-checked witnesses with batches of length 3, 4 and 5; atomicity of `apply_all` (proved by the lemma, stated by no scenario); cost probe for one new universal property |
| `review_cex.rs` | independent Rust test (no cucumber, no glossary): both REFUTED counterexamples fail on compiled Rust; the long-batch witnesses agree with the Lean model |
| `mutation_results_with_reviewer_mutants.{md,json}`, `mutation_run.log` | full rerun of the harness (40 builder mutants + 15 controls, all as recorded) plus 5 reviewer mutants `r1`..`r5` |
| `r3_survivor_reproved.diff`, `r3_survivor_reproved_run.log` | mutant `r3` (apply_all does not roll back once two transfers were applied) with the lemma and two scenario proofs re-proved against it: `./run.sh` exits 0, every scenario PROVED. A true survivor of the scenario set. |

Reviewer mutants: `r1` batch stops after three transfers; `r2` total sums only the first three accounts; `r3` no rollback once two transfers applied; `r4` a rejected last (non-first) transfer is counted; `r5` one unit minted on the third loop iteration (conservation false). `r1`, `r2`, `r3`, `r5`: no example row differs and the search finds nothing; the run fails only because a hand-written lemma no longer compiles.
