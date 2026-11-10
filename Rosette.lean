/-
Rosette: lemma boundaries inside elaborated Lean proof terms.

Library modules:
* `Rosette.Candidates` — enumerate candidate lemma boundaries (Prop-typed subterms) of a proof.
* `Rosette.Lift`       — turn selected candidates into kernel-checked lemmas.

Experiments (they `import Mathlib`; the heavy ones only run when an environment variable is set,
otherwise they just elaborate):
* `Rosette.Tests`  — tests on eight Mathlib theorems; runs at compile time (a few seconds) and
                     rewrites `out/rosette_tests_candidates.jsonl`.
* `Rosette.Corpus` — ground-truth corpus for H1 (`ROSETTE_CORPUS=1`).
* `Rosette.Bench`  — boundary-recovery benchmark for H1 (`bench/run_bench.sh`).
* `Rosette.Reuse`  — statement recurrence across proofs for H2 (`bench/run_reuse.sh`).
* `Rosette.Demo`   — three long proofs lifted hierarchically; runs at compile time (about a
                     minute) and rewrites `out/demo/generated/`.
-/
import Rosette.Candidates
import Rosette.Lift
import Rosette.Tests
import Rosette.Corpus
import Rosette.Bench
import Rosette.Reuse
import Rosette.Demo
