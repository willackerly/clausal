/-
Proof of the scenario statement `Spec.wallet.transfer_short_example.stmt` (lean/Wallet/Statements.lean).

Hand-written (by a person or an agent). clausal created this file as a `sorry`
stub and never edits it again. The theorem must be named exactly `Spec.wallet.transfer_short_example`
and its type must be exactly `Spec.wallet.transfer_short_example.stmt`: the audit checks both, so a
theorem of some other type is not counted as a proof.

Usual recipe: `intro` the variables and Givens, `apply Bdd.okN_of_spec` (N = number
of things the call returns), `unfold` the model function, `step*`, then arithmetic.
-/
import Wallet.Statements
open Aeneas Aeneas.Std Result

/-- features/wallet.feature:50  Transferring more than you have is rejected and changes nothing -/
theorem Spec.wallet.transfer_short_example : Spec.wallet.transfer_short_example.stmt := by
  intro alice bob h1 h2
  apply Bdd.ok3_of_spec
  unfold wallet.transfer
  step*
