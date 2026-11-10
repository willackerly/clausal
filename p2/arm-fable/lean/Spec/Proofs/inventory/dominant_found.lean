/-
Proof of the scenario statement `Spec.inventory.dominant_found.stmt` (lean/Spec/Statements.lean).

Hand-written (by a person or an agent). slicegen created this file as a `sorry`
stub and never edits it again. The theorem must be named exactly `Spec.inventory.dominant_found`
and its type must be exactly `Spec.inventory.dominant_found.stmt`: the audit checks both, so a
theorem of some other type is not counted as a proof.

Straight-line code: `intro` the variables and Givens, `apply Bdd.okN_of_spec` (N = number
of things the call returns), `unfold` the model function, `step*`, then arithmetic.
A call with a loop cannot be unfolded and stepped that way. Helper lemmas may go in
modules of their own under lean/Lemmas/ (library `Lemmas`), imported from here.
-/
import Spec.Statements
import Lemmas.Dominant
open Aeneas Aeneas.Std Result

/-- features/inventory.feature:197  A product in more than half of the bins is the dominant product -/
theorem Spec.inventory.dominant_found : Spec.inventory.dominant_found.stmt := by
  intro bins p main _ hmaj
  obtain ⟨o, ho, c, hc, hq⟩ := Bdd.ok_of_spec (Lemmas.dominant_spec main)
  refine ⟨o, ho, ?_⟩
  have hmaj' : main.bins.val.length < 2 * Lemmas.cnt p main.bins.val := hmaj
  have hcp : c = p := by
    by_contra hne
    have := hc p hne
    omega
  subst hcp
  have hle : Lemmas.cnt c main.bins.val ≤ main.bins.val.length := List.length_filter_le _ _
  rw [hq, if_pos (by omega)]
