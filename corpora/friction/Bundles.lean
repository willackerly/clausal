/-
Bundle-mining exporter (friction census, "packet" test).

Stand-alone program (imports only `Lean`); loads the BUILT environment of a corpus and reads
everything at `Expr` level.  Compiled against each corpus's own toolchain by `bundles_run.sh`.

  bundles <modules.txt> <roots,csv> <theorems.txt> <outPrefix>

Writes
  <outPrefix>.thm.jsonl   one record per exported theorem
  <outPrefix>.pkg.jsonl   one record per structure / class (constructor telescope) and per
                          Prop-valued definition whose body is a conjunction / existential
                          (project AND imported libraries): the candidates that could already
                          package a bundle.

A record is a TELESCOPE: binders `b` (index, name, kind, type key) and ATOMS `a`.
An atom is a Prop-valued binder type, split through top-level `∧`; for the conclusion (and for the
body of a Prop definition) it is split through `∧` and `∃` (the ∃-bound variable becomes a binder
of kind `ex`).  Atom fields: `s` source binder index (-1 = conclusion/body), `k` canonical key
(telescope variable i is written `§i`, instance-implicit arguments and universe levels dropped,
bound variables `#j`), `sz` tree size (same measure as the other exports), `m` all telescope
variables occurring (implicit arguments included), `hd` head constant after peeling, `pe` peel
string, `ng` negation parity, `pos`/`fin` positivity / finiteness shape, `so` order relation on a
set-like carrier, `tc` head is a type class.
-/
import Lean
open Lean Meta

namespace Bundles

def nameStr (n : Name) : String := n.toString (escape := false)

def isZeroLit (e : Expr) : Bool :=
  let e := e.consumeMData
  match e with
  | .lit (.natVal 0) => true
  | _ =>
    if e.isAppOfArity ``OfNat.ofNat 3 then
      match (e.getArg! 1).consumeMData with
      | .lit (.natVal 0) => true
      | x => x.isAppOfArity ``OfNat.ofNat 3 && (x.getArg! 1).consumeMData == .lit (.natVal 0)
    else e.isAppOfArity ``Zero.zero 2

def isTopLit (e : Expr) : Bool := e.consumeMData.isAppOfArity `Top.top 2

/-- Same peeling as Friction.lean. -/
partial def peelProp (e : Expr) (acc : String := "") (neg : Bool := false) : Expr × String × Bool :=
  match e with
  | .mdata _ b => peelProp b acc neg
  | .forallE _ _ b _ => peelProp b (acc.push 'A') neg
  | .letE _ _ v b _ => peelProp (b.instantiate1 v) acc neg
  | _ =>
    if e.getAppFn.isLambda then peelProp e.headBeta acc neg
    else if e.isAppOfArity ``Not 1 then peelProp e.appArg! (acc.push 'N') (!neg)
    else if e.isAppOfArity ``optParam 2 || e.isAppOfArity ``autoParam 2 || e.isAppOfArity ``outParam 1 then
      peelProp (e.getArg! 0) acc neg
    else if e.isAppOfArity `Fact 1 then peelProp e.appArg! (acc.push 'F') neg
    else if e.isAppOfArity ``Exists 2 then
      match e.appArg!.consumeMData with
      | .lam _ _ b _ => peelProp b (acc.push 'E') neg
      | _ => (e, acc, neg)
    else (e, acc, neg)

/-- (pos, fin, subject) exactly as Friction.lean's `shapeOf`. -/
def shapeOfRaw (core : Expr) (neg : Bool) : String × String × Option Expr :=
  let args := core.getAppArgs
  match core.getAppFn.constName?, args.size with
  | some ``LT.lt, 4 =>
    if neg then ("", "", none) else
    if isZeroLit args[2]! then ("lt", "", some args[3]!)
    else if isTopLit args[3]! then ("", "lt_top", some args[2]!) else ("", "", none)
  | some ``GT.gt, 4 =>
    if neg then ("", "", none) else
    if isZeroLit args[3]! then ("lt", "", some args[2]!)
    else if isTopLit args[2]! then ("", "lt_top", some args[3]!) else ("", "", none)
  | some ``LE.le, 4 => if !neg && isZeroLit args[2]! then ("le", "", some args[3]!) else ("", "", none)
  | some ``GE.ge, 4 => if !neg && isZeroLit args[3]! then ("le", "", some args[2]!) else ("", "", none)
  | some ``Ne, 3 =>
    if neg then ("", "", none) else
    if isZeroLit args[2]! then ("ne", "", some args[1]!)
    else if isZeroLit args[1]! then ("ne", "", some args[2]!)
    else if isTopLit args[2]! then ("", "ne_top", some args[1]!)
    else if isTopLit args[1]! then ("", "ne_top", some args[2]!) else ("", "", none)
  | some ``Eq, 3 =>
    if !neg then ("", "", none) else
    if isZeroLit args[2]! then ("ne", "", some args[1]!)
    else if isZeroLit args[1]! then ("ne", "", some args[2]!)
    else if isTopLit args[2]! then ("", "ne_top", some args[1]!)
    else if isTopLit args[1]! then ("", "ne_top", some args[2]!) else ("", "", none)
  | _, _ => ("", "", none)

def shapeOf (core : Expr) (neg : Bool) : String × String :=
  let (p, f, s) := shapeOfRaw core neg
  match s with
  | some x => if (p != "" && isZeroLit x) || (f != "" && isTopLit x) then ("", "") else (p, f)
  | none => (p, f)

def headName (e : Expr) : Name :=
  match e.getAppFn.consumeMData with
  | .const n _ => n
  | .fvar _ => `«<fvar>»
  | .bvar _ => `«<bvar>»
  | .sort _ => `«<sort>»
  | .lam .. => `«<lam>»
  | .forallE .. => `«<forall>»
  | .proj .. => `«<proj>»
  | .letE .. => `«<let>»
  | .lit _ => `«<lit>»
  | _ => `«<other>»

def setTypes : List Name := [`Set, `Finset, `Multiset, `Filter, `Submodule, `Subgroup, `AddSubgroup,
  `Subspace, `MeasurableSpace, `TopologicalSpace, `Submonoid, `AddSubmonoid, `Subalgebra, `Ideal, `Setoid]

def isSetOrder (core : Expr) : Bool :=
  match core.getAppFn.constName? with
  | some n =>
    (n == ``LE.le || n == ``LT.lt || n == ``GE.ge || n == ``GT.gt) && core.getAppNumArgs == 4 &&
      (match (core.getArg! 0).getAppFn.consumeMData with
       | .const t _ => setTypes.contains t
       | _ => false)
  | none => false

/-- Tree node count, same measure as Friction.lean / the corpus exports (mdata transparent). -/
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

def sizeOf' (e : Expr) : Nat := ((treeSize e).run {}).1

def binderInfosOf (env : Environment) (n : Name) : Array BinderInfo :=
  match env.find? n with
  | none => #[]
  | some ci => Id.run do
    let mut t := ci.type
    let mut out := #[]
    let mut go := true
    while go do
      match t with
      | .forallE _ _ b bi => out := out.push bi; t := b
      | .mdata _ b => t := b
      | _ => go := false
    return out

abbrev SerM := StateM (Std.HashMap Name (Array BinderInfo))

partial def ser (env : Environment) (idx : Std.HashMap FVarId Nat) (e : Expr) : SerM String := do
  match e with
  | .mdata _ b => ser env idx b
  | .fvar id => match idx[id]? with
    | some k => return s!"§{k}"
    | none => return "§x"
  | .bvar i => return s!"#{i}"
  | .const n _ => return nameStr n
  | .sort l => return (if l.isZero then "Prop" else "Sort")
  | .lit (.natVal n) => return toString n
  | .lit (.strVal s) => return s.quote
  | .lam _ d b _ => return s!"(λ {← ser env idx d}. {← ser env idx b})"
  | .forallE _ d b _ => return s!"(∀ {← ser env idx d}. {← ser env idx b})"
  | .letE _ t v b _ => return s!"(let {← ser env idx t} := {← ser env idx v}. {← ser env idx b})"
  | .proj s i b => return s!"({nameStr s}.{i} {← ser env idx b})"
  | .mvar _ => return "?m"
  | .app .. =>
    let fn := e.getAppFn
    let args := e.getAppArgs
    let bis ← match fn.consumeMData with
      | .const n _ => do
        match (← get)[n]? with
        | some b => pure b
        | none =>
          let b := binderInfosOf env n
          modify fun s => s.insert n b
          pure b
      | _ => pure #[]
    let mut out := "(" ++ (← ser env idx fn)
    for i in [0:args.size] do
      if i < bis.size && bis[i]!.isInstImplicit then continue
      out := out ++ " " ++ (← ser env idx args[i]!)
    return out ++ ")"

def hexOf (h : UInt64) : String :=
  let s := String.ofList (Nat.toDigits 16 h.toNat)
  "".pushn '0' (16 - s.length) ++ s

partial def stripM : Expr → Expr
  | .mdata _ b => stripM b
  | e => e

def isPropSafe (e : Expr) : MetaM Bool := do
  try isProp e catch _ => return false

structure St where
  idx : Std.HashMap FVarId Nat := {}
  binders : Array Json := #[]
  atoms : Array Json := #[]
  bc : Std.HashMap Name (Array BinderInfo) := {}

abbrev M := StateRefT St MetaM

def serM (e : Expr) : M String := do
  let env ← getEnv
  let s ← get
  let (r, bc) := (ser env s.idx e).run s.bc
  modify fun s => { s with bc := bc }
  return r

def mentionsOf (e : Expr) : M (Array Nat) := do
  let s ← get
  let ids := (collectFVars {} e).fvarIds.filterMap fun f => s.idx[f]?
  return ids.qsort (· < ·)

def biStr : BinderInfo → String
  | .default => "explicit"
  | .implicit => "implicit"
  | .strictImplicit => "strict"
  | .instImplicit => "inst"

def addBinder (x : Expr) (forceKind : Option String := none) : M (Nat × Bool) := do
  let decl ← x.fvarId!.getDecl
  let t := decl.type
  let isP ← isPropSafe t
  let kind := match forceKind with
    | some k => k
    | none => if decl.binderInfo.isInstImplicit then "inst"
              else if isP then "hyp"
              else if (stripM t).isSort then "type" else "term"
  let i := (← get).binders.size
  let sz := sizeOf' t
  let tk ← if sz > 400 then pure ("BIG:" ++ hexOf (hash t)) else serM t
  let (core, _, _) := peelProp t
  let j := Json.mkObj [("i", i), ("n", decl.userName.eraseMacroScopes.toString), ("k", kind),
    ("bi", biStr decl.binderInfo), ("p", isP), ("tk", tk), ("th", nameStr (headName core)), ("sz", sz),
    ("m", toJson (← mentionsOf t))]
  modify fun s => { s with idx := s.idx.insert x.fvarId! i, binders := s.binders.push j }
  return (i, isP)

def addAtom (src : Int) (t : Expr) : M Unit := do
  let env ← getEnv
  let (core, peel, neg) := peelProp t
  let (pos, fin) := shapeOf core neg
  let head := headName core
  let sz := sizeOf' t
  let key ← if sz > 3000 then pure ("BIG:" ++ hexOf (hash t)) else serM t
  let j := Json.mkObj [("s", toJson src), ("k", key), ("sz", sz), ("m", toJson (← mentionsOf t)),
    ("hd", nameStr head), ("pe", peel), ("ng", neg), ("pos", pos), ("fin", fin),
    ("so", toJson (isSetOrder core)), ("tc", toJson (isClass env head))]
  modify fun s => { s with atoms := s.atoms.push j }

/-- split a hypothesis through top-level `∧` only -/
partial def splitAnd (src : Int) (t : Expr) : M Unit := do
  let t := stripM t
  if t.isAppOfArity ``And 2 then
    splitAnd src (t.getArg! 0); splitAnd src (t.getArg! 1)
  else addAtom src t

/-- split a conclusion / definition body through `∧` and `∃` -/
partial def splitConcl (t : Expr) (k : M α) : M α := do
  let t := stripM t
  if t.isAppOfArity ``And 2 then
    splitConcl (t.getArg! 0) (splitConcl (t.getArg! 1) k)
  else if t.isAppOfArity ``Exists 2 then
    match stripM t.appArg! with
    | .lam n d b bi =>
      withLocalDecl n bi d fun x => do
        let _ ← addBinder x (some "ex")
        splitConcl (b.instantiate1 x) k
    | _ => do addAtom (-1) t; k
  else do addAtom (-1) t; k

def addTele (xs : Array Expr) : M Unit := do
  for x in xs do
    let (i, isP) ← addBinder x
    if isP then splitAnd i (← x.fvarId!.getDecl).type

def finish (name : String) (kind : String) (extra : List (String × Json)) : M Json := do
  let s ← get
  return Json.mkObj ([("name", toJson name), ("kind", toJson kind), ("b", toJson s.binders), ("a", toJson s.atoms)] ++ extra)

def thmRecord (n : Name) (ty : Expr) : MetaM Json :=
  (forallTelescope ty fun xs concl => do
    addTele xs
    let nb := (← get).binders.size
    splitConcl concl (finish (nameStr n) "thm" [("size", sizeOf' ty), ("nb", nb), ("csz", sizeOf' concl)])).run' {}

def structRecord (n : Name) (ctor : ConstantInfo) (nparams : Nat) (isCls : Bool) : MetaM Json :=
  (forallTelescope ctor.type fun xs _ => do
    addTele xs
    finish (nameStr n) (if isCls then "class" else "structure") [("np", nparams)]).run' {}

def defRecord (n : Name) (val : Expr) : MetaM (Option Json) :=
  (lambdaTelescope val fun xs body => do
    let body := stripM body
    if !(body.isAppOfArity ``And 2 || body.isAppOfArity ``Exists 2) then return none
    addTele xs
    let np := (← get).binders.size
    let j ← splitConcl body (finish (nameStr n) "def" [("np", np)])
    return some j).run' {}

partial def endsInProp : Expr → Bool
  | .forallE _ _ b _ => endsInProp b
  | .mdata _ b => endsInProp b
  | .sort l => l.isZero
  | _ => false

unsafe def main (args : List String) : IO UInt32 := do
  let [modsFile, rootsS, thmFile, outPrefix] := args
    | throw <| IO.userError "usage: bundles modules.txt roots theorems.txt outPrefix"
  initSearchPath (← findSysroot)
  enableInitializersExecution
  let modNames := ((← IO.FS.lines modsFile).filter (· ≠ "")).map (·.toName)
  let env ← importModules (modNames.map fun m => { module := m }) {} (trustLevel := 1024) (loadExts := true)
  let roots := (rootsS.splitOn ",").map (·.toName)
  let projIdx : Array Bool := env.header.moduleNames.map fun m => roots.contains m.getRoot
  let modStr : Array String := env.header.moduleNames.map (·.toString)
  let isProj (n : Name) : Bool :=
    match env.getModuleIdxFor? n with
    | some i => projIdx[i.toNat]!
    | none => false
  let modOf (n : Name) : String :=
    match env.getModuleIdxFor? n with
    | some i => modStr[i.toNat]!
    | none => ""
  let mut byStr : Std.HashMap String Name := {}
  for (n, _) in env.constants.map₁.toList do
    if isProj n then
      byStr := byStr.insert (n.toString (escape := false)) n
      byStr := byStr.insert n.toString n
  let coreCtx : Core.Context := { fileName := "<bundles>", fileMap := default, maxHeartbeats := 0,
                                  maxRecDepth := 1000000 }
  let runMeta {α} (act : MetaM α) : IO (Except String α) := do
    try
      let (a, _) ← act.run'.toIO coreCtx { env := env }
      return .ok a
    catch e => return .error (toString e)
  -- theorems
  let h ← IO.FS.Handle.mk s!"{outPrefix}.thm.jsonl" .write
  let mut nThm : Nat := 0
  let mut nFail : Nat := 0
  let mut nMissing : Nat := 0
  for l in (← IO.FS.lines thmFile) do
    if l == "" then continue
    let some n := byStr[l]? | nMissing := nMissing + 1; continue
    let some ci := env.find? n | nMissing := nMissing + 1; continue
    match ← runMeta (thmRecord n ci.type) with
    | .ok j => h.putStrLn ((j.setObjVal! "module" (modOf n)).compress); nThm := nThm + 1
    | .error e => nFail := nFail + 1; IO.eprintln s!"FAIL {n}: {e}"
  h.flush
  -- packaging candidates: every structure/class and conjunctive Prop definition in the environment
  let h2 ← IO.FS.Handle.mk s!"{outPrefix}.pkg.jsonl" .write
  let mut nStruct : Nat := 0
  let mut nDef : Nat := 0
  let mut nPkgFail : Nat := 0
  for (n, ci) in env.constants.map₁.toList do
    if n.isInternal then continue
    match ci with
    | .inductInfo iv =>
      if isStructure env n then
        let some cn := iv.ctors.head? | continue
        let some cinfo := env.find? cn | continue
        match ← runMeta (structRecord n cinfo iv.numParams (isClass env n)) with
        | .ok j =>
          h2.putStrLn (((j.setObjVal! "module" (modOf n)).setObjVal! "proj" (isProj n)).compress)
          nStruct := nStruct + 1
        | .error _ => nPkgFail := nPkgFail + 1
    | .defnInfo dv =>
      if endsInProp dv.type then
        match ← runMeta (defRecord n dv.value) with
        | .ok (some j) =>
          h2.putStrLn (((j.setObjVal! "module" (modOf n)).setObjVal! "proj" (isProj n)).compress)
          nDef := nDef + 1
        | .ok none => pure ()
        | .error _ => nPkgFail := nPkgFail + 1
    | _ => pure ()
  h2.flush
  IO.FS.writeFile s!"{outPrefix}.meta.json" (Json.mkObj [("theorems", toJson nThm), ("thmFail", toJson nFail),
    ("thmMissing", toJson nMissing), ("structures", toJson nStruct), ("propDefs", toJson nDef), ("pkgFail", toJson nPkgFail)]).compress
  IO.eprintln s!"theorems {nThm} fail {nFail} missing {nMissing}; structures {nStruct}; prop defs {nDef}; pkg fail {nPkgFail}"
  return 0

end Bundles

unsafe def main (args : List String) : IO UInt32 := Bundles.main args
