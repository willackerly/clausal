/-
Proof of the scenario statement `Spec.ledger.batch_first_invalid.stmt` (lean/Wallet/Statements.lean).

Hand-written (by a person or an agent). clausal created this file as a `sorry`
stub and never edits it again. The theorem must be named exactly `Spec.ledger.batch_first_invalid`
and its type must be exactly `Spec.ledger.batch_first_invalid.stmt`: the audit checks both, so a
theorem of some other type is not counted as a proof.

Usual recipe: `intro` the variables and Givens, `apply Bdd.okN_of_spec` (N = number
of things the call returns), `unfold` the model function, `step*`, then arithmetic.
A call with a loop cannot be unfolded and stepped: use its hand-proved `@[step]` lemma
(lean/Ledger/Lemmas/), which carries the loop invariant.
-/
import Wallet.Statements
import Ledger.Lemmas.Batch
open Aeneas Aeneas.Std Result

/-- features/ledger.feature:22  A batch whose first transfer is invalid changes nothing -/
theorem Spec.ledger.batch_first_invalid : Spec.ledger.batch_first_invalid.stmt := by
  intro balances batch main _ hfirst
  obtain ⟨⟨n, l'⟩, e, -, -, h3, -⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_batch.spec main batch)
  obtain ⟨h0, rfl⟩ := h3 hfirst
  exact ⟨n, _, e, h0, rfl⟩
