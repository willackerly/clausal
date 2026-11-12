/-
Proof of the scenario statement `Spec.ledger.whole_rejected_unchanged.stmt` (lean/Wallet/Statements.lean).

Hand-written (by a person or an agent). clausal created this file as a `sorry`
stub and never edits it again. The theorem must be named exactly `Spec.ledger.whole_rejected_unchanged`
and its type must be exactly `Spec.ledger.whole_rejected_unchanged.stmt`: the audit checks both, so a
theorem of some other type is not counted as a proof.

Usual recipe: `intro` the variables and Givens, `apply Bdd.okN_of_spec` (N = number
of things the call returns), `unfold` the model function, `step*`, then arithmetic.
A call with a loop cannot be unfolded and stepped: use its hand-proved `@[step]` lemma
(lean/Ledger/Lemmas/), which carries the loop invariant.
-/
import Wallet.Statements
import Ledger.Lemmas.All
open Aeneas Aeneas.Std Result

/-- features/ledger.feature:219  A batch applied as a whole that is rejected leaves the ledger unchanged -/
theorem Spec.ledger.whole_rejected_unchanged : Spec.ledger.whole_rejected_unchanged.stmt := by
  intro balances batch main _
  obtain ⟨⟨b, l'⟩, e, -, hback, -⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_all.spec main batch)
  exact ⟨b, l', e, fun hb => congrArg (·.balances.val) (hback hb)⟩
