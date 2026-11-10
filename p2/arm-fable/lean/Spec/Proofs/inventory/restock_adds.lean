/-
Proof of the scenario statement `Spec.inventory.restock_adds.stmt` (lean/Spec/Statements.lean).

Hand-written (by a person or an agent). slicegen created this file as a `sorry`
stub and never edits it again. The theorem must be named exactly `Spec.inventory.restock_adds`
and its type must be exactly `Spec.inventory.restock_adds.stmt`: the audit checks both, so a
theorem of some other type is not counted as a proof.

Straight-line code: `intro` the variables and Givens, `apply Bdd.okN_of_spec` (N = number
of things the call returns), `unfold` the model function, `step*`, then arithmetic.
A call with a loop cannot be unfolded and stepped that way. Helper lemmas may go in
modules of their own under lean/Lemmas/ (library `Lemmas`), imported from here.
-/
import Spec.Statements
import Lemmas.Restock
open Aeneas Aeneas.Std Result

/-- features/inventory.feature:72  Every bin of the product gains the amount, up to the maximum -/
theorem Spec.inventory.restock_adds : Spec.inventory.restock_adds.stmt := by
  intro bins p a main _
  obtain ⟨⟨c, w'⟩, ho, hq1, hq2⟩ := Bdd.ok_of_spec (Lemmas.restock_spec main p a)
  refine ⟨c, w', ho, ?_⟩
  simp only [IVocab.restocked, IVocab.view] at hq1 ⊢
  rw [hq1, List.map_map, List.map_map]
  apply List.map_congr_left
  intro b _
  simpa using Lemmas.upd_view p a b
