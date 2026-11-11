/-
FRAME LIBRARY, part 4: facts about operations used by generated, kernel-checked glue proofs (a compiled
reading is equivalent to a flat statement; a Rule follows from its scenarios). Not definitions: nothing
here changes what any frame says.
-/
import Frames.Frames

namespace Frames
variable {σ α ρ : Type}

/-- One call gives at most one answer. -/
theorem Op.answer_unique {op : Op σ α ρ} {s : σ} {a : α} {r r₂ : ρ} {s' s₂' : σ}
    (e : op.run s a = some (r, s')) (e₂ : op.run s a = some (r₂, s₂')) : r = r₂ ∧ s' = s₂' := by
  rw [e] at e₂; cases e₂; exact ⟨rfl, rfl⟩

/-- A sequence answers exactly when both parts do, the second on the state the first left. -/
theorem Op.andThen_some {α₂ ρ₂ : Type} {first : Op σ α ρ} {second : Op σ α₂ ρ₂} {s : σ} {a : α × α₂}
    {r : ρ₂} {s' : σ} :
    (first.andThen second).run s a = some (r, s') ↔
      ∃ r₁ s₁, first.run s a.1 = some (r₁, s₁) ∧ second.run s₁ a.2 = some (r, s') := by
  show (match first.run s a.1 with | none => none | some (_, s₁) => second.run s₁ a.2) = some (r, s') ↔ _
  cases h : first.run s a.1 with
  | none => simp
  | some p =>
    obtain ⟨r₁, s₁⟩ := p
    constructor
    · intro e; exact ⟨r₁, s₁, rfl, e⟩
    · rintro ⟨_, _, e₁, e⟩; cases e₁; exact e

/-- An operation beside a bystander answers exactly when it does alone; the bystander is as it was. -/
theorem Op.beside_some {β : Type} {op : Op σ α ρ} {s : σ × β} {a : α} {r : ρ} {s' : σ × β} :
    (op.beside β).run s a = some (r, s') ↔ ∃ t, op.run s.1 a = some (r, t) ∧ s' = (t, s.2) := by
  show (match op.run s.1 a with | none => none | some (r, t) => some (r, (t, s.2))) = some (r, s') ↔ _
  cases h : op.run s.1 a with
  | none => simp
  | some p =>
    obtain ⟨r₁, t₁⟩ := p
    simp only [Option.some.injEq, Prod.mk.injEq]
    constructor
    · rintro ⟨rfl, rfl⟩; exact ⟨t₁, ⟨rfl, rfl⟩, rfl⟩
    · rintro ⟨t, ⟨rfl, rfl⟩, rfl⟩; exact ⟨rfl, rfl⟩

/-! ## What "if C then Q" says, beside its neighbours (kernel-checked, so the English of the frames can lean on it) -/

/-- Read with the default, "if C then Q" includes "the call gives an answer" for every input in scope,
    also where C does not hold. -/
theorem IfThen.alwaysAnswers {op : Op σ α ρ} {C : Cond σ α} {cls : AnswerClass ρ} (hc : op.calls = .every)
    (h : IfThen op C cls) : AlwaysAnswers op := by
  intro s a hs
  have h := h s a hs
  simp only [hc] at h ⊢
  obtain ⟨r, s', e, _⟩ := h
  exact ⟨r, s', e, trivial⟩

/-- "if C then Q" gives "always Q" on the operation narrowed to C (the weaker claim, which says nothing
    outside C). The converse fails: see `IfThen.alwaysAnswers`. -/
theorem IfThen.given {op : Op σ α ρ} {C : Cond σ α} {cls : AnswerClass ρ} (hc : op.calls = .every)
    (h : IfThen op C cls) : Always (op.given C) cls := by
  intro s a hs
  have h := h s a hs.1
  simp only [hc] at h ⊢
  obtain ⟨r, s', e, q⟩ := h
  exact ⟨r, s', e, q hs.2⟩

/-- The weaker claim plus "always answers" is "if C then Q". -/
theorem IfThen_of_given {op : Op σ α ρ} {C : Cond σ α} {cls : AnswerClass ρ} (hc : op.calls = .every)
    (ha : AlwaysAnswers op) (h : Always (op.given C) cls) : IfThen op C cls := by
  intro s a hs
  have ha := ha s a hs
  simp only [hc] at ha ⊢
  obtain ⟨r, s', e, _⟩ := ha
  refine ⟨r, s', e, fun c => ?_⟩
  have h := h s a ⟨hs, c⟩
  simp only [hc] at h
  obtain ⟨r₂, s₂, e₂, q⟩ := h
  have e₂ : op.run s a = some (r₂, s₂) := e₂
  rw [e] at e₂; cases e₂; exact q

/-- "Q exactly when C" is "if C then Q" and "Q only if C" together (frames 5 and 6), read with the default. -/
theorem ExactlyWhen_iff {op : Op σ α ρ} {cls : AnswerClass ρ} {C : Cond σ α} (hc : op.calls = .every) :
    ExactlyWhen op cls C ↔ IfThen op C cls ∧ OnlyIf op cls C := by
  constructor
  · intro h
    refine ⟨fun s a hs => ?_, fun s a hs => ?_⟩ <;>
    · have h := h s a hs
      simp only [hc] at h ⊢
      obtain ⟨r, s', e, q⟩ := h
      first | exact ⟨r, s', e, q.2⟩ | exact ⟨r, s', e, q.1⟩
  · rintro ⟨h₁, h₂⟩ s a hs
    have h₁ := h₁ s a hs
    have h₂ := h₂ s a hs
    simp only [hc] at h₁ h₂ ⊢
    obtain ⟨r, s', e, q₁⟩ := h₁
    obtain ⟨r₂, s₂, e₂, q₂⟩ := h₂
    rw [e] at e₂; cases e₂
    exact ⟨r, s', e, q₂, q₁⟩

end Frames
