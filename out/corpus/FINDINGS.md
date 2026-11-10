# Machine-corpus run: findings (2026-11-10)

Reviewed and rerun. Assembled from the final agent's report. Corpus: OpenAI's machine-generated Navier–Stokes/Euler formalisation (commit `f9e8bc5b`), with two human projects that have blueprints (PFR, Carleson) as ground truth.

## What was built
- All 2,659 files of the machine corpus compiled; 52,505 declarations (38,601 theorems) and 553,759 dependency edges exported from Lean. The median theorem is 8 source lines.
- PFR (1,118 declarations, 225 theorems in its blueprint) and Carleson (3,199 declarations, 229 in its blueprint) exported the same way.
- Scripts: `bench/outline.py`, `bench/validate_outline*.py`, `bench/corpus_reuse.py`; exporters under `corpora/`.

## H3: does graph structure predict what humans put in a blueprint? Not through dominators.

| Score | PFR | Carleson |
|---|---|---|
| Graph-only model (ranking quality, 0.5 = chance) | 0.85 | 0.87 |
| Gain from adding all dominator features | +0.001 | +0.003 |
| Theorem's own proof size alone | 0.77 | 0.81 |
| Everything beneath it, no dominators | 0.83 | 0.87 |

- The dominator gain is indistinguishable from zero in 12 of 12 variants. What the graph detects is mostly proof length and whether a theorem is in the main argument.
- "Short statement hiding a lot" points the wrong way: blueprint statements are longer than average (median 383 vs 191 nodes in PFR, 1,477 vs 239 in Carleson).
- Structure does better than membership: plain reachability between blueprint nodes recovers 87% (PFR) and 94% (Carleson) of the human dependency edges.
- A reviewer tried five ways to break the null result and could not.

## Outline of the machine proof: a correct map of bottlenecks, mostly unreadable

| | Navier–Stokes | Euler |
|---|---|---|
| Proof behind "chapters" (one statement is the only way in to 20+ declarations) | 65% (61 chapters) | 42% (54) |
| Skippable by trusting the top level of the outline | 56.5% with 13 statements | 33% with 19 |
| …of which behind a readable statement | about 10% | 0% |
| …behind an opaque "x : SomeStructure" | 42.6% | 11.6% |

- Most of what could be skipped sits behind statements that say nothing until a structure is unfolded, and unfolding needs over 40% of all definitions below the theorem.
- Of the 16 heaviest chapter statements, one reader rated 2 as milestones; a second reading agreed but was not blind.
- Against the paper's own outline: the leading profile, moment matching, the correction cycle and the comparison step are matched; the base field, torus charts and mean corrections are not.
- The paper's Section 3 plus file docstrings remain a better reading map. The outline adds which declarations are bottlenecks and which files sit beneath them.

## Redundancy: not what makes the corpus hard to read

- Repeated non-trivial sub-proofs: 0.15% and 0.03% of proof size in two samples, against 0.20% in Mathlib.
- Identical theorem statements: 0.9% (PFR 0.7%, Carleson 0.5%).
- Upper bound for a deduplication or generalisation pass: 3.7% of theorems, realistically about half that.
- 468 theorems were actually re-derived from a general statement and accepted by the kernel, including a new 39-line Sobolev estimate for arbitrary order.
- Specific to the machine corpus: copy-and-modify instead of generalising (13 cloned files, the same estimate proved for two parameter ranges).
- **For scale: 32.4% of theorems are used by none of the four headline theorems.** Dead code is an order of magnitude larger than duplication.

## Limitations
- H3 was tested on two human projects from one community; the machine corpus has no blueprint.
- Readability ratings are one reader's on 16 statements; the comparison with the paper is by filename keyword and by an agent, not an analyst.
- "Skippable" counts proof size only.
- In-proof redundancy comes from two samples of about 500 theorems.

## Next steps suggested by the run
1. Make chapter statements readable (unfold a structure's fields one level, or use the paper's sentence) and rate them blind.
2. Build a ground truth for the machine corpus by mapping the papers' numbered results to Lean declarations.
3. Remove dead code first: mechanical, checkable by compilation, and far larger than deduplication.

Detail: `out/corpus/validation/VALIDATION.md`, `out/corpus/outline/OUTLINE.md`, `out/corpus/reuse/REUSE.md`; reviewers' evidence in `out/corpus/review_method/` and `out/corpus/review_reader/`.

---

# Friction census and "packets" (2026-11-10)

Reviewed and rerun. This tested claims from an earlier chat, which gave no data: that analysis proofs bloat in four places, that machine proofs unfold abstractions humans keep, and that bundling side-conditions into "packets" would help. Corpora: the machine Navier–Stokes/Euler project against Carleson (human, harmonic analysis), with PFR as a second human project. 42,254 theorems exported at hypothesis level.

## Verdict per claim

| Claim | Verdict | Key numbers |
|---|---|---|
| A. Constants are threaded by hand (`∃ C, 0 < C ∧ …`) | Supported as a pattern, moderate in size | About 9% of machine proof mass, counting constants hidden inside the project's own predicates. A lemma that uses an `∃ C` lemma re-exports one 69.8% of the time (0.6% otherwise), in chains up to 13 deep. Carleson has one direct case; it names its constants |
| B. Cast and finiteness tax between ℝ and ℝ≥0∞ | Not supported for the machine corpus | Finiteness goals are 0.07% of its proof mass. The claim describes Carleson, which states estimates in ℝ≥0∞ |
| C. Domain surgery (indicators, cutoffs, supports) | Not supported | Under 1.5% of hypotheses in the machine corpus |
| D. Measurability / integrability / smoothness side-conditions | Partly supported; size not robust | 6% to 15% of machine proof mass depending on the counting rule. On theorems about integrals, machine and human both spend about a tenth of proof mass on it |
| Machine proofs unfold abstractions | Cannot tell | Statements are more bundled in the machine corpus, but elaborated proofs keep no record of unfolding. A source-level count points the chat's way (`change` used 0.31 times per `rw` against 0.02) |
| Packets help | Marginal as tested | A four-fact structure on 9 real theorems, kernel-checked: statements shrink 5.7% to 10.4% net, hypotheses go from 83 to 56, but proofs grow 7.6% because every outside lemma still takes the facts separately. This was a mechanical port, not proofs written for the packet |

## Two things the chat did not predict

- **The largest bulk is proving equations**: 53.5% of machine proof nodes sit under an equation goal. This is not machine-specific (Carleson 58.7%, PFR 68.5%).
- **The one excess that survives every control is type-class instance arguments**: 27.1% of machine proof nodes against 16.6% in Carleson. Unexplained; Lean and Mathlib versions differ between the corpora.

Also: the machine corpus already built packets of its own. 6.4% of its hypotheses are a project predicate carrying a smoothness fact, and 2.8% pair smoothness with a hidden constant bound. They carry smoothness and bounds, not measurability.

## What cannot be concluded

- Nothing can be attributed to machine authorship: one machine project, one comparable human project, different subjects and tool versions.
- How much of any of this is avoidable. The census measures where proof mass sits, not what a better abstraction would save.
- Whether a "≲" notation would remove the constant threading.

## Next steps suggested by the run

1. Measure unfolding and side-condition automation from the tactic-level record of each proof.
2. Find out why instance arguments are 27% of machine proof nodes.
3. A packet-native experiment on the corpus's own predicates: write the closure lemmas a human library would have, or a "≲"-style relation, and re-prove a family of theorems against them.

Detail: `out/corpus/friction/CENSUS.md`, `BUNDLES.md`, `ROBUSTNESS.md`, `SUMMARY.md`; family definitions in `bench/friction_families.json`.
