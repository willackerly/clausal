/-
`product_count`: a nested loop. The inner loop looks for an earlier bin with the same product
as bin `i`; the outer loop counts the bins whose product has not been seen before.
Inner invariant (generalised loop lemma): from position j the inner loop stops at i exactly when
bin i's product is not among bins j..i-1.
Outer invariant: count = number of different products among bins 0..i-1.
-/
import Mathlib.Data.Finset.Card
import Lemmas.Basic
import Vocab.Inventory
open Aeneas Aeneas.Std Result inventory

namespace PL

theorem card_toFinset_append_single (l : List Nat) (x : Nat) :
    ((l ++ [x]).toFinset).card = if x ∈ l then l.toFinset.card else l.toFinset.card + 1 := by
  have : (l ++ [x]).toFinset = insert x l.toFinset := by ext y; simp [or_comm]
  rw [this]; split
  · rw [Finset.card_insert_of_mem (by simpa)]
  · rw [Finset.card_insert_of_notMem (by simpa)]

theorem pc_inner_spec (v : alloc.vec.Vec Bin) (i : Usize) (hi : i.val < v.val.length) :
    ∀ (k : Nat) (j : Usize), i.val - j.val = k → j.val ≤ i.val →
    ∃ r, Warehouse.product_count_loop0_loop0 v i j = ok r ∧
      (r.val = i.val ↔
        v.val[i.val].product.val ∉ ((v.val.take i.val).drop j.val).map (fun b => b.product.val)) := by
  intro k
  induction k with
  | zero =>
    intro j hk hj
    have hji : i.val ≤ j.val := by omega
    refine ⟨j, ?_, ?_⟩
    · unfold Warehouse.product_count_loop0_loop0
      apply loop_done
      simp [Warehouse.product_count_loop0_loop0.body, hji]
    · have : (v.val.take i.val).drop j.val = [] := List.drop_eq_nil_of_le (by simp; omega)
      simp [this]; omega
  | succ k ih =>
    intro j hk hj
    have hlt : j.val < i.val := by omega
    have hjv : j.val < v.val.length := by omega
    have hd : (v.val.take i.val).drop j.val = v.val[j.val] :: (v.val.take i.val).drop (j.val + 1) := by
      rw [drop_cons _ j.val (by simp; omega)]; simp [List.getElem_take]
    rw [hd]
    by_cases hp : v.val[j.val].product = v.val[i.val].product
    · have hb : Warehouse.product_count_loop0_loop0.body v i j = ok (.done j) := by
        simp [Warehouse.product_count_loop0_loop0.body, hlt, vec_index_ok _ _ hjv, vec_index_ok _ _ hi, hp]
      refine ⟨j, by unfold Warehouse.product_count_loop0_loop0; exact loop_done hb, ?_⟩
      simp [hp]; omega
    · obtain ⟨j1, hj1, hv1⟩ := usize_succ_ok j (by scalar_tac)
      have hpv : ¬ (v.val[j.val].product.val = v.val[i.val].product.val) :=
        fun h => hp (UScalar.eq_of_val_eq h)
      have hb : Warehouse.product_count_loop0_loop0.body v i j = ok (.cont j1) := by
        simp [Warehouse.product_count_loop0_loop0.body, hlt, vec_index_ok _ _ hjv, vec_index_ok _ _ hi, hpv, hj1]
      rw [show Warehouse.product_count_loop0_loop0 v i j = Warehouse.product_count_loop0_loop0 v i j1
        from loop_cont hb]
      obtain ⟨r, hr, hiff⟩ := ih j1 (by omega) (by omega)
      refine ⟨r, hr, ?_⟩
      rw [hiff, hv1]; simp [hpv, Ne.symm hpv]

theorem pc_outer_spec (w : Warehouse) :
    ∀ (k : Nat) (count i : Usize), w.bins.val.length - i.val = k → i.val ≤ w.bins.val.length →
    count.val = ((w.bins.val.take i.val).map (fun b => b.product.val)).toFinset.card →
    count.val ≤ i.val →
    ∃ r, Warehouse.product_count_loop0 w count i = ok r ∧
      r.val = (w.bins.val.map (fun b => b.product.val)).toFinset.card := by
  intro k
  induction k with
  | zero =>
    intro count i hk hi hc hci
    have hi' : w.bins.val.length ≤ i.val := by omega
    refine ⟨count, ?_, ?_⟩
    · unfold Warehouse.product_count_loop0
      apply loop_done
      simp [Warehouse.product_count_loop0.body, hi']
    · rw [hc, List.take_of_length_le hi']
  | succ k ih =>
    intro count i hk hi hc hci
    have hlt : i.val < w.bins.val.length := by omega
    obtain ⟨j, hj, hjiff⟩ := pc_inner_spec w.bins i hlt _ 0#usize rfl (by simp)
    have h0 : (0#usize : Usize).val = 0 := by simp
    rw [h0, List.drop_zero] at hjiff
    obtain ⟨i1, hi1, hv1⟩ := usize_succ_ok i (by scalar_tac)
    have htake : (w.bins.val.take (i.val + 1)).map (fun b => b.product.val)
        = (w.bins.val.take i.val).map (fun b => b.product.val) ++ [w.bins.val[i.val].product.val] := by
      rw [List.take_add_one, List.getElem?_eq_getElem hlt, Option.toList_some, List.map_append,
        List.map_singleton]
    by_cases hx : w.bins.val[i.val].product.val ∈ (w.bins.val.take i.val).map (fun b => b.product.val)
    · have hji : ¬ j = i := fun h => by rw [h] at hjiff; exact (hjiff.mp rfl) hx
      have hb : Warehouse.product_count_loop0.body w count i = ok (.cont (count, i1)) := by
        simp [Warehouse.product_count_loop0.body, hlt, hj, hji, hi1]
      rw [show Warehouse.product_count_loop0 w count i = Warehouse.product_count_loop0 w count i1
        from loop_cont hb]
      refine ih count i1 (by omega) (by omega) ?_ (by omega)
      rw [hv1, htake, card_toFinset_append_single, ite_cond_eq_true _ _ (eq_true hx), hc]
    · have hji : j = i := UScalar.eq_of_val_eq (hjiff.mpr hx)
      obtain ⟨c1, hc1, hcv1⟩ := usize_succ_ok count (by scalar_tac)
      have hb : Warehouse.product_count_loop0.body w count i = ok (.cont (c1, i1)) := by
        simp [Warehouse.product_count_loop0.body, hlt, hj, hji, hi1, hc1]
      rw [show Warehouse.product_count_loop0 w count i = Warehouse.product_count_loop0 w c1 i1
        from loop_cont hb]
      refine ih c1 i1 (by omega) (by omega) ?_ (by omega)
      rw [hv1, htake, card_toFinset_append_single, ite_cond_eq_false _ _ (eq_false hx), hcv1, hc]

theorem product_count_spec (w : Warehouse) :
    ∃ r, Warehouse.product_count w = ok r ∧
      r.val = (w.bins.val.map (fun b => b.product.val)).toFinset.card :=
  pc_outer_spec w _ 0#usize 0#usize rfl (by simp) (by simp) (by simp)

end PL
