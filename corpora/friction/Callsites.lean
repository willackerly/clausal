/-
Call-site census for a hypothesis bundle (friction census, "packet" test).

  callsites <modules.txt> <roots,csv> <targets.txt> <out.jsonl>

targets.txt: one line per target theorem, `<name> <i1,i2,...>`: the binder positions of the bundle's
hypotheses in the theorem's telescope (= argument positions in an application).
Every project constant with a value (theorems, definitions and their auxiliaries) is scanned at Expr
level for applications of a target.  For each application and each bundle position the argument is
classified:
  own    a bound variable that refers to one of the caller's own leading binders (the caller simply
         passes its own hypothesis through);
  local  a bound variable introduced inside the proof (`have`, `fun`, `obtain` ...);
  built  any other term: the caller constructs the fact; `head` is its head constant, `sz` its tree size;
  missing  the application is partial and does not reach that position.
-/
import Lean
open Lean

namespace Callsites

def nameStr (n : Name) : String := n.toString (escape := false)

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

structure St where
  seen : Std.HashSet (ExprStructEq × Nat) := {}
  sites : Array Json := #[]
  sz : Std.HashMap ExprStructEq Nat := {}

def headStr (e : Expr) : String :=
  match e.getAppFn.consumeMData with
  | .const n _ => nameStr n
  | .proj s i _ => s!"proj:{nameStr s}.{i}"
  | .lam .. => "<lam>"
  | .fvar _ => "<fvar>"
  | .bvar _ => "<bvar-app>"
  | _ => "<other>"

partial def scan (targets : Std.HashMap Name (Array Nat)) (caller : String) (top : Nat) (e : Expr) (depth : Nat) :
    StateM St Unit := do
  let key : ExprStructEq × Nat := (⟨e⟩, if e.hasLooseBVars then depth else 0)
  if (← get).seen.contains key then return
  modify fun s => { s with seen := s.seen.insert key }
  match e with
  | .mdata _ b => scan targets caller top b depth
  | .lam _ d b _ => scan targets caller top d depth; scan targets caller top b (depth + 1)
  | .forallE _ d b _ => scan targets caller top d depth; scan targets caller top b (depth + 1)
  | .letE _ t v b _ => scan targets caller top t depth; scan targets caller top v depth; scan targets caller top b (depth + 1)
  | .proj _ _ b => scan targets caller top b depth
  | .app .. =>
    let fn := e.getAppFn
    let args := e.getAppArgs
    if let .const n _ := fn.consumeMData then
      if let some idxs := targets[n]? then
        let mut js : Array Json := #[]
        for i in idxs do
          if h : i < args.size then
            let a := (args[i]).consumeMData
            match a with
            | .bvar k =>
              -- binder level of the variable: depth - 1 - k; the caller's own binders are levels < top
              let lvl := depth - 1 - k
              js := js.push (Json.mkObj [("kind", if lvl < top then "own" else "local")])
            | _ =>
              let s ← get
              let (n', m) := (treeSize a).run s.sz
              modify fun s => { s with sz := m }
              js := js.push (Json.mkObj [("kind", "built"), ("head", headStr a), ("sz", n')])
          else js := js.push (Json.mkObj [("kind", "missing")])
        let j := Json.mkObj [("caller", caller), ("target", nameStr n), ("nargs", args.size), ("args", toJson js)]
        modify fun s => { s with sites := s.sites.push j }
    else scan targets caller top fn depth
    for a in args do scan targets caller top a depth
  | _ => return

partial def numLams : Expr → Nat
  | .lam _ _ b _ => numLams b + 1
  | .mdata _ b => numLams b
  | _ => 0

unsafe def main (args : List String) : IO UInt32 := do
  let [modsFile, rootsS, targetsFile, outFile] := args
    | throw <| IO.userError "usage: callsites modules.txt roots targets.txt out.jsonl"
  initSearchPath (← findSysroot)
  enableInitializersExecution
  let modNames := ((← IO.FS.lines modsFile).filter (· ≠ "")).map (·.toName)
  let env ← importModules (modNames.map fun m => { module := m }) {} (trustLevel := 1024) (loadExts := true)
  let roots := (rootsS.splitOn ",").map (·.toName)
  let projIdx : Array Bool := env.header.moduleNames.map fun m => roots.contains m.getRoot
  let isProj (n : Name) : Bool :=
    match env.getModuleIdxFor? n with
    | some i => projIdx[i.toNat]!
    | none => false
  let mut byStr : Std.HashMap String Name := {}
  for (n, _) in env.constants.map₁.toList do
    if isProj n then
      byStr := byStr.insert (n.toString (escape := false)) n
  let mut targets : Std.HashMap Name (Array Nat) := {}
  for l in (← IO.FS.lines targetsFile) do
    match l.splitOn " " with
    | [nm, idx] =>
      match byStr[nm]? with
      | some n => targets := targets.insert n ((idx.splitOn ",").toArray.map (·.toNat!))
      | none => IO.eprintln s!"unresolved {nm}"
    | _ => pure ()
  let h ← IO.FS.Handle.mk outFile .write
  let mut nSites : Nat := 0
  let mut nConsts : Nat := 0
  for (n, ci) in env.constants.map₁.toList do
    if !isProj n then continue
    let some v := ci.value? (allowOpaque := true) | continue
    nConsts := nConsts + 1
    let ((), st) := (scan targets (nameStr n) (numLams v) v 0).run {}
    for j in st.sites do
      h.putStrLn j.compress
      nSites := nSites + 1
  h.flush
  IO.eprintln s!"targets {targets.size}; scanned {nConsts} project constants; {nSites} call sites"
  return 0

end Callsites

unsafe def main (args : List String) : IO UInt32 := Callsites.main args
