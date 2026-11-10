# Erdős–Ginzburg–Ziv over ℤ — recovered skeleton

Combinatorics. Source: `Mathlib/Combinatorics/Additive/ErdosGinzburgZiv.lean`, lines 109–177: one
tactic block of 69 lines. Induction on the prime factorisation of `n` (cases `0`, `1`, prime,
composite). The composite case `m * n` builds, by an inner induction on `k`, a family of
`2m − 1` disjoint `n`-subsets each with sum divisible by `n`, then applies the induction
hypothesis for `m` to the family.

Everything in fenced blocks and stat lines below is copied from `generated/`, which Lean wrote
(`Rosette/Demo.lean`). The tables and prose are my reading. Rating scale: **meaningful** (a step of
the argument a combinatorialist would state), **technical** (technical-but-sensible bookkeeping an
author could name with a `have`), **junk** (artefact: tactic internals, proposition equalities,
instances, renamed copies of the parent, closed trivialities).

## Original statement

@@STATEMENT lifted@@

## Skeleton A — `Rosette.Lift` as shipped (score = hidingRatio)

@@RESULT lifted@@

@@SKELETON lifted@@

| lemma | what it says | rating | note |
|---|---|---|---|
| `1` | EGZ for `m` and EGZ for `n` (both `≥ 2`) imply EGZ for `m * n` | **meaningful** | The multiplicativity step, the heart of the proof. Not a `have`: it is the `composite` argument passed to `Nat.prime_composite_induction`. |
| `1.1` | `AddLeftReflectLE ℕ` | junk | Instance. |
| `1.2` | adding `t₀ ⊆ s \ ⋃𝒜` to a pairwise disjoint family keeps it pairwise disjoint | technical | First bullet of the final `refine`. The membership proof `this` appears as an argument of `Finset.cons` inside the statement. |
| `1.3` | a family of size 0 with the required properties exists | technical | Base case of the inner induction. |
| `2` | EGZ for a prime `p` | **meaningful** | The `prime` case; restates the file's private lemma with `≤` instead of `=`. |
| `2.1` | the same statement with `Fact (Nat.Prime p)` in place of `Nat.Prime p` | junk | The body after `have := Fact.mk hp`: a renamed copy of its parent. |
| `3` | EGZ for `n = 0` | technical | Printed with `↑0 ∣ …`. |
| `3.1` | `(∅.card = 0 ∧ ↑0 ∣ ∑ i ∈ ∅, a i) = True` | junk | `simp` output. |
| `4` | EGZ for `n = 1` | technical | Printed with the unreduced hypothesis `2 * 1 - 1 ≤ s.card`. |
| `4.1` | `(t.card = 1 ∧ ↑1 ∣ ∑ …) = (t.card = 1)` | junk | `simp` output. |
| `4.2` | `∃ t ⊆ s, t.card = 1` | technical | |

**Tally: 2 meaningful, 5 technical, 4 junk (of 11).** The four top-level lemmas are exactly the
four cases of the induction, and the main proof drops from 4059 to 205 nodes. That is a correct
and readable first level. The second level under `1` is poor: the proof's key intermediate
claim (the family of `2m − 1` sets) is missing.

## Skeleton B — `filtered`

@@RESULT filtered@@

@@SKELETON filtered@@

| lemma | rating | note |
|---|---|---|
| `1`, `2` | **meaningful** | as in A |
| `1.1` | technical | `(2m − k)·n − 1 = 2(mn) − 1 − ∑ t ∈ 𝒜, #t`: the second line of the author's `calc`. A boundary the author did write, though as a `calc` step, not a `have`. |
| `1.2`, `1.3`, `3`, `4`, `4.2` | technical | as in A |
| `2.1` | junk | renamed copy of `2` |
| `4.1` | junk | proposition equality; its proof has no head constant, so the head filter missed it |

**Tally: 2 meaningful, 6 technical, 2 junk (of 10).**

## Skeleton C — `wide` (statements up to 500 nodes; each pick at most half its parent)

@@RESULT wide@@

@@SKELETON wide@@

| lemma | what it says | rating | note |
|---|---|---|---|
| `1` | for every `k ≤ 2m − 1` there is a family of `k` pairwise disjoint `n`-subsets of `s` with sums divisible by `n` | **meaningful** | Verbatim the claim of the author's `suffices`. |
| `1.1` | inductive step `k → k + 1` for that family | technical | Correct step, but 364 nodes and 7 hypotheses: the family property is written out three times, and the induction hypothesis `ih` is quantified although the conclusion already assumes a family of size `k`. |
| `1.2` | base case `k = 0` | technical | |
| `1.3` | `k + 1 ≤ 2m − 1 → k ≤ 2m − 1` | junk | One instance of `Nat.le_of_succ_le`. |
| `2` | EGZ for a prime | **meaningful** | |
| `2.1` | copy of `2` with `Fact` | junk | |
| `3` | EGZ for `m` plus such a family for every `k ≤ 2m − 1` imply the conclusion for `m * n` | **meaningful** | The other half of the `suffices`. |
| `3.1` | the same with the family of size `2m − 1` already chosen | junk | Body after `obtain`: a near copy of `3`. |
| `3.2` | `2m − 1 ≤ 2m − 1` | junk | |
| `4`, `5`, `5.1` | cases `0`, `1`, and `∃ t ⊆ s, #t = 1` | technical | |

**Tally: 3 meaningful, 5 technical, 4 junk (of 12).** `1` and `3` together are precisely the
author's `suffices … by …` split, recovered from the term. The price of the half-of-parent limit
is that the multiplicativity lemma (A `1`) is no longer a node of its own.

## Comparison with the `have` statements the author wrote

The term contains only 3 `have` values of at least 20 nodes: the `suffices` claim, the counting
bound `2n − 1 ≤ #(s \ 𝒜.biUnion id)`, and `t₀ ∉ 𝒜`.

- The `suffices` claim ranks 6th of 252 by hidingRatio, but its closed statement has 214 nodes,
  so the shipped bound of 150 rejects it. `wide` recovers it.
- The counting bound ranks 28th (190 nodes, 5 hypotheses) and is never selected; `filtered`
  instead picks one line of the `calc` inside it.
- `t₀ ∉ 𝒜` ranks 108th. The author's three-word statement becomes a closed statement of 311
  nodes with 9 hypotheses, because its proof touches most of the local context. This is the
  clearest example in the demo of a `have` that is short only *in context*.
- The first-level structure (four cases) and the two halves of `suffices` are recovered although
  none of them is a `have` in the term: they are arguments of the induction principle and a
  continuation.

@@HAVES@@

## Verdict for this proof

Readable at the first level in all three configurations, and `wide` reproduces the author's own
decomposition. The statements are long because each one repeats the family property
`∀ t ∈ 𝒜, t ⊆ s ∧ #t = n ∧ n ∣ ∑ …`; a human would introduce a local definition for it. The
term has no such definition to offer, so this needs a presentation step (common-subterm
abbreviation across the lemmas of one skeleton).
