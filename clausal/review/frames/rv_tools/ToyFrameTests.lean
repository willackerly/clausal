/-
Reviewer's proposed addition to lean/Run/FrameTests.lean (V2/V3 review, second pass).

The fixtures give the definition-versus-checker comparison almost nothing to bite on: the definition is false at 125 of
23,700 evaluations and no call in scope ever gives no answer. This toy operation (core Lean only) gives NO answer at
input 0, REJECTS at input 1 (state unchanged) and ACCEPTS from 2 on (state grows by the input), and every frame with a
surface form is stated of it with a claim that is false at some points. Each line has the FTEST format the report
already reads, so a disagreement fails the run.

To try it alone: from a scratch copy's lean/ directory, `lake env lean <path>/ToyFrameTests.lean`.
-/
import Frames.Check
open Frames

namespace ToyFT

@[reducible] def toy : Op Nat Nat Bool where
  run s n := if n = 0 then none else if n = 1 then some (false, s) else some (true, s + n)
  accepted b := b = true
instance : DecidablePred toy.accepted := fun b => inferInstanceAs (Decidable (b = true))
instance (s a : Nat) : Decidable (toy.scope s a) := inferInstanceAs (Decidable True)

def pts : List (Nat × Nat) := (List.range 4).flatMap fun s => (List.range 5).map fun n => (s, n)

def tline (frame : String) (f : Nat → Nat → Bool × Bool) : String :=
  let rs := pts.map fun (s, n) => f s n
  s!"FTEST\t{frame}\ttoy operation (no answer at 0, rejected at 1, accepted from 2)\t{rs.length}\t{(rs.filter fun p => p.1 == p.2).length}\t{(rs.filter fun p => !p.1).length}"

@[reducible] def m : Measure Nat Nat Nat := fun s _ => s
@[reducible] def acc : AnswerClass Bool := fun b => toy.accepted b
@[reducible] def c3 : Cond Nat Nat := fun _ n => 3 ≤ n
@[reducible] def coll : Coll Nat Nat Bool Nat := fun _ n _ => List.range n
@[reducible] def small : ItemCond Nat Nat Nat := fun _ _ x => x < 2

#eval show IO Unit from do
  IO.println (tline "always_answers" fun s n => (decide (AlwaysAnswers.at toy s n), Check.alwaysAnswers toy s n))
  IO.println (tline "never_changes" fun s n => (decide (NeverChanges.at toy m s n), Check.neverChanges toy m s n))
  IO.println (tline "always" fun s n => (decide (Always.at toy acc s n), Check.always toy acc s n))
  IO.println (tline "never" fun s n => (decide (Never.at toy acc s n), Check.never toy acc s n))
  IO.println (tline "if_then" fun s n => (decide (IfThen.at toy (fun _ n => 1 ≤ n) acc s n), Check.ifThen toy (fun _ n => 1 ≤ n) acc s n))
  IO.println (tline "only_if" fun s n => (decide (OnlyIf.at toy acc c3 s n), Check.onlyIf toy acc c3 s n))
  IO.println (tline "exactly_when" fun s n => (decide (ExactlyWhen.at toy acc c3 s n), Check.exactlyWhen toy acc c3 s n))
  IO.println (tline "rejected_unchanged" fun s n => (decide (RejectedUnchanged.at toy s n), Check.rejectedUnchanged toy s n))
  IO.println (tline "increases_by" fun s n => (decide (IncreasesBy.at toy m (fun _ n => n) s n), Check.increasesBy toy m (fun _ n => n) s n))
  IO.println (tline "decreases_by" fun s n => (decide (DecreasesBy.at toy m (fun _ n => n) s n), Check.decreasesBy toy m (fun _ n => n) s n))
  IO.println (tline "becomes" fun s n => (decide (Becomes.at toy m (fun s n => s + n) s n), Check.becomes toy m (fun s n => s + n) s n))
  IO.println (tline "result_is" fun s n => (decide (ResultIs.at toy (fun b => b) (fun _ n => decide (3 ≤ n)) s n),
                                            Check.resultIs toy (fun b => b) (fun _ n => decide (3 ≤ n)) s n))
  IO.println (tline "result_at_most" fun s n => (decide (ResultAtMost.at toy (fun b => if b then 1 else 0) (fun _ n => if 3 ≤ n then 1 else 0) s n),
                                                 Check.resultAtMost toy (fun b => if b then 1 else 0) (fun _ n => if 3 ≤ n then 1 else 0) s n))
  IO.println (tline "result_at_least" fun s n => (decide (ResultAtLeast.at toy (fun b => if b then 1 else 0) (fun _ n => if n = 1 then 1 else 0) s n),
                                                  Check.resultAtLeast toy (fun b => if b then 1 else 0) (fun _ n => if n = 1 then 1 else 0) s n))
  IO.println (tline "at_most" fun s n => (decide (AtMost.at toy m (fun s _ => s + 2) s n), Check.atMost toy m (fun s _ => s + 2) s n))
  IO.println (tline "at_least" fun s n => (decide (AtLeast.at toy m (fun s _ => s + 2) s n), Check.atLeast toy m (fun s _ => s + 2) s n))
  IO.println (tline "every_of" fun s n => (decide (EveryOf.at toy coll small s n), Check.everyOf toy coll small s n))
  IO.println (tline "none_of" fun s n => (decide (NoneOf.at toy coll (fun _ _ x => 2 ≤ x) s n), Check.noneOf toy coll (fun _ _ x => 2 ≤ x) s n))
  IO.println (tline "changes_only" fun s n => (decide (ChangesOnly.at toy (fun _ => List.range 3) (fun s k => s + k) (fun _ n => if 4 ≤ n then [0, 1, 2] else []) s n),
                                               Check.changesOnly toy (fun _ => List.range 3) (fun s k => s + k) (fun _ n => if 4 ≤ n then [0, 1, 2] else []) s n))
  IO.println (tline "rejected calls only: never_changes" fun s n => (decide (NeverChanges.at toy.rejected m s n), Check.neverChanges toy.rejected m s n))
  IO.println (tline "accepted calls only: never_changes" fun s n => (decide (NeverChanges.at toy.successful m s n), Check.neverChanges toy.successful m s n))

end ToyFT
