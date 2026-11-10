/- The loop invariant of `find_bin`. -/
import Vocab.Inventory
open Aeneas Aeneas.Std Result ControlFlow

namespace Lemmas
open inventory IVocab

theorem find_bin_loop_spec (w : Warehouse) (p : U32) (n : U64) (i : Usize)
    (hi : i.val ≤ w.bins.val.length) (hs : ∀ b ∈ w.bins.val.take i.val, ¬ binHolds p n b) :
    Warehouse.find_bin_loop w p n i ⦃ o =>
      match o with
      | some k => (∃ h : k.val < w.bins.val.length, binHolds p n (w.bins.val[k.val])) ∧
                    ∀ b ∈ w.bins.val.take k.val, ¬ binHolds p n b
      | none => ∀ b ∈ w.bins.val, ¬ binHolds p n b ⦄ := by
  unfold Warehouse.find_bin_loop
  apply loop.spec_decr_nat (fun (x : Usize) => w.bins.val.length - x.val)
    (fun (x : Usize) => x.val ≤ w.bins.val.length ∧ ∀ b ∈ w.bins.val.take x.val, ¬ binHolds p n b)
  · rintro j ⟨hj, hsj⟩
    unfold Warehouse.find_bin_loop.body
    step*
    · have hlt : j.val < w.bins.val.length := by scalar_tac
      refine ⟨by scalar_tac, ?_, by scalar_tac⟩
      rw [i2_post, List.take_succ_eq_append_getElem hlt]
      intro b' hb'
      rcases List.mem_append.1 hb' with h | h
      · exact hsj b' h
      · simp at h; subst h; rintro ⟨_, h2⟩; scalar_tac
    · have hlt : j.val < w.bins.val.length := by scalar_tac
      refine ⟨by scalar_tac, ?_, by scalar_tac⟩
      rw [i2_post, List.take_succ_eq_append_getElem hlt]
      intro b' hb'
      rcases List.mem_append.1 hb' with h | h
      · exact hsj b' h
      · simp at h; subst h; rintro ⟨h1, _⟩; simp_all
    · have hlt : j.val = w.bins.val.length := by scalar_tac
      simp_all
  · exact ⟨hi, hs⟩

theorem find_bin_spec (w : Warehouse) (p : U32) (n : U64) :
    Warehouse.find_bin w p n ⦃ o =>
      match o with
      | some k => (∃ h : k.val < w.bins.val.length, binHolds p n (w.bins.val[k.val])) ∧
                    ∀ b ∈ w.bins.val.take k.val, ¬ binHolds p n b
      | none => ∀ b ∈ w.bins.val, ¬ binHolds p n b ⦄ :=
  find_bin_loop_spec w p n 0#usize (by simp) (by simp)

end Lemmas
