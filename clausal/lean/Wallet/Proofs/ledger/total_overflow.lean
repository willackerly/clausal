/-
Proof of the scenario statement `Spec.ledger.total_overflow.stmt` (lean/Wallet/Statements.lean).

Hand-written (by a person or an agent). clausal created this file as a `sorry`
stub and never edits it again. The theorem must be named exactly `Spec.ledger.total_overflow`
and its type must be exactly `Spec.ledger.total_overflow.stmt`: the audit checks both, so a
theorem of some other type is not counted as a proof.

Usual recipe: `intro` the variables and Givens, `apply Bdd.okN_of_spec` (N = number
of things the call returns), `unfold` the model function, `step*`, then arithmetic.
A call with a loop cannot be unfolded and stepped: use its hand-proved `@[step]` lemma
(lean/Ledger/Lemmas/), which carries the loop invariant.
-/
import Wallet.Statements
import Ledger.Lemmas.Total
open Aeneas Aeneas.Std Result

/-- features/ledger.feature:123  The total of balances that do not fit is reported as absent -/
theorem Spec.ledger.total_overflow : Spec.ledger.total_overflow.stmt := by
  intro balances main _ hbig
  obtain ⟨o, e, -, h2⟩ := Bdd.ok_of_spec (ledger.Ledger.total.spec main)
  exact ⟨o, e, h2 hbig⟩
