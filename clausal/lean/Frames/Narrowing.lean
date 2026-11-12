/-
FRAME LIBRARY, part 5: NARROWED CLAIMS THAT SAY NOTHING (plan node Q1).

"successful" / "rejected" narrow a claim to the calls that give an answer of that kind
(`Op.HoldsAt`, `Op.HoldsAt2`, Frames/Core.lean). Under a narrowing the frame's content has to hold only
of answers of the narrowed kind, so a content that FOLLOWS FROM THE NARROWING ITSELF holds of every
operation whatever: such a rule constrains no code. Example: "A successful <operation> never loses
acceptance when <variation>" is `Monotone op.successful v op.accepted`, and both calls are
assumed accepted before the frame says anything.

Every theorem below is of the form

    the calls are narrowed  →  what the narrowing settles about the frame's holes  →  the frame holds

with NO hypothesis about `op.run`: it holds for every possible operation of those types. The compiler
(clausal/clausal/narrowing.py) refuses a Rule clause exactly when one of the theorems named `Narrowed.*`
applies, and names the theorem in the refusal. What the narrowing settles about a domain word (the side
hypotheses `h`) is declared per operation in the Clausebook (`narrowing:`) and kernel-checked on every
run (lean/Run/Narrowing.lean); it is never trusted.

Core Lean only, like the rest of the library.
-/
import Frames.Frames

namespace Frames
variable {σ α ρ μ ν ι κ : Type}

/-- The answers a claim about `op` covers: every answer by default; under "successful" the accepted ones;
    under "rejected" the others. (Which CALLS are covered is `Op.HoldsAt`; this is its condition on the answer.) -/
@[reducible] def Op.covered (op : Op σ α ρ) (r : ρ) : Prop :=
  match op.calls with
  | .every    => True
  | .accepted => op.accepted r
  | .rejected => ¬ op.accepted r

/-- The claim is narrowed: it is about accepted calls only, or about rejected calls only. -/
@[reducible] def Op.narrowed (op : Op σ α ρ) : Prop := op.calls ≠ .every

namespace Narrowed

/-- "successful" narrows. -/
theorem narrowed_successful {op : Op σ α ρ} : op.successful.narrowed := fun h => Calls.noConfusion h
/-- "rejected" narrows. -/
theorem narrowed_rejected {op : Op σ α ρ} : op.rejected.narrowed := fun h => Calls.noConfusion h

/-! ## The two general facts: under a narrowing, a content that follows from the narrowing holds -/

/-- One call. -/
theorem holdsAt {op : Op σ α ρ} (hn : op.narrowed) {Q : σ → α → ρ → σ → Prop}
    (h : ∀ s a r s', op.covered r → Q s a r s') (s : σ) (a : α) : op.HoldsAt Q s a := by
  intro _
  unfold Op.narrowed at hn
  have h' := h s a
  unfold Op.covered at h'
  cases hc : op.calls with
  | every => exact absurd hc hn
  | accepted => rw [hc] at h'; exact fun r s' _ hr => h' r s' hr
  | rejected => rw [hc] at h'; exact fun r s' _ hr => h' r s' hr

/-- Two calls. -/
theorem holdsAt2 {op : Op σ α ρ} (hn : op.narrowed) {rel : Variation σ α} {Q : ρ → σ → ρ → σ → Prop}
    (h : ∀ r s' r₂ s₂', op.covered r → op.covered r₂ → Q r s' r₂ s₂') (s : σ) (a : α) (s₂ : σ) (a₂ : α) :
    op.HoldsAt2 rel Q s a s₂ a₂ := by
  intro _ _ _
  unfold Op.narrowed at hn
  unfold Op.covered at h
  cases hc : op.calls with
  | every => exact absurd hc hn
  | accepted => rw [hc] at h; exact fun r s' r₂ s₂' _ _ hr hr₂ => h r s' r₂ s₂' hr hr₂
  | rejected => rw [hc] at h; exact fun r s' r₂ s₂' _ _ hr hr₂ => h r s' r₂ s₂' hr hr₂

/-! ## One theorem per reason the compiler gives (the name is printed in the refusal) -/

/-- The narrowing covers no answer at all (an operation every answer of which is accepted has no rejected
    call, and the other way round): whatever is claimed of such calls holds. -/
theorem covers_no_call {op : Op σ α ρ} (hn : op.narrowed) (h : ∀ r, ¬ op.covered r)
    {Q : σ → α → ρ → σ → Prop} (s : σ) (a : α) : op.HoldsAt Q s a :=
  holdsAt hn (fun _ _ r _ hr => absurd hr (h r)) s a

/-- The same for a claim that compares two calls. -/
theorem covers_no_call2 {op : Op σ α ρ} (hn : op.narrowed) (h : ∀ r, ¬ op.covered r)
    {rel : Variation σ α} {Q : ρ → σ → ρ → σ → Prop} (s : σ) (a : α) (s₂ : σ) (a₂ : α) : op.HoldsAt2 rel Q s a s₂ a₂ :=
  holdsAt2 hn (fun r _ _ _ hr _ => absurd hr (h r)) s a s₂ a₂

/-- Frame 1. "A successful X always answers": only calls that answer are covered. -/
theorem alwaysAnswers {op : Op σ α ρ} (hn : op.narrowed) : AlwaysAnswers op :=
  holdsAt hn (fun _ _ _ _ _ => trivial)

/-- Frame 4. "A successful X is always accepted": every covered answer is in the class. -/
theorem always {op : Op σ α ρ} (hn : op.narrowed) {cls : AnswerClass ρ} (h : ∀ r, op.covered r → cls r) : Always op cls :=
  holdsAt hn (fun _ _ r _ hr => h r hr)

/-- Frame 4. "A successful X is never rejected": no covered answer is in the class. -/
theorem never {op : Op σ α ρ} (hn : op.narrowed) {cls : AnswerClass ρ} (h : ∀ r, op.covered r → ¬ cls r) : Never op cls :=
  holdsAt hn (fun _ _ r _ hr => h r hr)

/-- Frame 5. "A successful X is accepted whenever C": every covered answer is in the class, whatever C. -/
theorem ifThen {op : Op σ α ρ} (hn : op.narrowed) {C : Cond σ α} {cls : AnswerClass ρ} (h : ∀ r, op.covered r → cls r) :
    IfThen op C cls :=
  holdsAt hn (fun _ _ r _ hr _ => h r hr)

/-- Frame 6. "A rejected X is accepted only if C": no covered answer is in the class, whatever C. -/
theorem onlyIf {op : Op σ α ρ} (hn : op.narrowed) {cls : AnswerClass ρ} {C : Cond σ α} (h : ∀ r, op.covered r → ¬ cls r) :
    OnlyIf op cls C :=
  holdsAt hn (fun _ _ r _ hr hc => absurd hc (h r hr))

/-- Frame 12. "A successful X never loses acceptance when V": the second call is covered, so it is in the class. -/
theorem monotone_holds {op : Op σ α ρ} (hn : op.narrowed) {more : Variation σ α} {cls : AnswerClass ρ}
    (h : ∀ r, op.covered r → cls r) : Monotone op more cls :=
  holdsAt2 hn (fun _ _ r₂ _ _ hr₂ _ => h r₂ hr₂)

/-- Frame 12. "A successful X never loses that it is rejected when V": the first call is covered, so it is not in the
    class, and there is nothing to lose. -/
theorem monotone_fails {op : Op σ α ρ} (hn : op.narrowed) {more : Variation σ α} {cls : AnswerClass ρ}
    (h : ∀ r, op.covered r → ¬ cls r) : Monotone op more cls :=
  holdsAt2 hn (fun r _ _ _ hr _ hc => absurd hc (h r hr))

/-- Frame 14. "A successful X gives the same answer when V", where any two covered answers show the same view
    (a yes/no answer: every accepted answer is yes). -/
theorem independentOf {op : Op σ α ρ} (hn : op.narrowed) {differOnlyIn : Variation σ α} {view : ρ → σ → ν}
    (h : ∀ r s' r₂ s₂', op.covered r → op.covered r₂ → view r s' = view r₂ s₂') : IndependentOf op differOnlyIn view :=
  holdsAt2 hn h

/-- Frame 16, by the view: as frame 14. -/
theorem independentGiven_view {op : Op σ α ρ} (hn : op.narrowed) {differOnlyIn : Variation σ α} {cls : AnswerClass ρ}
    {view : ρ → σ → ν} (h : ∀ r s' r₂ s₂', op.covered r → op.covered r₂ → view r s' = view r₂ s₂') :
    IndependentGiven op differOnlyIn cls view :=
  holdsAt2 hn (fun r s' r₂ s₂' hr hr₂ _ => h r s' r₂ s₂' hr hr₂)

/-- Frame 16, by the condition: the first call is covered, so it is not in the class the condition asks for. -/
theorem independentGiven_fails {op : Op σ α ρ} (hn : op.narrowed) {differOnlyIn : Variation σ α} {cls : AnswerClass ρ}
    {view : ρ → σ → ν} (h : ∀ r, op.covered r → ¬ cls r) : IndependentGiven op differOnlyIn cls view :=
  holdsAt2 hn (fun r _ _ _ hr _ hc => absurd hc (h r hr))

end Narrowed

/-! ## The fixed tactics of lean/Run/Narrowing.lean

`narrowed_calls` shows that an operation's claim is narrowed; `narrow_side` proves a side hypothesis `h` of a theorem
above (what the narrowing settles about a class of answers, or about the answers themselves) for a concrete operation,
by unfolding its notion of acceptance. `vacuous_by_narrowing` tries to prove a whole claim, stated for an arbitrary
`run`, through the two general facts: it is run on every narrowed claim the compiler did NOT refuse, where it has to
fail. They are proof search, not part of what is trusted: what they prove the kernel has checked. -/

macro "narrowed_calls" : tactic => `(tactic| first
  | exact Frames.Narrowed.narrowed_successful
  | exact Frames.Narrowed.narrowed_rejected
  | (intro h; cases h))

macro "narrow_two" : tactic => `(tactic| (
  rename_i h hc
  first
    | exact hc h
    | exact h hc
    | exact absurd h hc
    | exact absurd hc h
    | exact h.trans hc.symm
    | (cases h; cases hc; done)
    | (cases hc; cases h; done)))

macro "narrow_pair" : tactic => `(tactic| (
  rename_i r _ r₂ _ h h₂
  first
    | exact h.trans h₂.symm
    | (cases r <;> cases r₂ <;> first
        | rfl
        | exact absurd rfl h
        | exact absurd rfl h₂
        | (refine absurd ?_ h; intro e; cases e; done)
        | (refine absurd ?_ h₂; intro e; cases e; done)
        | contradiction
        | (cases h; done)
        | (cases h₂; done))))

macro "narrow_one" : tactic => `(tactic| (
  rename_i h
  first
    | exact h trivial
    | exact absurd trivial h
    | (cases h; done)))

macro "narrow_close" : tactic => `(tactic| first
  | assumption
  | contradiction
  | trivial
  | narrow_one
  | narrow_two
  | narrow_pair
  | (simp_all; done))

macro "narrow_side" : tactic => `(tactic| first
  | (intros; narrow_close)
  | (intros; intro _; narrow_close))

macro "vacuous_by_narrowing" : tactic => `(tactic| (
  intro run
  first
    | (intro s a
       refine Frames.Narrowed.holdsAt (by narrowed_calls) ?_ s a
       intro _ _ _ _ _
       first
         | narrow_close
         | (intro _; narrow_close)
         | (intro _ _; narrow_close))
    | (intro s a s₂ a₂
       refine Frames.Narrowed.holdsAt2 (by narrowed_calls) ?_ s a s₂ a₂
       intro _ _ _ _ _ _
       first
         | narrow_close
         | (intro _; narrow_close)
         | (intro hc; clear hc; narrow_close))))

/-! ## The facts of the readability critique (docs/studies/2026-11-12/readability-critique.md, section 2.1)

Stated as they were there: about ANY `run` and any variation. They are instances of the theorems above. -/
namespace Narrowed.Critique

/-- `Monotone op.successful v op.accepted` holds for every operation and every variation. -/
theorem monotone_successful (op : Op σ α ρ) (v : Variation σ α) : Monotone op.successful v op.accepted :=
  monotone_holds narrowed_successful (fun _ h => h)

/-- The same for `op.rejected`: a rejected first call has no acceptance to lose. -/
theorem monotone_rejected (op : Op σ α ρ) (v : Variation σ α) : Monotone op.rejected v op.accepted :=
  monotone_fails narrowed_rejected (fun _ h => h)

/-- A yes/no answer whose acceptance is "yes": two accepted calls give the same answer, whatever `run` is. -/
theorem sameAnswer_successful (run : σ → α → Option (Bool × σ)) (v : Variation σ α) :
    IndependentOf ({ run := run, accepted := fun ans => ans = true } : Op σ α Bool).successful v (fun ans _ => ans) :=
  independentOf narrowed_successful (fun _ _ _ _ (h : _ = true) (h₂ : _ = true) => h.trans h₂.symm)

/-- ... and two rejected calls give the same answer. -/
theorem sameAnswer_rejected (run : σ → α → Option (Bool × σ)) (v : Variation σ α) :
    IndependentOf ({ run := run, accepted := fun ans => ans = true } : Op σ α Bool).rejected v (fun ans _ => ans) :=
  independentOf narrowed_rejected (fun r _ r₂ _ (h : ¬ r = true) (h₂ : ¬ r₂ = true) => by
    cases r <;> cases r₂ <;> first | rfl | exact absurd rfl h | exact absurd rfl h₂)

/-- An operation that never answers satisfies every claim about its rejected calls (here: "never changes M").
    NOT a reason for a refusal: it is about one operation, not about every operation. It is the reason the report
    flags a narrowed clause that covered no call on the grid. -/
theorem neverChanges_of_silent (op : Op σ α ρ) (m : Measure σ α μ) (h : ∀ s a, op.run s a = none) :
    NeverChanges op.rejected m := by
  intro s a _ r s' hr
  rw [show op.rejected.run s a = op.run s a from rfl, h s a] at hr
  exact absurd hr (by simp)

end Narrowed.Critique

end Frames
