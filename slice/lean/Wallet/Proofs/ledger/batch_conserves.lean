/-
Proof of the scenario statement `Spec.ledger.batch_conserves.stmt` (lean/Wallet/Statements.lean).

Hand-written (by a person or an agent). slicegen created this file as a `sorry`
stub and never edits it again. The theorem must be named exactly `Spec.ledger.batch_conserves`
and its type must be exactly `Spec.ledger.batch_conserves.stmt`: the audit checks both, so a
theorem of some other type is not counted as a proof.

Usual recipe: `intro` the variables and Givens, `apply Bdd.okN_of_spec` (N = number
of things the call returns), `unfold` the model function, `step*`, then arithmetic.
A call with a loop cannot be unfolded and stepped: use its hand-proved `@[step]` lemma
(lean/Ledger/Lemmas/), which carries the loop invariant.
-/
import Wallet.Statements
import Ledger.Lemmas.Batch
open Aeneas Aeneas.Std Result

/-- features/ledger.feature:9  Applying any batch of transfers conserves the total of all balances -/
theorem Spec.ledger.batch_conserves : Spec.ledger.batch_conserves.stmt := by
  intro balances batch main _
  obtain ⟨⟨n, l'⟩, e, h1, -, -⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_batch.spec main batch)
  exact ⟨n, l', e, h1⟩
