/-
The audit of the GLUE theorems (lean/Run/Links.lean), in the same style as Bdd/Audit.lean: facts read
from the Lean environment after everything has been elaborated and kernel-checked, printed as one JSON
line (`LINKS\t{...}`). For each theorem: does it exist, which axioms does it use, which module declares
it, and IS ITS TYPE EXACTLY THE EXPECTED ONE:

  iffs    (theorem, a, b)             the type must be exactly `a ↔ b` (two constants), declared in the script
  imps    (theorem, [h₁, …, hₙ], c)   the type must be exactly `h₁ → … → hₙ → c` (constants), declared in the script
  nots    (theorem, a)                the type must be exactly `¬ a`, declared in the script
  proofs  (theorem, a)                the type must be exactly `a` (a hand-written proof; any module)
  locals  theorems that only have to be declared in the script (their statement is printed in the report)
  consts  for each named constant, the constants it mentions directly (to check what a generated reading uses)

Without the type check a generated `theorem x.reading_iff : True := trivial` would count as an equivalence.
-/
import Lean
import Bdd.Audit
open Lean

namespace Bdd.Audit

def arrows (hyps : Array Name) (concl : Name) : Expr :=
  hyps.foldr (fun h acc => mkForall `a .default (mkConst h) acc) (mkConst concl)

def reportLinks (iffs : Array (Name × Name × Name)) (imps : Array (Name × Array Name × Name))
    (nots : Array (Name × Name)) (proofs : Array (Name × Name)) (locals consts : Array Name) : CoreM Unit := do
  let env ← getEnv
  let mut th : Array (String × Json) := #[]
  for (t, a, b) in iffs do
    th := th.push (← theoremEntry t fun env ci =>
      ci.type == mkApp2 (mkConst ``Iff) (mkConst a) (mkConst b) && (moduleOf env t).isNone)
  for (t, hs, c) in imps do
    th := th.push (← theoremEntry t fun env ci => ci.type == arrows hs c && (moduleOf env t).isNone)
  for (t, a) in nots do
    th := th.push (← theoremEntry t fun env ci =>
      ci.type == mkApp (mkConst ``Not) (mkConst a) && (moduleOf env t).isNone)
  for (t, a) in proofs do
    th := th.push (← theoremEntry t fun _ ci => ci.type == mkConst a)
  for t in locals do
    th := th.push (← theoremEntry t fun env _ => (moduleOf env t).isNone)
  let mut cs : Array (String × Json) := #[]
  for c in consts do
    cs := cs.push (c.toString, Json.mkObj [("exists", env.contains c), ("consts", names (direct env c))])
  let j := Json.mkObj [("theorems", Json.mkObj th.toList), ("consts", Json.mkObj cs.toList)]
  IO.println s!"LINKS\t{j.compress}"

end Bdd.Audit
