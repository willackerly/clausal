/-
HAND-WRITTEN (not generated). EVERY frame of lean/Frames on a TOY operation, so that the comparison of each
frame's DEFINITION (`decide (F.at ...)`) with its executable reading (`Frames.Check.F ...`) has something
to catch. Added after the review of the frame library (2026-11-10), from the reviewer's
review/frames/rv_tools/ToyFrameTests.lean; the four frames with no surface form were added here.

Why it is needed: on the wallet and the ledger the definition of a frame is false at very few evaluations
and no call in scope ever gives no answer, so a checker that is wrong only where a claim FAILS, or only
on a SILENT call, passes the fixture comparison (4 of the reviewer's 7 deliberately broken checkers did).

The toy operation (core Lean only; nothing here knows about wallets, ledgers or Aeneas):

  input 0        gives NO answer
  input 1        is REJECTED, state unchanged
  input 2, 3, …  is ACCEPTED, the state grows by the input

Every frame is stated of it with a claim that is true at some points and false at others.

Run once per pipeline run with `lake env lean Run/FrameToyTests.lean` (it imports the frame library only).
One line per test, in the format of Run/FrameTests.lean plus one column:
  FTEST <frame id> <what> <evaluations> <on which the two readings agree> <on which the claim is false> <on which the call (or one of two calls) gives no answer>
A disagreement is an error of the run; the report also says, per frame, whether any comparison of this run
saw a false claim and a silent call (`comparison untested for <frame>` otherwise).

Plan node L2 added frame 17 (`each_at_most`) to the frames above, and a second block for the two new MODIFIERS
(`equals`, `tied`), which have no checker in Frames/Check.lean: each is compared here with a second reading
written as a program, through a frame it is used in.
-/
import Frames.Check
open Frames

namespace ToyFT

@[reducible] def toy : Op Nat Nat Bool where
  run s n := if n = 0 then none else if n = 1 then some (false, s) else some (true, s + n)
  accepted b := b = true
instance : DecidablePred toy.accepted := fun b => inferInstanceAs (Decidable (b = true))
instance (s a : Nat) : Decidable (toy.scope s a) := inferInstanceAs (Decidable True)

def silent (n : Nat) : Bool := (toy.run 0 n).isNone

def pts : List (Nat × Nat) := (List.range 4).flatMap fun s => (List.range 5).map fun n => (s, n)
/-- two runs from the same state: (state, first input, second input) -/
def pts2 : List (Nat × Nat × Nat) :=
  (List.range 2).flatMap fun s => (List.range 5).flatMap fun n => (List.range 5).map fun n₂ => (s, n, n₂)
/-- two runs with the same input: (first state, second state, input) -/
def pts2s : List (Nat × Nat × Nat) :=
  (List.range 3).flatMap fun s => (List.range 3).flatMap fun s₂ => (List.range 5).map fun n => (s, s₂, n)

def what := "toy operation (no answer at 0, rejected at 1, accepted from 2)"

def out (frame note : String) (rs : List (Bool × Bool)) (nSilent : Nat) : String :=
  s!"FTEST\t{frame}\t{what}{note}\t{rs.length}\t{(rs.filter fun p => p.1 == p.2).length}\t{(rs.filter fun p => !p.1).length}\t{nSilent}"

def tline (frame : String) (f : Nat → Nat → Bool × Bool) (note : String := "") : String :=
  out frame note (pts.map fun (s, n) => f s n) (pts.filter fun (_, n) => silent n).length

def tline2 (frame : String) (f : Nat → Nat → Nat → Bool × Bool) (note : String := "") : String :=
  out frame note (pts2.map fun (s, n, n₂) => f s n n₂) (pts2.filter fun (_, n, n₂) => silent n || silent n₂).length

def tline2s (frame : String) (f : Nat → Nat → Nat → Bool × Bool) (note : String := "") : String :=
  out frame note (pts2s.map fun (s, s₂, n) => f s s₂ n) (pts2s.filter fun (_, _, n) => silent n).length

@[reducible] def m : Measure Nat Nat Nat := fun s _ => s
@[reducible] def acc : AnswerClass Bool := fun b => toy.accepted b
@[reducible] def c1 : Cond Nat Nat := fun _ n => 1 ≤ n
@[reducible] def c3 : Cond Nat Nat := fun _ n => 3 ≤ n
@[reducible] def coll : Coll Nat Nat Bool Nat := fun _ n _ => List.range n
@[reducible] def small : ItemCond Nat Nat Nat := fun _ _ x => x < 2
/-- "the second input is not larger" (for monotone: a smaller input never loses acceptance; false, 1 is rejected) -/
@[reducible] def notLarger : Variation Nat Nat := fun s a s₂ a₂ => s₂ = s ∧ a₂ ≤ a
/-- "the two calls differ only in the state" (for independent-of) -/
@[reducible] def sameInput : Variation Nat Nat := fun _ a _ a₂ => a₂ = a

#eval show IO Unit from do
  IO.println (tline "always_answers" fun s n => (decide (AlwaysAnswers.at toy s n), Check.alwaysAnswers toy s n))
  IO.println (tline "never_changes" fun s n => (decide (NeverChanges.at toy m s n), Check.neverChanges toy m s n))
  IO.println (tline "always" fun s n => (decide (Always.at toy acc s n), Check.always toy acc s n))
  IO.println (tline "never" fun s n => (decide (Never.at toy acc s n), Check.never toy acc s n))
  IO.println (tline "if_then" fun s n => (decide (IfThen.at toy c1 acc s n), Check.ifThen toy c1 acc s n))
  IO.println (tline "if_then" (note := "; a condition that is false at the silent input") fun s n =>
    (decide (IfThen.at toy c3 acc s n), Check.ifThen toy c3 acc s n))
  IO.println (tline "only_if" fun s n => (decide (OnlyIf.at toy acc c3 s n), Check.onlyIf toy acc c3 s n))
  IO.println (tline "exactly_when" fun s n => (decide (ExactlyWhen.at toy acc c3 s n), Check.exactlyWhen toy acc c3 s n))
  IO.println (tline "exactly_when" (note := "; a condition that holds of the rejected input") fun s n =>
    (decide (ExactlyWhen.at toy acc c1 s n), Check.exactlyWhen toy acc c1 s n))
  IO.println (tline "rejected_unchanged" fun s n => (decide (RejectedUnchanged.at toy s n), Check.rejectedUnchanged toy s n))
  IO.println (tline "increases_by" fun s n => (decide (IncreasesBy.at toy m (fun _ n => n) s n), Check.increasesBy toy m (fun _ n => n) s n))
  IO.println (tline "decreases_by" (note := "; by the input (never true; at state 0, input 1 a truncated subtraction would say true)") fun s n =>
    (decide (DecreasesBy.at toy m (fun _ n => n) s n), Check.decreasesBy toy m (fun _ n => n) s n))
  IO.println (tline "decreases_by" fun s n => (decide (DecreasesBy.at toy m (fun _ n => if n = 1 then 0 else n) s n),
                                               Check.decreasesBy toy m (fun _ n => if n = 1 then 0 else n) s n))
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
  -- the two weakenings: silent calls and calls of the other kind are outside the claim
  IO.println (tline "never_changes" (note := "; REJECTED calls only") fun s n =>
    (decide (NeverChanges.at toy.rejected m s n), Check.neverChanges toy.rejected m s n))
  IO.println (tline "never_changes" (note := "; ACCEPTED calls only") fun s n =>
    (decide (NeverChanges.at toy.successful m s n), Check.neverChanges toy.successful m s n))
  IO.println (tline "always" (note := "; REJECTED calls only") fun s n =>
    (decide (Always.at toy.rejected acc s n), Check.always toy.rejected acc s n))
  -- a Given: the scope narrowed to inputs from 1 on (the silent input is then outside the claim)
  IO.println (tline "always" (note := "; narrowed to inputs from 1 on") fun s n =>
    (decide (Always.at (toy.given c1) acc s n), Check.always (toy.given c1) acc s n))
  -- the frames with no surface form
  IO.println (tline "count_of" (note := "; exactly 2") fun s n =>
    (decide (CountOf.at toy coll small .exactly (fun _ _ => 2) s n), Check.countOf toy coll small .exactly (fun _ _ => 2) s n))
  IO.println (tline "count_of" (note := "; at most 1") fun s n =>
    (decide (CountOf.at toy coll small .atMost (fun _ _ => 1) s n), Check.countOf toy coll small .atMost (fun _ _ => 1) s n))
  IO.println (tline "count_of" (note := "; at least 2") fun s n =>
    (decide (CountOf.at toy coll small .atLeast (fun _ _ => 2) s n), Check.countOf toy coll small .atLeast (fun _ _ => 2) s n))
  IO.println (tline "agrees_with" fun s n =>
    (decide (AgreesWith.at toy (fun s n => (decide (2 ≤ n), s + n)) s n), Check.agreesWith toy (fun s n => (decide (2 ≤ n), s + n)) s n))
  IO.println (tline2 "monotone" (note := "; a smaller input never loses acceptance") fun s n n₂ =>
    (decide (Monotone.at toy notLarger acc s n s n₂), Check.monotone toy notLarger acc s n s n₂))
  IO.println (tline2 "monotone" (note := "; the same of ACCEPTED calls only") fun s n n₂ =>
    (decide (Monotone.at toy.successful notLarger acc s n s n₂), Check.monotone toy.successful notLarger acc s n s n₂))
  IO.println (tline2 "monotone" (note := "; a smaller input never loses rejection, REJECTED calls only") fun s n n₂ =>
    (decide (Monotone.at toy.rejected notLarger (fun b => ¬ acc b) s n s n₂), Check.monotone toy.rejected notLarger (fun b => ¬ acc b) s n s n₂))
  IO.println (tline2s "same_answer" (note := "; the answer is independent of the state") fun s s₂ n =>
    (decide (IndependentOf.at toy sameInput (fun r _ => r) s n s₂ n), Check.independentOf toy sameInput (fun r _ => r) s n s₂ n))
  IO.println (tline2s "same_answer" (note := "; the same definition (Frames.IndependentOf) with another view: the state afterwards is independent of the state") fun s s₂ n =>
    (decide (IndependentOf.at toy sameInput (fun _ s' => s') s n s₂ n), Check.independentOf toy sameInput (fun _ s' => s') s n s₂ n))
  -- frames 15 and 16 (added with their sentence forms)
  IO.println (tline "within" (note := "; every number below the input is below 2 + the old state") fun s n =>
    (decide (Within.at toy coll (fun s _ => List.range (s + 2)) s n), Check.within toy coll (fun s _ => List.range (s + 2)) s n))
  IO.println (tline "covers" (note := "; every number below 3 is below the input") fun s n =>
    (decide (Covers.at toy coll (fun _ _ => List.range 3) s n), Check.covers toy coll (fun _ _ => List.range 3) s n))
  IO.println (tline2 "same_answer_if" (note := "; if the first call is accepted, a smaller input gives the same answer") fun s n n₂ =>
    (decide (IndependentGiven.at toy notLarger acc (fun r _ => r) s n s n₂), Check.independentGiven toy notLarger acc (fun r _ => r) s n s n₂))
  IO.println (tline2 "same_answer_if" (note := "; if the first call is rejected, a smaller input gives the same answer") fun s n n₂ =>
    (decide (IndependentGiven.at toy notLarger (fun b => ¬ acc b) (fun r _ => r) s n s n₂),
     Check.independentGiven toy notLarger (fun b => ¬ acc b) (fun r _ => r) s n s n₂))

  -- frame 17 (plan node L2): a bound on every number of a collection of the state, read after the call
  IO.println (tline "each_at_most" (note := "; each of the numbers [state, 2] is at most 3 afterwards") fun s n =>
    (decide (EachAtMost.at toy (fun s _ => [s, 2]) (fun _ _ => 3) s n), Check.eachAtMost toy (fun s _ => [s, 2]) (fun _ _ => 3) s n))
  IO.println (tline "each_at_most" (note := "; an EMPTY collection (the call must still answer)") fun s n =>
    (decide (EachAtMost.at toy (fun _ _ => []) (fun _ _ => 0) s n), Check.eachAtMost toy (fun _ _ => []) (fun _ _ => 0) s n))
  IO.println (tline "each_at_most" (note := "; REJECTED calls only, a bound that is the state before") fun s n =>
    (decide (EachAtMost.at toy.rejected (fun s a => [s, a]) (fun s _ => s) s n), Check.eachAtMost toy.rejected (fun s a => [s, a]) (fun s _ => s) s n))

/-! ## The two modifiers of plan node L2, each against a second reading written as a program

Neither is a frame, so neither has a checker in Frames/Check.lean. Each is given one here, in the other style
("run it, then case on what was seen"), and compared with the definition through a frame it is used in. The
lines are reported under the modifier's own id. -/

/-- `equals` (a comparison of two values known before the call), as a scope: the claim is about the calls at which the
    two values are the same. Second reading: test the two values with `==`, then run the call. -/
def equalsScope (a b : Term Nat Nat Nat) (s n : Nat) : Bool × Bool :=
  (decide (Always.at (toy.given fun s n => a s n = b s n) acc s n),
   if a s n == b s n then (match toy.run s n with | none => false | some (r, _) => r) else true)

/-- `tied` (a sequence whose second input is got from the first). Second reading: run the first call; if it answers,
    run the second on the state it left with the tied input; the claim is about that last answer and state. -/
def tiedRun (tie : Nat → Nat) (s n : Nat) (test : Bool → Nat → Bool) : Bool :=
  match toy.run s n with
  | none => false
  | some (_, s₁) =>
    match toy.run s₁ (tie n) with
    | none => false
    | some (r, s') => test r s'

def tiedSilent (tie : Nat → Nat) : Nat := (pts.filter fun (_, n) => silent n || silent (tie n)).length

#eval show IO Unit from do
  IO.println (tline "equals" (note := "; as a scope: calls at which the input equals the state are accepted") (equalsScope (fun _ n => n) (fun s _ => s)))
  IO.println (tline "equals" (note := "; negated, as a scope: calls at which the input differs from the state are accepted") fun s n =>
    (decide (Always.at (toy.given fun s n => ¬ (n = s)) acc s n),
     if n == s then true else (match toy.run s n with | none => false | some (r, _) => r)))
  IO.println (out "tied" "; the same input again: the sequence is accepted"
    (pts.map fun (s, n) => (decide (Always.at ((toy.andThen toy).tied Frames.sameInput) acc s n), tiedRun (fun n => n) s n fun r _ => r))
    (tiedSilent fun n => n))
  IO.println (out "tied" "; the same input again: the state grows by twice the input"
    (pts.map fun (s, n) => (decide (Becomes.at ((toy.andThen toy).tied Frames.sameInput) m (fun s n => s + 2 * n) s n),
                            tiedRun (fun n => n) s n fun _ s' => s' == s + 2 * n))
    (tiedSilent fun n => n))
  IO.println (out "tied" "; another tie (4 minus the input): the sequence leaves the state grown by 4"
    (pts.map fun (s, n) => (decide (Becomes.at ((toy.andThen toy).tied fun n => 4 - n) m (fun s _ => s + 4) s n),
                            tiedRun (fun n => 4 - n) s n fun _ s' => s' == s + 4))
    (tiedSilent fun n => 4 - n))
  IO.println (out "tied" "; the same input again, ACCEPTED sequences only: the state grows by 4"
    (pts.map fun (s, n) => (decide (Becomes.at ((toy.andThen toy).tied Frames.sameInput).successful m (fun s _ => s + 4) s n),
                            match toy.run s n with
                            | none => true
                            | some (_, s₁) => match toy.run s₁ n with
                              | none => true
                              | some (r, s') => if r then s' == s + 4 else true))
    (tiedSilent fun n => n))

end ToyFT
