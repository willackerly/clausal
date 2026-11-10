/-
Proof of the scenario statement `Spec.ledger.two_batches_conserve.stmt` (lean/Wallet/Statements.lean).

Hand-written (by a person or an agent). slicegen created this file as a `sorry`
stub and never edits it again. The theorem must be named exactly `Spec.ledger.two_batches_conserve`
and its type must be exactly `Spec.ledger.two_batches_conserve.stmt`: the audit checks both, so a
theorem of some other type is not counted as a proof.

Usual recipe: `intro` the variables and Givens, `apply Bdd.okN_of_spec` (N = number
of things the call returns), `unfold` the model function, `step*`, then arithmetic.
A call with a loop cannot be unfolded and stepped: use its hand-proved `@[step]` lemma
(lean/Ledger/Lemmas/), which carries the loop invariant.
-/
import Wallet.Statements
import Ledger.Lemmas.Batch
open Aeneas Aeneas.Std Result

/-- features/ledger.feature:218  Two batches applied one after the other conserve the total -/
theorem Spec.ledger.two_batches_conserve : Spec.ledger.two_batches_conserve.stmt := by
  intro balances first second main _
  obtain ⟨⟨n1, l1⟩, e1, h1, -, -⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_batch.spec main first)
  refine ⟨n1, l1, e1, ?_⟩
  obtain ⟨⟨n2, l2⟩, e2, h2, hle, -⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_batch.spec l1 second)
  exact ⟨n2, l2, e2, h2.trans h1, hle⟩
