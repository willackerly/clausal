/-
FRAME LIBRARY, part 3: the second reading of every frame.

Each frame of Frames/Frames.lean is written here AGAIN, as a program: `Check.<frame> op holes s a : Bool`
runs the call and looks at what came back. The two readings are written in different styles on purpose
(a logical formula there; "run it, then case on what was seen" here) and are compared with each other on
generated inputs for the concrete operations of a project (FRET's practice of giving every template two
semantics and testing one against the other). The comparison evaluates the DEFINITION through the
`Decidable` instance at the end of this file, which is correct by construction (an instance carries a
proof), so a disagreement always means the checker and the definition say different things.
-/
import Frames.Frames

namespace Frames
variable {σ α ρ μ ν ι κ : Type}

/-- What one call showed, as a plain value. -/
inductive Seen (ρ σ : Type) where
  | outOfScope                    -- the claim is not about this input
  | noAnswer                      -- in scope, and the call gave no answer
  | notCovered                    -- it answered, but the claim is about the other kind of answer
  | answered (r : ρ) (s' : σ)     -- an answer the claim is about

/-- Run the call once and classify it. -/
def Op.observe (op : Op σ α ρ) [∀ s a, Decidable (op.scope s a)] [DecidablePred op.accepted]
    (s : σ) (a : α) : Seen ρ σ :=
  if op.scope s a then
    match op.run s a with
    | none => .noAnswer
    | some (r, s') =>
      match op.calls with
      | .every => .answered r s'
      | .accepted => if op.accepted r then .answered r s' else .notCovered
      | .rejected => if op.accepted r then .notCovered else .answered r s'
  else .outOfScope

/-- A call that gives no answer breaks a claim about every call (the default), and is outside a claim
    about accepted or rejected calls only. -/
def Op.silenceAllowed (op : Op σ α ρ) : Bool :=
  match op.calls with
  | .every => false
  | _ => true

namespace Check
variable (op : Op σ α ρ) [∀ s a, Decidable (op.scope s a)] [DecidablePred op.accepted]

/-- The shape every single-run checker has: `true` where the claim does not apply, the stated value for a
    silent call, and `test` on an answer. -/
@[inline] def on (s : σ) (a : α) (test : ρ → σ → Bool) : Bool :=
  match op.observe s a with
  | .outOfScope => true
  | .notCovered => true
  | .noAnswer => op.silenceAllowed
  | .answered r s' => test r s'

def alwaysAnswers (s : σ) (a : α) : Bool := on op s a fun _ _ => true

def neverChanges [DecidableEq μ] (m : Measure σ α μ) (s : σ) (a : α) : Bool :=
  on op s a fun _ s' => m s' a == m s a

def changesOnly [DecidableEq κ] [DecidableEq μ] (parts : σ → List κ) (m : σ → κ → μ) (X : Term σ α (List κ))
    (s : σ) (a : α) : Bool :=
  on op s a fun _ s' =>
    parts s' == parts s && (parts s).all fun k => (X s a).contains k || m s' k == m s k

def always (cls : AnswerClass ρ) [DecidablePred cls] (s : σ) (a : α) : Bool :=
  on op s a fun r _ => decide (cls r)

def never (cls : AnswerClass ρ) [DecidablePred cls] (s : σ) (a : α) : Bool :=
  on op s a fun r _ => !decide (cls r)

def ifThen (C : Cond σ α) [∀ s a, Decidable (C s a)] (cls : AnswerClass ρ) [DecidablePred cls]
    (s : σ) (a : α) : Bool :=
  on op s a fun r _ => if C s a then decide (cls r) else true

def onlyIf (cls : AnswerClass ρ) [DecidablePred cls] (C : Cond σ α) [∀ s a, Decidable (C s a)]
    (s : σ) (a : α) : Bool :=
  on op s a fun r _ => if cls r then decide (C s a) else true

def exactlyWhen (cls : AnswerClass ρ) [DecidablePred cls] (C : Cond σ α) [∀ s a, Decidable (C s a)]
    (s : σ) (a : α) : Bool :=
  on op s a fun r _ => decide (cls r) == decide (C s a)

def rejectedUnchanged [DecidableEq σ] (s : σ) (a : α) : Bool :=
  on op s a fun r s' => !decide (op.accepted r) && s' == s

def increasesBy (m : Measure σ α Nat) (f : Term σ α Nat) (s : σ) (a : α) : Bool :=
  on op s a fun _ s' => m s' a == m s a + f s a

def decreasesBy (m : Measure σ α Nat) (f : Term σ α Nat) (s : σ) (a : α) : Bool :=
  on op s a fun _ s' => f s a ≤ m s a && m s' a == m s a - f s a

def becomes [DecidableEq μ] (m : Measure σ α μ) (f : Term σ α μ) (s : σ) (a : α) : Bool :=
  on op s a fun _ s' => m s' a == f s a

def resultIs [DecidableEq μ] (out : Answer ρ μ) (f : Term σ α μ) (s : σ) (a : α) : Bool :=
  on op s a fun r _ => out r == f s a

def resultAtMost (out : Answer ρ Nat) (f : Term σ α Nat) (s : σ) (a : α) : Bool :=
  on op s a fun r _ => !(f s a < out r)

def resultAtLeast (out : Answer ρ Nat) (f : Term σ α Nat) (s : σ) (a : α) : Bool :=
  on op s a fun r _ => !(out r < f s a)

def atMost (m : Measure σ α Nat) (f : Term σ α Nat) (s : σ) (a : α) : Bool :=
  on op s a fun _ s' => !(f s a < m s' a)

def atLeast (m : Measure σ α Nat) (f : Term σ α Nat) (s : σ) (a : α) : Bool :=
  on op s a fun _ s' => !(m s' a < f s a)

def everyOf (coll : Coll σ α ρ ι) (P : ItemCond σ α ι) [∀ s a x, Decidable (P s a x)] (s : σ) (a : α) : Bool :=
  on op s a fun r s' => (coll s' a r).all fun x => decide (P s' a x)

def noneOf (coll : Coll σ α ρ ι) (P : ItemCond σ α ι) [∀ s a x, Decidable (P s a x)] (s : σ) (a : α) : Bool :=
  on op s a fun r s' => !(coll s' a r).any fun x => decide (P s' a x)

def countOf (coll : Coll σ α ρ ι) (P : ItemCond σ α ι) [∀ s a x, Decidable (P s a x)] (cmp : Cmp)
    (n : Term σ α Nat) (s : σ) (a : α) : Bool :=
  on op s a fun r s' =>
    let k := ((coll s' a r).filter fun x => decide (P s' a x)).length
    match cmp with
    | .atMost => !(n s a < k)
    | .atLeast => !(k < n s a)
    | .exactly => k == n s a

def agreesWith [DecidableEq ρ] [DecidableEq σ] (ref : Term σ α (ρ × σ)) (s : σ) (a : α) : Bool :=
  on op s a fun r s' => r == (ref s a).1 && s' == (ref s a).2

def within [DecidableEq ι] (sub : Coll σ α ρ ι) (sup : Term σ α (List ι)) (s : σ) (a : α) : Bool :=
  on op s a fun r s' => (sub s' a r).all fun x => (sup s a).contains x

def covers [DecidableEq ι] (sup : Coll σ α ρ ι) (sub : Term σ α (List ι)) (s : σ) (a : α) : Bool :=
  on op s a fun r s' => !(sub s a).any fun x => !(sup s' a r).contains x

/-- The shape every two-run checker has. -/
@[inline] def on2 (rel : Variation σ α) [∀ s a s₂ a₂, Decidable (rel s a s₂ a₂)]
    (s : σ) (a : α) (s₂ : σ) (a₂ : α) (test : ρ → σ → ρ → σ → Bool) : Bool :=
  if op.scope s a ∧ op.scope s₂ a₂ ∧ rel s a s₂ a₂ then
    match op.run s a, op.run s₂ a₂ with
    | some (r, s'), some (r₂, s₂') =>
      match op.calls with
      | .every => test r s' r₂ s₂'
      | .accepted => if op.accepted r ∧ op.accepted r₂ then test r s' r₂ s₂' else true
      | .rejected => if ¬ op.accepted r ∧ ¬ op.accepted r₂ then test r s' r₂ s₂' else true
    | _, _ => op.silenceAllowed
  else true

def monotone (more : Variation σ α) [∀ s a s₂ a₂, Decidable (more s a s₂ a₂)] (cls : AnswerClass ρ)
    [DecidablePred cls] (s : σ) (a : α) (s₂ : σ) (a₂ : α) : Bool :=
  on2 op more s a s₂ a₂ fun r _ r₂ _ => if cls r then decide (cls r₂) else true

def independentOf [DecidableEq ν] (differOnlyIn : Variation σ α) [∀ s a s₂ a₂, Decidable (differOnlyIn s a s₂ a₂)]
    (view : ρ → σ → ν) (s : σ) (a : α) (s₂ : σ) (a₂ : α) : Bool :=
  on2 op differOnlyIn s a s₂ a₂ fun r s' r₂ s₂' => view r s' == view r₂ s₂'

def independentGiven [DecidableEq ν] (differOnlyIn : Variation σ α) [∀ s a s₂ a₂, Decidable (differOnlyIn s a s₂ a₂)]
    (cls : AnswerClass ρ) [DecidablePred cls] (view : ρ → σ → ν) (s : σ) (a : α) (s₂ : σ) (a₂ : α) : Bool :=
  on2 op differOnlyIn s a s₂ a₂ fun r s' r₂ s₂' => if cls r then view r s' == view r₂ s₂' else true

end Check

/-! ## Deciding the DEFINITION at one call

Not a third reading: an instance of `Decidable` contains a proof that its answer is the truth of the
proposition, so `decide (F.at op holes s a)` is the definition's own verdict at `(s, a)`. -/

instance Op.decHoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop)
    [∀ s a, Decidable (op.scope s a)] [DecidablePred op.accepted] [∀ s a r s', Decidable (Q s a r s')]
    (s : σ) (a : α) : Decidable (op.HoldsAt Q s a) :=
  if hs : op.scope s a then
    match hc : op.calls, hr : op.run s a with
    | .every, none => isFalse (by
        intro h; have h := h hs; simp only [hc, hr] at h; obtain ⟨_, _, e, _⟩ := h; cases e)
    | .every, some (r, s') =>
        if hq : Q s a r s' then isTrue (by intro _; simp only [hc, hr]; exact ⟨r, s', rfl, hq⟩)
        else isFalse (by
          intro h; have h := h hs; simp only [hc, hr] at h
          obtain ⟨r₁, s₁, e, q⟩ := h; cases e; exact hq q)
    | .accepted, none => isTrue (by intro _; simp only [hc, hr]; intro _ _ e; cases e)
    | .accepted, some (r, s') =>
        if ha : op.accepted r then
          if hq : Q s a r s' then isTrue (by intro _; simp only [hc, hr]; intro _ _ e _; cases e; exact hq)
          else isFalse (by intro h; have h := h hs; simp only [hc, hr] at h; exact hq (h r s' rfl ha))
        else isTrue (by intro _; simp only [hc, hr]; intro _ _ e h; cases e; exact absurd h ha)
    | .rejected, none => isTrue (by intro _; simp only [hc, hr]; intro _ _ e; cases e)
    | .rejected, some (r, s') =>
        if ha : op.accepted r then
          isTrue (by intro _; simp only [hc, hr]; intro _ _ e h; cases e; exact absurd ha h)
        else
          if hq : Q s a r s' then isTrue (by intro _; simp only [hc, hr]; intro _ _ e _; cases e; exact hq)
          else isFalse (by intro h; have h := h hs; simp only [hc, hr] at h; exact hq (h r s' rfl ha))
  else isTrue (fun h => absurd h hs)

instance Op.decHoldsAt2 (op : Op σ α ρ) (rel : Variation σ α) (Q : ρ → σ → ρ → σ → Prop)
    [∀ s a, Decidable (op.scope s a)] [DecidablePred op.accepted] [∀ s a s₂ a₂, Decidable (rel s a s₂ a₂)]
    [∀ r s' r₂ s₂', Decidable (Q r s' r₂ s₂')]
    (s : σ) (a : α) (s₂ : σ) (a₂ : α) : Decidable (op.HoldsAt2 rel Q s a s₂ a₂) :=
  if hs : op.scope s a ∧ op.scope s₂ a₂ ∧ rel s a s₂ a₂ then
    match hc : op.calls, hr : op.run s a, hr₂ : op.run s₂ a₂ with
    | .every, some (r, s'), some (r₂, s₂') =>
        if hq : Q r s' r₂ s₂' then
          isTrue (by intro _ _ _; simp only [hc, hr, hr₂]; exact ⟨r, s', r₂, s₂', rfl, rfl, hq⟩)
        else isFalse (by
          intro h; have h := h hs.1 hs.2.1 hs.2.2; simp only [hc, hr, hr₂] at h
          obtain ⟨_, _, _, _, e, e₂, q⟩ := h; cases e; cases e₂; exact hq q)
    | .every, none, _ => isFalse (by
        intro h; have h := h hs.1 hs.2.1 hs.2.2; simp only [hc, hr] at h
        obtain ⟨_, _, _, _, e, _, _⟩ := h; cases e)
    | .every, some _, none => isFalse (by
        intro h; have h := h hs.1 hs.2.1 hs.2.2; simp only [hc, hr₂] at h
        obtain ⟨_, _, _, _, _, e, _⟩ := h; cases e)
    | .accepted, some (r, s'), some (r₂, s₂') =>
        if ha : op.accepted r ∧ op.accepted r₂ then
          if hq : Q r s' r₂ s₂' then
            isTrue (by intro _ _ _; simp only [hc, hr, hr₂]; intro _ _ _ _ e e₂ _ _; cases e; cases e₂; exact hq)
          else isFalse (by
            intro h; have h := h hs.1 hs.2.1 hs.2.2; simp only [hc, hr, hr₂] at h
            exact hq (h r s' r₂ s₂' rfl rfl ha.1 ha.2))
        else isTrue (by
          intro _ _ _; simp only [hc, hr, hr₂]; intro _ _ _ _ e e₂ h h₂; cases e; cases e₂; exact absurd ⟨h, h₂⟩ ha)
    | .accepted, none, _ => isTrue (by intro _ _ _; simp only [hc, hr]; intro _ _ _ _ e; cases e)
    | .accepted, some _, none => isTrue (by intro _ _ _; simp only [hc, hr₂]; intro _ _ _ _ _ e; cases e)
    | .rejected, some (r, s'), some (r₂, s₂') =>
        if ha : ¬ op.accepted r ∧ ¬ op.accepted r₂ then
          if hq : Q r s' r₂ s₂' then
            isTrue (by intro _ _ _; simp only [hc, hr, hr₂]; intro _ _ _ _ e e₂ _ _; cases e; cases e₂; exact hq)
          else isFalse (by
            intro h; have h := h hs.1 hs.2.1 hs.2.2; simp only [hc, hr, hr₂] at h
            exact hq (h r s' r₂ s₂' rfl rfl ha.1 ha.2))
        else isTrue (by
          intro _ _ _; simp only [hc, hr, hr₂]; intro _ _ _ _ e e₂ h h₂; cases e; cases e₂; exact absurd ⟨h, h₂⟩ ha)
    | .rejected, none, _ => isTrue (by intro _ _ _; simp only [hc, hr]; intro _ _ _ _ e; cases e)
    | .rejected, some _, none => isTrue (by intro _ _ _; simp only [hc, hr₂]; intro _ _ _ _ _ e; cases e)
  else isTrue (fun h₁ h₂ h₃ => absurd ⟨h₁, h₂, h₃⟩ hs)

end Frames
