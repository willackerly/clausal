/-
Reviewer's probe (V2/V3 frame library review, second pass). Core Lean + the frame library only.
Run from a scratch copy: `cd rv/lean && lake env lean ../../rv_tools/ReviewProbeV2.lean`.
Each theorem is a claim made in the review; the kernel checks it.
-/
import Frames.Frames
open Frames

namespace ReviewV2

/-! ## 1. The default (D1, D2) as the definitions say it -/

/-- "never changes M", read with the default, includes "the call gives an answer" for every input in scope. -/
theorem neverChanges_answers {σ α ρ μ : Type} (op : Op σ α ρ) (m : Measure σ α μ) (h : op.calls = .every)
    (hn : NeverChanges op m) : ∀ s a, op.scope s a → ∃ r s', op.run s a = some (r, s') := by
  intro s a hs
  have := hn s a hs
  simp only [h] at this
  obtain ⟨r, s', e, _⟩ := this
  exact ⟨r, s', e⟩

/-- ...and it covers a call that is REJECTED: the measure is unchanged on it too. -/
theorem neverChanges_covers_rejected {σ α ρ μ : Type} (op : Op σ α ρ) (m : Measure σ α μ) (h : op.calls = .every)
    (hn : NeverChanges op m) (s : σ) (a : α) (hs : op.scope s a) (r : ρ) (s' : σ)
    (e : op.run s a = some (r, s')) (_hrej : ¬ op.accepted r) : m s' a = m s a := by
  have := hn s a hs
  simp only [h] at this
  obtain ⟨r₁, s₁, e₁, q⟩ := this
  rw [e] at e₁; cases e₁; exact q

/-! ## 2. "if-then" does NOT include "the call gives an answer" outside its condition

A toy operation that gives no answer at input 0 and accepts every other input. The compiled reading of
"<op> is accepted whenever <C>" (`IfThen`) holds of it, but the echo printed for that rule says
"assuming nothing: every state and every input / then the call gives an answer [default D1]", which is false of it. -/

def toy : Op Unit Nat Bool where
  run _ n := if n = 0 then none else some (true, ())
  accepted b := b = true

theorem toy_ifThen : IfThen toy (fun _ n => n ≠ 0) (fun b => toy.accepted b) := by
  intro s a ⟨_, ha⟩
  show ∃ r s', toy.run s a = some (r, s') ∧ toy.accepted r
  exact ⟨true, (), by simp [toy, ha], rfl⟩

theorem toy_not_alwaysAnswers : ¬ AlwaysAnswers toy := by
  intro h
  obtain ⟨r, s', e, _⟩ := h () 0 trivial
  simp [toy] at e

/-- So the echo's reading (D1 for every input, plus the if-then) is strictly stronger than the Lean. -/
theorem echo_of_ifThen_is_stronger :
    IfThen toy (fun _ n => n ≠ 0) (fun b => toy.accepted b) ∧
      ¬ (AlwaysAnswers toy ∧ IfThen toy (fun _ n => n ≠ 0) (fun b => toy.accepted b)) :=
  ⟨toy_ifThen, fun h => toy_not_alwaysAnswers h.1⟩

/-- The fail-closed alternative: the same claim written as one HoldsAt with the condition inside. -/
def IfThenStrict {σ α ρ : Type} (op : Op σ α ρ) (C : Cond σ α) (cls : AnswerClass ρ) : Prop :=
  ∀ s a, op.HoldsAt (fun s a r _ => C s a → cls r) s a

theorem toy_not_ifThenStrict : ¬ IfThenStrict toy (fun _ n => n ≠ 0) (fun b => toy.accepted b) := by
  intro h
  obtain ⟨r, s', e, _⟩ := h () 0 trivial
  simp [toy] at e

/-! ## 3. A "rejected" clause about an operation that never rejects covers no call (vacuous) -/

def neverRejects : Op Nat Nat Nat where
  run s n := some (n, s + n)       -- changes the state
  accepted _ := True               -- like `L.counted`: every answer is an acceptance

theorem rejected_clause_vacuous (m : Measure Nat Nat Nat) : NeverChanges neverRejects.rejected m := by
  intro s a _ r s' _ hrej
  exact absurd trivial hrej

/-! ## 4. Typed holes: polymorphic hole types let ONE frame state any property of (input, answer, state after)

`EveryOf` with the answer itself as the "collection" is `Op.Holds` for an arbitrary predicate that does not mention
the state before. Nothing in the Lean types stops this; what stops it is that no vocabulary piece produces such a
collection or item condition (and those pieces are human-signed: today 0 of 87 are). -/
theorem everyOf_is_general {σ α ρ : Type} (op : Op σ α ρ) (R : α → ρ → σ → Prop) :
    EveryOf op (fun _ _ r => [r]) (fun s' a r => R a r s') ↔ op.Holds (fun _ a r s' => R a r s') := by
  simp [EveryOf, EveryOf.at, Op.Holds]

end ReviewV2

#print axioms ReviewV2.echo_of_ifThen_is_stronger
#print axioms ReviewV2.rejected_clause_vacuous
#print axioms ReviewV2.everyOf_is_general
#print axioms ReviewV2.neverChanges_covers_rejected
