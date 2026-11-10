/-
Proof of the scenario statement `Spec.inventory.count_at_most_bins.stmt` (lean/Spec/Statements.lean).

Hand-written (by a person or an agent). slicegen created this file as a `sorry`
stub and never edits it again. The theorem must be named exactly `Spec.inventory.count_at_most_bins`
and its type must be exactly `Spec.inventory.count_at_most_bins.stmt`: the audit checks both, so a
theorem of some other type is not counted as a proof.

Straight-line code: `intro` the variables and Givens, `apply Bdd.okN_of_spec` (N = number
of things the call returns), `unfold` the model function, `step*`, then arithmetic.
A call with a loop cannot be unfolded and stepped that way. Helper lemmas may go in
modules of their own under lean/Lemmas/ (library `Lemmas`), imported from here.
-/
import Spec.Statements
open Aeneas Aeneas.Std Result

/-- features/inventory.feature:184  There are no more products than bins -/
theorem Spec.inventory.count_at_most_bins : Spec.inventory.count_at_most_bins.stmt := by
  sorry
