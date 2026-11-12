/-
The audit of the GLUE theorems (lean/Run/Links.lean), in the same style as Bdd/Audit.lean: facts read
from the Lean environment after everything has been elaborated and kernel-checked, printed as one JSON
line (`LINKS\t{...}`). For each theorem: does it exist, which axioms does it use, which module declares
it, and IS ITS TYPE EXACTLY THE EXPECTED ONE:

  iffs    (theorem, a, b)             the type must be exactly `a ↔ b` (two constants), declared in the script;
                                      AND ITS PROOF MAY NOT USE A PROOF OF EITHER SIDE (`uses_proof`, see below)
  imps    (theorem, [h₁, …, hₙ], c)   the type must be exactly `h₁ → … → hₙ → c` (constants), declared in the script
  nots    (theorem, a)                the type must be exactly `¬ a`, declared in the script
  proofs  (theorem, a)                the type must be exactly `a` (a hand-written proof; any module)
  locals  theorems that only have to be declared in the script (their statement is printed in the report)
  consts  for each named constant, the constants it mentions directly, and which of those belong to THIS PROJECT
          (declared in the script or in a module of the project, not in Lean's core, Mathlib or the Aeneas library):
          the report checks the project constants of a generated reading against an allowlist

Without the type check a generated `theorem x.reading_iff : True := trivial` would count as an equivalence.

`uses_proof` (added after the review of the frame library). An equivalence between two PROVED closed propositions
can be proved from the two proofs alone (`⟨fun _ => proofOfB, fun _ => proofOfA⟩`), which says nothing about whether
the two statements mean the same. So for each `a ↔ b` the audit walks everything the proof reaches through
constants of this project (the values of theorems included) and reports whether it meets a theorem whose type is
exactly `a` or exactly `b`, or the constants `<id>` / `<id>.reading_holds` by name. The report counts such an
equivalence as absent.
-/
import Lean
import Bdd.Audit
open Lean

namespace Bdd.Audit

def arrows (hyps : Array Name) (concl : Name) : Expr :=
  hyps.foldr (fun h acc => mkForall `a .default (mkConst h) acc) (mkConst concl)

/-- The libraries of this project. A constant declared in one of them, or in the script being run, is a project constant. -/
def projectRoots : Array Name := #[`Frames, `Bdd, `Generated, `Wallet, `Ledger, `Counter, `Run]

def isProject (env : Environment) (n : Name) : Bool :=
  match moduleOf env n with
  | none => true
  | some m => projectRoots.contains m.getRoot

/-- Everything the PROOF of `root` reaches through constants of this project. Unlike `closure`, the values of
    theorems are entered; constants of the libraries are recorded but not entered. -/
partial def proofReach (env : Environment) (root : Name) : NameSet := Id.run do
  let mut seen : NameSet := {}
  let mut todo : Array Name := #[root]
  while !todo.isEmpty do
    let n := todo.back!
    todo := todo.pop
    if seen.contains n then continue
    seen := seen.insert n
    if isProject env n then
      match env.find? n with
      | some ci =>
        for m in usedBy ci do
          if !seen.contains m then todo := todo.push m
      | none => pure ()
  return seen

/-- Does the proof of the equivalence `t : a ↔ b` use a proof of `a` or of `b`? -/
def usesProofOfSide (env : Environment) (t a b : Name) : Bool :=
  let reach := (proofReach env t).erase t
  reach.contains b.getPrefix || reach.contains (t.getPrefix ++ `reading_holds) ||
  reach.toArray.any fun n =>
    match env.find? n with
    | some (.thmInfo ci) => ci.type == mkConst a || ci.type == mkConst b
    | _ => false

def reportLinks (iffs : Array (Name × Name × Name)) (imps : Array (Name × Array Name × Name))
    (nots : Array (Name × Name)) (proofs : Array (Name × Name)) (locals consts : Array Name)
    (roots : Array Name := #[]) : CoreM Unit := do
  -- `roots`: the library roots of the declared projects (projects.yaml, written into the generated script). Each must be
  -- a root this audit enters; otherwise a proof resting on that library would be read as resting on nothing of the
  -- project. No LINKS line is printed, so the run stops.
  for r in roots do
    unless projectRoots.contains r do
      throwError "the library root {r} of a declared project (projects.yaml) is not in Bdd.Audit.projectRoots (lean/Bdd/AuditLinks.lean): add it"
  let env ← getEnv
  let mut th : Array (String × Json) := #[]
  for (t, a, b) in iffs do
    th := th.push (← theoremEntry t
      (fun env ci => ci.type == mkApp2 (mkConst ``Iff) (mkConst a) (mkConst b) && (moduleOf env t).isNone)
      (fun env => [("uses_proof", Json.bool (usesProofOfSide env t a b))]))
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
    cs := cs.push (c.toString, Json.mkObj [("exists", env.contains c), ("consts", names (direct env c)),
      ("project", names ((direct env c).filter (isProject env)))])
  let j := Json.mkObj [("theorems", Json.mkObj th.toList), ("consts", Json.mkObj cs.toList)]
  IO.println s!"LINKS\t{j.compress}"

end Bdd.Audit
