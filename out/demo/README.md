# Rosette demo: three long Mathlib proofs, lifted

**Bottom line.** Lifting works mechanically on all three proofs (every lemma kernel-checked, no
new axioms). The statements it recovers are good for the number-theory and combinatorics proofs
and useless for the analysis proof. Ranking by hidingRatio alone picks mostly artefacts; simple
filters fix the artefacts but do not make the analysis proof readable. For proofs like the
Sobolev inequality a source-level presentation layer is needed; for proofs like Pell the term
level is close to sufficient.

## What was run

`Rosette/Demo.lean` lifts hierarchically: up to 6 lemmas out of the theorem, then up to 3 out of
each lifted lemma. It does this under three configurations and checks each result.

| config | selection |
|---|---|
| `lifted` (A) | `Rosette.Lift` as shipped: rank by hidingRatio, proof ≥ 40 nodes, statement ≤ 150 nodes, pick ≤ 80 % of parent |
| `filtered` (B) | A, but never select a typeclass-instance proof, a term in function position, a proof headed by rewriting plumbing (`congrArg`, `Eq.trans`, `_simp_` lemmas, …) or by a tactic-internal lemma, or a statement that prints with tactic-internal notation (`≍`, `rawCast`, `::ᵣ`, …) |
| `wide` (C) | B, with statement ≤ 500 nodes and pick ≤ 50 % of parent |

The three theorems were chosen by hand, one each from analysis, number theory and combinatorics,
from a list of the longest single-declaration tactic proofs in the Mathlib source. They are an
illustration, not a sample.

| theorem | area | source | proof term (DAG / tree) | write-up |
|---|---|---|---|---|
| `MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq_inner` (Gagliardo–Nirenberg–Sobolev) | analysis, PDE-adjacent | 119 lines | 12792 / 1189531 | [md](MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq_inner.md) |
| `Pell.exists_of_not_isSquare` | number theory | 63 lines | 7089 / 319530 | [md](Pell.exists_of_not_isSquare.md) |
| `Int.erdos_ginzburg_ziv` | combinatorics | 69 lines | 4059 / 39563 | [md](Int.erdos_ginzburg_ziv.md) |

Checked by Lean for all 9 runs (3 theorems × 3 configs): every lifted declaration is a `theorem`
added through `addDecl` with synchronous kernel checking; `X.<config>` has a statement
syntactically identical to `X`; it calls each of its top-level lemmas; its axioms are
`propext`, `Classical.choice`, `Quot.sound`, a subset of the original's.

## Ratings

My reading of each lifted statement against the source proof. **M** = meaningful (a step of the
mathematical argument), **T** = technical-but-sensible (bookkeeping an author could name with a
`have`), **J** = junk (artefact). "Residual" is the size of the main proof after lifting.

| theorem | config | lemmas | M | T | J | residual main proof |
|---|---|---|---|---|---|---|
| Sobolev | A `lifted` | 16 | 0 | 1 | 15 | 12792 → 11581 |
| Sobolev | B `filtered` | 16 | 0 | 12 | 4 | 12792 → 12141 |
| Sobolev | C `wide` | 24 | 0 | 16 | 8 | 12792 → 8383 |
| Pell | A `lifted` | 18 | 5 | 7 | 6 | 7089 → 1724 |
| Pell | B `filtered` | 12 | 4 | 8 | 0 | 7089 → 1728 |
| Pell | C `wide` | 21 | 6 | 11 | 4 | 7089 → 673 |
| Erdős–Ginzburg–Ziv | A `lifted` | 11 | 2 | 5 | 4 | 4059 → 205 |
| Erdős–Ginzburg–Ziv | B `filtered` | 10 | 2 | 6 | 2 | 4059 → 205 |
| Erdős–Ginzburg–Ziv | C `wide` | 12 | 3 | 5 | 4 | 4059 → 298 |
| **all** | A | 45 | 7 | 13 | 25 | |
| **all** | B | 38 | 6 | 26 | 6 | |
| **all** | C | 57 | 9 | 32 | 16 | |

- As shipped, more than half of what is lifted is junk (25 of 45), and in the analysis proof 15 of 16.
- Filtering removes most junk (25 → 6) without adding anything meaningful.
- Meaningful statements appear almost only at the first level of the tree. Of the 9 meaningful
  lemmas in C, 7 are top-level; the second level is mostly side conditions.
- The ratings are one reader's judgement on 140 statements, with no second rater. This table is
  from the rerun after the review fixes (candidates are now one per distinct subterm, and no
  variable is listed twice in a statement). Pell and Erdős–Ginzburg–Ziv lift exactly the same
  lemmas as before. The Sobolev runs lift more (A 11 → 16, B 10 → 16, C 21 → 24), because slots
  that used to be taken by repeated positions of one subterm now go to distinct lemmas; the 14
  additional Sobolev statements were rated in the rerun, by the same rule.

### What was recovered that a mathematician would recognise

- Pell: "`√d` is irrational", "irrational ⟹ infinitely many rationals of bounded norm",
  "pigeonhole on the norm", "norm 0 is impossible", "two rationals of norm `m` congruent mod `m`
  give a solution", the Brahmagupta identity. In C most steps of the textbook proof appear in
  the tree, four of them at top level; the Brahmagupta identity and the divisibility step are
  second-level (`1.1`, `1.3`), and the pigeonhole step is in contrapositive form.
- Erdős–Ginzburg–Ziv: the four induction cases, the multiplicativity step
  "EGZ(m) ∧ EGZ(n) ⟹ EGZ(mn)", and in C both halves of the author's `suffices`.
- Sobolev: nothing. The best items are exponent identities such as
  `((p(n−1)/(n−p) − 1)·(p/(p−1)))⁻¹ = p⁻¹ − n⁻¹`.

### Against the author's `have` statements

Rank under hidingRatio of the `have` values present in each term (candidates of ≥ 20 nodes):

| theorem | `have` values | median rank | in top 10 % | closed statement > 150 nodes |
|---|---|---|---|---|
| Pell | 9 | 7.7 % | 5 of 9 | 2 of 9 |
| Erdős–Ginzburg–Ziv | 3 | 11.1 % | 1 of 3 | 3 of 3 |
| Sobolev | 25 (plus one `finrank ℝ E = finrank ℝ E` left by the elaborator) | 29.6 % | 6 of 25 | 14 of 25 |

These ranks should not be read as support for H1. No baseline was computed for them, and the
323-pair benchmark (`out/bench/RESULTS.md`) shows that proof size alone, or depth in the tree
alone, puts human boundaries almost as high. Two observations matter more than the ranks:

1. Several of the best recovered lemmas are **not** `have`s at all: continuations ("the rest of
   the proof after this point"), induction cases, a `calc` line, the body of a `suffices`. So
   `have` values are an incomplete ground truth for good boundaries.
2. Several real `have`s are unreachable for a size ratio by construction: one-line facts named
   because they are used later (`hv : ContDiff ℝ 1 v` ranks last of 1152, ratio 0.05).

## Failure patterns, and what would address each

Each pattern is something observed in the generated files. "Tested" means configuration B or C
tried the remedy; otherwise it is a proposal.

| # | pattern | example | remedy | status |
|---|---|---|---|---|
| 1 | **Tactic certificates outrank the mathematics.** `ring`, `field_simp`, `norm_num` leave long proofs of short statements about their own normal forms. | Sobolev A: `↑p = Mathlib.Tactic.FieldSimp.NF.eval [] * ↑p`; `Nat.rawCast 1 * (Int.negOfNat 1).rawCast = …` | Reject a candidate whose statement mentions a constant from a tactic namespace. Needs the statement's constants in `Candidate`; B approximates it on the printed text. | Tested: Sobolev junk 15 → 4 |
| 2 | **Congruence plumbing.** `simp`, `rw`, `mod_cast`, `convert` produce proofs of `(P) = (Q)`, `P = True`, `a ≍ b`. | Pell A: `(1 ≤ ↑q.den ^ 2) = (1 ≤ \|↑q.den\|)`; Sobolev A: `(a ≤ b) ≍ (a' ≤ b')` | Reject when the conclusion is `Eq` at type `Prop`, or `HEq`. B used the head constant of the proof as a proxy. | Tested, leaky: proofs with no head constant and heads such as `Iff.of_eq` still get through (Pell C `5.1`–`5.3`, EGZ B `4.1`) |
| 3 | **Typeclass-instance proofs.** | Pell A: `AddLeftReflectLE ℝ` | Filter on `stmtIsClass` (already computed). | Tested: gone |
| 4 | **Closed statements are inflated by context.** Instance binders, `let`s re-bound in every lemma, anonymous-constructor proofs printed as `⋯`. The author's one-line `have` becomes hundreds of nodes, and a fixed bound rejects it. | Sobolev: the central `calc` has a closed statement of 886 nodes and 15 hypotheses; 14 of 25 `have`s exceed 150. EGZ: `t₀ ∉ 𝒜` becomes 311 nodes, 9 hypotheses. | Measure and print the statement *relative to the parent's context*: binders the parent theorem already has cost nothing and go into a shared `variable` block; charge only for what is new. | Partly tested: raising the bound to 500 (C) lets real `have`s in (Sobolev `h2p`, Pell `hM`, `hd₁`, EGZ `suffices`), but does not shorten them |
| 5 | **Continuations and renamed copies.** hidingRatio likes "the rest of the proof", whose conclusion is the theorem's. Sometimes this is the best lemma available, sometimes a copy of its parent with one hypothesis renamed. | good: Pell `1`, `1.1`; bad: EGZ `2.1` (`Fact (Nat.Prime p)` for `Nat.Prime p`), EGZ C `3.1` | Keep a continuation only if it hides between about 20 % and 80 % of its parent and its hypotheses differ from the parent's by more than a repackaging. C's 50 % limit is a crude version. | Partly tested |
| 6 | **Facts named for use, not for length.** A one-line `have` with a long statement scores near zero. | Sobolev `hv`, `h2v` (ratios 0.05, 0.11) | Add a use-count term: how many times the bound variable occurs in the rest of the proof. Size alone cannot rank these. | Proposal |
| 7 | **Local definitions do not survive.** `set`/`let` values are re-bound per lemma, sometimes folded and unfolded in the same statement. | Sobolev C `4.3`: `0 < ↑n − ↑1 → ↑(Module.finrank ℝ E) − 1 ≠ 0`; `γ` printed as `NNReal.mk (↑p * (↑n - 1) / (↑n - ↑p)) ⋯` | Lift each `let` once as a definition of the skeleton and state the lemmas in terms of it. | Proposal |
| 8 | **Repeated sub-statements.** One long predicate recurs in every lemma. | EGZ: `∀ t ∈ 𝒜, t ⊆ s ∧ #t = n ∧ ↑n ∣ ∑ i ∈ t, a i` appears up to three times per statement | Abbreviate the largest subterm shared by the statements of one skeleton. | Proposal |
| 9 | **Invisible elaboration detail.** Coercion targets and instance paths are not printed, so a statement can look false, and two different terms can print identically. | Pell C `1`: `f := fun q => (↑q.num, ↑q.den)` hides `ZMod m.natAbs`; `√↑d ^ 2 = ↑d` lifted as 55-node and 70-node lemmas with the same text | Print type ascriptions on `let`s and on casts whose target is not in the statement; merge candidates that are definitionally equal, not only syntactically equal. | Proposal |
| 10 | **Reuse is detected only among siblings.** The same statement is lifted again under another parent with another name. | Sobolev C: `1 ≤ p → ↑p ≠ 0` twice, `0 < n → ↑n ≠ 0` three times; Pell A: `√d² = d` three times | One table of statement hashes for the whole tree; hoist a shared lemma to the common ancestor. | Proposal (relevant to H2: the only within-proof reuse found so far is of side conditions and junk) |
| 11 | **The term states what the tactic produced, not what the author wrote.** | Pell B `1.3`: after `contrapose!` the pigeonhole step is `(¬∃ m, …) → ¬…`; names like `this`, `a✝¹`, `e'_3` | Take statements and names from the source `have`/`obtain` syntax where one exists. | Proposal, needs source-level layer |
| 12 | **Interfaces are not minimal.** The lemma quantifies every hypothesis the proof term mentions. | Sobolev B `2` assumes `HolderConjugate n n'` to get `0 < n`; Pell `1.2` assumes `Infinite` where `Nonempty` is used | Hard in general. Cheap version: flag hypotheses used only through a projection or one lemma. | Proposal |
| 13 | **Slots get filled.** With `k` fixed, weak candidates are taken once good ones run out. | Pell C `6`: `∃ n, 2\|ξ\| + 1 < ↑n`, ratio 0.75 | A minimum score (ratio > 1 at least) in `selectCandidates`. | Proposal |
| 14 | **The size measure moves when a term is closed.** DAG size of a subterm in context and of the closed lemma value differ, because closing turns free variables into bound ones and breaks sharing. | EGZ A `1`: 2042 nodes in context, 3525 as a closed proof | Compute hidingRatio on closed terms, or report tree size with explicit sharing. Until then "residual" sizes are not additive. | Proposal |

## Is the term level readable enough?

- **Yes, nearly, when the context is thin.** Pell and EGZ live in `ℤ`, `ℚ`, `Finset` with almost
  no instance arguments. Lean prints the lifted statements much as a human would write them, and
  after filtering the first level of the tree is a fair outline of the proof. The remaining
  defects (patterns 8, 9, 11) are cosmetic but need information the term does not print.
- **No, when the context is thick.** In the Sobolev proof the mathematical steps are not short
  statements with long proofs; they are a `calc` over local definitions inside a large typeclass
  context. Closed, each step is hundreds of nodes. Better scoring does not fix this: with an
  oracle choosing the author's own boundaries the output would still be unreadable.
- **What this suggests.** Use the term level for what it is good at (enumerating boundaries
  including ones the author did not mark, checking each lift in the kernel, hashing statements
  for reuse) and take the *presentation* from the source: ambient `variable`s, named local
  definitions, `calc` chains, hypothesis names. Candidate boundaries should be seeded from source
  structure (`have`, `suffices`, `obtain … : T`, `calc` steps, `induction`/`cases` arms) and from
  continuations, and scored with pattern 4's relative size plus pattern 6's use count.

## Reproduce

```sh
cd /Users/will/dev/lean-rosette
export PATH="$HOME/.elan/bin:$PATH"
lake build Rosette.Lift
lake env lean Rosette/Demo.lean     # about 1.5 minutes; writes out/demo/generated/*.md
python3 out/demo/assemble.py        # rebuilds out/demo/<theorem>.md from templates/ + generated/
```

- `generated/<theorem>.<config>.md` is written by Lean and never edited.
- `templates/<theorem>.md` holds the hand-written tables and prose; `assemble.py` copies the
  generated blocks into it verbatim.
- If selection parameters change, the generated blocks change and the hand-written ratings in
  `templates/` and in this file must be redone by hand.
