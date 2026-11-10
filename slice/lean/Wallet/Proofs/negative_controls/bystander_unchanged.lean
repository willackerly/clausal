/-
Proof of the scenario statement `Spec.negative_controls.bystander_unchanged.stmt` (lean/Wallet/Statements.lean).

Hand-written (by a person or an agent). slicegen created this file as a `sorry`
stub and never edits it again. The theorem must be named exactly `Spec.negative_controls.bystander_unchanged`
and its type must be exactly `Spec.negative_controls.bystander_unchanged.stmt`: the audit checks both, so a
theorem of some other type is not counted as a proof.

Usual recipe: `intro` the variables and Givens, `apply Bdd.okN_of_spec` (N = number
of things the call returns), `unfold` the model function, `step*`, then arithmetic.
-/
import Wallet.Statements
open Aeneas Aeneas.Std Result

/-- features/negative.feature:22  A deposit does not touch a bystander -/
theorem Spec.negative_controls.bystander_unchanged : Spec.negative_controls.bystander_unchanged.stmt := by
  intro a b amount alice bob h1 h2 h3
  apply Bdd.ok2_of_spec
  unfold wallet.Wallet.deposit
  step*
