/-
FRAME LIBRARY, part 2: the frames. Each frame is a statement shape about one operation with typed
holes (Frames/Core.lean). For each frame `F`:

  F.at op holes s a    what it says about the single call (s, a)
  F op holes           the frame: `F.at` for every state and every input

The fail-closed defaults are in `Op.HoldsAt` and nowhere else: with the default (`calls = every`) a
frame covers every input in scope, accepted or rejected, and includes "the call gives an answer".
"Before" and "after" mean before and after ONE call; no frame speaks about intermediate states.

The numbering follows the first catalogue (out/prior_art_vocabulary.md, section 1).
-/
import Frames.Core

namespace Frames
variable {σ α ρ μ ν ι κ : Type}

/-! ### 1. always answers -/
@[reducible] def AlwaysAnswers.at (op : Op σ α ρ) (s : σ) (a : α) : Prop :=
  op.HoldsAt (fun _ _ _ _ => True) s a
/-- "op always answers": every call in scope returns (no panic, no abort, no divergence). -/
def AlwaysAnswers (op : Op σ α ρ) : Prop := ∀ s a, AlwaysAnswers.at op s a

/-! ### 2. never changes M -/
@[reducible] def NeverChanges.at (op : Op σ α ρ) (m : Measure σ α μ) (s : σ) (a : α) : Prop :=
  op.HoldsAt (fun s a _ s' => m s' a = m s a) s a
/-- "op never changes M": the measure after the call equals the measure before. -/
def NeverChanges (op : Op σ α ρ) (m : Measure σ α μ) : Prop := ∀ s a, NeverChanges.at op m s a

/-! ### 3. changes only X -/
@[reducible] def ChangesOnly.at (op : Op σ α ρ) (parts : σ → List κ) (m : σ → κ → μ) (X : Term σ α (List κ))
    (s : σ) (a : α) : Prop :=
  op.HoldsAt (fun s a _ s' => parts s' = parts s ∧ ∀ k ∈ parts s, k ∉ X s a → m s' k = m s k) s a
/-- "of the parts, op changes only X": the parts are the same parts afterwards, and the measure of every
    part outside `X` is as it was. -/
def ChangesOnly (op : Op σ α ρ) (parts : σ → List κ) (m : σ → κ → μ) (X : Term σ α (List κ)) : Prop :=
  ∀ s a, ChangesOnly.at op parts m X s a

/-! ### 4. always Q / never B, for a class of answers -/
@[reducible] def Always.at (op : Op σ α ρ) (cls : AnswerClass ρ) (s : σ) (a : α) : Prop :=
  op.HoldsAt (fun _ _ r _ => cls r) s a
/-- "op always answers in class Q" (for instance: is always accepted). -/
def Always (op : Op σ α ρ) (cls : AnswerClass ρ) : Prop := ∀ s a, Always.at op cls s a

@[reducible] def Never.at (op : Op σ α ρ) (cls : AnswerClass ρ) (s : σ) (a : α) : Prop :=
  op.HoldsAt (fun _ _ r _ => ¬ cls r) s a
/-- "op never answers in class B": defined as always-not, so there is one reading. -/
def Never (op : Op σ α ρ) (cls : AnswerClass ρ) : Prop := ∀ s a, Never.at op cls s a

/-! ### 5. if C then Q -/
@[reducible] def IfThen.at (op : Op σ α ρ) (C : Cond σ α) (cls : AnswerClass ρ) (s : σ) (a : α) : Prop :=
  op.HoldsAt (fun s a r _ => C s a → cls r) s a
/-- "if C then op answers in class Q". Fail-closed like every other frame: with the default the call must
    give an answer for EVERY input in scope, whether C holds or not; only the class of the answer depends
    on C. (To make no claim at all outside C, narrow the operation with `Op.given C` and use frame 4:
    in a Rule, "<operation> for which C is always accepted". `Frames.IfThen_of_given` and
    `Frames.IfThen.alwaysAnswers` in Frames/Lemmas.lean state the difference.) -/
def IfThen (op : Op σ α ρ) (C : Cond σ α) (cls : AnswerClass ρ) : Prop := ∀ s a, IfThen.at op C cls s a

/-! ### 6. Q only if C -/
@[reducible] def OnlyIf.at (op : Op σ α ρ) (cls : AnswerClass ρ) (C : Cond σ α) (s : σ) (a : α) : Prop :=
  op.HoldsAt (fun s a r _ => cls r → C s a) s a
/-- "op answers in class Q only if C": the converse direction, never inferred from "if". -/
def OnlyIf (op : Op σ α ρ) (cls : AnswerClass ρ) (C : Cond σ α) : Prop := ∀ s a, OnlyIf.at op cls C s a

/-! ### 7. Q exactly when C -/
@[reducible] def ExactlyWhen.at (op : Op σ α ρ) (cls : AnswerClass ρ) (C : Cond σ α) (s : σ) (a : α) : Prop :=
  op.HoldsAt (fun s a r _ => cls r ↔ C s a) s a
/-- "op answers in class Q exactly when C": frames 5 and 6 together. -/
def ExactlyWhen (op : Op σ α ρ) (cls : AnswerClass ρ) (C : Cond σ α) : Prop := ∀ s a, ExactlyWhen.at op cls C s a

/-! ### 8. rejected and unchanged -/
@[reducible] def RejectedUnchanged.at (op : Op σ α ρ) (s : σ) (a : α) : Prop :=
  op.HoldsAt (fun s _ r s' => ¬ op.accepted r ∧ s' = s) s a
/-- "op is rejected and changes nothing" (narrow the operation with `Op.given` for "... when C"). -/
def RejectedUnchanged (op : Op σ α ρ) : Prop := ∀ s a, RejectedUnchanged.at op s a

/-! ### 9. changes M by exactly f / M is now f / the result is f -/
@[reducible] def IncreasesBy.at (op : Op σ α ρ) (m : Measure σ α Nat) (f : Term σ α Nat) (s : σ) (a : α) : Prop :=
  op.HoldsAt (fun s a _ s' => m s' a = m s a + f s a) s a
/-- "op increases M by exactly f". -/
def IncreasesBy (op : Op σ α ρ) (m : Measure σ α Nat) (f : Term σ α Nat) : Prop := ∀ s a, IncreasesBy.at op m f s a

@[reducible] def DecreasesBy.at (op : Op σ α ρ) (m : Measure σ α Nat) (f : Term σ α Nat) (s : σ) (a : α) : Prop :=
  op.HoldsAt (fun s a _ s' => m s' a + f s a = m s a) s a
/-- "op decreases M by exactly f" (so M was at least f). -/
def DecreasesBy (op : Op σ α ρ) (m : Measure σ α Nat) (f : Term σ α Nat) : Prop := ∀ s a, DecreasesBy.at op m f s a

@[reducible] def Becomes.at (op : Op σ α ρ) (m : Measure σ α μ) (f : Term σ α μ) (s : σ) (a : α) : Prop :=
  op.HoldsAt (fun s a _ s' => m s' a = f s a) s a
/-- "after op, M is f". -/
def Becomes (op : Op σ α ρ) (m : Measure σ α μ) (f : Term σ α μ) : Prop := ∀ s a, Becomes.at op m f s a

@[reducible] def ResultIs.at (op : Op σ α ρ) (out : Answer ρ μ) (f : Term σ α μ) (s : σ) (a : α) : Prop :=
  op.HoldsAt (fun s a r _ => out r = f s a) s a
/-- "the result of op is f". -/
def ResultIs (op : Op σ α ρ) (out : Answer ρ μ) (f : Term σ α μ) : Prop := ∀ s a, ResultIs.at op out f s a

/-! ### 10. at most / at least -/
@[reducible] def ResultAtMost.at (op : Op σ α ρ) (out : Answer ρ Nat) (f : Term σ α Nat) (s : σ) (a : α) : Prop :=
  op.HoldsAt (fun s a r _ => out r ≤ f s a) s a
/-- "the result of op is at most f". -/
def ResultAtMost (op : Op σ α ρ) (out : Answer ρ Nat) (f : Term σ α Nat) : Prop := ∀ s a, ResultAtMost.at op out f s a

@[reducible] def ResultAtLeast.at (op : Op σ α ρ) (out : Answer ρ Nat) (f : Term σ α Nat) (s : σ) (a : α) : Prop :=
  op.HoldsAt (fun s a r _ => f s a ≤ out r) s a
/-- "the result of op is at least f". -/
def ResultAtLeast (op : Op σ α ρ) (out : Answer ρ Nat) (f : Term σ α Nat) : Prop := ∀ s a, ResultAtLeast.at op out f s a

@[reducible] def AtMost.at (op : Op σ α ρ) (m : Measure σ α Nat) (f : Term σ α Nat) (s : σ) (a : α) : Prop :=
  op.HoldsAt (fun s a _ s' => m s' a ≤ f s a) s a
/-- "after op, M is at most f". -/
def AtMost (op : Op σ α ρ) (m : Measure σ α Nat) (f : Term σ α Nat) : Prop := ∀ s a, AtMost.at op m f s a

@[reducible] def AtLeast.at (op : Op σ α ρ) (m : Measure σ α Nat) (f : Term σ α Nat) (s : σ) (a : α) : Prop :=
  op.HoldsAt (fun s a _ s' => f s a ≤ m s' a) s a
/-- "after op, M is at least f". -/
def AtLeast (op : Op σ α ρ) (m : Measure σ α Nat) (f : Term σ α Nat) : Prop := ∀ s a, AtLeast.at op m f s a

/-! ### 11. counting over a named collection

The collection is read AFTER the call (it may depend on the state afterwards, the input and the
answer); each item is judged on the state after the call. -/
@[reducible] def EveryOf.at (op : Op σ α ρ) (coll : Coll σ α ρ ι) (P : ItemCond σ α ι) (s : σ) (a : α) : Prop :=
  op.HoldsAt (fun _ a r s' => ∀ x ∈ coll s' a r, P s' a x) s a
/-- "every X of XS is P" ("each"). -/
def EveryOf (op : Op σ α ρ) (coll : Coll σ α ρ ι) (P : ItemCond σ α ι) : Prop := ∀ s a, EveryOf.at op coll P s a

@[reducible] def NoneOf.at (op : Op σ α ρ) (coll : Coll σ α ρ ι) (P : ItemCond σ α ι) (s : σ) (a : α) : Prop :=
  op.HoldsAt (fun _ a r s' => ∀ x ∈ coll s' a r, ¬ P s' a x) s a
/-- "no X of XS is P". -/
def NoneOf (op : Op σ α ρ) (coll : Coll σ α ρ ι) (P : ItemCond σ α ι) : Prop := ∀ s a, NoneOf.at op coll P s a

/-- how a count is compared with a number -/
inductive Cmp where | atMost | atLeast | exactly
  deriving DecidableEq, Repr
@[reducible] def Cmp.holds : Cmp → Nat → Nat → Prop
  | .atMost, n, k => n ≤ k
  | .atLeast, n, k => k ≤ n
  | .exactly, n, k => n = k
instance (c : Cmp) (n k : Nat) : Decidable (c.holds n k) := by
  cases c <;> unfold Cmp.holds <;> infer_instance

@[reducible] def CountOf.at (op : Op σ α ρ) (coll : Coll σ α ρ ι) (P : ItemCond σ α ι)
    [∀ s a x, Decidable (P s a x)] (cmp : Cmp) (n : Term σ α Nat) (s : σ) (a : α) : Prop :=
  op.HoldsAt (fun s a r s' => cmp.holds ((coll s' a r).countP (fun x => decide (P s' a x))) (n s a)) s a
/-- "at most n / at least n / exactly n X of XS are P" ("once" is n = 1). -/
def CountOf (op : Op σ α ρ) (coll : Coll σ α ρ ι) (P : ItemCond σ α ι)
    [∀ s a x, Decidable (P s a x)] (cmp : Cmp) (n : Term σ α Nat) : Prop :=
  ∀ s a, CountOf.at op coll P cmp n s a

/-! ### 12. monotone: more A never loses Q -/
@[reducible] def Monotone.at (op : Op σ α ρ) (more : Variation σ α) (cls : AnswerClass ρ)
    (s : σ) (a : α) (s₂ : σ) (a₂ : α) : Prop :=
  op.HoldsAt2 more (fun r _ r₂ _ => cls r → cls r₂) s a s₂ a₂
/-- "more never loses Q": whenever the second (state, input) is `more` than the first and the first
    call answers in class Q, so does the second. -/
def Monotone (op : Op σ α ρ) (more : Variation σ α) (cls : AnswerClass ρ) : Prop :=
  ∀ s a s₂ a₂, Monotone.at op more cls s a s₂ a₂

/-! ### 13. agrees with a reference -/
@[reducible] def AgreesWith.at (op : Op σ α ρ) (ref : Term σ α (ρ × σ)) (s : σ) (a : α) : Prop :=
  op.HoldsAt (fun s a r s' => (r, s') = ref s a) s a
/-- "op agrees with REF": the answer and the state afterwards are exactly what the reference gives.
    (To compare the answer only, or a view of it, use `ResultIs`.) -/
def AgreesWith (op : Op σ α ρ) (ref : Term σ α (ρ × σ)) : Prop := ∀ s a, AgreesWith.at op ref s a

/-! ### 14. independent of (two runs) -/
@[reducible] def IndependentOf.at (op : Op σ α ρ) (differOnlyIn : Variation σ α) (view : ρ → σ → ν)
    (s : σ) (a : α) (s₂ : σ) (a₂ : α) : Prop :=
  op.HoldsAt2 differOnlyIn (fun r s' r₂ s₂' => view r s' = view r₂ s₂') s a s₂ a₂
/-- "what is seen of op is independent of H": two calls whose (state, input) differ only in H show the
    same view. Also used for "does not change when the input is reordered / repeated". -/
def IndependentOf (op : Op σ α ρ) (differOnlyIn : Variation σ α) (view : ρ → σ → ν) : Prop :=
  ∀ s a s₂ a₂, IndependentOf.at op differOnlyIn view s a s₂ a₂

/-! ### 15. containment between a collection of the input and a collection of the answer

The input's collection is read BEFORE the call; the answer's collection is read off the answer (and, as in
frame 11, the state after the call). -/
@[reducible] def Within.at (op : Op σ α ρ) (sub : Coll σ α ρ ι) (sup : Term σ α (List ι)) (s : σ) (a : α) : Prop :=
  op.HoldsAt (fun s a r s' => ∀ x ∈ sub s' a r, x ∈ sup s a) s a
/-- "every X of the answer is an X of the input": the answer's collection is contained in the input's. -/
def Within (op : Op σ α ρ) (sub : Coll σ α ρ ι) (sup : Term σ α (List ι)) : Prop := ∀ s a, Within.at op sub sup s a

@[reducible] def Covers.at (op : Op σ α ρ) (sup : Coll σ α ρ ι) (sub : Term σ α (List ι)) (s : σ) (a : α) : Prop :=
  op.HoldsAt (fun s a r s' => ∀ x ∈ sub s a, x ∈ sup s' a r) s a
/-- "every X of the input is an X of the answer": the input's collection is contained in the answer's. -/
def Covers (op : Op σ α ρ) (sup : Coll σ α ρ ι) (sub : Term σ α (List ι)) : Prop := ∀ s a, Covers.at op sup sub s a

/-! ### 16. independent of, given the first answer (two runs) -/
@[reducible] def IndependentGiven.at (op : Op σ α ρ) (differOnlyIn : Variation σ α) (cls : AnswerClass ρ)
    (view : ρ → σ → ν) (s : σ) (a : α) (s₂ : σ) (a₂ : α) : Prop :=
  op.HoldsAt2 differOnlyIn (fun r s' r₂ s₂' => cls r → view r s' = view r₂ s₂') s a s₂ a₂
/-- "if the first call answers in class Q, a second call that differs only in H shows the same view":
    frame 14 conditioned on the FIRST run's answer. Fail-closed like the others: both calls must answer
    whatever the first answer is. -/
def IndependentGiven (op : Op σ α ρ) (differOnlyIn : Variation σ α) (cls : AnswerClass ρ) (view : ρ → σ → ν) : Prop :=
  ∀ s a s₂ a₂, IndependentGiven.at op differOnlyIn cls view s a s₂ a₂

end Frames
