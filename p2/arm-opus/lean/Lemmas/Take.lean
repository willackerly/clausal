/-
`take`: takes units of one product from the earliest bins first, stopping early when nothing is
left to take. Loop lemma, generalised over the state: if the bins (as pairs) are `pre ++ rest` with
`pre` the bins before position `i`, the loop leaves `pre ++ takeFrom p left rest` and has
`left - (units of p in rest)` still to take.
-/
import Lemmas.Basic
import Lemmas.StockOf
import Vocab.Inventory
open Aeneas Aeneas.Std Result inventory

namespace PL

theorem ite_ok {α} (c : Prop) [Decidable c] (a b : α) :
    (if c then ok a else ok b : Result α) = ok (if c then a else b) := by
  split <;> rfl

theorem takeFrom_zero (p : Nat) : ∀ l, IVocab.takeFrom p 0 l = l
  | [] => rfl
  | (q, u) :: rest => by
    by_cases h : q = p <;> simp [IVocab.takeFrom, h, takeFrom_zero p rest]

theorem stockIn_takeFrom (p : Nat) : ∀ (l : List (Nat × Nat)) (need : Nat),
    IVocab.stockIn p (IVocab.takeFrom p need l) + min need (IVocab.stockIn p l) = IVocab.stockIn p l
  | [], need => by simp [IVocab.takeFrom, stockIn_nil]
  | (q, u) :: rest, need => by
    have ih := stockIn_takeFrom p rest (need - min u need)
    by_cases h : q = p
    · simp only [IVocab.takeFrom, h, ite_true, stockIn_cons] at ih ⊢
      omega
    · simp only [IVocab.takeFrom, h, ite_false, stockIn_cons]
      have := stockIn_takeFrom p rest need
      omega

theorem view_set (s : Warehouse) (i : Usize) (b : Bin) :
    IVocab.view { bins := alloc.vec.Vec.set s.bins i b }
      = (IVocab.view s).set i.val (b.product.val, b.qty.val) := by
  simp [IVocab.view]

theorem take_loop_spec (p : U32) :
    ∀ (k : Nat) (s : Warehouse) (left : U64) (i : Usize) (pre rest : List (Nat × Nat)),
    rest.length = k → IVocab.view s = pre ++ rest → pre.length = i.val →
    ∃ v left', Warehouse.take_loop s p left i = ok (v, left') ∧
      IVocab.view { bins := v } = pre ++ IVocab.takeFrom p.val left.val rest ∧
      left'.val = left.val - IVocab.stockIn p.val rest := by
  intro k
  induction k with
  | zero =>
    intro s left i pre rest hk hv hpre
    have hr : rest = [] := List.eq_nil_of_length_eq_zero hk
    subst hr
    have hlen : s.bins.val.length ≤ i.val := by
      have := congrArg List.length hv; simp [IVocab.view] at this; omega
    refine ⟨s.bins, left, ?_, ?_, ?_⟩
    · unfold Warehouse.take_loop
      apply loop_done
      simp [Warehouse.take_loop.body, hlen]
    · simpa [IVocab.takeFrom] using hv
    · simp [stockIn_nil]
  | succ k ih =>
    intro s left i pre rest hk hv hpre
    obtain ⟨x, rest', rfl⟩ : ∃ x rest', rest = x :: rest' := by
      cases rest with
      | nil => simp at hk
      | cons x r => exact ⟨x, r, rfl⟩
    have hlen : s.bins.val.length = i.val + rest'.length + 1 := by
      have := congrArg List.length hv; simp [IVocab.view] at this; omega
    have hlt : i.val < s.bins.val.length := by omega
    have hx : x = (s.bins.val[i.val].product.val, s.bins.val[i.val].qty.val) := by
      have h1 : (IVocab.view s)[i.val]? = some x := by
        rw [hv, List.getElem?_append_right (by omega)]; simp [hpre]
      have h2 : (IVocab.view s)[i.val]? = some (s.bins.val[i.val].product.val, s.bins.val[i.val].qty.val) := by
        simp [IVocab.view, hlt]
      rw [h1] at h2; exact Option.some.inj h2
    subst hx
    obtain ⟨i1, hi1, hv1⟩ := usize_succ_ok i (by scalar_tac)
    by_cases hl0 : left.val = 0
    · -- nothing left to take: the loop stops
      have hb : Warehouse.take_loop.body p s left i = ok (.done (s.bins, left)) := by
        simp [Warehouse.take_loop.body, hlt, hl0]
      refine ⟨s.bins, left, by unfold Warehouse.take_loop; exact loop_done hb, ?_, ?_⟩
      · rw [hl0, takeFrom_zero]; exact hv
      · simp [hl0]
    · by_cases hp : s.bins.val[i.val].product = p
      · -- take min (bin, left) from this bin
        obtain ⟨q1, l1, hqv1, hlv1, hb⟩ : ∃ q1 l1 : U64,
            q1.val = s.bins.val[i.val].qty.val - min s.bins.val[i.val].qty.val left.val ∧
            l1.val = left.val - min s.bins.val[i.val].qty.val left.val ∧
            Warehouse.take_loop.body p s left i = ok (.cont
              ({ bins := alloc.vec.Vec.set s.bins i { s.bins.val[i.val] with qty := q1 } }, l1, i1)) := by
          by_cases hql : s.bins.val[i.val].qty.val < left.val
          · obtain ⟨q1, hq1, hqv1⟩ := usub_ok s.bins.val[i.val].qty s.bins.val[i.val].qty (le_refl _)
            obtain ⟨l1, hl1, hlv1⟩ := usub_ok left s.bins.val[i.val].qty (by omega)
            refine ⟨q1, l1, by rw [hqv1]; omega, by rw [hlv1]; omega, ?_⟩
            simp [Warehouse.take_loop.body, hlt, show 0 < left.val by omega, vec_index_ok _ _ hlt,
              vec_index_mut_ok _ _ hlt, hp, ite_ok, hi1, hql, hq1, hl1]
          · obtain ⟨q1, hq1, hqv1⟩ := usub_ok s.bins.val[i.val].qty left (by omega)
            obtain ⟨l1, hl1, hlv1⟩ := usub_ok left left (le_refl _)
            refine ⟨q1, l1, by rw [hqv1]; omega, by rw [hlv1]; omega, ?_⟩
            simp [Warehouse.take_loop.body, hlt, show 0 < left.val by omega, vec_index_ok _ _ hlt,
              vec_index_mut_ok _ _ hlt, hp, ite_ok, hi1, hql, hq1, hl1]
        rw [show Warehouse.take_loop s p left i = Warehouse.take_loop
          { bins := alloc.vec.Vec.set s.bins i { s.bins.val[i.val] with qty := q1 } } p l1 i1 from loop_cont hb]
        obtain ⟨v, left', hr, hvv, hlv⟩ := ih { bins := alloc.vec.Vec.set s.bins i { s.bins.val[i.val] with qty := q1 } } l1 i1 (pre ++ [(p.val, q1.val)]) rest' (by simpa using hk)
          (by rw [view_set, hv, List.set_append_right _ _ (by omega)]; simp [hpre, hp])
          (by simp [hpre, hv1])
        refine ⟨v, left', hr, ?_, ?_⟩
        · rw [hvv]; simp [IVocab.takeFrom, hp, hqv1, hlv1]
        · rw [hlv, hlv1, stockIn_cons]; simp [hp]; omega
      · have hb : Warehouse.take_loop.body p s left i = ok (.cont (s, left, i1)) := by
          simp [Warehouse.take_loop.body, hlt, show 0 < left.val by omega, vec_index_ok _ _ hlt, hp, hi1]
        rw [show Warehouse.take_loop s p left i = Warehouse.take_loop s p left i1 from loop_cont hb]
        have hpv : ¬ (s.bins.val[i.val].product.val = p.val) := fun h => hp (UScalar.eq_of_val_eq h)
        obtain ⟨v, left', hr, hvv, hlv⟩ := ih s left i1 (pre ++ [(s.bins.val[i.val].product.val,
          s.bins.val[i.val].qty.val)]) rest' (by simpa using hk) (by rw [hv]; simp) (by simp [hpre, hv1])
        refine ⟨v, left', hr, ?_, ?_⟩
        · rw [hvv]; simp [IVocab.takeFrom, hpv]
        · rw [hlv, stockIn_cons]; simp [hpv]

theorem take_spec (w : Warehouse) (p : U32) (want : U64) :
    ∃ t w', Warehouse.take w p want = ok (t, w') ∧
      IVocab.view w' = IVocab.takeFrom p.val want.val (IVocab.view w) ∧
      t.val = min want.val (IVocab.stock w p) := by
  obtain ⟨v, left', hr, hvv, hlv⟩ := take_loop_spec p _ w want 0#usize [] (IVocab.view w) rfl rfl rfl
  obtain ⟨t, ht, htv⟩ := usub_ok want left' (by omega)
  refine ⟨t, { bins := v }, by simp [Warehouse.take, hr, ht], by simpa using hvv, ?_⟩
  rw [htv, hlv]; simp only [IVocab.stock]; omega

end PL
