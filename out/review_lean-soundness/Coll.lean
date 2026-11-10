import Mathlib
import Rosette.Lift
open Lean Meta Elab Command Rosette
set_option maxHeartbeats 0

def Rev.canonLevels (stmt : Expr) : Expr :=
  let ps := (collectLevelParams {} stmt).params
  stmt.instantiateLevelParams ps.toList ((List.range ps.size).map fun i => Level.param (Name.mkNum `u i))

partial def Rev.stripMData (e : Expr) : Expr :=
  e.replace fun | .mdata _ b => some (Rev.stripMData b) | _ => none

/-- first differing pair of subterms -/
partial def Rev.diff (a b : Expr) : Option (Expr × Expr) :=
  if a == b then none else
  match a, b with
  | .app f x, .app g y => (Rev.diff f g).orElse fun _ => Rev.diff x y
  | .lam _ t x _, .lam _ s y _ => (Rev.diff t s).orElse fun _ => Rev.diff x y
  | .forallE _ t x _, .forallE _ s y _ => (Rev.diff t s).orElse fun _ => Rev.diff x y
  | .letE _ t v x _, .letE _ s w y _ => ((Rev.diff t s).orElse fun _ => Rev.diff v w).orElse fun _ => Rev.diff x y
  | .mdata _ x, .mdata _ y => (Rev.diff x y).orElse fun _ => some (a, b)
  | .proj _ _ x, .proj _ _ y => (Rev.diff x y).orElse fun _ => some (a, b)
  | _, _ => some (a, b)

run_meta do
  let n := ``AddCircle.lintegral_preimage
  let proof ← proofOfConst n
  let r ← candidatesOfExprCore proof { ppStatements := false }
  let mut tab : Std.HashMap UInt64 (Expr × Nat) := {}
  for c in r.cands do
    let res ← IO.mkRef (none : Option Expr)
    let onTarget (_ : Path) (e : Expr) : MetaM Expr := do
      let ty := (← inferType e).headBeta
      let ifc ← interfaceOf e ty
      let (stmt, _) ← closeOver ifc e ty
      res.set (some stmt); return e
    let st ← IO.mkRef ({} : Rosette.State)
    discard <| ((visit proof #[] none "root" 0).run { cfg := {}, lift? := some { targets := #[c.path], onTarget } }) st
    let some stmt ← res.get | continue
    let cs := Rev.canonLevels stmt
    match tab[c.stmtHash]? with
    | some (o, oid) =>
      unless o == cs do
        let so := Rev.stripMData o; let sc := Rev.stripMData cs
        logInfo m!"collision #{oid} vs #{c.id}: equal after stripping mdata = {so == sc}; hash recomputed equal = {statementHash o == statementHash cs}"
        if let some (x, y) := Rev.diff so sc then
          logInfo m!"first diff: {x}  VS  {y}\nraw: {repr x}\n VS \n{repr y}"
        logInfo m!"A: {o}\nB: {cs}"
    | none => tab := tab.insert c.stmtHash (cs, c.id)
