/-
Fixed support for scenario statements. Nothing here is specific to one crate.

* `ok_of_spec`, `ok2_of_spec`, `ok3_of_spec`: bridge from Aeneas's total-correctness
  triple `spec m Q` to the plain form `∃ r, m = ok r ∧ Q r` used by generated
  statements, so proofs can use `step*` while statements need no Aeneas notation.
* `Check`, `run`, `runThens`, `showResult`: executable observation of a model call
  through `Result.match` (Aeneas's `Result` is not an inductive, so `decide` cannot
  evaluate the model, but the interpreter can).
-/
import Aeneas
open Aeneas Aeneas.Std Result

namespace Bdd

theorem ok_of_spec {α} {m : Result α} {Q : α → Prop} (h : Std.WP.spec m Q) :
    ∃ r, m = ok r ∧ Q r := by
  cases m using Result.cases with
  | ret r => exact ⟨r, rfl, by simpa using h⟩
  | vis i k => simp at h
  | div => simp at h

/-- The same under the name the generator uses for a call that returns one thing. -/
theorem ok1_of_spec {α} {m : Result α} {Q : α → Prop} (h : Std.WP.spec m Q) :
    ∃ r, m = ok r ∧ Q r := ok_of_spec h

theorem ok2_of_spec {α β} {m : Result (α × β)} {Q : α → β → Prop}
    (h : Std.WP.spec m (fun r => Q r.1 r.2)) : ∃ a b, m = ok (a, b) ∧ Q a b := by
  obtain ⟨⟨a, b⟩, e, q⟩ := ok_of_spec h; exact ⟨a, b, e, q⟩

theorem ok3_of_spec {α β γ} {m : Result (α × β × γ)} {Q : α → β → γ → Prop}
    (h : Std.WP.spec m (fun r => Q r.1 r.2.1 r.2.2)) : ∃ a b c, m = ok (a, b, c) ∧ Q a b c := by
  obtain ⟨⟨a, b, c⟩, e, q⟩ := ok_of_spec h; exact ⟨a, b, c, e, q⟩

/-- `ok` is injective: two successful results of the same call are equal. -/
theorem ok_inj {α} {a b : α} (h : (ok a : Result α) = ok b) : a = b := by
  simpa using h

/-- If the call returned `x`, and its specification says `Q` of whatever it returns, then `Q x`. -/
theorem post_of_spec {α} {m : Result α} {Q : α → Prop} {x : α} (e : m = ok x) (h : Std.WP.spec m Q) : Q x := by
  obtain ⟨r, e', q⟩ := ok_of_spec h
  rw [e] at e'
  rw [ok_inj e']; exact q

/-- Outcome of evaluating one scenario at one concrete input. -/
inductive Check | pass | givenFalse | thenFalse | panicked | diverged
  deriving Repr, DecidableEq

def Check.name : Check → String
  | .pass => "pass" | .givenFalse => "givenFalse" | .thenFalse => "thenFalse"
  | .panicked => "panicked" | .diverged => "diverged"

/-- Run the model call and evaluate the (decided) postcondition on what it returned. -/
def run {α} (r : Result α) (T : α → Bool) : Check :=
  match Result.match r with
  | .ok o => if T o then .pass else .thenFalse
  | .div => .diverged
  | .vis _ _ => .panicked

/-- Each Then conjunct separately; `none` if the call panicked or diverged. -/
def runThens {α} (r : Result α) (T : α → List Bool) : Option (List Bool) :=
  match Result.match r with
  | .ok o => some (T o)
  | _ => none

/-- Printable form of what the call returned. -/
def showResult {α} (r : Result α) (f : α → String) : String :=
  match Result.match r with
  | .ok o => f o
  | .div => "DIVERGED"
  | .vis _ _ => "PANICKED"

/-- Did the call return, and does `T` hold of what it returned? Used by the search to prefer a
    satisfying input at which the operation actually changes something (a non-degenerate witness). -/
def runChanged {α} (r : Result α) (T : α → Bool) : Bool :=
  match Result.match r with
  | .ok o => T o
  | _ => false

def bits (l : List Bool) : String := String.ofList (l.map fun b => if b then '1' else '0')

def optBits : Option (List Bool) → String
  | some l => bits l
  | none => "-"

/-- Line formats read back by clausal (tab-separated). -/
def rowLine (id : String) (n : Nat) (c : Check) (g : List Bool) (t : Option (List Bool)) (ret : String) : String :=
  s!"ROW\t{id}\t{n}\t{c.name}\t{bits g}\t{optBits t}\t{ret}"
def badLine (idx : List Nat) (c : Check) (t : Option (List Bool)) (ret : String) : String :=
  s!"{idx}\t{c.name}\t{optBits t}\t{ret}"
def searchLine (id : String) (tried : Nat) (sat bad : Option String) : String :=
  s!"SEARCH\t{id}\t{tried}\t{sat.getD "-"}\t{bad.getD "-\t-\t-\t-"}"

end Bdd
