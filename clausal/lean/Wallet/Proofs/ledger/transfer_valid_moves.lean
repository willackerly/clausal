/-
Proof of the scenario statement `Spec.ledger.transfer_valid_moves.stmt` (lean/Wallet/Statements.lean).

Hand-written (by a person or an agent). clausal created this file as a `sorry`
stub and never edits it again. The theorem must be named exactly `Spec.ledger.transfer_valid_moves`
and its type must be exactly `Spec.ledger.transfer_valid_moves.stmt`: the audit checks both, so a
theorem of some other type is not counted as a proof.

Usual recipe: `intro` the variables and Givens, `apply Bdd.okN_of_spec` (N = number
of things the call returns), `unfold` the model function, `step*`, then arithmetic.
A call with a loop cannot be unfolded and stepped: use its hand-proved `@[step]` lemma
(lean/Ledger/Lemmas/), which carries the loop invariant.
-/
import Wallet.Statements
import Ledger.Lemmas.Apply
open Aeneas Aeneas.Std Result

/-- features/ledger.feature:79  A valid transfer is accepted and moves exactly its amount -/
theorem Spec.ledger.transfer_valid_moves : Spec.ledger.transfer_valid_moves.stmt := by
  intro balances t main _ hvalid
  obtain ⟨⟨b, l'⟩, e, h⟩ := Bdd.ok_of_spec (ledger.Ledger.apply.spec main t)
  obtain ⟨hb, -, hm, ht, -⟩ | ⟨-, hinv, -⟩ := h
  · exact ⟨b, l', e, hb, hm, ht⟩
  · exact absurd hvalid hinv
