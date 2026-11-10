/-
Proof of the scenario statement `Spec.ledger.total_is_sum.stmt` (lean/Wallet/Statements.lean).

Hand-written (by a person or an agent). slicegen created this file as a `sorry`
stub and never edits it again. The theorem must be named exactly `Spec.ledger.total_is_sum`
and its type must be exactly `Spec.ledger.total_is_sum.stmt`: the audit checks both, so a
theorem of some other type is not counted as a proof.

Usual recipe: `intro` the variables and Givens, `apply Bdd.okN_of_spec` (N = number
of things the call returns), `unfold` the model function, `step*`, then arithmetic.
A call with a loop cannot be unfolded and stepped: use its hand-proved `@[step]` lemma
(lean/Ledger/Lemmas/), which carries the loop invariant.
-/
import Wallet.Statements
import Ledger.Lemmas.Total
open Aeneas Aeneas.Std Result

/-- features/ledger.feature:110  The total is the sum of the balances when that fits -/
theorem Spec.ledger.total_is_sum : Spec.ledger.total_is_sum.stmt := by
  intro balances sum main _ hsum
  obtain ⟨o, e, h1, -⟩ := Bdd.ok_of_spec (ledger.Ledger.total.spec main)
  obtain ⟨s, rfl, hs⟩ := h1 (by rw [hsum]; scalar_tac)
  refine ⟨_, e, ?_⟩
  simp only [LVocab.resultIs, Option.some.injEq]
  scalar_tac
