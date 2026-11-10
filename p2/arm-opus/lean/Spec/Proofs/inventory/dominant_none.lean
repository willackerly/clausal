/-
Proof of the scenario statement `Spec.inventory.dominant_none.stmt` (lean/Spec/Statements.lean).

Hand-written (by a person or an agent). slicegen created this file as a `sorry`
stub and never edits it again. The theorem must be named exactly `Spec.inventory.dominant_none`
and its type must be exactly `Spec.inventory.dominant_none.stmt`: the audit checks both, so a
theorem of some other type is not counted as a proof.

Straight-line code: `intro` the variables and Givens, `apply Bdd.okN_of_spec` (N = number
of things the call returns), `unfold` the model function, `step*`, then arithmetic.
A call with a loop cannot be unfolded and stepped that way. Helper lemmas may go in
modules of their own under lean/Lemmas/ (library `Lemmas`), imported from here.
-/
import Spec.Statements
import Lemmas.Dominant
open Aeneas Aeneas.Std Result

/-- features/inventory.feature:210  There is no dominant product when no product is in more than half of the bins -/
theorem Spec.inventory.dominant_none : Spec.inventory.dominant_none.stmt := by
  intro bins main _ hnone
  obtain ⟨r, hr, -, h2⟩ := PL.dominant_spec main
  refine ⟨r, hr, ?_⟩
  cases r with
  | none => rfl
  | some c =>
    have hc := h2 c rfl
    have hpos : 0 < IVocab.binsOf main c := by omega
    obtain ⟨b, hb, hbc⟩ : ∃ b ∈ main.bins.val, b.product = c := by
      unfold IVocab.binsOf at hpos
      obtain ⟨b, hb⟩ := List.exists_mem_of_length_pos hpos
      rw [List.mem_filter] at hb
      exact ⟨b, hb.1, by simpa using hb.2⟩
    exact absurd (hbc ▸ hc) (hnone b hb)
