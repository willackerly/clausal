/-
Generic helpers for reasoning about the Aeneas model by equations (`f ... = ok r`):
one unfolding step of the `loop` combinator, and the scalar / vector operations that the
loop bodies use, each stated as "this call returns `ok` of that value".
-/
import Aeneas
import Bdd.Basic
open Aeneas Aeneas.Std Result

namespace PL

/-- One iteration that continues. -/
theorem loop_cont {α β} {body : α → Result (ControlFlow α β)} {x x' : α}
    (h : body x = ok (.cont x')) : loop body x = loop body x' := by
  rw [loop]; simp [h]

/-- One iteration that stops. -/
theorem loop_done {α β} {body : α → Result (ControlFlow α β)} {x : α} {y : β}
    (h : body x = ok (.done y)) : loop body x = ok y := by
  rw [loop]; simp [h]

theorem uadd_ok {ty} (x y : UScalar ty) (h : x.val + y.val ≤ UScalar.max ty) :
    ∃ z, x + y = ok z ∧ z.val = x.val + y.val :=
  Bdd.ok_of_spec (UScalar.add_spec h)

theorem usub_ok {ty} (x y : UScalar ty) (h : y.val ≤ x.val) :
    ∃ z, x - y = ok z ∧ z.val = x.val - y.val := by
  obtain ⟨z, e, hz, -⟩ := Bdd.ok_of_spec (UScalar.sub_spec h)
  exact ⟨z, e, hz⟩

theorem vec_index_ok {α} (v : alloc.vec.Vec α) (i : Usize) (h : i.val < v.val.length) :
    alloc.vec.Vec.index (core.slice.index.SliceIndexUsizeSlice α) v i = ok (v.val[i.val]) := by
  simp [alloc.vec.Vec.index_usize, h]

theorem vec_index_mut_ok {α} (v : alloc.vec.Vec α) (i : Usize) (h : i.val < v.val.length) :
    alloc.vec.Vec.index_mut (core.slice.index.SliceIndexUsizeSlice α) v i
      = ok (v.val[i.val], alloc.vec.Vec.set v i) := by
  simp [alloc.vec.Vec.index_mut_usize, alloc.vec.Vec.index_usize, h]

theorem drop_cons {α} (l : List α) (i : Nat) (h : i < l.length) :
    l.drop i = l[i] :: l.drop (i + 1) := by
  exact List.drop_eq_getElem_cons h

end PL

namespace PL

theorem val_eq_iff {ty} (x y : UScalar ty) : x.val = y.val ↔ x = y :=
  ⟨UScalar.eq_of_val_eq, UScalar.val_eq_of_eq⟩

theorem u64_checked_add_cases (x y : U64) :
    (∃ z, U64.checked_add x y = some z ∧ z.val = x.val + y.val) ∨
    (U64.checked_add x y = none ∧ U64.max < x.val + y.val) := by
  have h := U64.checked_add_bv_spec x y
  cases hc : U64.checked_add x y with
  | none => rw [hc] at h; exact Or.inr ⟨rfl, h⟩
  | some z => rw [hc] at h; exact Or.inl ⟨z, rfl, h.2.1⟩

end PL

namespace PL

theorem usize_succ_ok (i : Usize) (h : i.val < Usize.max) :
    ∃ z, i + 1#usize = ok z ∧ z.val = i.val + 1 := by
  obtain ⟨z, e, hz⟩ := uadd_ok i 1#usize (by scalar_tac)
  exact ⟨z, e, by scalar_tac⟩

end PL
