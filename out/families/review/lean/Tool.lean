/-
M9 families: measurement.  One JSON line per declaration (prefix `MEASURE `), at Expr level.
Sizes: tree node count (unshared) and number of distinct subterms (DAG), as in the corpus exports.
Instance cost: instance-implicit argument slots filled in the proof term, and the distinct nodes inside them.
-/
import Mathlib.Lean.Expr.Basic
import Lean

open Lean Meta Elab Command

namespace Fam

partial def treeSize (e : Expr) : StateM (Std.HashMap ExprStructEq Nat) Nat := do
  match e with
  | .mdata _ b => treeSize b
  | _ =>
    if let some r := (← get)[(⟨e⟩ : ExprStructEq)]? then return r
    let r ← match e with
      | .app f a => do pure ((← treeSize f) + (← treeSize a) + 1)
      | .lam _ d b _ => do pure ((← treeSize d) + (← treeSize b) + 1)
      | .forallE _ d b _ => do pure ((← treeSize d) + (← treeSize b) + 1)
      | .letE _ t v b _ => do pure ((← treeSize t) + (← treeSize v) + (← treeSize b) + 1)
      | .proj _ _ b => do pure ((← treeSize b) + 1)
      | _ => pure 1
    modify (·.insert ⟨e⟩ r)
    return r

/-- (tree size, number of distinct subterms) -/
def sizes (e : Expr) : Nat × Nat :=
  let (r, m) := (treeSize e).run {}
  (r, m.size)

/-- binder infos of a constant's type, syntactically -/
partial def binderInfos : Expr → List BinderInfo
  | .forallE _ _ b bi => bi :: binderInfos b
  | .mdata _ b => binderInfos b
  | _ => []

structure InstAcc where
  seen : Std.HashSet ExprStructEq := {}
  slots : Nat := 0
  instArgs : Array Expr := #[]
  apps : Nat := 0

/-- Walk distinct subterms; at each constant-headed application count the instance-implicit slots. -/
partial def instWalk (env : Environment) (e : Expr) : StateM InstAcc Unit := do
  if (← get).seen.contains ⟨e⟩ then return
  modify fun s => { s with seen := s.seen.insert ⟨e⟩ }
  match e with
  | .app .. =>
    let f := e.getAppFn
    let args := e.getAppArgs
    if let .const c _ := f then
      if let some ci := env.find? c then
        let bis := binderInfos ci.type
        modify fun s => { s with apps := s.apps + 1 }
        let mut i := 0
        for a in args do
          if (bis.getD i .default).isInstImplicit then
            modify fun s => { s with slots := s.slots + 1, instArgs := s.instArgs.push a }
          i := i + 1
    instWalk env f
    for a in args do instWalk env a
  | .lam _ d b _ => do instWalk env d; instWalk env b
  | .forallE _ d b _ => do instWalk env d; instWalk env b
  | .letE _ t v b _ => do instWalk env t; instWalk env v; instWalk env b
  | .proj _ _ b => instWalk env b
  | .mdata _ b => instWalk env b
  | _ => pure ()

/-- (constant-headed applications, instance slots filled, distinct nodes inside instance arguments) -/
def instCost (env : Environment) (e : Expr) : Nat × Nat × Nat :=
  let (_, acc) := (instWalk env e).run {}
  let (_, m) := (acc.instArgs.forM (fun a => do let _ ← treeSize a)).run {}
  (acc.apps, acc.slots, m.size)

def measure (group : String) (n : Name) (extra : List (String × Json) := []) : CommandElabM Json := do
  let env ← getEnv
  let some ci := env.find? n | throwError "missing {n}"
  let (st, sd) := sizes ci.type
  let (nb, nh, ninst, nexp) ← liftTermElabM <| forallTelescope ci.type fun xs _ => do
    let mut nh : Nat := 0; let mut nexp : Nat := 0; let mut ninst : Nat := 0
    for x in xs do
      let d ← x.fvarId!.getDecl
      let isP ← isProp d.type
      if d.binderInfo.isInstImplicit then ninst := ninst + 1
      else if isP then nh := nh + 1
      if d.binderInfo == .default then nexp := nexp + 1
    return (xs.size, nh, ninst, nexp)
  let mut fields : List (String × Json) := [("group", group), ("name", toJson n.toString), ("kind", toJson (match ci with | .thmInfo _ => "theorem" | .defnInfo _ => "def" | .inductInfo _ => "inductive" | _ => "other")),
    ("statementTree", toJson st), ("statementDag", toJson sd), ("binders", toJson nb), ("hyps", toJson nh),
    ("instBinders", toJson ninst), ("explicit", toJson nexp)]
  if let some v := ci.value? (allowOpaque := true) then
    let (vt, vd) := sizes v
    let (apps, slots, inodes) := instCost env v
    fields := fields ++ [("valueTree", toJson vt), ("valueDag", toJson vd), ("apps", toJson apps),
      ("instSlots", toJson slots), ("instNodes", toJson inodes),
      ("consts", toJson v.getUsedConstants.size)]
  if group != "orig" then
    let ax ← liftCoreM <| collectAxioms n
    fields := fields ++ [("axioms", toJson (ax.map (·.toString)))]
    if ax.contains ``sorryAx then throwError "sorry in {n}"
  return Json.mkObj (fields ++ extra)

/-- Does `a` state exactly what `b` states (up to universe parameter names)? -/
def sameStatement (a b : Name) : CommandElabM Bool := do
  let env ← getEnv
  let some ca := env.find? a | throwError "missing {a}"
  let some cb := env.find? b | throwError "missing {b}"
  if ca.levelParams.length != cb.levelParams.length then return false
  return ca.type == cb.type.instantiateLevelParams cb.levelParams (ca.levelParams.map Level.param)

/-- the two statements are definitionally equal (default transparency): used when re-elaborating the corpus's
statement text in a scratch file picks a different but equal instance term -/
def defeqStatement (a b : Name) : CommandElabM Bool := do
  let env ← getEnv
  let some ca := env.find? a | throwError "missing {a}"
  let some cb := env.find? b | throwError "missing {b}"
  if ca.levelParams.length != cb.levelParams.length then return false
  liftTermElabM <| Meta.isDefEq ca.type (cb.type.instantiateLevelParams cb.levelParams (ca.levelParams.map Level.param))

def report (fam : String) (rows : List (String × Name)) : CommandElabM Unit := do
  for (g, n) in rows do
    IO.println ("MEASURE " ++ (← measure g n [("family", toJson fam)]).compress)

/-- pairs (original, re-derived): measure both and record whether the re-derived one states exactly the original -/
def reportPairs (fam : String) (g : String) (rows : List (Name × Name)) : CommandElabM Unit := do
  for (o, r) in rows do
    IO.println ("MEASURE " ++ (← measure "orig" o [("family", toJson fam), ("pairedWith", toJson r.toString), ("role", toJson g)]).compress)
    IO.println ("MEASURE " ++ (← measure g r [("family", toJson fam), ("pairedWith", toJson o.toString), ("same", toJson (← sameStatement o r)), ("sameDefeq", toJson (← defeqStatement o r))]).compress)

end Fam
