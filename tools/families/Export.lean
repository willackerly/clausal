/-
M9 families: feature exporter.

Stand-alone program (imports only `Lean`).  Loads the BUILT environment of a project, read only, and
writes one JSON record per project definition / structure / theorem with a TYPED TREE of its body,
its type signature and (for theorems) its statement.  Everything downstream (shape keys at each
looseness level, anti-unification, API profiles, clustering) is computed from these trees by
`families.py`; nothing is read from source text.

  export <modules.txt> <roots,csv> <outPrefix> <shard> <nshards>

Tree grammar (s-expression).  `tag` is a coarse type tag of the node: `Prop` for a proposition, `U` for
a type, `F>H` for a function into something with head `H`, `$` for a type variable, otherwise the head
constant of the node's type after reducible unfolding (`Real`, `Nat`, `Set`, ...).
  (A tag head arg..)   application; head is a constant name, `$i` (parameter), `#k` (bound var) or a node
  (C tag Name)         constant standing as an argument
  (V tag i)            i-th parameter of the definition
  (B tag k)            bound variable, de Bruijn index k
  (N tag n)            numeric literal n of type `tag`  (`@OfNat.ofNat T n _` or a raw literal)
  (S)                  string literal          (U)  a sort
  *                    erased argument: instance, proof, or a type passed implicitly
  (L T B)              lambda with domain T
  (Q bi T B)           dependent arrow / universal quantifier, bi in d,i,s,c (default, implicit, strict, class)
  (I A B)              implication between propositions
  (K A B ..)           conjunction, flattened
Normalisations (choices, same as the M7 exporter): metadata and `let` removed, beta and eta reduced,
`a > b` written `b < a`, `a ≥ b` written `b ≤ a`, `a ≠ b` written `¬ a = b`, optParam/outParam/autoParam
stripped, primitive projections written as the projection function.  In definition BODIES and type
signatures project-local `@[reducible]` definitions are unfolded; in theorem statements they are not
(a definition must stay visible in the statements proved about it).
Structures: a data field is written `∃ field : T, rest`, a run of Prop fields as a conjunction, so a
structure and a hand-written `∃ C, 0 ≤ C ∧ ...` predicate have comparable bodies.
-/
import Lean
open Lean Meta

namespace Families

def nameStr (n : Name) : String :=
  let s := n.toString (escape := false)
  if s.any (fun c => c == ' ' || c == '(' || c == ')' || c == '"' || c == '\n') then "?bad" else s

structure Ctx where
  isProj : Name → Bool
  maxNodes : Nat := 4000
  fv : Std.HashMap FVarId (Bool × Nat) := {}
  depth : Nat := 0
  unfoldAbbrev : Bool := false

structure St where
  nodes : Nat := 0
  binfo : Std.HashMap Name (Array BinderInfo) := {}
  unfolded : Array Name := #[]

abbrev SkM := ReaderT Ctx (StateRefT St MetaM)

def tick : SkM Unit := do
  modify fun s => { s with nodes := s.nodes + 1 }
  if (← get).nodes > (← read).maxNodes then throwError "too big"

def binfos (c : Name) : SkM (Array BinderInfo) := do
  if let some b := (← get).binfo[c]? then return b
  let ci ← getConstInfo c
  let rec go (t : Expr) (acc : Array BinderInfo) : Array BinderInfo :=
    match t with
    | .forallE _ _ b bi => go b (acc.push bi)
    | .mdata _ b => go b acc
    | _ => acc
  let b := go ci.type #[]
  modify fun s => { s with binfo := s.binfo.insert c b }
  return b

def isTypeish (t : Expr) : Bool := t.getForallBody.consumeMData.isSort

def headTag (t : Expr) : String :=
  match t.consumeMData.getAppFn with
  | .const n _ => nameStr n
  | .fvar _ => "$"
  | .sort .zero => "Prop"
  | .sort _ => "U"
  | .bvar _ => "$"
  | _ => "?"

def tagOfType (t : Expr) : MetaM String := do
  let t ← try whnfR t catch _ => pure t
  match t with
  | .sort .zero => return "Prop"
  | .sort _ => return "U"
  | .forallE .. => return "F>" ++ headTag t.getForallBody
  | _ => return headTag t

def tagOf (e : Expr) : MetaM String := do
  try tagOfType (← inferType e) catch _ => return "?"

def fvTok (id : FVarId) : SkM (Option (Bool × Nat)) := do
  match (← read).fv[id]? with
  | some (true, i) => return some (true, i)
  | some (false, lvl) => return some (false, (← read).depth - 1 - lvl)
  | none => return none

def pushBound (x : Expr) (c : Ctx) : Ctx :=
  { c with fv := c.fv.insert x.fvarId! (false, c.depth), depth := c.depth + 1 }

def shouldUnfold (c : Name) : SkM Bool := do
  let r ← read
  unless r.unfoldAbbrev && r.isProj c do return false
  let env ← getEnv
  let some ci := env.find? c | return false
  unless ci matches .defnInfo _ do return false
  if isInstanceCore env c then return false
  if c.isInternalDetail then return false
  return (← getReducibilityStatus c) == .reducible

def biStr : BinderInfo → String
  | .default => "d" | .implicit => "i" | .strictImplicit => "s" | .instImplicit => "c"

mutual
partial def sk (e : Expr) : SkM String := do
  tick
  match e with
  | .mdata _ b => sk b
  | .letE _ _ v b _ => sk (b.instantiate1 v)
  | .sort _ => pure "(U)"
  | .mvar _ => pure "*"
  | .bvar _ => pure "*"
  | .lit (.natVal n) => pure s!"(N Nat {n})"
  | .lit (.strVal _) => pure "(S)"
  | .fvar id =>
    match ← fvTok id with
    | some (true, i) => pure s!"(V {← tagOf e} {i})"
    | some (false, k) => pure s!"(B {← tagOf e} {k})"
    | none => pure "*"
  | .const n _ =>
    if (← shouldUnfold n) then
      let ci ← getConstInfo n
      if let some v := ci.value? then
        if !v.hasLevelParam || true then
          modify fun s => { s with unfolded := s.unfolded.push n }
          return ← sk (v.instantiateLevelParams ci.levelParams (e.constLevels!))
    pure s!"(C {← tagOf e} {nameStr n})"
  | .lam n d b bi =>
    let e' := e.eta
    if !e'.isLambda then sk e' else
    let ds ← sk d
    withLocalDecl n bi d fun x => do
      let bs ← withReader (pushBound x) (sk (b.instantiate1 x))
      pure s!"(L {ds} {bs})"
  | .forallE n d b bi =>
    if !b.hasLooseBVars && (← isProp d) && (← isProp b) then
      pure s!"(I {← sk d} {← sk b})"
    else
      let ds ← sk d
      withLocalDecl n bi d fun x => do
        let bs ← withReader (pushBound x) (sk (b.instantiate1 x))
        pure s!"(Q {biStr bi} {ds} {bs})"
  | .proj S i s =>
    let env ← getEnv
    let nm : String :=
      if isStructure env S then
        let fs := getStructureFields env S
        if h : i < fs.size then nameStr (S ++ fs[i]) else s!"{nameStr S}._{i}"
      else s!"{nameStr S}._{i}"
    let np := match env.find? S with
      | some (.inductInfo iv) => iv.numParams
      | _ => 0
    let stars := String.join (List.replicate np " *")
    let ss ← sk s
    pure s!"(A {← tagOf e} {nm}{stars} {ss})"
  | .app .. => skApp e

partial def conjuncts (e : Expr) (acc : Array Expr) : Array Expr :=
  let e := e.consumeMData
  if e.isAppOfArity ``And 2 then conjuncts (e.getArg! 1) (conjuncts (e.getArg! 0) acc) else acc.push e

partial def skApp (e : Expr) : SkM String := do
  let f := e.getAppFn
  let args := e.getAppArgs
  if f.isLambda || f.isMData || f.isLet then return ← sk (mkAppN f.consumeMData args).headBeta
  if let .const c us := f then
    if c == ``GT.gt && args.size == 4 then
      return ← sk (mkAppN (.const ``LT.lt us) #[args[0]!, args[1]!, args[3]!, args[2]!])
    if c == ``GE.ge && args.size == 4 then
      return ← sk (mkAppN (.const ``LE.le us) #[args[0]!, args[1]!, args[3]!, args[2]!])
    if c == ``Ne && args.size == 3 then
      return ← sk (mkApp (.const ``Not []) (mkAppN (.const ``Eq us) args))
    if (c == ``optParam || c == ``outParam || c == ``autoParam) && args.size ≥ 1 then
      return ← sk args[0]!
    if c == ``OfNat.ofNat && args.size == 3 then
      if let .lit (.natVal n) := args[1]!.consumeMData then
        return s!"(N {← tagOfType args[0]!} {n})"
    if c == ``And && args.size == 2 then
      let cs := conjuncts e #[]
      let mut out := "(K"
      for x in cs do out := out ++ " " ++ (← sk x)
      return out ++ ")"
    if (← shouldUnfold c) then
      let ci ← getConstInfo c
      if let some v := ci.value? then
        if us.length == ci.levelParams.length then
          modify fun s => { s with unfolded := s.unfolded.push c }
          return ← sk ((v.instantiateLevelParams ci.levelParams us).beta args)
  let (hd, bis) ← match f with
    | .const c _ => pure (nameStr c, ← binfos c)
    | .fvar id => match ← fvTok id with
      | some (true, i) => pure (s!"${i}", #[])
      | some (false, k) => pure (s!"#{k}", #[])
      | none => pure ("*", #[])
    | _ => pure (← sk f, #[])
  let mut out := ""
  for i in [0:args.size] do
    let a := args[i]!
    let bi := bis.getD i .default
    if bi == .instImplicit then out := out ++ " *"
    else
      let t ← inferType a
      if (← isProp t) then out := out ++ " *"
      else if bi != .default && isTypeish t then out := out ++ " *"
      else if bi != .default && (← isClass? t).isSome then out := out ++ " *"
      else out := out ++ " " ++ (← sk a)
  pure s!"(A {← tagOf e} {hd}{out})"
end

def paramKind (x : Expr) : MetaM String := do
  let d ← x.fvarId!.getDecl
  let t := d.type
  if d.binderInfo == .instImplicit || (← isClass? t).isSome then return "i"
  if isTypeish t then return "t"
  if (← isProp t) then return "h"
  return "v"

def mkCtx (isProj : Name → Bool) (xs : Array Expr) (unfoldAbbrev : Bool) (maxNodes : Nat) : Ctx := Id.run do
  let mut fv : Std.HashMap FVarId (Bool × Nat) := {}
  for i in [0:xs.size] do fv := fv.insert xs[i]!.fvarId! (true, i)
  return { isProj, fv, unfoldAbbrev, maxNodes }

def runSk (ctx : Ctx) (e : Expr) : MetaM (Option (String × Nat × Array Name)) := do
  try
    let (s, st) ← ((sk e).run ctx).run {}
    return some (s, st.nodes, st.unfolded)
  catch _ => return none

def jstrs (a : Array String) : Json := Json.arr (a.map Json.str)

def lastStr (n : Name) : String := match n with
  | .str _ s => s
  | _ => ""

def irreducibleBody? (env : Environment) (v : Expr) : Option Name := Id.run do
  let cs := v.getUsedConstants
  if cs.size > 12 then return none
  for c in cs do
    if let some ci := env.find? c then
      let t := ci.type
      if let .const w _ := t.getAppFn then
        if lastStr w == "Wrapper" && t.getAppNumArgs ≥ 1 then
          if let .const d _ := t.appArg!.getAppFn then return some d
  -- hygienic form: `L := wrapped✝.1`, `wrapped✝ : { b // b = @definition✝ }`
  for c in cs do
    if (c.toString.splitOn "wrapped").length > 1 then
      if let some ci := env.find? c then
        for d in ci.type.getUsedConstants do
          if (d.toString.splitOn "definition").length > 1 then return some d
  return none

def ppShort (e : Expr) (lim : Nat := 700) : MetaM String := do
  try
    let f ← ppExpr e
    let s := f.pretty 110
    return if s.length > lim then (s.take lim).toString ++ " …" else s
  catch _ => return ""

def skipName (env : Environment) (n : Name) : Bool :=
  n.isInternalDetail || isAuxRecursor env n || isNoConfusion env n || isMatcherCore env n ||
    env.isProjectionFn n || isRecCore env n

/-- parameters: kind, name, tag of the type, tree of the type (earlier parameters are `(V ..)`) -/
def paramsJson (isProj : Name → Bool) (xs : Array Expr) : MetaM Json := do
  let mut out := #[]
  for i in [0:xs.size] do
    let x := xs[i]!
    let d ← x.fvarId!.getDecl
    let ctx := mkCtx isProj (xs.extract 0 i) true 600
    let t := match ← runSk ctx d.type with
      | some (s, _, _) => s
      | none => "(BIG)"
    out := out.push (Json.mkObj [("k", ← paramKind x), ("n", d.userName.toString (escape := false)),
      ("bi", biStr d.binderInfo), ("t", t)])
  return Json.arr out

def emitDefn (isProj : Name → Bool) (modS : String) (n : Name) (ci : ConstantInfo) (v0 : Expr) :
    MetaM (Option Json) := do
  let env ← getEnv
  let (v, kind) := match irreducibleBody? env v0 with
    | some d => match (env.find? d).bind (·.value?) with
      | some v' => (v', "irreducible_def")
      | none => (v0, "def")
    | none => (v0, "def")
  let red ← getReducibilityStatus n
  let kind := if kind == "def" && red == .reducible then "abbrev" else kind
  lambdaTelescope v fun xs body => do
    let bt ← inferType body
    let isP ← isProp body
    let rtag ← tagOfType bt
    let ps ← paramsJson isProj xs
    let isRec := ci.isPartial || (body.find? fun e => e.isConst && (lastStr e.constName! == "brecOn" ||
        lastStr e.constName! == "rec" || lastStr e.constName! == "fix")).isSome
    let mut fields : List (String × Json) := [("rec", "def"), ("name", nameStr n), ("module", modS),
      ("kind", kind), ("isProp", isP), ("rtag", rtag), ("params", ps), ("isRec", isRec),
      ("pp", Json.str (← ppShort ci.type 500)), ("ppBody", Json.str (← ppShort body 700))]
    match ← runSk (mkCtx isProj xs true 4000) body with
    | some (s, nn, unf) =>
      fields := fields ++ ([("body", Json.str s), ("nodes", toJson nn), ("unf", jstrs (unf.map nameStr))] : List (String × Json))
    | none => fields := fields ++ ([("big", Json.bool true)] : List (String × Json))
    if let some (s, _, _) ← runSk (mkCtx isProj xs true 600) bt then
      fields := fields ++ ([("rty", Json.str s)] : List (String × Json))
    return some (Json.mkObj fields)

def emitStruct (isProj : Name → Bool) (modS : String) (n : Name) (iv : InductiveVal) :
    MetaM (Option Json) := do
  let env ← getEnv
  let some ctor := iv.ctors.head? | return none
  let cinfo ← getConstInfo ctor
  forallTelescope cinfo.type fun xs _ => do
    let ps := xs.extract 0 iv.numParams
    let fs := xs.extract iv.numParams xs.size
    let psJ ← paramsJson isProj ps
    let mut isPf := #[]
    for f in fs do isPf := isPf.push (← isProp (← inferType f))
    let nData := (isPf.filter (!·)).size
    let rec go (i : Nat) (ctx : Ctx) (fuel : Nat) : StateRefT St MetaM String := do
      match fuel with
      | 0 => return "*"
      | fuel + 1 =>
      if i ≥ fs.size then return "(C Prop True)"
      let t ← inferType fs[i]!
      if isPf[i]! then
        let mut j := i
        let mut parts := #[]
        while j < fs.size && isPf[j]! do
          parts := parts.push (← (sk (← inferType fs[j]!)).run ctx)
          j := j + 1
        if j < fs.size then parts := parts.push (← go j ctx fuel)
        if parts.size == 1 then return parts[0]!
        return "(K " ++ " ".intercalate parts.toList ++ ")"
      else
        let ts ← (sk t).run ctx
        let rest ← go (i + 1) (pushBound fs[i]! ctx) fuel
        return s!"(A Prop Exists (L {ts} {rest}))"
    let ctx := mkCtx isProj ps true 4000
    let r ← try
        let (s, st) ← (go 0 ctx (fs.size + 2)).run {}
        pure (some (s, st.nodes, st.unfolded))
      catch _ => pure none
    let selfT := mkAppN (.const n (iv.levelParams.map mkLevelParam)) ps
    let isP ← isProp selfT
    let mut fnames := #[]
    for f in fs do fnames := fnames.push ((← f.fvarId!.getDecl).userName.toString (escape := false))
    let mut fields : List (String × Json) := [("rec", "def"), ("name", nameStr n), ("module", modS),
      ("kind", if isClass env n then "class" else "structure"), ("isProp", isP),
      ("rtag", if isP then "Prop" else "U"), ("params", psJ), ("isRec", false),
      ("nfields", fs.size), ("ndata", nData), ("fields", jstrs fnames),
      ("pp", Json.str (← ppShort cinfo.type 700)), ("ppBody", "")]
    match r with
    | some (s, nn, unf) =>
      fields := fields ++ ([("body", Json.str s), ("nodes", toJson nn), ("unf", jstrs (unf.map nameStr))] : List (String × Json))
    | none => fields := fields ++ ([("big", Json.bool true)] : List (String × Json))
    fields := fields ++ ([("rty", Json.str (if isP then "(C U Prop)" else "(U)"))] : List (String × Json))
    return some (Json.mkObj fields)

def emitThm (isProj : Name → Bool) (modS : String) (n : Name) (ci : ConstantInfo) : MetaM (Option Json) := do
  let ctx := mkCtx isProj #[] false 2500
  let mut fields : List (String × Json) := [("rec", "thm"), ("name", nameStr n), ("module", modS)]
  match ← runSk ctx ci.type with
  | some (s, nn, _) => fields := fields ++ ([("st", Json.str s), ("nodes", toJson nn)] : List (String × Json))
  | none => fields := fields ++ ([("big", Json.bool true)] : List (String × Json))
  -- project constants of the statement, read from the term (instances and erased arguments included)
  let cs := ci.type.getUsedConstants.filter isProj
  fields := fields ++ ([("pc", jstrs (cs.map nameStr))] : List (String × Json))
  return some (Json.mkObj fields)

unsafe def main (args : List String) : IO UInt32 := do
  let (modsFile, rootsS, outPrefix, shardS, nshardS) ← match args with
    | [a, b, c, d, e] => pure (a, b, c, d, e)
    | _ => throw <| IO.userError "usage: export modules.txt roots outPrefix shard nshards"
  let shard := shardS.toNat!
  let nshards := nshardS.toNat!
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
  let opts : Options := ({} : Options).setBool `pp.unicode.fun true
  let coreCtx : Core.Context := { fileName := "<families>", fileMap := default, maxHeartbeats := 0, options := opts }
  let runM {α} (x : MetaM (Option α)) : IO (Option α) := do
    try
      let (a, _) ← x.run'.toIO coreCtx { env := env }
      return a
    catch _ => return none
  let h ← IO.FS.Handle.mk s!"{outPrefix}.{shard}.jsonl" .write
  let all := ((env.constants.map₁.toList.map (·.1)).filter isProj).toArray.qsort (fun a b => a.toString < b.toString)
  let mut written := 0
  let mut failed := 0
  let mut nInst := 0
  let mut nClassValued := 0
  let mut k := 0
  for n in all do
    k := k + 1
    unless k % nshards == shard do continue
    let some ci := env.find? n | continue
    match ci with
    | .defnInfo dv =>
      if skipName env n then continue
      if isInstanceCore env n then nInst := nInst + 1; continue
      let cv ← runM (do return some (← forallTelescope ci.type fun _ b => do return (← isClass? b).isSome))
      if cv == some true then nClassValued := nClassValued + 1; continue
      match ← runM (emitDefn isProj (modOf n) n ci dv.value) with
      | some j => h.putStrLn j.compress; written := written + 1
      | none => failed := failed + 1; h.putStrLn (Json.mkObj [("rec", "fail"), ("name", nameStr n)]).compress
    | .inductInfo iv =>
      if n.isInternalDetail then continue
      if isStructure env n && iv.numIndices == 0 then
        match ← runM (emitStruct isProj (modOf n) n iv) with
        | some j => h.putStrLn j.compress; written := written + 1
        | none => failed := failed + 1; h.putStrLn (Json.mkObj [("rec", "fail"), ("name", nameStr n)]).compress
      else
        h.putStrLn (Json.mkObj [("rec", "inductive"), ("name", nameStr n), ("module", modOf n)]).compress
    | .thmInfo _ =>
      if n.isInternalDetail then continue
      match ← runM (emitThm isProj (modOf n) n ci) with
      | some j => h.putStrLn j.compress; written := written + 1
      | none => failed := failed + 1; h.putStrLn (Json.mkObj [("rec", "fail"), ("name", nameStr n)]).compress
    | _ => pure ()
  h.flush
  IO.eprintln s!"shard {shard}: {written} records, {failed} failed, {nInst} instances skipped, {nClassValued} class-valued defs skipped"
  return 0

end Families

unsafe def main (args : List String) : IO UInt32 := Families.main args
