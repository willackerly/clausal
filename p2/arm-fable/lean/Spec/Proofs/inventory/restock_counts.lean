/-
Proof of the scenario statement `Spec.inventory.restock_counts.stmt` (lean/Spec/Statements.lean).

Hand-written (by a person or an agent). slicegen created this file as a `sorry`
stub and never edits it again. The theorem must be named exactly `Spec.inventory.restock_counts`
and its type must be exactly `Spec.inventory.restock_counts.stmt`: the audit checks both, so a
theorem of some other type is not counted as a proof.

Straight-line code: `intro` the variables and Givens, `apply Bdd.okN_of_spec` (N = number
of things the call returns), `unfold` the model function, `step*`, then arithmetic.
A call with a loop cannot be unfolded and stepped that way. Helper lemmas may go in
modules of their own under lean/Lemmas/ (library `Lemmas`), imported from here.
-/
import Spec.Statements
import Lemmas.Restock
open Aeneas Aeneas.Std Result

/-- features/inventory.feature:84  Restocking reports how many bins it restocked -/
theorem Spec.inventory.restock_counts : Spec.inventory.restock_counts.stmt := by
  intro bins p a main _
  obtain ⟨⟨c, w'⟩, ho, hq1, hq2⟩ := Bdd.ok_of_spec (Lemmas.restock_spec main p a)
  exact ⟨c, w', ho, hq2⟩
