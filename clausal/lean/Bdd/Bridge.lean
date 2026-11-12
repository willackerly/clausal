/-
Facts used only by GENERATED GLUE PROOFS (a compiled reading is equivalent to the flat statement the
proofs are about; a Rule follows from its scenarios). They are not definitions and appear in no statement.
-/
import Aeneas
open Aeneas Aeneas.Std

namespace Bdd.Bridge

/-- Two unsigned 64-bit values are equal exactly when the numbers they stand for are. -/
theorem u64_val_eq {a b : U64} : a.val = b.val ↔ a = b := by
  constructor
  · intro h; scalar_tac
  · intro h; rw [h]

theorem usize_val_eq {a b : Usize} : a.val = b.val ↔ a = b := by
  constructor
  · intro h; scalar_tac
  · intro h; rw [h]

/-- `List.range` is injective. -/
theorem range_eq {m n : Nat} : List.range m = List.range n ↔ m = n := by
  constructor
  · intro h; simpa using congrArg List.length h
  · intro h; rw [h]

end Bdd.Bridge
