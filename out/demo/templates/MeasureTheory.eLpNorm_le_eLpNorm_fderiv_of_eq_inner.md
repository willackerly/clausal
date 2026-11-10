# Gagliardo–Nirenberg–Sobolev inequality — recovered skeleton

Analysis, PDE-adjacent. Source: `Mathlib/Analysis/FunctionalSpaces/SobolevInequality.lean`, lines
467–585: one tactic block of 119 lines. The argument: reduce `p > 1` to the `p = 1` inequality
applied to `v = ‖u‖^γ` with `γ = p(n−1)/(n−p)`; bound `‖Dv‖` by `γ ‖u‖^(γ−1) ‖Du‖`; apply
Hölder with exponents `p, q`; divide by `(∫‖u‖^p')^(1/q)`. About half of the source is exponent
arithmetic (`h2p … h4γ`), the other half is one long `calc`.

**This is the negative case of the demo.** No configuration recovers a single step of the
mathematical argument.

Everything in fenced blocks and stat lines below is copied from `generated/`, which Lean wrote
(`Rosette/Demo.lean`). The tables and prose are my reading. Rating scale: **meaningful** (a step of
the argument an analyst would state), **technical** (technical-but-sensible bookkeeping an author
could name with a `have`), **junk** (artefact: tactic internals, proposition equalities,
instances, renamed copies of the parent, closed trivialities).

## Original statement

@@STATEMENT lifted@@

## Skeleton A — `Rosette.Lift` as shipped (score = hidingRatio)

@@RESULT lifted@@

@@SKELETON lifted@@

| lemma | what it says | rating | note |
|---|---|---|---|
| `1` | `p(n−1) − (n−p) = n(p−1)` | technical | Verbatim the author's `have … := by ring` inside `h3γ`. The statement carries two instance arguments and a `let n := Module.finrank ℝ E` for what is an identity in two real variables. |
| `1.1`, `1.2`, `1.3` | identities between `Nat.rawCast` / `Int.negOfNat … .rawCast` expressions | junk | Certificates of the `ring` normaliser. |
| `2`, `2.1`, `3`, `3.1` | `self = self' → a = a' → b = b' → (a ≤ b) ≍ (a' ≤ b')` and variants | junk | Heterogeneous-equality congruence lemmas that `convert` builds inline. Binder names are `a✝¹`, `e'_2`, `a'✝¹`. |
| `4` | `p = NF.eval [] * p` | junk | `field_simp` normal form. |
| `4.1`, `4.2`, `4.3` | `((1, p) ::ᵣ []).eval = p` and variants; `4.3` is `X = X` | junk | `field_simp` internals. |
| `5`, `5.1` | `a = a' → b = b' → a * b ≍ a' * b'` | junk | The same kind of `convert` congruence lemma, for `HMul`. |
| `6`, `6.1` | `IsRightCancelAdd ℝ`, `AddRightReflectLE ℝ` | junk | Typeclass-instance proofs. |

**Tally: 0 meaningful, 1 technical, 15 junk (of 16).** The main proof goes from 12792 to 11581
nodes: nothing of substance was lifted. Statements about tactic internals are short and their
proofs are long, so hidingRatio prefers them to everything the author wrote.

(Before the enumeration was made DAG-aware this configuration lifted 11 lemmas: several of the six
top-level slots were taken by repeated positions of one subterm. With one candidate per distinct
subterm all six slots go to distinct lemmas; the five extra ones are more junk.)

## Skeleton B — `filtered`

@@RESULT filtered@@

@@SKELETON filtered@@

| lemma | what it says | rating | note |
|---|---|---|---|
| `1` | `0 < p⁻¹ − n⁻¹ → p < n` | technical | The tail of the author's `have h2p`. |
| `1.1` | `n⁻¹ < p⁻¹ ↔ p < n` | technical | `inv_lt_inv₀` with its side conditions discharged. |
| `1.2` | `0 < p⁻¹ − n⁻¹ → n⁻¹ < p⁻¹` | junk | One `sub_pos` rewrite. |
| `2` | `1 < p → n − p < p(n−1)` | technical | Core of `h1γ : 1 < γ`. Carries the hypothesis `HolderConjugate n n'`, which the proof uses only to get `0 < n`. |
| `2.1` | `1 < p → n < p·n` | technical | |
| `2.2` | `n − p < p·n − p ↔ n < p·n` | junk | Instance of `sub_lt_sub_iff_right`. |
| `3` | `p' ≠ 0 → 0 ^ (1/p') = 0` | technical | Side goal of the degenerate case `∫‖u‖^p' = 0`. |
| `3.1` | `p' ≠ 0 → 0 < p'` | technical | |
| `4` | `1 ≤ p → (p : ℝ) ≠ 0` | technical | A `field_simp` side condition. |
| `4.1` | `1 ≤ p → 0 < p` | technical | |
| `5` | `n'⁻¹ − q⁻¹ = p'⁻¹` from `hp'` and the two Hölder-conjugate pairs | technical | The exponent identity behind the author's `h2q : 1/n' − 1/q = 1/p'`, which sets up the Hölder step. |
| `5.1` | `n'⁻¹ − q⁻¹ = p⁻¹ − n⁻¹` | technical | Its core, without `p'`. |
| `5.2` | `hp' → p'⁻¹ = p⁻¹ − n⁻¹` | junk | The hypothesis `hp'` restated with `n` folded. |
| `6` | `p < n → 0 < n − 1 → 0 ≤ p(n−1)/(n−p)` | technical | Non-negativity needed to form `γ` as an `NNReal`. |
| `6.1` | `1 ≤ p → 0 < p` | technical | Same statement as `4.1`, lifted again under another parent. |
| `6.2` | `p < n → 0 < n − p` | junk | One `sub_pos` rewrite. |

**Tally: 0 meaningful, 12 technical, 4 junk (of 16).** The filter does what it was meant to do
(15 junk → 4), and what is left is a list of true, legible, unilluminating inequalities between
exponents. Main proof 12792 → 12141 nodes: less was lifted than before.

## Skeleton C — `wide` (statements up to 500 nodes; each pick at most half its parent)

@@RESULT wide@@

@@SKELETON wide@@

| lemma | what it says | rating | note |
|---|---|---|---|
| `1` | `((γ − 1)·q)⁻¹ = p⁻¹ − n⁻¹` with `γ` and `q` written out | technical | The computation behind the author's `h3γ : (γ − 1) * q = p'`. It is the numerology of the proof, but printed as `((↑p * (↑n - 1) / (↑n - ↑p) - 1) * (↑p / (↑p - 1)))⁻¹` nobody would recognise it. |
| `2` | `(γ·n')⁻¹ = p⁻¹ − n⁻¹`, written out | technical | Behind `h2γ : γ * n' = p'`. |
| `3` | for `p = 1`: `p'⁻¹ = 1⁻¹ − n⁻¹ → p' = n'` | technical | The author's `suffices (p' : ℝ) = n'`. |
| `4` | the constant for `p = 1` equals the constant of the `p = 1` theorem | technical | Second goal of the `convert`. Seven binders of measure-space context for an identity between two constants. |
| `5` | `p < n` | technical | Verbatim the author's `have h2p`. |
| `6` | `1 < p(n−1)/(n−p)` | technical | `h1γ` with `γ` unfolded. |
| `1.1`, `2.1` | `1 ≤ p → (p : ℝ) ≠ 0` | technical | The same statement lifted under two parents with two names. |
| `1.2`, `2.2`, `3.1` | `0 < n → (n : ℝ) ≠ 0` | technical | Same statement, three parents, three names. |
| `1.3` | `p − 1 ≠ 0 → p(n−1) − (n−p) = n(p−1) → p(n−1) − (n−p) ≠ 0` | technical | A non-vanishing side condition; it takes the `ring` identity of A `1` as a hypothesis. |
| `2.3` | `p < n → n − p ≠ 0` | technical | Side condition. |
| `3.2`, `4.2` | `1 ≠ 0` | junk | |
| `3.3` | `0 < n − 1 → n − 1 ≠ 0` | junk | One instance of `ne_of_gt`. |
| `4.1` | `C * Real.toNNReal 1 = C` | junk | `simp` step. |
| `4.3` | `0 < ↑n − ↑1 → ↑(finrank ℝ E) − 1 ≠ 0` | junk | Also shows `n` and its unfolding in the same statement. |
| `5.1`, `5.3` | `n⁻¹ < p⁻¹ ↔ p < n`; `p' ≠ 0 → 0 < p'⁻¹` | technical | |
| `5.2` | `0 < p⁻¹ − n⁻¹ → n⁻¹ < p⁻¹` | junk | |
| `6.1` | `1 < p → n < p·n` | technical | |
| `6.2`, `6.3` | instances of `sub_lt_sub_iff_right` and `one_lt_div` | junk | |

**Tally: 0 meaningful, 16 technical, 8 junk (of 24).** Main proof 12792 → 8383 nodes. Relaxing
the statement bound lets in the exponent arithmetic the author did isolate (`h2p`, the cores of
`h1γ`, `h2γ`, `h3γ`, the `suffices`), which is an improvement, but it is all arithmetic.

## Comparison with the `have` statements the author wrote

The term contains 26 distinct `have` values of at least 20 nodes. One of them is
`Module.finrank ℝ E = Module.finrank ℝ E` (31 nodes, rank 795 of 1152). The source has one
`set n := finrank ℝ E` and no such `have`; it is elaborator residue. The other 25 are real.

- **The step that carries the proof is out of reach.** The author's `have := calc …` (the chain
  `(∫‖u‖^p')^(1/n') = ‖v‖_{n'} ≤ C‖Dv‖₁ ≤ … ≤ Cγ (∫‖Du‖^p)^(1/p) (∫‖u‖^p')^(1/q)`) is a `have`
  value of 3048 nodes. Its closed statement has **886 nodes and 15 hypotheses**, and ranks 100th
  of 1152. No bound I would call sensible admits it, and printed in closed form it runs to half a
  page before the conclusion starts (the generated list below truncates it at 700 characters).
- 14 of the 25 real `have`s have closed statements above the shipped bound of 150 nodes; the
  author's own statements are one line each. The inflation comes from five to seven instance
  binders, from `let n`, `let n'`, `let q`, `let γ` being re-bound in each statement, and from
  `γ` printing as `NNReal.mk (↑p * (↑n - 1) / (↑n - ↑p)) ⋯`.
- Under hidingRatio the 25 real `have`s have median rank at 30 % of the candidate list; 6 are in
  the top 10 %, 11 in the top 25 %, and 4 are in the bottom 12 %.
- The bottom ones are instructive. `hv : ContDiff ℝ 1 v` ranks 1152nd of 1152 (ratio 0.05) and
  `h2v : HasCompactSupport v` 1140th (0.11). Each is a one-line proof whose closed statement is
  about 470 nodes. These are exactly the facts the calc needs about `v`; the author names them
  because they are *used*, not because their proofs are long. A size ratio cannot see that.
- Exactly recovered: the `ring` identity (A `1`) and `h2p` (C `5`). Recovered in unfolded form:
  the cores of `h1γ`, `h2γ`, `h3γ` and the `suffices` of the `p = 1` case (C `6`, `2`, `1`, `3`).

@@HAVES@@

## Verdict for this proof

Term-level statements are **not** readable enough here, and the problem is not only ranking.
Even with an oracle that picks the author's own boundaries, the closed statements are several
hundred nodes of instance binders, re-bound `let`s and unfolded exponents. What the author's
text has and the term lacks: section `variable`s (so the ambient space, measure and function are
not restated), local definitions with names (`n'`, `q`, `γ`, `v`, `C`) shared by all steps, and
`calc`, which presents a chain of five inequalities as five lines without stating any of them as
a closed lemma. A source-level presentation layer is needed for proofs of this kind.
