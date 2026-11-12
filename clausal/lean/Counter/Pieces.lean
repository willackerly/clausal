/-
THE VOCABULARY, Lean side, for the counter crate (the third project, plan node X7): DOMAIN WORDS.
Hand-written and HUMAN-ASSERTED: each definition is the intended meaning of one domain word of the counter's
local book (../../clausebook/local/counter.yaml, kind `domain`). Modifiers and frames are not here: they are
shared, in lean/Frames.

  measure     a quantity of a counter                          (`count`)
  answer      which returned values count as accepted          (`said`)
  operation   a `Frames.Op` bound to ONE function of the Aeneas-generated model through a fixed
              constructor of lean/Bdd/Ops.lean. Nothing else in this file may mention a model function.

`mkCounter` and `showCounter` are not vocabulary: they build and print concrete counters for the search
scripts (glossary.yaml, `actors.counter`).
-/
import Generated.Counter
import Bdd.Ops
open Aeneas Aeneas.Std

deriving instance DecidableEq for counter.Counter

namespace Ctr
open counter

/-- "count": the count of one counter, as a number. -/
@[reducible] def count (c : Counter) : Nat := c.count.val

/-- "is accepted" for an operation that answers yes or no: it answered yes. -/
@[reducible] def said (r : Bool) : Prop := r = true

/-- "bump": state = the counter, input = the amount. -/
@[reducible] def bump : Frames.Op Counter U64 Bool := Bdd.opMut counter.Counter.bump said

/-- Constructor used only to build concrete counters for search and witnesses. -/
@[simp] def mkCounter (n : U64) : Counter := { count := n }

/-- Printing, for counterexample reports only. -/
def showCounter (c : Counter) : String := s!"count {c.count.val}"

end Ctr
