/-
Proof of the scenario statement `Spec.ledger.transfer_invalid_rejected.stmt` (lean/Wallet/Statements.lean).

Hand-written (by a person or an agent). slicegen created this file as a `sorry`
stub and never edits it again. The theorem must be named exactly `Spec.ledger.transfer_invalid_rejected`
and its type must be exactly `Spec.ledger.transfer_invalid_rejected.stmt`: the audit checks both, so a
theorem of some other type is not counted as a proof.

Usual recipe: `intro` the variables and Givens, `apply Bdd.okN_of_spec` (N = number
of things the call returns), `unfold` the model function, `step*`, then arithmetic.
A call with a loop cannot be unfolded and stepped: use its hand-proved `@[step]` lemma
(lean/Ledger/Lemmas/), which carries the loop invariant.
-/
import Wallet.Statements
import Ledger.Lemmas.Apply
open Aeneas Aeneas.Std Result

/-- features/ledger.feature:94  An invalid transfer is rejected and changes nothing -/
theorem Spec.ledger.transfer_invalid_rejected : Spec.ledger.transfer_invalid_rejected.stmt := by
  intro balances t main _ hinvalid
  obtain ⟨⟨b, l'⟩, e, h⟩ := Bdd.ok_of_spec (ledger.Ledger.apply.spec main t)
  obtain ⟨-, hv, -⟩ | ⟨hb, -, rfl, -⟩ := h
  · exact absurd hv hinvalid
  · exact ⟨b, _, e, hb, rfl⟩
