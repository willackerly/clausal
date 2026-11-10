/- Pure list facts for in-place loops, the missing fact about `saturating_add`, and the loop
   invariant of `restock`. -/
import Vocab.Inventory
import Lemmas.Stock
open Aeneas Aeneas.Std Result ControlFlow

namespace Lemmas
open inventory IVocab

theorem sat_val (x y : U64) :
    (core.num.U64.saturating_add x y).val = min (x.val + y.val) U64.max := by
  show (BitVec.ofNat _ (min (UScalar.max .U64) (x.val + y.val))).toNat = _
  have hb : UScalarTy.U64.numBits = 64 := rfl
  rw [BitVec.toNat_ofNat, UScalar.max_UScalarTy_U64_eq, U64.max_eq, hb]
  omega

/-- The list after the first `j` elements were replaced by their image under `f`. -/
def part {α} (f : α → α) (l : List α) (j : Nat) : List α := (l.take j).map f ++ l.drop j

theorem part_length {α} (f : α → α) (l : List α) (j : Nat) : (part f l j).length = l.length := by
  simp [part]; omega

theorem part_getElem {α} (f : α → α) (l : List α) (j : Nat) (h : j < l.length)
    (h' : j < (part f l j).length) : (part f l j)[j] = l[j] := by
  have hl : (List.map f (List.take j l)).length = j := by simp; omega
  simp only [part]
  rw [List.getElem_append_right (by omega)]
  simp [Nat.min_eq_left (Nat.le_of_lt h)]

theorem part_set {α} (f : α → α) (l : List α) (j : Nat) (h : j < l.length) :
    (part f l j).set j (f l[j]) = part f l (j+1) := by
  have hl : (List.map f (List.take j l)).length = j := by simp; omega
  unfold part
  rw [List.set_append, hl, ite_cond_eq_false _ _ (eq_false (Nat.lt_irrefl j)), Nat.sub_self, List.drop_eq_getElem_cons h,
    List.take_succ_eq_append_getElem h, List.map_append, List.append_assoc]
  rfl

theorem getElem_of_eq_part {α} (f : α → α) {l' l : List α} {j : Nat} (e : l' = part f l j)
    (h : j < l.length) (h' : j < l'.length) : l'[j] = l[j] := by
  subst e; exact part_getElem f l j h h'

theorem part_same {α} (f : α → α) (l : List α) (j : Nat) (h : j < l.length) (e : f l[j] = l[j]) :
    part f l j = part f l (j+1) := by
  rw [← part_set f l j h, e]
  have h' : j < (part f l j).length := by rw [part_length]; exact h
  rw [← part_getElem f l j h h', List.set_getElem_self]

theorem part_zero {α} (f : α → α) (l : List α) : part f l 0 = l := by simp [part]
theorem part_all {α} (f : α → α) (l : List α) : part f l l.length = l.map f := by simp [part]

/-- What `restock` does to one bin. -/
def upd (p : U32) (a : U64) (b : Bin) : Bin :=
  if b.product = p then { b with qty := core.num.U64.saturating_add b.qty a } else b

/-- Number of bins of product `p`. -/
def cnt (p : U32) (l : List Bin) : Nat := (l.filter fun b => b.product = p).length

theorem cnt_append (p : U32) (a b : List Bin) : cnt p (a ++ b) = cnt p a + cnt p b := by
  simp [cnt]

theorem cnt_take_succ (p : U32) (l : List Bin) (i : Nat) (h : i < l.length) :
    cnt p (l.take (i+1)) = cnt p (l.take i) + (if l[i].product = p then 1 else 0) := by
  rw [List.take_succ_eq_append_getElem h, cnt_append]
  by_cases e : l[i].product = p <;> simp [cnt, e]

theorem cnt_take_le (p : U32) (l : List Bin) (i : Nat) : cnt p (l.take i) ≤ i := by
  unfold cnt
  calc _ ≤ (l.take i).length := List.length_filter_le _ _
    _ ≤ i := by simp

theorem restock_loop_spec (w0 w : Warehouse) (p : U32) (a : U64) (count i : Usize)
    (hi : i.val ≤ w0.bins.val.length)
    (hw : w.bins.val = part (upd p a) w0.bins.val i.val)
    (hc : count.val = cnt p (w0.bins.val.take i.val)) :
    Warehouse.restock_loop w p a count i ⦃ r =>
      r.1.val = w0.bins.val.map (upd p a) ∧ r.2.val = cnt p w0.bins.val ⦄ := by
  unfold Warehouse.restock_loop
  apply loop.spec_decr_nat (fun (x : Warehouse × Usize × Usize) => w0.bins.val.length - x.2.2.val)
    (fun (x : Warehouse × Usize × Usize) => x.2.2.val ≤ w0.bins.val.length ∧
      x.1.bins.val = part (upd p a) w0.bins.val x.2.2.val ∧
      x.2.1.val = cnt p (w0.bins.val.take x.2.2.val))
  · rintro ⟨s, c, j⟩ ⟨hj, hsj, hcj⟩
    simp only at hj hsj hcj
    unfold Warehouse.restock_loop.body
    have hlen : s.bins.val.length = w0.bins.val.length := by rw [hsj, part_length]
    step*
    · have hlt : j.val < w0.bins.val.length := by
        have h1 : j.val < s.bins.val.length := by scalar_tac
        omega
      have hbj : b = w0.bins.val[j.val] := by
        rw [b_post]; exact getElem_of_eq_part _ hsj hlt _
      have hcl := cnt_take_le p w0.bins.val j.val
      by_cases hb : b.product = p
      · simp only [hb, ite_true, lift]
        step*
        rcases x with ⟨b1, back⟩
        simp only at x_post x_post1 ⊢
        step*
        refine ⟨by scalar_tac, ?_, ?_, by scalar_tac⟩
        · have hb1 : b1 = b := by rw [b_post]; assumption
          rw [x_post1, alloc.vec.Vec.set_val_eq, i2_post, ← part_set _ _ _ hlt, ← hsj, ← hbj, hb1]
          congr 1
          simp [upd, hb]
        · rw [i2_post, cnt_take_succ _ _ _ hlt, ← hbj, if_pos hb]; scalar_tac
      · simp only [hb, ite_false]
        step*
        have hu : upd p a w0.bins.val[j.val] = w0.bins.val[j.val] := by
          rw [← hbj]; simp [upd, hb]
        refine ⟨by scalar_tac, ?_, ?_, by scalar_tac⟩
        · rw [i2_post, ← part_same _ _ _ hlt hu]; exact hsj
        · rw [i2_post, cnt_take_succ _ _ _ hlt, ← hbj, if_neg hb]; scalar_tac
    · have hjl : j.val = w0.bins.val.length := by scalar_tac
      rw [hjl] at hsj hcj
      rw [part_all] at hsj
      rw [List.take_length] at hcj
      exact ⟨hsj, hcj⟩
  · exact ⟨hi, hw, hc⟩

theorem restock_spec (w : Warehouse) (p : U32) (a : U64) :
    Warehouse.restock w p a ⦃ r =>
      r.2.bins.val = w.bins.val.map (upd p a) ∧ r.1.val = cnt p w.bins.val ⦄ := by
  unfold Warehouse.restock
  have h := restock_loop_spec w w p a 0#usize 0#usize (by simp) (by simp [part_zero]) (by simp [cnt])
  apply WP.spec_bind h
  rintro ⟨v, c⟩ ⟨h1, h2⟩
  simp_all

theorem upd_view (p : U32) (a : U64) (b : Bin) :
    ((upd p a b).product.val, (upd p a b).qty.val) =
      (b.product.val, if b.product.val = p.val then min (b.qty.val + a.val) U64.max else b.qty.val) := by
  unfold upd
  by_cases h : b.product = p
  · simp [h, sat_val]
  · have : ¬ b.product.val = p.val := fun e => h ((u32_val_eq _ _).1 e)
    simp [h, this]

end Lemmas
