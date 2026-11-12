/-
FRAME LIBRARY, part 1: the abstract operation, the pieces a frame's holes are filled with, and the
modifiers. PROJECT-INDEPENDENT: nothing here knows about any project's operations or words, Rust or Aeneas, and the
library imports nothing but Lean's core, so it can be lifted into a package of its own.

An OPERATION is one call of some code: it starts from a state and an input, and either gives an
ANSWER (a returned value and the state afterwards) or gives none (it panics, aborts or never returns).
Which answers count as ACCEPTED is part of the operation; every other answer is a REJECTION.

A frame (Frames/Frames.lean) is a statement shape about an operation. Its holes are TYPED:

  Measure σ α μ    a quantity of the state (it may name parts by the input)   σ → α → μ
  Answer ρ μ       a quantity of the returned value                 ρ → μ
  Term σ α μ       a value known before the call                    σ → α → μ
  Cond σ α         a condition on the state before and the input    σ → α → Prop
  AnswerClass ρ    a class of returned values                       ρ → Prop
  Coll σ α ρ ι     a named collection, read after the call          σ → α → ρ → List ι
  ItemCond σ α ι   a condition on one item of a collection          σ → α → ι → Prop
  Variation σ α    a relation between two (state, input) pairs      σ → α → σ → α → Prop
  Nums σ α         a collection of numbers of the state             σ → α → List Nat

NO frame has a hole of type `σ → α → ρ → σ → Prop` (an arbitrary relation between before and after).
That type appears only in `Op.HoldsAt` below, the one place where the fail-closed defaults are written
down; `HoldsAt` is not a frame and generated statements may not mention it (the audit checks).
-/

namespace Frames

/-- Which calls a claim is about. `every` is the default and the strict one. -/
inductive Calls where
  /-- every call in scope, accepted or rejected; and every such call must give an answer -/
  | every
  /-- only calls that give an answer that is accepted (asked for with "successful") -/
  | accepted
  /-- only calls that give an answer that is a rejection (asked for with "rejected") -/
  | rejected
  deriving DecidableEq, Repr

/-- One operation: what a call does, which answers are acceptances, and which calls a claim covers. -/
structure Op (σ α ρ : Type) where
  /-- one call from state `s` with input `a`: `some (r, s')` = it answers `r` and leaves `s'`;
      `none` = it gives no answer -/
  run : σ → α → Option (ρ × σ)
  /-- the answers that count as accepted; every other answer is a rejection -/
  accepted : ρ → Prop
  /-- the inputs a claim is about. Everything, unless a Given or a scoping modifier narrows it. -/
  scope : σ → α → Prop := fun _ _ => True
  /-- the calls a claim is about. Every call, unless "successful" / "rejected" narrows it. -/
  calls : Calls := .every

abbrev Measure (σ α μ : Type) := σ → α → μ
abbrev Answer (ρ μ : Type) := ρ → μ
abbrev Term (σ α μ : Type) := σ → α → μ
abbrev Cond (σ α : Type) := σ → α → Prop
abbrev AnswerClass (ρ : Type) := ρ → Prop
abbrev Coll (σ α ρ ι : Type) := σ → α → ρ → List ι
abbrev ItemCond (σ α ι : Type) := σ → α → ι → Prop
abbrev Variation (σ α : Type) := σ → α → σ → α → Prop
abbrev Nums (σ α : Type) := σ → α → List Nat

variable {σ α ρ μ ι β : Type}

/-! ## The one place the defaults live

`HoldsAt op Q s a`: what a frame with pointwise content `Q` says about the single call `(s, a)`.

* outside the scope: nothing;
* `calls = every` (the default): the call gives an answer AND `Q` holds of it. So every frame, read
  with the default, includes "always answers", and covers rejected calls as well as accepted ones;
* `calls = accepted` / `rejected`: IF the call gives an answer of that kind, `Q` holds of it. Calls that
  give the other kind of answer, or no answer, are not covered. -/
def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop :=
  op.scope s a →
    match op.calls with
    | .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s'
    | .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s'
    | .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'

/-- The same for every state and every input. -/
def Op.Holds (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) : Prop := ∀ s a, op.HoldsAt Q s a

/-- Two calls at once (frames 12 and 14 compare two runs). Both must be in scope; with the default
    both must answer. -/
def Op.HoldsAt2 (op : Op σ α ρ) (rel : Variation σ α) (Q : ρ → σ → ρ → σ → Prop)
    (s : σ) (a : α) (s₂ : σ) (a₂ : α) : Prop :=
  op.scope s a → op.scope s₂ a₂ → rel s a s₂ a₂ →
    match op.calls with
    | .every    => ∃ r s' r₂ s₂', op.run s a = some (r, s') ∧ op.run s₂ a₂ = some (r₂, s₂') ∧ Q r s' r₂ s₂'
    | .accepted => ∀ r s' r₂ s₂', op.run s a = some (r, s') → op.run s₂ a₂ = some (r₂, s₂') →
                     op.accepted r → op.accepted r₂ → Q r s' r₂ s₂'
    | .rejected => ∀ r s' r₂ s₂', op.run s a = some (r, s') → op.run s₂ a₂ = some (r₂, s₂') →
                     ¬ op.accepted r → ¬ op.accepted r₂ → Q r s' r₂ s₂'

/-! ## Modifiers on operations (operation → operation) -/

/-- "given C" / a Gherkin `Given`: narrow the scope to inputs satisfying `C`. -/
@[reducible] def Op.given (op : Op σ α ρ) (C : Cond σ α) : Op σ α ρ :=
  { op with scope := fun s a => op.scope s a ∧ C s a }

/-- "successful": the claim is about accepted calls only. NOT fail-closed; has to be asked for. -/
@[reducible] def Op.successful (op : Op σ α ρ) : Op σ α ρ := { op with calls := .accepted }

/-- "rejected": the claim is about rejected calls only. NOT fail-closed; has to be asked for. -/
@[reducible] def Op.rejected (op : Op σ α ρ) : Op σ α ρ := { op with calls := .rejected }

/-- "internal" / "between two members": every party the input names is a member of the state. -/
@[reducible] def Op.internal (op : Op σ α ρ) (member : σ → ι → Prop) (parties : α → List ι) : Op σ α ρ :=
  op.given (fun s a => ∀ p ∈ parties a, member s p)

/-- "A, then B": run `first`, then `second` on the state `first` left. The answer is `second`'s; no
    answer if either gives none. Scoping modifiers apply to the sequence, not to its parts. -/
@[reducible] def Op.andThen {α₂ ρ₂ : Type} (first : Op σ α ρ) (second : Op σ α₂ ρ₂) : Op σ (α × α₂) ρ₂ where
  run s a := match first.run s a.1 with
    | none => none
    | some (_, s₁) => second.run s₁ a.2
  accepted := second.accepted

/-- "A, then B, with <tie>": the input of the second call of a sequence is GOT FROM the input of the first by
    `tie`, so the sequence has ONE input and no call of it is outside the claim for want of a matching pair
    ("the same input": `tie` is the identity). It is said of a sequence (`Op.andThen`), and the scope, the
    accepted answers and the calls covered are the sequence's own. -/
@[reducible] def Op.tied {α₂ : Type} (op : Op σ (α × α₂) ρ) (tie : α → α₂) : Op σ α ρ where
  run s a := op.run s (a, tie a)
  accepted := op.accepted
  scope s a := op.scope s (a, tie a)
  calls := op.calls

/-- "the same input": the tie under which the second call is given the first call's input again. -/
@[reducible] def sameInput : α → α := fun a => a

/-- A bystander: something that exists beside the operation and is not passed to it. It is unchanged
    by construction, so any claim that it is unchanged says nothing about the code. -/
@[reducible] def Op.beside (op : Op σ α ρ) (β : Type) : Op (σ × β) α ρ where
  run s a := match op.run s.1 a with
    | none => none
    | some (r, s') => some (r, (s', s.2))
  accepted := op.accepted
  scope s a := op.scope s.1 a
  calls := op.calls

/-! ## Modifiers on measures and conditions -/

/-- "aggregate" / "the total of": the sum of a collection of numbers (a per-item measure taken over
    every item of the state). -/
@[reducible] def aggregate (xs : List Nat) : Nat := xs.sum

/-- "every X of XS is P" (as a condition, before the call). -/
@[reducible] def every (items : List ι) (P : ι → Prop) : Prop := ∀ x ∈ items, P x

/-- "no X of XS is P" (as a condition, before the call). -/
@[reducible] def noneOf (items : List ι) (P : ι → Prop) : Prop := ∀ x ∈ items, ¬ P x

/-- "some X of XS is P" (as a condition, before the call): at least one item is P. -/
@[reducible] def someOf (items : List ι) (P : ι → Prop) : Prop := ∃ x ∈ items, P x

/-- "the first X of XS is P": there is a first item and it is P. -/
@[reducible] def theFirst (items : List ι) (P : ι → Prop) : Prop := items ≠ [] ∧ ∀ x ∈ items.head?, P x

end Frames
