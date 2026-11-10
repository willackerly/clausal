/-
Proof of the scenario statement `Spec.ledger.batch_then_total.stmt` (lean/Wallet/Statements.lean).

Hand-written (by a person or an agent). slicegen created this file as a `sorry`
stub and never edits it again. The theorem must be named exactly `Spec.ledger.batch_then_total`
and its type must be exactly `Spec.ledger.batch_then_total.stmt`: the audit checks both, so a
theorem of some other type is not counted as a proof.

Usual recipe: `intro` the variables and Givens, `apply Bdd.okN_of_spec` (N = number
of things the call returns), `unfold` the model function, `step*`, then arithmetic.
A call with a loop cannot be unfolded and stepped: use its hand-proved `@[step]` lemma
(lean/Ledger/Lemmas/), which carries the loop invariant.
-/
import Wallet.Statements
import Ledger.Lemmas.Batch
import Ledger.Lemmas.Total
open Aeneas Aeneas.Std Result

/-- features/ledger.feature:204  The total computed after any batch is the total before it -/
theorem Spec.ledger.batch_then_total : Spec.ledger.batch_then_total.stmt := by
  intro balances sum batch main _ hsum
  -- first When: the batch loop conserves the total
  obtain ⟨⟨n, l1⟩, e1, h1, -, -⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_batch.spec main batch)
  refine ⟨n, l1, e1, ?_⟩
  -- second When: the summing loop, on the ledger the batch left
  obtain ⟨o, e2, h2, -⟩ := Bdd.ok_of_spec (ledger.Ledger.total.spec l1)
  obtain ⟨s, rfl, hs⟩ := h2 (by rw [h1, hsum]; scalar_tac)
  refine ⟨_, e2, ?_⟩
  simp only [LVocab.resultIs, Option.some.injEq]
  scalar_tac
