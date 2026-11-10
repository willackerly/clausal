/-
Census supplement to Friction.lean: per-theorem constant sets and a few Expr-level shape detectors
that the census (bench/friction_census.py) needs and Friction.lean does not emit.

Stand-alone program (imports only `Lean`); loads the BUILT environment of a corpus and reads
`Environment` / `Expr` only.  No source text and no pretty-printer output is parsed.

  census <modules.txt> <roots,csv> <primary.txt> <theorems.txt> <outPrefix> <shard> <nshards>

Writes <outPrefix>.thm.<shard>.jsonl, .tab.<shard>.jsonl, .meta.<shard>.json.

Per theorem (`thm`):
  sc    ids of all constants occurring in the statement (type), any position
  pc    [id, n] for the proof term: n = number of distinct maximal applications (or bare
        occurrences) headed by the constant.  Values of the theorem's own body auxiliaries are
        inlined (same rule as Friction.lean); the auxiliaries themselves are not counted.
  pj    [id, n]: primitive structure projections `Expr.proj S i` in the proof, per structure S
  lit   numeric literals `OfNat.ofNat T n _` with n >= 2 in the statement, distinct values, split by
        T = Real/NNReal/ENNReal ("real"), Nat ("nat"), anything else ("other"); `sci` = number of
        distinct `OfScientific.ofScientific` nodes (decimal literals)
  eps   [any, ex, strict]: distinct sub-propositions of the statement of the form
          any    : ∀ x : ℝ|ℝ≥0|ℝ≥0∞, 0 < x → B
          ex     : ... and B, after peeling ∀ / ∃ / last conjunct, passes through an ∃
          strict : ... and the atom reached is `_ < x` or `_ ≤ x` (x itself or a coercion of x)
        (`strict` is the ε-δ / ε-N shape: ∀ ε > 0, ∃ δ, ... , |...| < ε)
  ec    [n, signed, bound, both]: real-typed ∃ in the conclusion (through ∀ / ∧ / ∃); how many have a
        sign conjunct (`0 < C` or `0 ≤ C`), how many are used as an upper bound (some `l ≤ r` / `l < r`
        in the body with C in r and not in l, l not the literal 0), how many both
  integ distinct applications of an integral (integral, lintegral, intervalIntegral) in the statement
  rawLp ... of which the integrand contains a power whose base contains a norm / abs / enorm
Constant table (`tab`): name, module, isProject, kind, `resHead` / `nBinders` (head constant of the
result type and number of leading binders; for definitions `argHeads`, the head constants of the
first 8 binder types), structure facts, `eqnOf` (the definition a
`f.eq_N` / `f.eq_def` / `f.eq_unfold` equation lemma belongs to).
-/
import Lean
open Lean Meta

namespace Census

def nameStr (n : Name) : String := n.toString (escape := false)

structure Ids where
  idx : Std.HashMap Name Nat := {}
  names : Array Name := #[]

def Ids.get (s : Ids) (n : Name) : Ids × Nat :=
  match s.idx[n]? with
  | some i => (s, i)
  | none => ({ idx := s.idx.insert n s.names.size, names := s.names.push n }, s.names.size)

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

def isRealTy (e : Expr) : Bool :=
  match e.consumeMData with
  | .const n _ => n == `Real || n == `NNReal || n == `ENNReal
  | _ => false

/-- `0 < x` / `x > 0` where x is the bound variable with index k. -/
def isPosOf (h : Expr) (k : Nat) : Bool :=
  let h := h.consumeMData
  if h.isAppOfArity ``LT.lt 4 then
    isZeroLit (h.getArg! 2) && (h.getArg! 3).consumeMData == .bvar k
  else if h.isAppOfArity ``GT.gt 4 then
    isZeroLit (h.getArg! 3) && (h.getArg! 2).consumeMData == .bvar k
  else false

/-- Follow ∀ / ∃ / last conjunct to the final atom. Returns (atom, index of the tracked bvar, passed an ∃). -/
partial def tailAtom (e : Expr) (k : Nat) (ex : Bool) : Expr × Nat × Bool :=
  match e.consumeMData with
  | .forallE _ _ b _ => tailAtom b (k + 1) ex
  | e' =>
    if e'.isAppOfArity ``Exists 2 then
      match e'.appArg!.consumeMData with
      | .lam _ _ b _ => tailAtom b (k + 1) true
      | _ => (e', k, ex)
    else if e'.isAppOfArity ``And 2 then tailAtom e'.appArg! k ex
    else (e', k, ex)

/-- `0 < x`, `0 ≤ x`, `x > 0`, `x ≥ 0` for the bound variable k -/
def isSignOf (h : Expr) (k : Nat) : Bool :=
  let h := h.consumeMData
  if h.isAppOfArity ``LT.lt 4 || h.isAppOfArity ``LE.le 4 then
    isZeroLit (h.getArg! 2) && (h.getArg! 3).consumeMData == .bvar k
  else if h.isAppOfArity ``GT.gt 4 || h.isAppOfArity ``GE.ge 4 then
    isZeroLit (h.getArg! 3) && (h.getArg! 2).consumeMData == .bvar k
  else false

/-- a sign conjunct about bvar k, looking through ∧ and further ∃ -/
partial def signFor (e : Expr) (k : Nat) : Bool :=
  let e := e.consumeMData
  if e.isAppOfArity ``And 2 then signFor (e.getArg! 0) k || signFor (e.getArg! 1) k
  else if e.isAppOfArity ``Exists 2 then
    match e.appArg!.consumeMData with
    | .lam _ _ b _ => signFor b (k + 1)
    | _ => false
  else isSignOf e k

/-- some `l ≤ r` / `l < r` (or `r ≥ l` / `r > l`) inside e has bvar k in r and not in l:
the variable is used as an upper bound.  Tree walk with fuel. -/
partial def boundUse (e : Expr) (k : Nat) : StateM Nat Bool := do
  if (← get) == 0 then return false
  modify (· - 1)
  if !e.hasLooseBVar k then return false
  match e with
  | .mdata _ b => boundUse b k
  | .forallE _ d b _ => return (← boundUse d k) || (← boundUse b (k + 1))
  | .lam _ d b _ => return (← boundUse d k) || (← boundUse b (k + 1))
  | .letE _ t v b _ => return (← boundUse t k) || (← boundUse v k) || (← boundUse b (k + 1))
  | .proj _ _ b => boundUse b k
  | .app f a =>
    let le := e.isAppOfArity ``LT.lt 4 || e.isAppOfArity ``LE.le 4
    let ge := e.isAppOfArity ``GT.gt 4 || e.isAppOfArity ``GE.ge 4
    if le && (e.getArg! 3).hasLooseBVar k && !(e.getArg! 2).hasLooseBVar k && !isZeroLit (e.getArg! 2) then return true
    if ge && (e.getArg! 2).hasLooseBVar k && !(e.getArg! 3).hasLooseBVar k && !isZeroLit (e.getArg! 3) then return true
    return (← boundUse f k) || (← boundUse a k)
  | _ => return false

/-- real-typed ∃ of the conclusion reached through ∀ / ∧ / ∃:
(count, with a sign conjunct, used as an upper bound, both) -/
partial def scanEx (e : Expr) : StateM (Nat × Nat × Nat × Nat) Unit := do
  let e := e.consumeMData
  match e with
  | .forallE _ _ b _ => scanEx b
  | _ =>
    if e.isAppOfArity ``And 2 then
      scanEx (e.getArg! 0); scanEx (e.getArg! 1)
    else if e.isAppOfArity ``Exists 2 then
      if let .lam _ d b _ := e.appArg!.consumeMData then
        if isRealTy d then
          let sg := signFor b 0
          let (bu, _) := (boundUse b 0).run 2000000
          modify fun (a, s, u, su) => (a + 1, s + (if sg then 1 else 0), u + (if bu then 1 else 0),
                                       su + (if sg && bu then 1 else 0))
        scanEx b

partial def stripForalls : Expr → Expr
  | .forallE _ _ b _ => stripForalls b
  | .mdata _ b => stripForalls b
  | e => e

def powNames : List Name := [``HPow.hPow, `Real.rpow, `NNReal.rpow, `ENNReal.rpow, `Monoid.npow, ``Pow.pow]
def normNames : List Name := [`Norm.norm, `abs, `enorm, `nnnorm, `ENorm.enorm, `NNNorm.nnnorm]
def integralNames : List Name := [`MeasureTheory.integral, `MeasureTheory.lintegral, `intervalIntegral]

def hasNorm (e : Expr) : Bool :=
  (e.find? fun x => match x with | .const n _ => normNames.contains n | _ => false).isSome

/-- the integrand contains `b ^ p` with a norm inside `b` -/
def hasPowNorm (e : Expr) : Bool :=
  (e.find? fun x =>
    x.isApp && (match x.getAppFn with
      | .const n _ => powNames.contains n && x.getAppNumArgs ≥ 2 &&
          hasNorm (x.getArg! (x.getAppNumArgs - 2))
      | _ => false)).isSome

structure SSt where
  seen : Std.HashSet ExprStructEq := {}
  consts : Std.HashSet Name := {}
  litReal : Std.HashSet Nat := {}
  litNat : Std.HashSet Nat := {}
  litOther : Std.HashSet Nat := {}
  sci : Nat := 0
  epsAny : Nat := 0
  epsEx : Nat := 0
  epsStrict : Nat := 0
  integ : Nat := 0
  rawLp : Nat := 0

partial def sv (e : Expr) : StateM SSt Unit := do
  if (← get).seen.contains ⟨e⟩ then return
  modify fun s => { s with seen := s.seen.insert ⟨e⟩ }
  match e with
  | .mdata _ b => sv b
  | .const n _ => modify fun s => { s with consts := s.consts.insert n }
  | .app f a =>
    if e.isAppOfArity ``OfNat.ofNat 3 then
      if let .lit (.natVal n) := (e.getArg! 1).consumeMData then
        if n ≥ 2 then
          let ty := (e.getArg! 0).consumeMData
          if isRealTy ty then modify fun s => { s with litReal := s.litReal.insert n }
          else if ty.isConstOf ``Nat then modify fun s => { s with litNat := s.litNat.insert n }
          else modify fun s => { s with litOther := s.litOther.insert n }
    if e.isAppOfArity ``OfScientific.ofScientific 5 then modify fun s => { s with sci := s.sci + 1 }
    if let .const n _ := e.getAppFn then
      if integralNames.contains n && (match f with | .app .. => true | _ => true) then
        -- count only the saturated application: its last argument is the integrand or the measure
        let args := e.getAppArgs
        let full := (n == `MeasureTheory.integral && args.size == 6) ||
                    (n == `MeasureTheory.lintegral && args.size == 4) ||
                    (n == `intervalIntegral && args.size == 7)
        if full then
          modify fun s => { s with integ := s.integ + 1 }
          if args.any hasPowNorm then modify fun s => { s with rawLp := s.rawLp + 1 }
    sv f; sv a
  | .forallE _ d b _ =>
    if isRealTy d then
      if let .forallE _ h b2 _ := b.consumeMData then
        if isPosOf h 0 then
          let (atom, k, ex) := tailAtom b2 1 false
          -- the right-hand side is ε itself, or a one-argument function (a coercion) applied to it
          let isVar (r : Expr) : Bool :=
            let r := r.consumeMData
            r == .bvar k || (r.isApp && r.getAppNumArgs == 1 && r.appArg!.consumeMData == .bvar k)
          let strict := ex && (atom.isAppOfArity ``LT.lt 4 || atom.isAppOfArity ``LE.le 4) &&
            isVar (atom.getArg! 3)
          modify fun s => { s with epsAny := s.epsAny + 1,
                                   epsEx := s.epsEx + (if ex then 1 else 0),
                                   epsStrict := s.epsStrict + (if strict then 1 else 0) }
    sv d; sv b
  | .lam _ d b _ => sv d; sv b
  | .letE _ t v b _ => sv t; sv v; sv b
  | .proj s _ b => modify (fun st => { st with consts := st.consts.insert s }); sv b
  | _ => pure ()

structure PSt where
  seen : Std.HashSet ExprStructEq := {}
  counted : Std.HashSet ExprStructEq := {}
  cnt : Std.HashMap Name Nat := {}
  pj : Std.HashMap Name Nat := {}

partial def pv (auxVal : Name → Option Expr) (e : Expr) (isFn : Bool) : StateM PSt Unit := do
  match e with
  | .mdata _ b => pv auxVal b isFn
  | _ =>
    if !isFn && (e.isApp || e.isConst) then
      unless (← get).counted.contains ⟨e⟩ do
        modify fun s => { s with counted := s.counted.insert ⟨e⟩ }
        if let .const n _ := e.getAppFn then
          if (auxVal n).isNone then
            modify fun s => { s with cnt := s.cnt.insert n (s.cnt.getD n 0 + 1) }
    if (← get).seen.contains ⟨e⟩ then return
    modify fun s => { s with seen := s.seen.insert ⟨e⟩ }
    match e with
    | .app f a => pv auxVal f true; pv auxVal a false
    | .lam _ d b _ => pv auxVal d false; pv auxVal b false
    | .forallE _ d b _ => pv auxVal d false; pv auxVal b false
    | .letE _ t v b _ => pv auxVal t false; pv auxVal v false; pv auxVal b false
    | .proj s _ b =>
      modify fun st => { st with pj := st.pj.insert s (st.pj.getD s 0 + 1) }
      pv auxVal b false
    | .const n _ => if let some v := auxVal n then pv auxVal v false
    | _ => pure ()

partial def chainParent (isPrim : Name → Bool) : Name → Option Name
  | .str p _ | .num p _ =>
    if isPrim p then some p
    else if isPrivateName p && isPrim (privateToUserName p) then some (privateToUserName p)
    else chainParent isPrim p
  | .anonymous => none

partial def resultHead : Expr → Nat → String × Nat
  | .forallE _ _ b _, k => resultHead b (k + 1)
  | .mdata _ b, k => resultHead b k
  | e, k => (match e.getAppFn with | .const n _ => nameStr n | .sort _ => "<sort>" | _ => "", k)

/-- head constants of the leading binder types (first 8) -/
partial def binderHeads : Expr → Nat → List String
  | .forallE _ d b _, k =>
    if k ≥ 8 then [] else
    (match d.getAppFn with | .const n _ => nameStr n | .sort _ => "<sort>" | .forallE .. => "<pi>" | _ => "") :: binderHeads b (k + 1)
  | .mdata _ b, k => binderHeads b k
  | _, _ => []

partial def resultIsProp : Expr → Bool
  | .forallE _ _ b _ => resultIsProp b
  | .mdata _ b => resultIsProp b
  | .sort .zero => true
  | _ => false

def eqnParent (env : Environment) (n : Name) : Option Name :=
  match n with
  | .str p s =>
    let isEq := s == "eq_def" || s == "eq_unfold" ||
      (s.startsWith "eq_" && (s.toList.drop 3).length > 0 && (s.toList.drop 3).all Char.isDigit)
    if !isEq then none else
    match env.find? p with
    | some (.defnInfo _) => some p
    | some (.opaqueInfo _) => some p
    | _ => none
  | _ => none

unsafe def main (args : List String) : IO UInt32 := do
  let [modsFile, rootsS, primFile, thmFile, outPrefix, shardS, nshardS] := args
    | throw <| IO.userError "usage: census modules.txt roots primary.txt theorems.txt outPrefix shard nshards"
  let shard := shardS.toNat!
  let nshards := nshardS.toNat!
  let t0 ← IO.monoMsNow
  initSearchPath (← findSysroot)
  enableInitializersExecution
  let modNames := ((← IO.FS.lines modsFile).filter (· ≠ "")).map (·.toName)
  let env ← importModules (modNames.map fun m => { module := m }) {} (trustLevel := 1024) (loadExts := true)
  let t1 ← IO.monoMsNow
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
  let mut primary : Std.HashSet Name := {}
  for l in (← IO.FS.lines primFile) do
    if l == "" then continue
    if let some n := byStr[l]? then primary := primary.insert n
  let mut thms : Array Name := #[]
  let mut thmMissing := 0
  for l in (← IO.FS.lines thmFile) do
    if l == "" then continue
    match byStr[l]? with
    | some n => thms := thms.push n
    | none => thmMissing := thmMissing + 1
  let isPrim (n : Name) : Bool := primary.contains n
  let h ← IO.FS.Handle.mk s!"{outPrefix}.thm.{shard}.jsonl" .write
  let mut ids : Ids := {}
  let mut written := 0
  for k in [0:thms.size] do
    unless k % nshards == shard do continue
    let n := thms[k]!
    let some ci := env.find? n | continue
    let auxVal (c : Name) : Option Expr :=
      if c == n || !isProj c || isPrim c || env.isProjectionFn c then none
      else match env.find? c with
        | some (.thmInfo v) => (match chainParent isPrim c with | some p => if p == n then some v.value else none | none => some v.value)
        | some (.defnInfo v) => (match chainParent isPrim c with | some p => if p == n then some v.value else none | none => some v.value)
        | _ => none
    let ((), ss) := (sv ci.type).run {}
    let mut sc : Array Nat := #[]
    for c in ss.consts.toList do
      let (ids', i) := ids.get c
      ids := ids'
      sc := sc.push i
    let val? : Option Expr := match ci with
      | .thmInfo v => some v.value
      | .defnInfo v => some v.value
      | .opaqueInfo v => some v.value
      | _ => none
    let mut pc : Array (Array Nat) := #[]
    let mut pj : Array (Array Nat) := #[]
    if let some v := val? then
      let ((), ps) := (pv auxVal v false).run {}
      for (c, m) in ps.cnt.toList do
        let (ids', i) := ids.get c
        ids := ids'
        pc := pc.push #[i, m]
      for (c, m) in ps.pj.toList do
        let (ids', i) := ids.get c
        ids := ids'
        pj := pj.push #[i, m]
    let cap (s : Std.HashSet Nat) : Json := toJson ((s.toArray.qsort (· < ·)).extract 0 40)
    h.putStrLn (Json.mkObj [
      ("name", nameStr n), ("sc", toJson sc), ("pc", toJson pc), ("pj", toJson pj),
      ("lit", Json.mkObj [("real", cap ss.litReal), ("nat", cap ss.litNat), ("other", cap ss.litOther),
                          ("nReal", toJson ss.litReal.size), ("nNat", toJson ss.litNat.size),
                          ("nOther", toJson ss.litOther.size), ("sci", toJson ss.sci)]),
      ("eps", toJson #[ss.epsAny, ss.epsEx, ss.epsStrict]),
      ("ec", (let ((), (a, sg, u, su)) := (scanEx (stripForalls ci.type)).run (0, 0, 0, 0); toJson #[a, sg, u, su])),
      ("integ", toJson ss.integ), ("rawLp", toJson ss.rawLp)]).compress
    written := written + 1
    if written % 1000 == 0 then h.flush
  h.flush
  -- constant table
  let coreCtx : Core.Context := { fileName := "<census>", fileMap := default, maxHeartbeats := 0,
                                  maxRecDepth := 1000000 }
  let ht ← IO.FS.Handle.mk s!"{outPrefix}.tab.{shard}.jsonl" .write
  for i in [0:ids.names.size] do
    let c := ids.names[i]!
    let mut fields : List (String × Json) := [("id", toJson i), ("name", nameStr c), ("module", modOf c),
      ("isProject", toJson (isProj c))]
    match env.find? c with
    | none => fields := fields ++ [("kind", Json.str "?")]
    | some ci =>
      let kind : String := match ci with
        | .thmInfo _ => "thm" | .defnInfo _ => "def" | .inductInfo _ => "ind" | .ctorInfo _ => "ctor"
        | .recInfo _ => "rec" | .axiomInfo _ => "axiom" | .opaqueInfo _ => "opaque" | .quotInfo _ => "quot"
      let (rh, nb) := resultHead ci.type 0
      fields := fields ++ [("resHead", Json.str rh), ("nBinders", toJson nb)]
      if kind == "def" then fields := fields ++ [("argHeads", toJson (binderHeads ci.type 0))]
      fields := fields ++ [("kind", Json.str kind), ("resProp", toJson (resultIsProp ci.type)),
        ("isClass", toJson (isClass env c)), ("isProjFn", toJson (env.isProjectionFn c))]
      if isStructure env c then
        let fs := getStructureFields env c
        fields := fields ++ [("isStruct", toJson true), ("nFields", toJson fs.size)]
        if let .inductInfo iv := ci then
          if let [ctor] := iv.ctors then
            if let some cinfo := env.find? ctor then
              let act : MetaM Nat := forallTelescope cinfo.type fun xs _ => do
                let mut np := 0
                for j in [iv.numParams:xs.size] do
                  if ← (try isProp (← inferType xs[j]!) catch _ => pure false) then np := np + 1
                return np
              let r ← (try
                  let (a, _) ← act.run'.toIO coreCtx { env := env }
                  pure (some a)
                catch _ => pure none)
              if let some np := r then fields := fields ++ [("nPropFields", toJson np)]
      if let some p := eqnParent env c then
        fields := fields ++ [("eqnOf", Json.str (nameStr p)), ("eqnOfProject", toJson (isProj p))]
    ht.putStrLn (Json.mkObj fields).compress
  ht.flush
  let t2 ← IO.monoMsNow
  let mut metaFields : List (String × Json) := [
    ("shard", toJson shard), ("nshards", toJson nshards), ("leanVersion", Lean.versionString),
    ("theoremsListed", toJson thms.size), ("theoremsUnresolved", toJson thmMissing),
    ("written", toJson written), ("constants", toJson ids.names.size),
    ("importMs", toJson (t1 - t0)), ("totalMs", toJson (t2 - t0))]
  if shard == 0 then
    -- project import graph, from the environment header
    let mut imps : List (String × Json) := []
    for i in [0:env.header.moduleNames.size] do
      if projIdx[i]! then
        let ds := env.header.moduleData[i]!.imports.filterMap fun im =>
          if roots.contains im.module.getRoot then some im.module.toString else none
        imps := (modStr[i]!, toJson ds) :: imps
    metaFields := metaFields ++ [("projectImports", Json.mkObj imps)]
  IO.FS.writeFile s!"{outPrefix}.meta.{shard}.json" (Json.mkObj metaFields).compress
  IO.eprintln s!"[shard {shard}] wrote {written}; total {t2 - t0} ms"
  return 0

end Census

unsafe def main (args : List String) : IO UInt32 := Census.main args
