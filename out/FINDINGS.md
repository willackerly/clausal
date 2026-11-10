# Maths core: findings (2026-11-09)

Both hypotheses failed on human-written Mathlib. The tooling works; the scoring idea does not.

## What was built
- `Rosette/Candidates.lean`: lists every proof-valued piece of a theorem's proof term with its sizes, dependencies and stand-alone statement.
- `Rosette/Lift.lean`: `#rosette_lift Foo.bar` turns chosen pieces into real lemmas and rebuilds the theorem on top of them; Lean's kernel re-checks everything. No lifting failures in a 1,274-theorem sweep.
- `bench/`: the test set (323 theorem/helper pairs from Mathlib), benchmark and reuse scripts. `lake build Rosette` succeeds (62 s).

## H1: does "proof hidden per unit of statement" find the human's lemma boundary? No.
323 theorems, helper lemma pasted back in, median 112 candidates each.

| rule | first pick % | top-5 % |
|---|---|---|
| hiding ratio | 7.7 | 47.1 |
| proof size only | 5.9 | 40.9 |
| depth in the proof only | 5.9 | 34.1 |
| fewest dependencies (the earlier "small state" idea) | 0.0 | 3.1 |
| random | 1.9 | 9.0 |

- Most of the margin over random is shared with rules that ignore statements entirely.
- When the helper is under half the size of its theorem (82 cases), the ratio is at chance (top-5 6.1% vs 6.0%).
- Asked where to stop among nested choices, the ratio picks the human's cut 4.6% of the time; a random pick gets 22.7%.
- The "small state" idea is worse than random.

## H2: do statements recur across proofs? Not usefully, in Mathlib.
600 theorems in three areas. 4,122 statements recur, but 98.6% are automation output or facts the library already has. 18 survive with any saving, worth 0.2% of proof size, and none is clearly worth naming.

## Readability demo
Three hand-picked long proofs, one rater.
- Pell's equation and Erdős–Ginzburg–Ziv: lifted lemmas form a fair outline of the textbook argument.
- Sobolev inequality: only exponent arithmetic comes out; the real steps have statements of ~900 nodes and 15 hypotheses. Needs presentation taken from the source text, not a better score.
- Unfiltered, 25 of 45 lifted statements are junk; filters cut that to 6.

## Prior art (`out/prior_art.md`)
- All five papers in the original chat's table exist; one was misdescribed.
- The closest work was missing from it: Proof-Refactor (arXiv:2606.03743) already does single-proof extract-and-repair into helper lemmas.
- The proof-to-statement ratio is already published as a descriptive measure (Aksenov et al., arXiv:2603.20396).
- OpenAI's Navier–Stokes/Euler repository is already about 38,500 theorems with a median length of 10 lines. Its proofs are small; what it lacks is hierarchy and a small readable interface.
- Apparent gaps: repository-scale restructuring across proofs, a deterministic score instead of an LLM judge, and selecting which statements a human must read.

## Limitations
- Everything was measured on a library humans had already factored; nothing here covers machine-generated proofs.
- The H1 test set favours large, explicitly marked helpers, and counts a good-but-different lemma as a miss.
- H2 classes are heuristics; savings are bookkeeping, no shared lemma was actually factored.
- The demo ratings come from one reader on three chosen theorems.

## Next steps
1. Run on machine-generated proofs (the OpenAI repository), where both hypotheses are untested.
2. Move from scoring pieces inside one proof to selecting interfaces in the dependency graph between lemmas.
3. Present statements relative to their parent's context so analysis-style proofs become readable.

Detail: `out/bench/RESULTS.md`, `out/reuse/REUSE.md`, `out/demo/README.md`, reviewers' evidence in `out/review_*`.
