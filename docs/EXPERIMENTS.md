# Experiment inventory

Everything tried so far, in order. One entry per experiment: the claim, how it was tested, the result, and where the evidence is. Update an entry when its status changes; add new ones at the end.

Status values: **final** (reviewed and rerun), **preliminary** (results exist, review pending), **running**, **not started**.

## Summary

| # | Experiment | Result | Status |
|---|---|---|---|
| 0 | Original scaffold ("Lean-Ghidra") | Discarded: never ran against Lean | final |
| 1 | H1: hiding ratio finds human lemma boundaries | Negative | final |
| 2 | "Small goal state" baseline | Negative, worse than random | final |
| 3 | H2: statements recur across Mathlib proofs | Negative | final |
| 4 | Kernel-checked lifting | Works | final |
| 5 | Readability of lifted statements | Mixed | final (thin evidence) |
| 6 | Prior-art check | Idea partly published | final |
| 7 | Vertical slice: wallet | Works after review fixes | final |
| 8 | Refinement-graph schema v2 | Fits both sides on small examples | final (thin on maths side) |
| 9 | H3: dominators predict blueprint nodes | Negative so far | preliminary |
| 10 | Dominator outline of Navier–Stokes | Partial, mostly unreadable | preliminary |
| 11 | Reuse in the machine corpus | — | running |
| 12 | Slice with loops (ledger) | — | running |
| 13 | Friction census and "packets" | — | running |

## 0. Original scaffold

- **What:** Python profiler scoring tactic states by "working-memory load" `W`, a slicer using `extract_goal`, a linter, a 2x2 agent arena.
- **Why discarded:** the example theorem was `sorry`, the trace was hand-written, analysis used regex, nothing had run in Lean.
- **Where:** `_to_delete/`.

## 1. H1: hiding ratio

- **Claim:** among all proof-valued pieces of a proof term, the piece a human factored out ranks high by proof size ÷ statement size.
- **Method:** 323 Mathlib theorem/helper pairs (helper private or `aux`-named, used at most twice). Paste the helper's proof back into the theorem, enumerate candidates, rank.
- **Result:** first pick 7.7%, top-5 47.1%, against 5.9% / 40.9% for proof size alone and 1.9% / 9.0% for random. At chance when the helper is under half its theorem's size. On the "where to stop" task it picks the human cut 4.6% of the time against 22.7% for random.
- **Why it fails:** most of the apparent signal is tree position; the ratio prefers the deepest large piece, humans cut higher.
- **Caveats:** test set favours large marked helpers; a good-but-different lemma counts as a miss.
- **Where:** `Rosette/Bench.lean`, `bench/score.py`, `out/bench/RESULTS.md`, `out/review_benchmark-validity/`.

## 2. "Small goal state" baseline

- **Claim (from the original brainstorm):** good boundaries are where few hypotheses are in play.
- **Result:** fewest-dependencies ranking gets first pick 0.0%, top-5 3.1%. Worse than random.
- **Where:** same files as 1.

## 3. H2: reuse in Mathlib

- **Claim:** closed statements recur across different proofs often enough to factor.
- **Method:** 600 theorems in three areas, 156,984 candidates, hashed up to bound-variable names; two generalisation levels; filters for automation output and library lemmas.
- **Result:** 4,122 statements recur; 98.6% trivial. 18 survive with any saving, 0.2% of proof size, none clearly worth naming.
- **Caveats:** filters are heuristics; no lemma was actually factored; humans had already done the factoring.
- **Where:** `Rosette/Reuse.lean`, `bench/reuse.py`, `out/reuse/REUSE.md`.

## 4. Kernel-checked lifting

- **What:** `#rosette_lift` turns chosen sub-proofs into real auxiliary theorems and rebuilds the original on top; the kernel checks both; results may not use new axioms.
- **Result:** no failures in a 1,274-theorem sweep. Two measurement bugs found in review and fixed (duplicated binders, tree-walk double counting).
- **Where:** `Rosette/Candidates.lean`, `Rosette/Lift.lean`, `Rosette/Tests.lean`, `bench/sweep.lean`.

## 5. Readability demo

- **Method:** lift lemmas from three hand-picked long proofs; one reader rates each statement.
- **Result:** Pell and Erdős–Ginzburg–Ziv give fair outlines. Sobolev gives only exponent arithmetic; its real steps have ~900-node statements. Unfiltered, 25 of 45 statements are junk; filters cut that to 6.
- **Lesson:** analysis proofs need statements shown relative to their surrounding context.
- **Where:** `Rosette/Demo.lean`, `out/demo/`.

## 6. Prior art

- **Result:** the five papers cited in the brainstorm exist (one misdescribed). Closest work, missing from it: Proof-Refactor (arXiv:2606.03743). The ratio appears in Aksenov et al. (arXiv:2603.20396). OpenAI's Navier–Stokes repository is ~38,500 short theorems in flat directories.
- **Gaps that looked open:** repository-scale restructuring, deterministic scoring, selecting what a human must read.
- **Where:** `out/prior_art.md`.

## 7. Vertical slice: wallet

- **Claim:** a Gherkin scenario can get a machine-checked verdict about real Rust.
- **Method:** Rust → Charon/Aeneas → Lean model; `.feature` + `glossary.yaml` → generated Lean statements; hand-written proofs; audit; the same feature file run by cucumber-rs.
- **Result:** 7 scenarios proved for all inputs, 1 proved for an instance, 1 false claim refuted with a counterexample confirmed on compiled Rust, plus unbound and vacuous controls.
- **Review found:** a proof of `True` counted as a proof (fixed); three real bugs survived because scenarios were incomplete (fixed with more scenarios and coverage theorems); a misleading glossary entry passed (partly fixed with a second reading in Rust).
- **Mutation test:** 18 of 18 injected bugs noticed after fixes (11 before). Example rows alone catch 17.
- **Open:** glossary unsigned; straight-line code only.
- **Where:** `slice/FINDINGS.md`, `slice/DESIGN.md`, `slice/mutation/`.

## 8. Schema v2

- **What:** nodes with an interface and implementations; edges with evidence (kernel-checked, tested, tool-trusted, human-asserted); staleness computed from digests.
- **Result:** validates the slice's graph (109 nodes, 275 edges) and an 11-node maths example assembled by script.
- **Open:** the maths tooling does not emit it; nine open questions listed in the doc.
- **Where:** `docs/SCHEMA.md`, `slice/schema/`.

## 9. H3: dominators predict blueprint nodes (preliminary)

- **Claim:** statements that large regions of a proof can only be reached through are the ones humans put in a blueprint.
- **Method:** PFR (1,118 declarations, 219 blueprint nodes) and Carleson (3,199, 180). Score every theorem by graph features; compare with blueprint membership.
- **Result so far:** graph-only model AUC 0.85 / 0.87, but dominator features add +0.001. The signal is proof size. Blueprint theorems have larger statements than average, so dividing by statement size hurts. "Has a docstring" does as well as the best graph score. Lean reachability recovers 87–94% of the human `\uses` edges.
- **Where:** `bench/validate_outline.py`, `out/corpus/validation/VALIDATION.md`.

## 10. Dominator outline of Navier–Stokes (preliminary)

- **Method:** dominator tree of the 52,505-declaration graph from each headline theorem.
- **Result so far:** one very wide hub. 13 statements cover 54% of the Navier–Stokes proof mass, 19 cover 33% of Euler. Of the 15 heaviest chapter statements, one reader rated 2 milestones, 9 technical, 4 unreadable. Chapter boundaries are mostly chosen objects whose content is in a structure defined elsewhere.
- **Lesson:** definitions, not lemmas, are the interface a reader cannot skip.
- **Where:** `bench/outline.py`, `out/corpus/outline/`.

## 11. Reuse in the machine corpus (running)

- **Plan:** cluster near-identical theorem statements across the Navier–Stokes corpus; write and check general lemmas for at least three clusters; repeat the in-proof measure for comparison with Mathlib's 0.2%.
- **Where:** `bench/corpus_reuse.py`, `corpora/ns_reuse/`, `out/corpus/reuse/`.

## 12. Slice with loops (running)

- **Plan:** an 85-line ledger over `Vec` with two `while` loops; scenarios including "any batch conserves the total"; effort log; loop mutants.
- **Known so far:** Aeneas translated it first time. `for` ranges, `iter().sum()` and `try_fold` closures do not translate with the pinned version.
- **Where:** `slice/ledger/`, `slice/DESIGN.md` section 12.

## 13. Friction census and packets (running)

- **Claims (from an earlier chat, unmeasured):** analysis proofs bloat from constant tracking, real/extended-real casts, domain surgery and measurability side-conditions; machine proofs unfold abstractions humans keep; bundling side-conditions into structures would help.
- **Plan:** hypothesis-level export of Navier–Stokes, Carleson and PFR; share of hypotheses and proof mass per family; mine recurring hypothesis bundles; define one as a structure and restate at least eight real theorems against it, kernel-checked.
- **Where:** `corpora/friction/`, `bench/friction_*.py`, `out/corpus/friction/`.

## Ideas ruled out or parked

| Idea | Why |
|---|---|
| Tune the hiding ratio further on Mathlib | Fails on controls, not just on headline numbers |
| Tactic-text slicing with `extract_goal` | Its own docs say the output may not type-check; term-level lifting is sound |
| Library-layer removal, module graphs, clustering as outline methods | Tried in experiment 10; none gives a narrow interface |
| LLM-judged readability as the main metric | Published already; kept as a possible comparison, not the core |
