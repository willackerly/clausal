/-
Proof of the scenario statement `Spec.wallet.withdraw_too_much.stmt` (lean/Wallet/Statements.lean).

Hand-written (by a person or an agent). slicegen created this file as a `sorry`
stub and never edits it again. The theorem must be named exactly `Spec.wallet.withdraw_too_much`
and its type must be exactly `Spec.wallet.withdraw_too_much.stmt`: the audit checks both, so a
theorem of some other type is not counted as a proof.

Usual recipe: `intro` the variables and Givens, `apply Bdd.okN_of_spec` (N = number
of things the call returns), `unfold` the model function, `step*`, then arithmetic.
-/
import Wallet.Statements
open Aeneas Aeneas.Std Result

/-- features/wallet.feature:24  Withdrawing more than the balance is rejected and changes nothing -/
theorem Spec.wallet.withdraw_too_much : Spec.wallet.withdraw_too_much.stmt := by
  intro a amount alice h1 h2
  apply Bdd.ok2_of_spec
  unfold wallet.Wallet.withdraw
  step*
