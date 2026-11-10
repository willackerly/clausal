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

end Frames
