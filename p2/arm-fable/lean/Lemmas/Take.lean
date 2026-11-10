/- Pure facts about the reference `takeFrom`, and the loop invariant of `take`. -/
import Vocab.Inventory
import Lemmas.Stock
open Aeneas Aeneas.Std Result ControlFlow

namespace Lemmas
open inventory IVocab

/-- One bin as a pair (product, units). -/
def vw (b : Bin) : Nat × Nat := (b.product.val, b.qty.val)

theorem view_eq (w : Warehouse) : view w = w.bins.val.map vw := rfl

theorem takeFrom_zero (p : Nat) (l : List (Nat × Nat)) : takeFrom p 0 l = l := by
  induction l with
  | nil => rfl
  | cons e t ih => obtain ⟨q, u⟩ := e; simp [takeFrom, ih]

theorem takeFrom_nil (p n : Nat) : takeFrom p n [] = [] := by
  cases n <;> rfl

theorem stockIn_cons (p q u : Nat) (t : List (Nat × Nat)) :
    stockIn p ((q, u) :: t) = (if q = p then u else 0) + stockIn p t := by
  by_cases h : q = p <;> simp [stockIn, h]

theorem stockIn_nil (p : Nat) : stockIn p [] = 0 := rfl

theorem stockIn_takeFrom (p : Nat) (l : List (Nat × Nat)) :
    ∀ n, stockIn p (takeFrom p n l) + min n (stockIn p l) = stockIn p l := by
  induction l with
  | nil => intro n; simp [takeFrom_nil, stockIn_nil]
  | cons e t ih =>
    obtain ⟨q, u⟩ := e
    intro n
    by_cases h : q = p
    · have := ih (n - min u n)
      simp only [takeFrom, h, if_true, stockIn_cons] at this ⊢
      omega
    · have := ih n
      simp only [takeFrom, h, if_false, stockIn_cons] at this ⊢
      omega

/-- One loop step on a bin of the product. -/
theorem take_step_eq (p : Nat) (v : List (Nat × Nat)) (i : Nat) (h : i < v.length) (u left : Nat)
    (he : v[i] = (p, u)) :
    (v.set i (p, u - min u left)).take (i+1) ++
        takeFrom p (left - min u left) ((v.set i (p, u - min u left)).drop (i+1)) =
      v.take i ++ takeFrom p left (v.drop i) := by
  rw [List.drop_set_of_lt (by omega), List.drop_eq_getElem_cons h, he,
    List.take_succ_eq_append_getElem (by simpa using h), List.take_set_of_le (by omega),
    List.getElem_set_self]
  simp [takeFrom]

/-- One loop step on a bin of another product. -/
theorem take_step_ne (p : Nat) (v : List (Nat × Nat)) (i : Nat) (h : i < v.length) (left : Nat)
    (hne : v[i].1 ≠ p) :
    v.take (i+1) ++ takeFrom p left (v.drop (i+1)) = v.take i ++ takeFrom p left (v.drop i) := by
  rw [List.drop_eq_getElem_cons h, List.take_succ_eq_append_getElem h]
  generalize v[i] = e at hne
  obtain ⟨q, u⟩ := e
  simp only at hne
  simp [takeFrom, hne]

theorem stockIn_drop (p : Nat) (v : List (Nat × Nat)) (i : Nat) (h : i < v.length) :
    stockIn p (v.drop i) = (if v[i].1 = p then v[i].2 else 0) + stockIn p (v.drop (i+1)) := by
  rw [List.drop_eq_getElem_cons h]
  generalize v[i] = e
  obtain ⟨q, u⟩ := e
  exact stockIn_cons p q u _

/-- The invariant is kept by a step on a bin of the product. -/
theorem take_inv_eq (p : Nat) (V V0 : List (Nat × Nat)) (j : Nat) (hlt : j < V.length) (u l want : Nat)
    (he : V[j] = (p, u))
    (hF : V.take j ++ takeFrom p l (V.drop j) = takeFrom p want V0) (hle : l ≤ want)
    (hL : l - min l (stockIn p (V.drop j)) = want - min want (stockIn p V0)) :
    (V.set j (p, u - min u l)).take (j+1) ++
        takeFrom p (l - min u l) ((V.set j (p, u - min u l)).drop (j+1)) = takeFrom p want V0 ∧
      l - min u l ≤ want ∧
      (l - min u l) - min (l - min u l) (stockIn p ((V.set j (p, u - min u l)).drop (j+1)))
        = want - min want (stockIn p V0) := by
  refine ⟨by rw [take_step_eq p V j hlt u l he]; exact hF, by omega, ?_⟩
  have h := stockIn_drop p V j hlt
  rw [he] at h
  simp only [ite_true] at h
  rw [List.drop_set_of_lt (by omega), ← hL, h]
  omega

/-- The invariant is kept by a step on a bin of another product. -/
theorem take_inv_ne (p : Nat) (V V0 : List (Nat × Nat)) (j : Nat) (hlt : j < V.length) (l want : Nat)
    (hne : V[j].1 ≠ p)
    (hF : V.take j ++ takeFrom p l (V.drop j) = takeFrom p want V0)
    (hL : l - min l (stockIn p (V.drop j)) = want - min want (stockIn p V0)) :
    V.take (j+1) ++ takeFrom p l (V.drop (j+1)) = takeFrom p want V0 ∧
      l - min l (stockIn p (V.drop (j+1))) = want - min want (stockIn p V0) := by
  refine ⟨by rw [take_step_ne p V j hlt l hne]; exact hF, ?_⟩
  have h := stockIn_drop p V j hlt
  rw [if_neg hne] at h
  rw [← hL, h]; simp

theorem take_loop_spec (V0 : List (Nat × Nat)) (w : Warehouse) (p : U32) (want left : U64) (i : Usize)
    (hi : i.val ≤ w.bins.val.length)
    (h1 : (w.bins.val.map vw).take i.val ++ takeFrom p.val left.val ((w.bins.val.map vw).drop i.val)
            = takeFrom p.val want.val V0)
    (h2 : left.val ≤ want.val)
    (h3 : left.val - min left.val (stockIn p.val ((w.bins.val.map vw).drop i.val))
            = want.val - min want.val (stockIn p.val V0)) :
    Warehouse.take_loop w p left i ⦃ r =>
      r.1.val.map vw = takeFrom p.val want.val V0 ∧ r.2.val ≤ want.val ∧
        want.val - r.2.val = min want.val (stockIn p.val V0) ⦄ := by
  unfold Warehouse.take_loop
  apply loop.spec_decr_nat (fun (x : Warehouse × U64 × Usize) => x.1.bins.val.length - x.2.2.val)
    (fun (x : Warehouse × U64 × Usize) => x.2.2.val ≤ x.1.bins.val.length ∧
      (x.1.bins.val.map vw).take x.2.2.val ++
          takeFrom p.val x.2.1.val ((x.1.bins.val.map vw).drop x.2.2.val) = takeFrom p.val want.val V0 ∧
      x.2.1.val ≤ want.val ∧
      x.2.1.val - min x.2.1.val (stockIn p.val ((x.1.bins.val.map vw).drop x.2.2.val))
          = want.val - min want.val (stockIn p.val V0))
  · rintro ⟨s, l, j⟩ ⟨hj, hF, hle, hL⟩
    simp only at hj hF hle hL
    unfold Warehouse.take_loop.body
    step*
    · have hlt : j.val < (s.bins.val.map vw).length := by
        have h1 : j.val < s.bins.val.length := by scalar_tac
        simpa using h1
      have hV : (s.bins.val.map vw)[j.val] = (b.product.val, b.qty.val) := by
        simp [vw, b_post]
      by_cases hb : b.product = p
      · simp only [hb, ite_true]
        by_cases hq : b.qty < l
        · simp only [hq, ite_true]
          step as ⟨q', hq'⟩
          step as ⟨bb, hbb1, hbb2⟩
          rcases bb with ⟨b1, back⟩
          simp only at hbb1 hbb2 ⊢
          step as ⟨l', hl'⟩
          step as ⟨j', hj'⟩
          have hV' : List.map vw (back { product := b1.product, qty := q' }).val
              = (List.map vw s.bins.val).set j.val (p.val, b.qty.val - min b.qty.val l.val) := by
            rw [hbb2, alloc.vec.Vec.set_val_eq, List.map_set]
            congr 1
            have : q'.val = b.qty.val - min b.qty.val l.val := by scalar_tac
            simp [vw, hbb1, ← b_post, hb, this]
          have hl2 : l'.val = l.val - min b.qty.val l.val := by scalar_tac
          obtain ⟨g1, g2, g3⟩ := take_inv_eq p.val _ V0 j.val hlt b.qty.val l.val want.val
            (by rw [hV, hb]) hF hle hL
          rw [hV', hl2, hj']
          refine ⟨?_, g1, g2, g3, ?_⟩
          · simp [hbb2]; scalar_tac
          · simp [hbb2]; scalar_tac
        · simp only [hq, ite_false]
          step as ⟨q', hq'⟩
          step as ⟨bb, hbb1, hbb2⟩
          rcases bb with ⟨b1, back⟩
          simp only at hbb1 hbb2 ⊢
          step as ⟨l', hl'⟩
          step as ⟨j', hj'⟩
          have hV' : List.map vw (back { product := b1.product, qty := q' }).val
              = (List.map vw s.bins.val).set j.val (p.val, b.qty.val - min b.qty.val l.val) := by
            rw [hbb2, alloc.vec.Vec.set_val_eq, List.map_set]
            congr 1
            have : q'.val = b.qty.val - min b.qty.val l.val := by scalar_tac
            simp [vw, hbb1, ← b_post, hb, this]
          have hl2 : l'.val = l.val - min b.qty.val l.val := by scalar_tac
          obtain ⟨g1, g2, g3⟩ := take_inv_eq p.val _ V0 j.val hlt b.qty.val l.val want.val
            (by rw [hV, hb]) hF hle hL
          rw [hV', hl2, hj']
          refine ⟨?_, g1, g2, g3, ?_⟩
          · simp [hbb2]; scalar_tac
          · simp [hbb2]; scalar_tac
      · simp only [hb, ite_false]
        step*
        have hne : (s.bins.val.map vw)[j.val].1 ≠ p.val := by
          rw [hV]; intro e; exact hb ((u32_val_eq _ _).1 e)
        obtain ⟨g1, g2⟩ := take_inv_ne p.val _ V0 j.val hlt l.val want.val hne hF hL
        rw [i2_post]
        exact ⟨by scalar_tac, g1, hle, g2, by scalar_tac⟩
    · have h0 : l.val = 0 := by scalar_tac
      rw [h0, takeFrom_zero, List.take_append_drop] at hF
      rw [h0] at hL
      exact ⟨hF, hle, by omega⟩
    · have hjl : j.val = s.bins.val.length := by scalar_tac
      have hd : List.drop j.val (List.map vw s.bins.val) = [] := by simp [hjl]
      have ht : List.take j.val (List.map vw s.bins.val) = List.map vw s.bins.val := by simp [hjl]
      rw [hd, ht, takeFrom_nil, List.append_nil] at hF
      rw [hd, stockIn_nil] at hL
      exact ⟨hF, hle, by omega⟩
  · exact ⟨hi, h1, h2, h3⟩

theorem take_spec (w : Warehouse) (p : U32) (want : U64) :
    Warehouse.take w p want ⦃ r =>
      r.2.bins.val.map vw = takeFrom p.val want.val (w.bins.val.map vw) ∧
        r.1.val = min want.val (stockIn p.val (w.bins.val.map vw)) ⦄ := by
  unfold Warehouse.take
  have h := take_loop_spec (w.bins.val.map vw) w p want want 0#usize (by simp) (by simp)
    (Nat.le_refl _) (by simp)
  apply WP.spec_bind h
  rintro ⟨v, left⟩ ⟨h1, h2, h3⟩
  simp only at h1 h2 h3 ⊢
  step*

end Lemmas
