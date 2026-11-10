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

---

# Maths track, second step (2026-11-10, overnight)

Four experiments, each checked by a reviewer on a different model. All readers and raters were models, labelled as proxies. Numbers below are the post-review ones.

## Dead code: confirmed by deleting and rebuilding

Everything classified dead was deleted in a copy of the machine corpus, and all four headline theorems still compile with the same three axioms.

| | Before | After | Change |
|---|---:|---:|---:|
| Project files | 2,657 | 2,424 | −233 |
| Source lines | 640,860 | 482,466 | −24.7% |
| Theorems | 38,601 | 26,961 | −30.2% |

- **Negative control:** 19 of 20 deletions of used declarations broke the build. The one that did not is a private instance that only shortens type-class search.
- **Hidden dependencies:** in a sample of 300 unreachable theorems, 8 deletions broke the build (2.7%). All are one-line `rfl` lemmas that `simp` uses without leaving a trace in the proof term.
- **Held back:** 1,810 unreachable declarations were not deleted (simp lemmas, instances, names used in `open` or `variable` commands).
- **The outline is unchanged** on the trimmed graph, byte for byte.
- A reader of this corpus can ignore about a quarter of it. The trimmed corpus proves the four headline theorems only; the paper-form local theorem and the appendix results are gone from it.

## Ground truth from the papers

- 117 numbered paper items (86 Navier–Stokes, 31 Euler) mapped to 321 Lean declarations, each mapping with evidence and a confidence.
- Two samples read against the paper: the builder's 20 (60% full match, 95% match or partial) and a reviewer's 15 (no wrong mapping among 10 at "certain" or "probable"; the "guess" level is unreliable, as labelled).
- Only 53 of the 85 mapped Navier–Stokes items lie below the headline theorem at all: the paper-facing restatements are mostly not used by the headline proof.
- Baselines: the dominator outline hits 8 of 85 Navier–Stokes items exactly (chance about 0.4) and 4 of 31 for Euler. "Has a docstring" is a strong cheap signal for Navier–Stokes and weak for Euler.

## Definition-centred outline: more followable, not more meaningful

| | Navier–Stokes | Euler |
|---|---|---|
| Proof mass beneath statements whose named definitions are all printed (old outline: 0% by the same mechanical test) | 28.0% | 0.35% |
| Median statement length, characters (old) | 299 (982) | 863 (1,047) |
| Paper items reached exactly (old) | 12 of 85 (8) | 7 of 31 (4) |

- Against the papers the gain is small and mostly comes from definitions, which only an outline that prints them can reach. Counting statements only: 10 against 8 for Navier–Stokes, 2 against 3 for Euler.
- **Proxy ratings (six model readers, 30 entries per outline):**

| Label | Old outline | New outline |
|---|---|---|
| Milestone | 8.3% | 6.7% |
| Technical step | 7.2% | 27.8% |
| Opaque | 83.3% | 17.2% |
| Unreadable | 1.1% | 48.3% |

- The new outline traded "opaque" for "unreadable". No more milestones surfaced. Whether the net is a gain depends on which model read: two readers of one model called most new entries unreadable.
- Readers agreed far less on the new outline (agreement 0.36 against 0.78), and six model readers behave more like three.
- The comparison is confounded by format: new entries are about five times longer and carry docstrings. It cannot separate "definitions shown" from "more text shown".
- Euler remains unreadable either way.

## Constant threading: Mathlib's big-O fits, but does not pay for itself here

The longest chain of hand-threaded constants (13 theorems) was restated through one relation and proved again, with Lean checking each new statement implies the original.

- **No new relation was needed.** Mathlib's big-O over a set fits the multi-parameter case exactly.
- **11 of 13 conclusions restated; 8 of 13 native proofs never handle an explicit constant.** Nothing was weakened.
- **Proofs shrank 2.4% to 4.2%.** Steps that only pass a constant along shrank 27%; steps that do analysis were flat; steps meeting an interface with explicit constants grew.
- **Statements did not get smaller** (source size roughly flat). What disappears is the `∃ C, 0 ≤ C ∧` prefix from 12 conclusions.
- **The supporting library costs about eight times the saving** on this family, and outside the family there was no measured saving: a sample of 10 other theorems came out larger where it went through.
- **The corpus had already built this relation at least three times without sharing it**: one project predicate is equivalent to big-O and carries its own copies of the algebra; two others hide a constant but have no algebra, so every use reopens them.

The honest reading: constant threading is real, but as proof compression it is a small prize (an optimistic ceiling of about 0.1% of the corpus). The more interesting observation is the last bullet: the machine re-invented an existing library abstraction several times instead of using or sharing it.

## What this adds up to

- **Works and is cheap:** telling a reader what to ignore.
- **Works as infrastructure:** a paper-derived ground truth, so outlines can be scored against something other than our own ratings.
- **Mixed:** printing definitions makes statements followable but long; it did not surface milestones, and model readers disagree.
- **Small:** compression from a better abstraction, on the one pattern that looked most promising.

Detail: `out/corpus/deadcode/DEADCODE.md`, `out/corpus/papers/TRUTH.md`, `out/corpus/outline2/` (OUTLINE2.md, METHOD.md, RATINGS.md), `out/corpus/lesssim/LESSSIM.md`.
