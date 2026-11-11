/-
M7 re-invented abstractions: skeleton exporter.

Stand-alone program (imports only `Lean`).  Loads the BUILT environment of a project (read only) and
writes, for the matcher in `reinvent.py`, a "skeleton" of definition bodies and theorem statements.

  export <modules.txt> <roots,csv> <outPrefix> <shard> <nshards> <mode> [names.txt]

mode `defs`     : definitions and structures (project and library), and "characterisation" theorems
                  `∀ xs, L xs ↔ R` / `L xs = R` (an alternative body for the notion L)
mode `defsproj` : the same, project constants only
mode `thms`     : statement skeletons of project theorems, and of library theorems that mention a
                  constant listed in names.txt

Skeleton grammar (s-expression, one string):
  $i            i-th parameter of the definition / i-th leading binder of the theorem
  #k            bound variable, de Bruijn index k
  %n  %s        literal
  *             erased argument: instance, proof, or a type passed implicitly
  Name          constant (not Prop-valued)
  (p H a..)     Prop-valued application of head H (constant, $i, #k or a nested term)
  (a H a..)     other application
  (\ T B)       lambda with domain T
  (! T B)       dependent arrow / universal quantifier
  (> A B)       implication between propositions
  (& A B ..)    conjunction, flattened (also the Prop fields of a structure)
Normalisations (stated because they are choices): metadata and `let` removed, beta and eta reduced,
`a > b` written `b < a`, `a ≥ b` written `b ≤ a`, `a ≠ b` written `¬ a = b`, optParam/outParam/autoParam
stripped, primitive projections written as the projection function.  For PROJECT definitions,
project-local `@[reducible]` definitions are unfolded (body level 0); `body1` additionally unfolds
project-local non-reducible definitions, one level.
-/
import Lean
open Lean Meta

namespace Reinvent

def nameStr (n : Name) : String :=
  let s := n.toString (escape := false)
  if s.any (fun c => c == ' ' || c == '(' || c == ')' || c == '"' || c == '\n') then "?bad" else s

structure Cfg where
  isProj : Name → Bool
  maxNodes : Nat := 400

structure Ctx where
  cfg : Cfg
  fv : Std.HashMap FVarId (Bool × Nat) := {}
  depth : Nat := 0
  unfoldAbbrev : Bool := false
  budget : Nat := 0

structure St where
  nodes : Nat := 0
  binfo : Std.HashMap Name (Array BinderInfo) := {}
  unfolded : Array Name := #[]

abbrev SkM := ReaderT Ctx (StateRefT St MetaM)

def tick : SkM Unit := do
  modify fun s => { s with nodes := s.nodes + 1 }
  if (← get).nodes > (← read).cfg.maxNodes then throwError "too big"

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

def fvTok (id : FVarId) : SkM String := do
  match (← read).fv[id]? with
  | some (true, i) => return s!"${i}"
  | some (false, lvl) => return s!"#{(← read).depth - 1 - lvl}"
  | none => return "*"

def lastStr (n : Name) : String := match n with
  | .str _ s => s
  | _ => ""

def isTypeish (t : Expr) : Bool := t.getForallBody.consumeMData.isSort

def pushBound (x : Expr) (c : Ctx) : Ctx :=
  { c with fv := c.fv.insert x.fvarId! (false, c.depth), depth := c.depth + 1 }

def shouldUnfold (c : Name) : SkM (Option Nat) := do
  let r ← read
  unless r.unfoldAbbrev && r.cfg.isProj c do return none
  let env ← getEnv
  let some ci := env.find? c | return none
  unless ci matches .defnInfo _ do return none
  if isInstanceCore env c then return none
  if c.isInternalDetail then return none
  if (← getReducibilityStatus c) == .reducible then return some r.budget
  if r.budget > 0 then return some (r.budget - 1)
  return none

mutual
partial def sk (e : Expr) : SkM String := do
  tick
  match e with
  | .mdata _ b => sk b
  | .letE _ _ v b _ => sk (b.instantiate1 v)
  | .sort _ => pure "*"
  | .mvar _ => pure "*"
  | .bvar _ => pure "*"
  | .lit (.natVal n) => pure s!"%{n}"
  | .lit (.strVal _) => pure "%s"
  | .fvar id =>
    let tok ← fvTok id
    if (← isProp e) then pure s!"(p {tok})" else pure tok
  | .const n _ =>
    if (← isProp e) then pure s!"(p {nameStr n})" else pure (nameStr n)
  | .lam n d b bi =>
    let e' := e.eta
    if !e'.isLambda then sk e' else
    let ds ← sk d
    withLocalDecl n bi d fun x => do
      let bs ← withReader (pushBound x) (sk (b.instantiate1 x))
      pure s!"(\\ {ds} {bs})"
  | .forallE n d b bi =>
    if !b.hasLooseBVars && (← isProp d) then
      pure s!"(> {← sk d} {← sk b})"
    else
      let ds ← sk d
      withLocalDecl n bi d fun x => do
        let bs ← withReader (pushBound x) (sk (b.instantiate1 x))
        pure s!"(! {ds} {bs})"
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
    let hd := if (← isProp e) then "p" else "a"
    pure s!"({hd} {nm}{stars} {ss})"
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
    if c == ``And && args.size == 2 then
      let cs := conjuncts e #[]
      let mut out := "(&"
      for x in cs do out := out ++ " " ++ (← sk x)
      return out ++ ")"
    if let some b ← shouldUnfold c then
      let ci ← getConstInfo c
      if let some v := ci.value? then
        if us.length == ci.levelParams.length then
          modify fun s => { s with unfolded := s.unfolded.push c }
          return ← withReader (fun r => { r with budget := b })
            (sk ((v.instantiateLevelParams ci.levelParams us).beta args))
  let (hd, bis) ← match f with
    | .const c _ => pure (nameStr c, ← binfos c)
    | .fvar id => pure (← fvTok id, #[])
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
  let tag := if (← isProp e) then "p" else "a"
  pure s!"({tag} {hd}{out})"
end

def paramKind (x : Expr) : MetaM String := do
  let d ← x.fvarId!.getDecl
  let t := d.type
  if d.binderInfo == .instImplicit || (← isClass? t).isSome then return "i"
  if isTypeish t then return "t"
  if (← isProp t) then return "h"
  return "v"

def runSk (cfg : Cfg) (xs : Array Expr) (unfoldAbbrev : Bool) (budget : Nat) (e : Expr) :
    MetaM (Option (String × Nat × Array Name)) := do
  let mut fv : Std.HashMap FVarId (Bool × Nat) := {}
  for i in [0:xs.size] do fv := fv.insert xs[i]!.fvarId! (true, i)
  let ctx : Ctx := { cfg, fv, unfoldAbbrev, budget }
  try
    let (s, st) ← ((sk e).run ctx).run {}
    return some (s, st.nodes, st.unfolded)
  catch _ => return none

def jstrs (a : Array String) : Json := Json.arr (a.map Json.str)

def paramJson (xs : Array Expr) : MetaM (Json × Json) := do
  let mut ks := #[]
  let mut ns := #[]
  for x in xs do
    ks := ks.push (← paramKind x)
    ns := ns.push ((← x.fvarId!.getDecl).userName.toString (escape := false))
  return (jstrs ks, jstrs ns)

/-- The real body of a Mathlib `irreducible_def`: `L := wrapped.1`, `wrapped : Wrapper @definition`. -/
def irreducibleBody? (env : Environment) (v : Expr) : Option Name := Id.run do
  let cs := v.getUsedConstants
  if cs.size > 3 then return none
  for c in cs do
    if let some ci := env.find? c then
      let t := ci.type
      if let .const w _ := t.getAppFn then
        if lastStr w == "Wrapper" && t.getAppNumArgs ≥ 1 then
          if let .const d _ := t.appArg!.getAppFn then return some d
  return none

def ppShort (e : Expr) (lim : Nat := 700) : MetaM String := do
  try
    let f ← ppExpr e
    let s := f.pretty 100
    return if s.length > lim then (s.take lim).toString ++ " …" else s
  catch _ => return ""

def skipName (env : Environment) (n : Name) : Bool :=
  n.isInternalDetail || isAuxRecursor env n || isNoConfusion env n || isMatcherCore env n ||
    env.isProjectionFn n || isRecCore env n

def emitDefn (cfg : Cfg) (isProj : Bool) (modS : String) (n : Name) (ci : ConstantInfo) (v0 : Expr) :
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
    let (ks, ns) ← paramJson xs
    let some (s0, n0, _) ← runSk cfg xs isProj 0 body | return none
    let isP ← isProp body
    let mut fields : List (String × Json) := [("name", nameStr n), ("module", modS), ("proj", isProj),
      ("kind", kind), ("isProp", isP), ("pk", ks), ("pn", ns), ("body", s0), ("nodes", n0),
      ("rec", ci.isPartial || (body.find? fun e => e.isConst && (lastStr e.constName! == "brecOn" ||
        lastStr e.constName! == "rec" || lastStr e.constName! == "fix")).isSome)]
    if isProj then
      if let some (s1, n1, unf) ← runSk cfg xs true 1 body then
        if s1 != s0 then
          fields := fields ++ ([("body1", Json.str s1), ("nodes1", toJson n1), ("unf", jstrs (unf.map nameStr))] : List (String × Json))
      fields := fields ++ ([("pp", Json.str (← ppShort (← mkForallFVars xs (← inferType body)) 400))] : List (String × Json))
    return some (Json.mkObj fields)

def emitStruct (cfg : Cfg) (isProj : Bool) (modS : String) (n : Name) (iv : InductiveVal) :
    MetaM (Option Json) := do
  let env ← getEnv
  let some ctor := iv.ctors.head? | return none
  let cinfo ← getConstInfo ctor
  forallTelescope cinfo.type fun xs _ => do
    let ps := xs.extract 0 iv.numParams
    let fs := xs.extract iv.numParams xs.size
    let (ks, ns) ← paramJson ps
    let mut fv : Std.HashMap FVarId (Bool × Nat) := {}
    for i in [0:ps.size] do fv := fv.insert ps[i]!.fvarId! (true, i)
    -- nested encoding: data field = existential binder, run of Prop fields = conjunction
    let mut isPf := #[]
    for f in fs do isPf := isPf.push (← isProp (← inferType f))
    let nData := (isPf.filter (!·)).size
    let rec go (i : Nat) (ctx : Ctx) (fuel : Nat) : StateRefT St MetaM String := do
      match fuel with
      | 0 => return "*"
      | fuel + 1 =>
      if i ≥ fs.size then return "(p True)"
      let t ← inferType fs[i]!
      if isPf[i]! then
        let mut j := i
        let mut parts := #[]
        while j < fs.size && isPf[j]! do
          parts := parts.push (← (sk (← inferType fs[j]!)).run ctx)
          j := j + 1
        if j < fs.size then parts := parts.push (← go j ctx fuel)
        if parts.size == 1 then return parts[0]!
        return "(& " ++ " ".intercalate parts.toList ++ ")"
      else
        let ts ← (sk t).run ctx
        let rest ← go (i + 1) (pushBound fs[i]! ctx) fuel
        return s!"(p Exists (\\ {ts} {rest}))"
    let ctx : Ctx := { cfg, fv }
    let r ← try
        let (s, st) ← (go 0 ctx (fs.size + 2)).run {}
        pure (some (s, st.nodes))
      catch _ => pure none
    let some (s, nodes) := r | return none
    let isP ← isProp (mkAppN (.const n (iv.levelParams.map mkLevelParam)) ps)
    let mut fields : List (String × Json) := [("name", nameStr n), ("module", modS), ("proj", isProj),
      ("kind", if isClass env n then "class" else "structure"), ("isProp", isP), ("pk", ks), ("pn", ns),
      ("body", s), ("nodes", nodes), ("nfields", fs.size), ("ndata", nData)]
    if isProj then
      fields := fields ++ ([("pp", Json.str (← ppShort cinfo.type 400))] : List (String × Json))
    return some (Json.mkObj fields)

/-- `∀ xs, L as ↔ R` or `L as = R` with the value arguments of `L` distinct variables. -/
def emitChar (cfg : Cfg) (isProj : Bool) (modS : String) (n : Name) (ci : ConstantInfo) :
    MetaM (Option Json) := do
  let env ← getEnv
  forallTelescope ci.type fun xs body => do
    let body := body.consumeMData
    let (lhs, rhs, rel) ←
      if body.isAppOfArity ``Iff 2 then pure (body.getArg! 0, body.getArg! 1, "iff")
      else if body.isAppOfArity ``Eq 3 then pure (body.getArg! 1, body.getArg! 2, "eq")
      else return none
    let .const L _ := lhs.getAppFn | return none
    let some lci := env.find? L | return none
    let okKind := match lci with
      | .defnInfo _ => !env.isProjectionFn L && !isInstanceCore env L
      | .inductInfo _ => true
      | _ => false
    unless okKind do return none
    if L.isInternalDetail then return none
    let (ksJ, nsJ) ← paramJson xs
    let mut kinds := #[]
    for x in xs do kinds := kinds.push (← paramKind x)
    if kinds.contains "h" then return none
    let args := lhs.getAppArgs
    let mut argmap : Array Int := #[]
    let mut seen : Array Nat := #[]
    for a in args do
      let a := a.consumeMData
      match (if a.isFVar then xs.findIdx? (· == a) else none) with
      | some i =>
        if kinds[i]! == "v" then
          if seen.contains i then return none
          seen := seen.push i
        argmap := argmap.push i
      | none =>
        let t ← inferType a
        if isTypeish t || (← isClass? t).isSome || (← isProp t) then argmap := argmap.push (-1)
        else return none
    -- every value variable of the theorem must be an argument of L
    for i in [0:xs.size] do
      if kinds[i]! == "v" && !seen.contains i then return none
    if seen.isEmpty then return none
    let some (s, nodes, _) ← runSk { cfg with maxNodes := 150 } xs false 0 rhs | return none
    if nodes < 2 then return none
    let isP ← isProp rhs
    return some (Json.mkObj [("kind", "char"), ("name", nameStr L), ("thm", nameStr n), ("module", modS),
      ("proj", isProj), ("rel", rel), ("isProp", isP), ("pk", ksJ), ("pn", nsJ),
      ("argmap", Json.arr (argmap.map fun i => Json.num (JsonNumber.fromInt i))),
      ("body", s), ("nodes", nodes)])

def emitThm (cfg : Cfg) (isProj : Bool) (modS : String) (n : Name) (ci : ConstantInfo) (withPP : Bool) :
    MetaM (Option Json) := do
  forallTelescope ci.type fun xs concl => do
    let (ks, _) ← paramJson xs
    let mut fv : Std.HashMap FVarId (Bool × Nat) := {}
    for i in [0:xs.size] do fv := fv.insert xs[i]!.fvarId! (true, i)
    let ctx : Ctx := { cfg := { cfg with maxNodes := 500 }, fv }
    let r ← try
        let act : SkM (Array Json × String) := do
          let mut hyps : Array Json := #[]
          for i in [0:xs.size] do
            let t ← inferType xs[i]!
            if (← isProp t) then
              hyps := hyps.push (Json.arr #[Json.num i, Json.str (← sk t)])
          let c ← sk concl
          return (hyps, c)
        let (x, _) ← (act.run ctx).run {}
        pure (some x)
      catch _ => pure none
    let some (hyps, c) := r | return none
    let mut fields : List (String × Json) := [("name", nameStr n), ("module", modS), ("proj", isProj),
      ("pk", ks), ("hyps", Json.arr hyps), ("concl", c)]
    if withPP then fields := fields ++ ([("pp", Json.str (← ppShort ci.type 600))] : List (String × Json))
    return some (Json.mkObj fields)

unsafe def main (args : List String) : IO UInt32 := do
  let (modsFile, rootsS, outPrefix, shardS, nshardS, mode, namesFile) ← match args with
    | [a, b, c, d, e, f] => pure (a, b, c, d, e, f, "")
    | [a, b, c, d, e, f, g] => pure (a, b, c, d, e, f, g)
    | _ => throw <| IO.userError "usage: export modules.txt roots outPrefix shard nshards mode [names.txt]"
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
  let mut wanted : Std.HashSet Name := {}
  if namesFile != "" then
    let mut byStr : Std.HashMap String Name := {}
    for (n, _) in env.constants.map₁.toList do
      byStr := byStr.insert (n.toString (escape := false)) n
    for l in (← IO.FS.lines namesFile) do
      if let some n := byStr[l]? then wanted := wanted.insert n
  let cfg : Cfg := { isProj }
  let opts : Options := ({} : Options).setBool `pp.unicode.fun true
  let coreCtx : Core.Context := { fileName := "<reinvent>", fileMap := default, maxHeartbeats := 0, options := opts }
  let runM {α} (x : MetaM (Option α)) : IO (Option α) := do
    try
      let (a, _) ← x.run'.toIO coreCtx { env := env }
      return a
    catch _ => return none
  let h ← IO.FS.Handle.mk s!"{outPrefix}.{mode}.{shard}.jsonl" .write
  let all := (env.constants.map₁.toList.map (·.1)).toArray.qsort (fun a b => a.toString < b.toString)
  let mut written := 0
  let mut k := 0
  for n in all do
    k := k + 1
    unless k % nshards == shard do continue
    let some ci := env.find? n | continue
    let pj := isProj n
    if mode == "defsproj" && !pj then continue
    if mode == "defs" || mode == "defsproj" then
      match ci with
      | .defnInfo dv =>
        if skipName env n || isInstanceCore env n then continue
        if let some j ← runM (do
            if (← forallTelescope ci.type fun _ b => do return (← isClass? b).isSome) then return none
            emitDefn cfg pj (modOf n) n ci dv.value) then
          h.putStrLn j.compress; written := written + 1
      | .inductInfo iv =>
        if n.isInternalDetail then continue
        if isStructure env n && iv.numIndices == 0 then
          if let some j ← runM (emitStruct cfg pj (modOf n) n iv) then
            h.putStrLn j.compress; written := written + 1
      | .thmInfo _ =>
        if n.isInternalDetail then continue
        if let some j ← runM (emitChar cfg pj (modOf n) n ci) then
          h.putStrLn j.compress; written := written + 1
      | _ => pure ()
    else if mode == "thms" then
      match ci with
      | .thmInfo _ =>
        if n.isInternalDetail then continue
        let take := pj || (ci.type.find? fun e => e.isConst && wanted.contains e.constName!).isSome
        unless take do continue
        if let some j ← runM (emitThm cfg pj (modOf n) n ci (!pj)) then
          h.putStrLn j.compress; written := written + 1
      | _ => pure ()
  h.flush
  IO.eprintln s!"shard {shard}: {written} records"
  return 0

end Reinvent

unsafe def main (args : List String) : IO UInt32 := Reinvent.main args
