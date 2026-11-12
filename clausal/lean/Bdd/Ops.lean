/-
Fixed support: how an Aeneas-generated model function becomes an operation of the frame library
(lean/Frames). Nothing here is specific to one crate.

* `toOption`: what a model call gave, as a plain value: `some r` if it returned `ok r`, `none` if it
  failed (panic) or diverged. This is the "gives an answer / gives none" of `Frames.Op.run`.
* `opMut`, `opMut2`, `opRead`, `opRead0`: one constructor per shape of Rust signature
  (`&mut self` + argument; two `&mut` + argument; `&self` + argument; `&self`).
  A `&self` function hands no state back, so the state after it is the state before, by construction.
* bridge lemmas used by generated equivalence proofs.
-/
import Aeneas
import Frames.Check
open Aeneas Aeneas.Std Result

namespace Bdd
variable {σ σ₂ α ρ : Type}

def toOption {β : Type} (m : Result β) : Option β :=
  match Result.match m with
  | .ok r => some r
  | _ => none

@[simp] theorem toOption_ok {β : Type} (r : β) : toOption (ok r) = some r := by
  simp [toOption]

theorem toOption_eq_some {β : Type} {m : Result β} {r : β} : toOption m = some r ↔ m = ok r := by
  cases m using Result.cases with
  | ret x => simp [toOption]
  | vis i k => simp [toOption]
  | div => simp [toOption]

/-- `fn(&mut self, a) -> r`: the model returns the answer and the state afterwards. -/
@[reducible] def opMut (f : σ → α → Result (ρ × σ)) (accepted : ρ → Prop) : Frames.Op σ α ρ where
  run s a := toOption (f s a)
  accepted := accepted

/-- `fn(&mut x, &mut y, a) -> r`: the state is the pair. -/
@[reducible] def opMut2 (f : σ → σ₂ → α → Result (ρ × σ × σ₂)) (accepted : ρ → Prop) : Frames.Op (σ × σ₂) α ρ where
  run s a := toOption (f s.1 s.2 a)
  accepted := accepted

/-- `fn(&self, a) -> r`: the state is not handed back, so it is unchanged by construction. -/
@[reducible] def opRead (f : σ → α → Result ρ) (accepted : ρ → Prop) : Frames.Op σ α ρ where
  run s a := match toOption (f s a) with
    | some r => some (r, s)
    | none => none
  accepted := accepted

/-- `fn(&self) -> r`: no argument; the input is `Unit`. -/
@[reducible] def opRead0 (f : σ → Result ρ) (accepted : ρ → Prop) : Frames.Op σ Unit ρ where
  run s _ := match toOption (f s) with
    | some r => some (r, s)
    | none => none
  accepted := accepted

theorem read_eq_some {β : Type} {m : Result β} {s s' : σ} {r : β} :
    (match toOption m with | some r => some (r, s) | none => none) = some (r, s') ↔ m = ok r ∧ s' = s := by
  cases h : toOption m with
  | none => simp; intro e; rw [e] at h; simp at h
  | some x =>
    have hx := toOption_eq_some.mp h
    subst hx
    simp only [Option.some.injEq, Prod.mk.injEq]
    constructor
    · rintro ⟨rfl, rfl⟩; exact ⟨rfl, rfl⟩
    · rintro ⟨e, rfl⟩; exact ⟨Result.ok_injective e, rfl⟩

/-! What `run = some (r, s')` says in terms of the model function, one fact per constructor. -/
theorem opMut_some {f : σ → α → Result (ρ × σ)} {acc : ρ → Prop} {s : σ} {a : α} {r : ρ} {s' : σ} :
    (opMut f acc).run s a = some (r, s') ↔ f s a = ok (r, s') := toOption_eq_some

theorem opMut2_some {f : σ → σ₂ → α → Result (ρ × σ × σ₂)} {acc : ρ → Prop} {s : σ × σ₂} {a : α} {r : ρ}
    {s' : σ × σ₂} : (opMut2 f acc).run s a = some (r, s') ↔ f s.1 s.2 a = ok (r, s') := toOption_eq_some

theorem opRead_some {f : σ → α → Result ρ} {acc : ρ → Prop} {s : σ} {a : α} {r : ρ} {s' : σ} :
    (opRead f acc).run s a = some (r, s') ↔ f s a = ok r ∧ s' = s := read_eq_some

theorem opRead0_some {f : σ → Result ρ} {acc : ρ → Prop} {s : σ} {a : Unit} {r : ρ} {s' : σ} :
    (opRead0 f acc).run s a = some (r, s') ↔ f s = ok r ∧ s' = s := read_eq_some

/-- For a kernel-checked refutation at a concrete input: if the model returned `x`, and stepping through the
    model shows that whatever it returns cannot be `x`, there is a contradiction. -/
theorem false_of_spec {β : Type} {m : Result β} {x : β} (e : m = ok x)
    (h : Std.WP.spec m (fun out => out = x → False)) : False := by
  cases m using Result.cases with
  | ret r =>
    have h' : r = x → False := by simpa using h
    exact h' (Result.ok_injective e)
  | vis i k => simp at h
  | div => simp at h

end Bdd
