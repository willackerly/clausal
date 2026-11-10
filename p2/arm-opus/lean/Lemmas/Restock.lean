/-
`restock`: an in-place update of every bin of one product, plus a count.
Invariant (relative to the bins `bs` before the loop): the bins before position `i` are restocked,
the bins from `i` on are untouched, and `count` is the number of bins of the product before `i`.
-/
import Lemmas.Basic
import Lemmas.FindBin
import Vocab.Inventory
open Aeneas Aeneas.Std Result inventory

namespace PL

/-- What the loop does to one bin. -/
def restockBin (p : U32) (a : U64) (b : Bin) : Bin :=
  if b.product = p then { b with qty := core.num.U64.saturating_add b.qty a } else b

/-- The fact about `saturating_add` that the Aeneas library does not ship. -/
theorem sat_add_val (x y : U64) :
    (core.num.U64.saturating_add x y).val = min (x.val + y.val) U64.max := by
  have hm : UScalar.max UScalarTy.U64 = U64.max := by simp
  show (BitVec.ofNat _ (Min.min (UScalar.max UScalarTy.U64) (x.val + y.val))).toNat = _
  rw [BitVec.toNat_ofNat, hm, Nat.min_comm]
  apply Nat.mod_eq_of_lt
  have : U64.max = 18446744073709551615 := U64.max_eq
  have : Min.min (x.val + y.val) U64.max ≤ U64.max := Nat.min_le_right _ _
  simp only [UScalarTy.numBits]
  omega

theorem count_take_succ (bs : List Bin) (p : U32) (i : Nat) (h : i < bs.length) :
    ((bs.take (i + 1)).filter fun b => b.product = p).length
      = ((bs.take i).filter fun b => b.product = p).length + (if bs[i].product = p then 1 else 0) := by
  rw [List.take_add_one, List.getElem?_eq_getElem h, Option.toList_some, List.filter_append,
    List.length_append]
  by_cases hp : bs[i].product = p <;> simp [hp]

theorem restock_loop_spec (bs : List Bin) (p : U32) (a : U64) :
    ∀ (k : Nat) (s : Warehouse) (c i : Usize) (hl : s.bins.val.length = bs.length),
    bs.length - i.val = k → i.val ≤ bs.length →
    (∀ j (hj : j < bs.length), s.bins.val[j]'(by omega) = if j < i.val then restockBin p a bs[j] else bs[j]) →
    c.val = ((bs.take i.val).filter fun b => b.product = p).length →
    ∃ v c', Warehouse.restock_loop s p a c i = ok (v, c') ∧
      v.val = bs.map (restockBin p a) ∧ c'.val = (bs.filter fun b => b.product = p).length := by
  intro k
  induction k with
  | zero =>
    intro s c i hl hk hi hs hc
    have hi' : bs.length ≤ i.val := by omega
    refine ⟨s.bins, c, ?_, ?_, ?_⟩
    · unfold Warehouse.restock_loop
      apply loop_done
      simp [Warehouse.restock_loop.body, hl, hi']
    · apply List.ext_getElem (by simp [hl])
      intro j h1 h2
      rw [hs j (by omega)]; simp; omega
    · rw [hc, List.take_of_length_le hi']
  | succ k ih =>
    intro s c i hl hk hi hs hc
    have hlt : i.val < bs.length := by omega
    have hlt' : i.val < s.bins.val.length := by omega
    have hsi : s.bins.val[i.val] = bs[i.val] := by rw [hs i.val hlt]; simp
    have hcle : c.val ≤ i.val := by
      rw [hc]; exact (List.length_filter_le _ _).trans (by simp)
    obtain ⟨i1, hi1, hv1⟩ := usize_succ_ok i (by scalar_tac)
    by_cases hp : bs[i.val].product = p
    · obtain ⟨c1, hc1, hcv1⟩ := usize_succ_ok c (by scalar_tac)
      have hb : Warehouse.restock_loop.body p a s c i = ok (.cont
          ({ bins := alloc.vec.Vec.set s.bins i
              { s.bins.val[i.val] with qty := core.num.U64.saturating_add s.bins.val[i.val].qty a } },
            c1, i1)) := by
        simp [Warehouse.restock_loop.body, hlt', vec_index_ok _ _ hlt', vec_index_mut_ok _ _ hlt',
          hsi, hp, hc1, hi1, lift]
      rw [show Warehouse.restock_loop s p a c i = Warehouse.restock_loop _ p a c1 i1 from loop_cont hb]
      refine ih _ c1 i1 (by simp [hl]) (by omega) (by omega) ?_ ?_
      · intro j hj
        simp only [alloc.vec.Vec.set_val_eq, List.getElem_set]
        by_cases hji : i.val = j
        · subst hji; simp [hv1, restockBin, hp, hsi]
        · simp only [hji, ite_false, hs j hj, hv1]
          by_cases hj' : j < i.val
          · simp [hj', show j < i.val + 1 by omega]
          · simp [hj', show ¬ j < i.val + 1 by omega]
      · rw [hv1, count_take_succ bs p i.val hlt, hcv1, hc]; simp [hp]
    · have hb : Warehouse.restock_loop.body p a s c i = ok (.cont (s, c, i1)) := by
        simp [Warehouse.restock_loop.body, hlt', vec_index_ok _ _ hlt', hsi, hp, hi1]
      rw [show Warehouse.restock_loop s p a c i = Warehouse.restock_loop s p a c i1 from loop_cont hb]
      refine ih s c i1 hl (by omega) (by omega) ?_ ?_
      · intro j hj
        rw [hs j hj, hv1]
        by_cases hji : j = i.val
        · subst hji; simp [restockBin, hp]
        · by_cases hj' : j < i.val
          · simp [hj', show j < i.val + 1 by omega]
          · simp [hj', show ¬ j < i.val + 1 by omega]
      · rw [hv1, count_take_succ bs p i.val hlt, hc]; simp [hp]

theorem restock_spec (w : Warehouse) (p : U32) (a : U64) :
    ∃ c w', Warehouse.restock w p a = ok (c, w') ∧
      w'.bins.val = w.bins.val.map (restockBin p a) ∧ c.val = IVocab.binsOf w p := by
  obtain ⟨v, c, hr, hv, hc⟩ := restock_loop_spec w.bins.val p a _ w 0#usize 0#usize rfl rfl (by simp)
    (by intro j hj; simp) (by simp)
  exact ⟨c, { bins := v }, by simp [Warehouse.restock, hr], hv, by simp [IVocab.binsOf, hc]⟩

end PL
