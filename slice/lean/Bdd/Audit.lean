/-
The audit: facts read from the Lean environment after everything has been
elaborated and kernel-checked, printed as one JSON line (`AUDIT\t{...}`).

* theorems: does the constant exist, which axioms does it depend on
  (`Lean.collectAxioms`; `sorryAx` in the list means "not proved"), which module
  declares it, and IS ITS TYPE THE EXPECTED ONE. A scenario proof `<id>` must have
  type exactly `<id>.stmt`, a refutation exactly `¬ <id>.stmt`; the other derived
  theorems must be declared by the audit script itself (not imported from a
  hand-written file). Without this a `theorem <id> : True` would count as a proof.
* stmts:    the constants a generated statement mentions directly. The report
  compares these with what the glossary says the scenario should use, because
  the generator is untrusted.
* defs:     for each glossary definition, the model functions it depends on
  transitively (must be none) and its size in expression nodes.
* fns:      the constants each model function mentions directly, and those it reaches
  through other model functions (to list the Aeneas library models it relies on,
  and whether it contains a loop).
-/
import Lean
open Lean

namespace Bdd.Audit

def usedBy (ci : ConstantInfo) (withValue : Bool := true) : Array Name :=
  let s : NameSet := ci.type.getUsedConstants.foldl (fun acc n => acc.insert n) {}
  let s := if withValue then
      match ci.value? (allowOpaque := true) with
      | some v => v.getUsedConstants.foldl (fun acc n => acc.insert n) s
      | none => s
    else s
  s.toArray

def direct (env : Environment) (n : Name) : Array Name :=
  match env.find? n with
  | some ci => usedBy ci
  | none => #[]

/-- Transitive closure of constants reachable from `root`; proofs of theorems are not entered. -/
partial def closure (env : Environment) (root : Name) : NameSet := Id.run do
  let mut seen : NameSet := {}
  let mut todo : Array Name := #[root]
  while !todo.isEmpty do
    let n := todo.back!
    todo := todo.pop
    if seen.contains n then continue
    seen := seen.insert n
    match env.find? n with
    | some ci =>
      let isThm := match ci with | .thmInfo _ => true | _ => false
      for m in usedBy ci (withValue := !isThm) do
        if !seen.contains m then todo := todo.push m
    | none => pure ()
  return seen

partial def exprSize : Expr → Nat
  | .app f a => exprSize f + exprSize a + 1
  | .lam _ t b _ => exprSize t + exprSize b + 1
  | .forallE _ t b _ => exprSize t + exprSize b + 1
  | .letE _ t v b _ => exprSize t + exprSize v + exprSize b + 1
  | .mdata _ e => exprSize e
  | .proj _ _ e => exprSize e + 1
  | _ => 1

def names (a : Array Name) : Json := Json.arr (a.map fun n => Json.str n.toString)

/-- Where a constant was declared: an imported module's name, or `none` for the current file. -/
def moduleOf (env : Environment) (n : Name) : Option Name :=
  (env.getModuleIdxFor? n).bind fun i => env.header.moduleNames[i.toNat]?

def theoremEntry (t : Name) (typeOk : Environment → ConstantInfo → Bool)
    (extra : Environment → List (String × Json) := fun _ => []) : CoreM (String × Json) := do
  let env ← getEnv
  match env.find? t with
  | some ci =>
    let ax ← collectAxioms t
    let isThm := match ci with | .thmInfo _ => true | _ => false
    let m := moduleOf env t
    return (t.toString, Json.mkObj (([("exists", true), ("axioms", names ax), ("is_theorem", isThm),
      ("type_ok", typeOk env ci), ("local", m.isNone),
      ("module", match m with | some m => Json.str m.toString | none => Json.null)] : List (String × Json)) ++ extra env))
  | none =>
    return (t.toString, Json.mkObj [("exists", false), ("axioms", names #[]), ("is_theorem", false),
      ("type_ok", false), ("local", false), ("module", Json.null)])

/--
`proofs`:      (theorem, statement) pairs; the theorem's type must be exactly the constant `statement`.
`refutations`: (theorem, statement) pairs; the type must be exactly `¬ statement`, declared in this file.
`derived`:     theorems generated into the audit script; they must be declared in this file.
-/
def report (proofs refutations : Array (Name × Name)) (derived stmts defs fns : Array Name) : CoreM Unit := do
  let env ← getEnv
  let mut th : Array (String × Json) := #[]
  for (t, s) in proofs do
    th := th.push (← theoremEntry t fun _ ci => ci.type == mkConst s)
  for (t, s) in refutations do
    th := th.push (← theoremEntry t fun env ci =>
      ci.type == mkApp (mkConst ``Not) (mkConst s) && (moduleOf env t).isNone)
  for t in derived do
    th := th.push (← theoremEntry t fun env _ => (moduleOf env t).isNone)
  let mut st : Array (String × Json) := #[]
  for s in stmts do
    st := st.push (s.toString, Json.mkObj [("exists", env.contains s), ("consts", names (direct env s))])
  let mut df : Array (String × Json) := #[]
  for d in defs do
    let cl := closure env d
    let hits := fns.filter fun f => cl.contains f
    let size := match env.find? d with
      | some ci => (match ci.value? with | some v => exprSize v | none => 0)
      | none => 0
    df := df.push (d.toString, Json.mkObj [("exists", env.contains d), ("model_deps", names hits),
      ("closure_size", cl.size), ("size", size)])
  let mut fn : Array (String × Json) := #[]
  for f in fns do
    -- `closure`: the constants mentioned by `f` or by any model function `f` reaches through other
    -- model functions (a loop, its body, a callee). Library constants are listed, not entered.
    let mut seen : NameSet := {}
    let mut todo : Array Name := #[f]
    let mut reach : NameSet := {}
    while !todo.isEmpty do
      let n := todo.back!
      todo := todo.pop
      if seen.contains n then continue
      seen := seen.insert n
      for m in direct env n do
        reach := reach.insert m
        if fns.contains m && !seen.contains m then todo := todo.push m
    fn := fn.push (f.toString, Json.mkObj [("exists", env.contains f), ("consts", names (direct env f)),
      ("closure", names reach.toArray)])
  let j := Json.mkObj [("theorems", Json.mkObj th.toList), ("stmts", Json.mkObj st.toList),
    ("defs", Json.mkObj df.toList), ("fns", Json.mkObj fn.toList)]
  IO.println s!"AUDIT\t{j.compress}"

end Bdd.Audit
