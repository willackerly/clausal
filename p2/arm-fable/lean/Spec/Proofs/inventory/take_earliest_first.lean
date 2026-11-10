/-
Proof of the scenario statement `Spec.inventory.take_earliest_first.stmt` (lean/Spec/Statements.lean).

Hand-written (by a person or an agent). slicegen created this file as a `sorry`
stub and never edits it again. The theorem must be named exactly `Spec.inventory.take_earliest_first`
and its type must be exactly `Spec.inventory.take_earliest_first.stmt`: the audit checks both, so a
theorem of some other type is not counted as a proof.

Straight-line code: `intro` the variables and Givens, `apply Bdd.okN_of_spec` (N = number
of things the call returns), `unfold` the model function, `step*`, then arithmetic.
A call with a loop cannot be unfolded and stepped that way. Helper lemmas may go in
modules of their own under lean/Lemmas/ (library `Lemmas`), imported from here.
-/
import Spec.Statements
import Lemmas.Take
open Aeneas Aeneas.Std Result

/-- features/inventory.feature:122  Units are taken from the earliest bins of the product first -/
theorem Spec.inventory.take_earliest_first : Spec.inventory.take_earliest_first.stmt := by
  intro bins p n main _
  obtain ⟨⟨t, w'⟩, ho, hq1, hq2⟩ := Bdd.ok_of_spec (Lemmas.take_spec main p n)
  exact ⟨t, w', ho, hq1⟩
