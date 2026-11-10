/-
`find_bin`: linear search with early exit.
Invariant: no bin before position `i` holds enough of the product.
-/
import Lemmas.Basic
import Vocab.Inventory
open Aeneas Aeneas.Std Result inventory

namespace PL

theorem mem_take_succ {α} (l : List α) (i : Nat) (h : i < l.length) (b : α) :
    b ∈ l.take (i + 1) ↔ b ∈ l.take i ∨ b = l[i] := by
  rw [List.take_add_one, List.getElem?_eq_getElem h, Option.toList_some, List.mem_append, List.mem_singleton]

theorem find_bin_loop_spec (w : Warehouse) (p : U32) (n : U64) :
    ∀ (k : Nat) (i : Usize), w.bins.val.length - i.val = k → i.val ≤ w.bins.val.length →
    (∀ b ∈ w.bins.val.take i.val, ¬ IVocab.binHolds p n b) →
    ∃ r, Warehouse.find_bin_loop w p n i = ok r ∧
      (∀ j, r = some j → (∃ b ∈ w.bins.val[j.val]?, IVocab.binHolds p n b) ∧
                          ∀ b ∈ w.bins.val.take j.val, ¬ IVocab.binHolds p n b) ∧
      (r = none → ∀ b ∈ w.bins.val, ¬ IVocab.binHolds p n b) := by
  intro k
  induction k with
  | zero =>
    intro i hk hi hpre
    have hi' : w.bins.val.length ≤ i.val := by omega
    refine ⟨none, ?_, by simp, ?_⟩
    · unfold Warehouse.find_bin_loop
      apply loop_done
      simp [Warehouse.find_bin_loop.body, hi']
    · intro _ b hb
      exact hpre b (by rw [List.take_of_length_le hi']; exact hb)
  | succ k ih =>
    intro i hk hi hpre
    have hlt : i.val < w.bins.val.length := by omega
    obtain ⟨i1, hi1, hv1⟩ := usize_succ_ok i (by scalar_tac)
    by_cases hh : IVocab.binHolds p n w.bins.val[i.val]
    · have hb : Warehouse.find_bin_loop.body w p n i = ok (.done (some i)) := by
        obtain ⟨hp, hq⟩ := hh
        simp [Warehouse.find_bin_loop.body, hlt, vec_index_ok _ _ hlt, hp, hq]
      refine ⟨some i, by unfold Warehouse.find_bin_loop; exact loop_done hb, ?_, by simp⟩
      intro j hj; cases hj
      exact ⟨⟨_, by simp [hlt], hh⟩, hpre⟩
    · have hb : Warehouse.find_bin_loop.body w p n i = ok (.cont i1) := by
        simp only [IVocab.binHolds, not_and, not_le] at hh
        by_cases hp : w.bins.val[i.val].product = p
        · have hq := hh hp
          simp [Warehouse.find_bin_loop.body, hlt, vec_index_ok _ _ hlt, hp, hi1, hq]
        · simp [Warehouse.find_bin_loop.body, hlt, vec_index_ok _ _ hlt, hp, hi1]
      rw [show Warehouse.find_bin_loop w p n i = Warehouse.find_bin_loop w p n i1 from loop_cont hb]
      refine ih i1 (by omega) (by omega) ?_
      intro b hbm
      rw [hv1, mem_take_succ _ _ hlt] at hbm
      rcases hbm with hbm | rfl
      · exact hpre b hbm
      · exact hh

theorem find_bin_spec (w : Warehouse) (p : U32) (n : U64) :
    ∃ r, Warehouse.find_bin w p n = ok r ∧
      (∀ j, r = some j → (∃ b ∈ w.bins.val[j.val]?, IVocab.binHolds p n b) ∧
                          ∀ b ∈ w.bins.val.take j.val, ¬ IVocab.binHolds p n b) ∧
      (r = none → ∀ b ∈ w.bins.val, ¬ IVocab.binHolds p n b) :=
  find_bin_loop_spec w p n _ 0#usize rfl (by simp) (by simp)

end PL
