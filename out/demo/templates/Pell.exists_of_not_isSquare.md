# Pell's equation has a nontrivial solution — recovered skeleton

Number theory. Source: `Mathlib/NumberTheory/Pell.lean`, lines 324–386: one tactic block of 63
lines with no helper lemma of its own. The classical argument: Dirichlet approximation gives
infinitely many rationals `q` with `|q.num² − d·q.den²| < M`; pigeonhole gives one value `m` taken
infinitely often; `m ≠ 0` because `d` is not a square; pigeonhole again modulo `m` gives two such
rationals congruent mod `m`; composing them (Brahmagupta) and dividing by `m` gives a solution.

Everything in fenced blocks and stat lines below is copied from `generated/`, which Lean wrote
(`Rosette/Demo.lean`). The tables and prose are my reading.

## Original statement

@@STATEMENT lifted@@

Rating scale used in all tables:

- **meaningful** — a step of the mathematical argument that a number theorist would state.
- **technical** — technical-but-sensible: bookkeeping an author could plausibly name with a `have`
  (casts, side conditions, a trivial base case).
- **junk** — an artefact: tactic internals, an equation between propositions, a typeclass
  instance, a renamed copy of its parent, or a closed triviality.

## Skeleton A — `Rosette.Lift` as shipped (score = hidingRatio)

@@RESULT lifted@@

@@SKELETON lifted@@

| lemma | what it says | rating | note |
|---|---|---|---|
| `1` | infinitely many `q` with `\|N(q)\| < M` ⟹ a solution exists | **meaningful** | Not a `have`: it is the *rest of the proof* after `hM`. As a lemma it is exactly the "pigeonhole half" of the theorem. |
| `1.1` | infinitely many `q` with `N(q) = m`, `m ≠ 0` ⟹ a solution exists | **meaningful** | Again a continuation. The cleanest statement in the file. |
| `1.2` | infinitely many `q` with `N(q) = 0` contradicts `d` non-square | **meaningful** | The author's `hm₀ : m ≠ 0` with `m` specialised to 0. Hypothesis is stronger than needed (`Infinite`, the proof only uses `Nonempty`). |
| `1.3` | pigeonhole: bounded norm infinitely often ⟹ some norm value infinitely often | **meaningful** | Matches the author's `obtain ⟨m, hm⟩ : ∃ m, … .Infinite`. |
| `2` | `√d` is irrational | **meaningful** | Verbatim the author's `have hξ`. |
| `2.1` | `√d` is not an integer | technical | |
| `2.2` | `√d ^ 2 = d` | technical | |
| `3` | `q.num / q.den = q` in `ℝ` | technical | Verbatim the author's `have h1`. |
| `3.1`, `3.2` | `(Rat.divInt … = q) = (… = ↑q)` | junk | Equations between propositions produced by `mod_cast`. |
| `4` | `1 ≤ q.den ^ 2` | technical | Last step of the estimate. |
| `4.1` | `1 ≤ \|q.den\|` | technical | |
| `4.2` | `(1 ≤ q.den ^ 2) = (1 ≤ \|q.den\|)` | junk | A `rw` step as a proposition equality. |
| `5`, `5.1`, `5.2` | `AddLeftReflectLE ℝ`, `IsLeftCancelAdd ℝ`, `ContravariantClass ℝ ℝ …` | junk | Instance-synthesis output. |
| `6`, `6.1` | `d = √d ^ 2`, `√d ^ 2 = d` | technical | The same fact as `2.2`, lifted three times under three names. |

**Tally: 5 meaningful, 7 technical, 6 junk (of 18).** The main proof shrinks from 7089 to 1724
nodes, and lemma `1` from 5166 to 194, so the top of this tree really is a readable outline:
*irrational → (infinitely many small norms, left inline) → pigeonhole → nonzero → solution*.

## Skeleton B — `filtered` (same score; instances, rewriting plumbing and tactic vocabulary excluded)

@@RESULT filtered@@

@@SKELETON filtered@@

| lemma | rating | note |
|---|---|---|
| `1`, `1.1`, `1.2`, `2` | **meaningful** | as in A |
| `1.3` | technical | Now the *contrapositive* of the pigeonhole step, `(¬∃ m, …Infinite) → ¬ …Infinite`: this is what `contrapose! hM` left in the term. True and readable, but inside-out compared with what the author wrote. |
| `2.1`, `2.2`, `3`, `4`, `4.1`, `5`, `6` | technical | `5` is `√d ^ 2 = d` again, `6` is `0 < q.den`. |

**Tally: 4 meaningful, 8 technical, 0 junk (of 12).** The filter removes all six junk lemmas and
costs nothing here.

## Skeleton C — `wide` (filtered; statements up to 500 nodes; each pick at most half its parent)

@@RESULT wide@@

@@SKELETON wide@@

| lemma | what it says | rating | note |
|---|---|---|---|
| `1` | two distinct `q₁, q₂` of norm `m ≠ 0` with the same image under `f` ⟹ a solution | **meaningful** | The composition step. But `f` prints as `fun q => (↑q.num, ↑q.den)`: the target `ZMod m.natAbs × ZMod m.natAbs` is invisible, and without it the statement reads as false (it looks like `q₁ = q₂`). |
| `1.1` | Brahmagupta: `((x₁x₂ − d y₁y₂)/m)² − d((x₁y₂ − x₂y₁)/m)² = 1` | **meaningful** | The first bullet of the final `refine`. |
| `1.2` | the `y`-component is nonzero | technical | The second bullet. |
| `1.3` | `m ∣ x₁x₂ − d y₁y₂` | **meaningful** | Verbatim the author's `have hd₁`, again with the invisible `ZMod` cast. |
| `2` | `√d` irrational ⟹ infinitely many `q` with `\|N(q)\| < M` | **meaningful** | Verbatim the author's `have hM`. |
| `2.1`, `2.2`, `2.3` | `q.num/q.den = q`, `1 ≤ q.den²`, `√d² = d` | technical | |
| `3` | `√d` is irrational | **meaningful** | `have hξ`. |
| `3.1` | `ξ = x → √d² = x·x` | technical | |
| `3.2`, `3.3` | `√d ^ 2 = d` twice | technical | Two lemmas with identical printed statements (55 and 70 nodes): different elaborated casts, so they were not merged. |
| `4` | norm 0 infinitely often is impossible | **meaningful** | `hm₀`. |
| `4.1`, `4.2`, `4.3` | `q.den ∣ q.num`; `den²·a² = den²·d`; `0 < q.den` | technical | |
| `5` | contrapositive pigeonhole | technical | as B `1.3` |
| `5.1` | `(x ∈ ⋃ …) = ((−M < i ∧ i < M) ∧ …)` | junk | Proposition equality from `simp only`; its proof has no head constant, so the head filter missed it. |
| `5.2` | `i ∈ Set.Ioo (−M) M ↔ −M < i ∧ i < M` | junk | Unfolding of a definition (head `Iff.of_eq`, not on the filter list). |
| `5.3` | `{q \| N(q) = i} = {q \| N(q) = i}` | junk | A reflexive equation with an unused hypothesis. |
| `6` | `∃ n : ℤ, 2\|ξ\| + 1 < n` | junk | One instance of `exists_int_gt`; ratio 0.75, picked only because `k = 6` slots had to be filled. |

**Tally: 6 meaningful, 11 technical, 4 junk (of 21).** Main proof 7089 → 673 nodes. This is the
best outline of the three: every step of the informal proof above is a top-level lemma.

## Comparison with the `have` statements the author wrote

The elaborated term contains 9 `have` values of at least 20 nodes: `hξ`, `hM`, `h0`, `h1`, `hm₀`,
the `NeZero` instance, `hd₁`, `hd₂`, and the cast `(m : ℚ) ≠ 0`.

- Recovered with an identical statement: `hξ`, `h1` (A, B, C); `hM`, `hd₁` (C only, their closed
  statements are 182 and 177 nodes, above the default bound of 150).
- Recovered in an equivalent form: `hm₀` (as "norm 0 infinitely often ⟹ False").
- Never recovered: `h0`, `hd₂`, the `NeZero` instance, the cast. All four are small.
- Recovered although they are *not* `have`s: the pigeonhole step (an `obtain … : ∃ m, …`), and
  the two continuation lemmas `1` and `1.1`. The continuations are the most useful output: they
  are the statements a human would write if asked to split this proof into three lemmas, and no
  `have` in the source corresponds to them.
- Under hidingRatio the five substantive `have`s rank 31st–64th of 833 candidates (top 4–8 %);
  the median `have` is at 7.7 %. What outranks them is the chain of "rest of the proof" bodies.

@@HAVES@@

## Verdict for this proof

Term-level statements are readable enough here. The objects are integers and rationals, there is
one implicit variable and no instance argument, and Lean prints the lifted statements essentially
as a human would write them. Two presentation defects remain and both need information the term
does not print: the invisible `ZMod` coercion target in `f`, and the contrapositive left by
`contrapose!`.
