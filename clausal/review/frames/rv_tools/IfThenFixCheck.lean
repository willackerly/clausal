/- Reviewer: does the proposed fail-closed `IfThen` build, separate the toy, and agree with its checker on it?
   Run from rv2/lean after applying the proposed change: `lake env lean ../../rv_tools/IfThenFixCheck.lean`. -/
import Frames.Check
open Frames

@[reducible] def toy : Op Unit Nat Bool where
  run _ n := if n = 0 then none else some (n ≠ 1, ())
  accepted b := b = true
instance : DecidablePred toy.accepted := fun b => inferInstanceAs (Decidable (b = true))
instance (s : Unit) (a : Nat) : Decidable (toy.scope s a) := inferInstanceAs (Decidable True)

-- no answer at 0, rejected at 1, accepted from 2 on; claim: accepted whenever n ≥ 1 (false at 0: silent; false at 1: rejected)
#eval (List.range 4).map fun n =>
  (n, decide (IfThen.at toy (fun _ n => 1 ≤ n) (fun b => toy.accepted b) () n),
      Check.ifThen toy (fun _ n => 1 ≤ n) (fun b => toy.accepted b) () n)

theorem toy_not_ifThen : ¬ IfThen toy (fun _ n => 2 ≤ n) (fun b => toy.accepted b) := by
  intro h
  obtain ⟨r, s', e, _⟩ := h () 0 trivial
  simp [toy] at e
#print axioms toy_not_ifThen
