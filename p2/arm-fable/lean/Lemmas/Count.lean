/- Counting distinct products: pure facts and the two loop invariants of `product_count`. -/
import Vocab.Inventory
import Lemmas.Stock
open Aeneas Aeneas.Std Result ControlFlow

namespace Lemmas
open inventory IVocab

/-- Number of different products among bins. -/
def dp (l : List Bin) : Nat := (l.map fun b => b.product.val).toFinset.card

theorem card_snoc (A : List Nat) (x : Nat) :
    (A ++ [x]).toFinset.card = A.toFinset.card + (if x ∈ A then 0 else 1) := by
  have e : (A ++ [x]).toFinset = insert x A.toFinset := by
    ext y; simp
  rw [e]
  split
  · rename_i h; rw [Finset.insert_eq_of_mem (by simpa using h)]; rfl
  · rename_i h; rw [Finset.card_insert_of_notMem (by simpa using h)]

theorem dp_take_succ (l : List Bin) (i : Nat) (h : i < l.length) :
    dp (l.take (i+1)) = dp (l.take i) +
      (if l[i].product.val ∈ (l.take i).map (fun b => b.product.val) then 0 else 1) := by
  unfold dp
  rw [List.take_succ_eq_append_getElem h, List.map_append]
  exact card_snoc _ _

theorem dp_le (l : List Bin) : dp l ≤ l.length := by
  unfold dp
  have := List.toFinset_card_le (l.map fun b => b.product.val)
  simpa using this

theorem pc_inner_spec (v : alloc.vec.Vec Bin) (i j : Usize) (hi : i.val < v.val.length)
    (hj : j.val ≤ i.val) (hpre : ∀ b ∈ v.val.take j.val, b.product ≠ v.val[i.val].product) :
    Warehouse.product_count_loop0_loop0 v i j ⦃ r =>
      r.val ≤ i.val ∧ (∀ b ∈ v.val.take r.val, b.product ≠ v.val[i.val].product) ∧
        (r.val < i.val → ∃ h : r.val < v.val.length, v.val[r.val].product = v.val[i.val].product) ⦄ := by
  unfold Warehouse.product_count_loop0_loop0
  apply loop.spec_decr_nat (fun (x : Usize) => i.val - x.val)
    (fun (x : Usize) => x.val ≤ i.val ∧ ∀ b ∈ v.val.take x.val, b.product ≠ v.val[i.val].product)
  · rintro k ⟨hk, hkp⟩
    unfold Warehouse.product_count_loop0_loop0.body
    step*
    have hkl : k.val < v.val.length := by scalar_tac
    refine ⟨by scalar_tac, ?_, by scalar_tac⟩
    rw [j1_post, List.take_succ_eq_append_getElem hkl]
    intro b' hb'
    rcases List.mem_append.1 hb' with h | h
    · exact hkp b' h
    · simp at h; subst h; rw [← b_post, ← b1_post]
      simpa using ‹(b.product != b1.product) = true›
  · exact ⟨hj, hpre⟩

theorem pc_inner_spec0 (v : alloc.vec.Vec Bin) (i : Usize) (hi : i.val < v.val.length) :
    Warehouse.product_count_loop0_loop0 v i 0#usize ⦃ r =>
      r.val ≤ i.val ∧ (∀ b ∈ v.val.take r.val, b.product ≠ v.val[i.val].product) ∧
        (r.val < i.val → ∃ h : r.val < v.val.length, v.val[r.val].product = v.val[i.val].product) ⦄ :=
  pc_inner_spec v i 0#usize hi (by simp) (by simp)

theorem pc_outer_spec (w : Warehouse) (count i : Usize) (hi : i.val ≤ w.bins.val.length)
    (hc : count.val = dp (w.bins.val.take i.val)) :
    Warehouse.product_count_loop0 w count i ⦃ r => r.val = dp w.bins.val ⦄ := by
  unfold Warehouse.product_count_loop0
  apply loop.spec_decr_nat (fun (x : Usize × Usize) => w.bins.val.length - x.2.val)
    (fun (x : Usize × Usize) => x.2.val ≤ w.bins.val.length ∧ x.1.val = dp (w.bins.val.take x.2.val))
  · rintro ⟨c, k⟩ ⟨hk, hck⟩
    simp only at hk hck
    unfold Warehouse.product_count_loop0.body
    step*
    · have hlt : k.val < w.bins.val.length := by scalar_tac
      have hstep := dp_take_succ w.bins.val k.val hlt
      have hcl : dp (w.bins.val.take k.val) ≤ k.val := by
        have := dp_le (w.bins.val.take k.val); simp at this; omega
      step with pc_inner_spec0 as ⟨r, hr1, hr2, hr3⟩
      by_cases hrk : r = k
      · subst hrk
        simp only [↓reduceIte]
        have hn : ¬ w.bins.val[r.val].product.val ∈ (w.bins.val.take r.val).map (fun b => b.product.val) := by
          intro hm
          obtain ⟨b, hb, e⟩ := List.mem_map.1 hm
          exact hr2 b hb ((u32_val_eq _ _).1 e)
        rw [if_neg hn] at hstep
        step as ⟨c2, hc2⟩
        step as ⟨k2, hk2⟩
        exact ⟨by scalar_tac, by rw [hk2, hstep]; scalar_tac, by scalar_tac⟩
      · simp only [hrk, ↓reduceIte]
        have hlt2 : r.val < k.val := by scalar_tac
        obtain ⟨hh, e⟩ := hr3 hlt2
        have hm : w.bins.val[k.val].product.val ∈ (w.bins.val.take k.val).map (fun b => b.product.val) := by
          refine List.mem_map.2 ⟨w.bins.val[r.val], ?_, by rw [e]⟩
          exact List.mem_iff_getElem.2 ⟨r.val, by simp; omega, by simp⟩
        rw [if_pos hm] at hstep
        step as ⟨k2, hk2⟩
        exact ⟨by scalar_tac, by rw [hk2, hstep]; scalar_tac, by scalar_tac⟩
    · have hkl : k.val = w.bins.val.length := by scalar_tac
      rw [hkl, List.take_length] at hck
      exact hck
  · exact ⟨hi, hc⟩

theorem product_count_spec (w : Warehouse) :
    Warehouse.product_count w ⦃ r => r.val = dp w.bins.val ⦄ :=
  pc_outer_spec w 0#usize 0#usize (by simp) (by simp [dp])

end Lemmas
