import Mathlib
import Rosette.Candidates

/-!
# Rosette.Bench — boundary-recovery benchmark (hypothesis H1)

For each ground-truth pair `(T, L)` of `bench/corpus.json`:

1. take the proof terms of `T` and `L` and erase **all** `mdata` from both;
2. *inline* `L` into `T`: every maximal application `L a₁ … aₙ` is replaced by `L`'s proof value
   with universe parameters instantiated and the arguments substituted (beta-reduced, including
   redexes that the substitution creates at head positions), so the constant `L` no longer occurs;
3. remember where the inlined copies sit (a private `mdata` tag, used only to compute the tree
   position, then erased again before anything is measured);
4. enumerate the candidates of the flattened term with `Rosette.Candidates` and write one JSON
   line with the numeric features of every distinct candidate (candidates with the same closed
   statement and sizes are merged) and which of them are the ground truth.

All ranking/scoring happens in `bench/score.py`; this file only produces raw data.

Run through `bench/run_bench.sh` (which adds a wall-clock watchdog and restart-on-crash), or
directly:

    ROSETTE_BENCH=1 ROSETTE_BENCH_OUT=out/bench/raw.jsonl lake env lean Rosette/Bench.lean

Environment variables: `ROSETTE_BENCH` (must be set to run), `ROSETTE_BENCH_START` /
`ROSETTE_BENCH_END` (item index range, end exclusive), `ROSETTE_BENCH_OUT` (appended to),
`ROSETTE_BENCH_PROGRESS` (file that receives the index of the item being processed),
`ROSETTE_BENCH_CORPUS` (default `bench/corpus.json`), `ROSETTE_BENCH_NOCHECK` (skip the kernel
re-check of the flattened proof).
-/

open Lean Meta

namespace Rosette.Bench

/-! ### Expression plumbing (pure, memoised on the DAG) -/

def tagKey : Name := `rosetteGT

def mkTag (e : Expr) : Expr := .mdata (KVMap.empty.insert tagKey (.ofBool true)) e

@[inline] def mapKids {m : Type → Type} [Monad m] (f : Expr → m Expr) (e : Expr) : m Expr := do
  match e with
  | .app a b => return e.updateApp! (← f a) (← f b)
  | .lam _ t b _ => return e.updateLambdaE! (← f t) (← f b)
  | .forallE _ t b _ => return e.updateForallE! (← f t) (← f b)
  | .letE _ t v b _ => return e.updateLetE! (← f t) (← f v) (← f b)
  | .proj _ _ b => return e.updateProj! (← f b)
  | .mdata _ b => return e.updateMData! (← f b)
  | _ => return e

private def isLeaf : Expr → Bool
  | .app .. | .lam .. | .forallE .. | .letE .. | .mdata .. | .proj .. => false
  | _ => true

/-- Erase every `mdata` node. -/
partial def stripAux (e : Expr) : StateM (Std.HashMap Expr Expr) Expr := do
  if isLeaf e then return e
  if let .mdata _ b := e then return ← stripAux b
  if let some r := (← get)[e]? then return r
  let r ← mapKids stripAux e
  modify (·.insert e r)
  return r

def stripMData (e : Expr) : Expr := ((stripAux e).run {}).1

/-- Number of distinct beta-redexes `(fun x => b) a` (after ignoring `mdata`). -/
partial def redexAux (e : Expr) : StateM (Std.HashSet Expr × Nat) Unit := do
  if isLeaf e then return
  if (← get).1.contains e then return
  modify fun (s, n) => (s.insert e, n)
  match e with
  | .app f a =>
    let rec unTag : Expr → Expr
      | .mdata _ b => unTag b
      | x => x
    if (unTag f).isLambda then modify fun (s, n) => (s, n + 1)
    redexAux f; redexAux a
  | .lam _ t b _ | .forallE _ t b _ => redexAux t; redexAux b
  | .letE _ t v b _ => redexAux t; redexAux v; redexAux b
  | .proj _ _ b | .mdata _ b => redexAux b
  | _ => pure ()

def countRedexes (e : Expr) : Nat := ((redexAux e).run ({}, 0)).2.2

/-! ### Inlining -/

def argFVar (i : Nat) : Expr := .fvar ⟨Name.mkNum `_rosette_arg i⟩

def argFVar? : Expr → Option Nat
  | .fvar ⟨.num `_rosette_arg i⟩ => some i
  | _ => none

/-- In `e` (the body of the helper's proof, with its formal parameters replaced by the
placeholder variables `argFVar i`), beta-reduce every application whose head is a placeholder
bound to a lambda, and replace every other occurrence of a placeholder by its argument. `off` is the number of binders we are under, needed because the actual arguments
may contain loose bound variables of the surrounding theorem. The `Nat` in the state counts
ground-truth tags that had to be dropped because a tagged argument was beta-reduced. -/
partial def substHead (args : Array Expr) (e : Expr) (off : Nat) :
    StateM (Std.HashMap (Expr × Nat) Expr × Nat) Expr := do
  if !e.hasFVar then return e
  if let some i := argFVar? e then
    -- the actual argument lives in the theorem's context: skip the `off` binders we are under
    return if h : i < args.size then args[i].liftLooseBVars 0 off else e
  if isLeaf e then return e
  if let some r := (← get).1[(e, off)]? then return r
  let r ← match e with
    | .app .. => do
      let f := e.getAppFn
      let as ← e.getAppArgs.mapM (substHead args · off)
      let plain : StateM (Std.HashMap (Expr × Nat) Expr × Nat) Expr := do
        return mkAppN (← substHead args f off) as
      match argFVar? f with
      | some i =>
        if h : i < args.size then
          let (v, tagged) := match args[i] with
            | .mdata _ b => (b, true)
            | a => (a, false)
          if v.isLambda then
            if tagged then modify fun (c, n) => (c, n + 1)
            pure ((v.liftLooseBVars 0 off).beta as).headBeta
          else plain
        else plain
      | none => plain
    | .lam _ t b _ => do pure (e.updateLambdaE! (← substHead args t off) (← substHead args b (off + 1)))
    | .forallE _ t b _ => do pure (e.updateForallE! (← substHead args t off) (← substHead args b (off + 1)))
    | .letE _ t v b _ => do
      pure (e.updateLetE! (← substHead args t off) (← substHead args v off) (← substHead args b (off + 1)))
    | .proj _ _ b => do pure (e.updateProj! (← substHead args b off))
    | .mdata _ b => do pure (e.updateMData! (← substHead args b off))
    | _ => pure e
  modify fun (c, n) => (c.insert (e, off) r, n)
  return r

/-- `body a₁ … aₙ`, beta-reduced. Returns the result and the number of dropped tags. -/
def betaInline (body : Expr) (args : Array Expr) : Expr × Nat :=
  let rec peel (b : Expr) (k : Nat) : Expr × Nat :=
    match b with
    | .lam _ _ b' _ => if k < args.size then peel b' (k + 1) else (b, k)
    | _ => (b, k)
  let (b, k) := peel body 0
  let fv := (Array.range k).map argFVar
  let b := b.instantiateRev fv
  let (b, st) := (substHead args b 0).run ({}, 0)
  ((mkAppN b (args.extract k args.size)).headBeta, st.2)

structure InlSt where
  cache : Std.HashMap Expr Expr := {}
  /-- distinct inlined application sites. -/
  sites : Nat := 0
  droppedTags : Nat := 0

/-- Replace every maximal application of the constant `L` by its (instantiated, beta-reduced)
proof value `vL`, wrapped in the ground-truth tag. Expects `mdata`-free input. -/
partial def inlineAux (L : Name) (lps : List Name) (vL : Expr) (e : Expr) : StateM InlSt Expr := do
  let f := e.getAppFn
  let isL := f.isConstOf L
  if isLeaf e && !isL then return e
  if let some r := (← get).cache[e]? then return r
  let r ←
    if isL then do
      let args ← e.getAppArgs.mapM (inlineAux L lps vL)
      let body := vL.instantiateLevelParams lps f.constLevels!
      let (r, dropped) := betaInline body args
      modify fun s => { s with sites := s.sites + 1, droppedTags := s.droppedTags + dropped }
      pure (mkTag r)
    else mapKids (inlineAux L lps vL) e
  modify fun s => { s with cache := s.cache.insert e r }
  return r

/-! ### Locating the tagged copies in `Rosette.Candidates` path coordinates -/

structure Tgt where
  path : Path
  /-- `exact`: the inlined term is a node of the traversal. `lamBody`: the helper was
  under-applied directly under a lambda, so its leading lambdas merged with the enclosing
  telescope; the node is the telescope body (same closed statement up to argument order). -/
  via : String
  sub : Expr

structure WSt where
  hasTag : Std.HashMap Expr Bool := {}
  tgts : Array Tgt := #[]
  lost : Array String := #[]
  steps : Nat := 0

partial def hasTagM (e : Expr) : StateM WSt Bool := do
  if isLeaf e then return false
  if e.isMData then return true
  if let some b := (← get).hasTag[e]? then return b
  let b ← match e with
    | .app f a => do pure ((← hasTagM f) || (← hasTagM a))
    -- binder types are not visited by the candidate traversal
    | .lam _ _ b _ => hasTagM b
    | .letE _ _ v b _ => do pure ((← hasTagM v) || (← hasTagM b))
    | .proj _ _ b => hasTagM b
    | _ => pure false
  modify fun s => { s with hasTag := s.hasTag.insert e b }
  return b

def maxWalkSteps : Nat := 300000
def maxTargets : Nat := 256

/-- Mirror of `Rosette.visit`'s path conventions on the tagged term, with tags transparent. -/
partial def walk (e : Expr) (path : Path) : StateM WSt Unit := do
  unless ← hasTagM e do return
  let s ← get
  if s.steps ≥ maxWalkSteps || s.tgts.size ≥ maxTargets then return
  modify fun s => { s with steps := s.steps + 1 }
  match e with
  | .mdata _ x =>
    modify fun s => { s with tgts := s.tgts.push { path, via := "exact", sub := x } }
    walk x path
  | .app .. =>
    -- spine of the stripped term: tags in function position are transparent (and lost)
    let rec spine (cur : Expr) (args : List Expr) : StateM WSt (Expr × List Expr) := do
      match cur with
      | .app f a => spine f (a :: args)
      | .mdata _ x =>
        modify fun s => { s with lost := s.lost.push "fnPosition" }
        spine x args
      | _ => return (cur, args)
    let (f, args) ← spine e []
    walk f (path.push 0)
    let mut i := 1
    for a in args do
      walk a (path.push i)
      i := i + 1
  | .lam .. =>
    let rec tele (cur : Expr) : StateM WSt Expr := do
      match cur with
      | .lam _ _ b _ => tele b
      | .mdata _ x =>
        if x.isLambda then
          modify fun s => { s with tgts := s.tgts.push { path := path.push 0, via := "lamBody", sub := x.getLambdaBody } }
          tele x
        else return cur
      | _ => return cur
    walk (← tele e) (path.push 0)
  | .letE _ _ v b _ => walk v (path.push 0); walk b (path.push 1)
  | .proj _ _ b => walk b (path.push 0)
  | _ => pure ()

/-! ### One item -/

private def trivialShape (e : Expr) : Bool :=
  let f := e.getAppFn
  (f.isFVar || f.isConst || f.isSort || f.isLit || f.isBVar) && e.getAppArgs.all isLeaf

private def hex64 (h : UInt64) : String :=
  let s := String.ofList (Nat.toDigits 16 h.toNat)
  "".pushn '0' (16 - s.length) ++ s

def benchCfg : Config := { ppStatements := false }

/-- Pretty-printed closed statement of the candidate at `path` (statements are not printed during
enumeration because that dominates the running time; only a few are needed for the report). -/
def statementAt (flat : Expr) (path : Path) (maxChars : Nat := 600) : MetaM String := do
  let out ← IO.mkRef ""
  let hook : LiftHook := {
    targets := #[path]
    onTarget := fun _ e => do
      let ty := (← inferType e).headBeta
      let ifc ← interfaceOf e ty
      let stmt ← mkForallFVars ifc.deps ty
      let str ← if dagSize stmt ≤ 1500 then pure (← ppExpr stmt).pretty
        else pure s!"<statement of {dagSize stmt} nodes not printed>"
      let str := " ".intercalate ((str.splitOn "\n").map (·.trimAscii.toString))
      out.set (if str.length > maxChars then (str.take maxChars).toString ++ " …" else str)
      return e }
  try
    discard <| ((visit flat #[] none "root" 0).run { cfg := benchCfg, lift? := some hook }).run' {}
  catch _ => out.set "<pp failed>"
  out.get

/-! ### DAG-aware enumeration

Flattened proofs share large subterms (the inlined helper body can occur many times, and
elaborated proofs are heavily shared anyway), so the enumeration must not walk the term as a
tree. `Rosette.visit` is DAG-aware as well since the review fixes; the enumerator below is kept
as a separate copy because it also has to resolve the ground-truth tree positions. It is the same
traversal with the same path conventions and the same per-candidate computation (`interfaceOf`,
`dagSize`, `statementHash` from `Rosette.Candidates`): a subterm that was already visited *with
the same free variables* is not visited again, since it would produce exactly the same closed
statement and sizes.
It also resolves the ground-truth paths: when the traversal reaches one, the candidate recorded
there (or the earlier identical one) is marked. -/

structure EnumSt where
  res : Result := {}
  sizes : Std.HashMap Expr Nat := {}
  /-- visited subterm ↦ candidate recorded for it (if any). -/
  seen : Std.HashMap Expr (Option Nat) := {}
  /-- ground-truth path ↦ candidate (if any) once the traversal has reached it. -/
  resolved : Std.HashMap Path (Option Nat) := {}

abbrev EnumM := ReaderT (Config × Std.HashSet Path) (StateRefT EnumSt MetaM)

private def kindOf' : Expr → String
  | .app .. => "app" | .lam .. => "lam" | .letE (nondep := nd) .. => if nd then "have" else "let"
  | .proj .. => "proj" | _ => "other"

private def recordCand (e : Expr) (path : Path) (parent : Option Nat) (role : String)
    (binderDepth tsize : Nat) : EnumM (Option Nat) := do
  let cfg := (← read).1
  if trivialShape e then return none
  try
    let ty ← inferType e
    unless (← isProp ty) do return none
    let dsize := dagSize e
    if dsize < cfg.minProofSize then return none
    let ty := ty.headBeta
    let ifc ← interfaceOf e ty
    let stmt ← mkForallFVars ifc.deps ty
    let ssize := dagSize stmt
    let s ← get
    let (stsize, sizes) := (treeSizeMemo stmt).run s.sizes
    set { s with sizes := sizes }
    let mut numProp := 0
    for x in ifc.args do
      if ← isProp (← inferType x) then numProp := numProp + 1
    let stmtIsClass := (← isClass? ty).isSome
    let id := (← get).res.cands.size
    let c : Candidate := {
      id, parent, path, depth := path.size, binderDepth, role, kind := kindOf' e
      stmtIsClass, headConst := e.getAppFn.constName?
      proofSizeDag := dsize, proofSizeTree := tsize
      statementSize := ssize, statementSizeTree := stsize
      numDeps := ifc.args.size, numPropDeps := numProp
      hidingRatio := dsize.toFloat / ssize.toFloat
      statement := "", stmtHash := statementHash stmt }
    modify fun s => { s with res := { s.res with cands := s.res.cands.push c } }
    return some id
  catch ex =>
    if ex.isRuntime then throw ex
    modify fun s => { s with res := { s.res with errors := s.res.errors + 1 } }
    return none

partial def enumVisit (e : Expr) (path : Path) (parent : Option Nat) (role : String)
    (binderDepth : Nat) : EnumM Unit := do
  let (cfg, tpaths) ← read
  let isT := tpaths.contains path
  let resolve (c : Option Nat) : EnumM Unit :=
    if isT then modify fun s => { s with resolved := s.resolved.insert path c } else pure ()
  let s ← get
  let (tsize, sizes) := (treeSizeMemo e).run s.sizes
  set { s with sizes := sizes }
  if tsize < cfg.minProofSize then resolve none; return
  if let some c := s.seen[e]? then resolve c; return
  if s.res.truncated then return
  let mark (why : String) : EnumM Unit :=
    modify fun s => { s with res := { s.res with truncated := true, note := why } }
  if s.res.visited ≥ cfg.maxVisited then mark s!"maxVisited = {cfg.maxVisited} reached"; return
  if s.res.cands.size ≥ cfg.maxCandidates then mark s!"maxCandidates = {cfg.maxCandidates} reached"; return
  Core.checkSystem "rosette"
  modify fun s => { s with res := { s.res with visited := s.res.visited + 1 } }
  let rec? ← recordCand e path parent role binderDepth tsize
  modify fun s => { s with seen := s.seen.insert e rec? }
  resolve rec?
  let parent := rec?.orElse fun _ => parent
  match e with
  | .app .. =>
    let args := e.getAppArgs
    enumVisit e.getAppFn (path.push 0) parent "fn" binderDepth
    for h : i in [0:args.size] do
      enumVisit args[i] (path.push (i + 1)) parent "arg" binderDepth
  | .lam .. =>
    lambdaTelescope e fun xs b =>
      enumVisit b (path.push 0) parent "lamBody" (binderDepth + xs.size)
  | .letE n t v b nondep =>
    enumVisit v (path.push 0) parent (if nondep then "haveValue" else "letValue") binderDepth
    withLetDecl n t v (nondep := nondep) fun x =>
      enumVisit (b.instantiate1 x) (path.push 1) parent
        (if nondep then "haveBody" else "letBody") (binderDepth + 1)
  | .proj _ _ b => enumVisit b (path.push 0) parent "proj" binderDepth
  | _ => pure ()

/-- Never throws on budget exhaustion (same contract as `candidatesOfExprCore`). -/
def enumDag (e : Expr) (tpaths : Std.HashSet Path) (cfg : Config) : MetaM EnumSt := do
  let ref ← IO.mkRef ({} : EnumSt)
  let act : MetaM Unit := withBudget cfg.maxHeartbeats do
    ((enumVisit e #[] none "root" 0).run (cfg, tpaths)) ref
  let fail (msg : String) : MetaM Unit :=
    ref.modify fun s => { s with res := { s.res with truncated := true, note := (msg.take 200).toString } }
  try
    tryCatchRuntimeEx act fun ex => do fail (← ex.toMessageData.toString)
  catch ex => fail (← ex.toMessageData.toString)
  ref.get

/-- Candidates with the same closed statement (hash) and the same proof and statement sizes are
the same lemma for every scoring rule; they are emitted as one group. -/
structure Group where
  rep : Nat
  count : Nat := 1
  minDepth : Nat
  isTarget : Bool := false
  underTarget : Bool := false
  aboveTarget : Bool := false

def runItem (item : Json) (names : Std.HashMap String Name) (kernelCheck : Bool) :
    MetaM (List (String × Json)) := do
  let getS (k : String) : MetaM String :=
    match item.getObjValAs? String k with
    | .ok s => pure s
    | .error e => throwError "corpus item lacks '{k}': {e}"
  let tStr ← getS "theoremFullName"
  let lStr ← getS "helperFullName"
  let some T := names[tStr]? | throwError "unknown theorem {tStr}"
  let some L := names[lStr]? | throwError "unknown helper {lStr}"
  let tInfo ← getConstInfo T
  let lInfo ← getConstInfo L
  let vT0 ← proofOfConst T
  let vL0 ← proofOfConst L
  let vT := stripMData vT0
  let vL := stripMData vL0
  let (tagged, ist) := (inlineAux L lInfo.levelParams vL vT).run {}
  let ((), wst) := (walk tagged #[]).run {}
  let flat := stripMData tagged
  let leakConst := (flat.find? (·.isConstOf L)).isSome
  let leakMData := (flat.find? (·.isMData)).isSome
  -- the flattened proof must still prove T
  let mut tc := "skipped"
  if kernelCheck then
    let env ← getEnv
    tc := match Kernel.check env {} flat with
      | .ok ty => match Kernel.isDefEq env {} ty tInfo.type with
        | .ok true => "ok"
        | .ok false => "typeMismatch"
        | .error _ => "defEqError"
      | .error _ => "kernelReject"
  let tpaths : Std.HashSet Path := wst.tgts.foldl (fun s t => s.insert t.path) {}
  let est ← enumDag flat tpaths benchCfg
  let res := est.res
  let cands := res.cands
  let mut tjs : Array Json := #[]
  let mut targetIds : Std.HashSet Nat := {}
  for t in wst.tgts do
    let sub := stripMData t.sub
    let d := dagSize sub
    let reached := est.resolved[t.path]?
    let cid := reached.join
    if let some i := cid then targetIds := targetIds.insert i
    let reason :=
      if cid.isSome then ""
      else if reached.isNone then (if res.truncated then "truncated" else "insideSharedDuplicate")
      else if trivialShape sub then "trivialShape"
      else if d < benchCfg.minProofSize then "belowMinProofSize"
      else "notRecorded"
    tjs := tjs.push <| Json.mkObj [
      ("path", toJson (pathToString t.path)), ("via", toJson t.via), ("dag", toJson d),
      ("cand", match cid with | some i => toJson i | none => Json.null), ("reason", toJson reason)]
  -- relation of every candidate to the ground truth (ids are pre-order, so parent < id)
  let mut under : Array Bool := Array.replicate cands.size false
  let mut above : Array Bool := Array.replicate cands.size false
  for c in cands do
    if let some p := c.parent then
      if targetIds.contains p || under[p]! then under := under.set! c.id true
  for i in targetIds do
    let mut cur := cands[i]!.parent
    while cur.isSome do
      let p := cur.get!
      above := above.set! p true
      cur := cands[p]!.parent
  -- group identical lemmas
  let mut gidx : Std.HashMap (UInt64 × Nat × Nat × Nat × Nat) Nat := {}
  let mut groups : Array Group := #[]
  for c in cands do
    let key := (c.stmtHash, c.proofSizeDag, c.proofSizeTree, c.statementSize, c.numDeps)
    let tgt := targetIds.contains c.id
    match gidx[key]? with
    | some g =>
      groups := groups.modify g fun gr => { gr with
        count := gr.count + 1, minDepth := min gr.minDepth c.depth
        isTarget := gr.isTarget || tgt, underTarget := gr.underTarget || under[c.id]!
        aboveTarget := gr.aboveTarget || above[c.id]! }
    | none =>
      gidx := gidx.insert key groups.size
      groups := groups.push { rep := c.id, minDepth := c.depth, isTarget := tgt,
                              underTarget := under[c.id]!, aboveTarget := above[c.id]! }
  -- statements for the report: ground truth, the root, and the best few under simple rules
  let nonRoot := groups.filter fun g => g.rep != 0
  let ratio (g : Group) : Float := cands[g.rep]!.hidingRatio
  let topRatio := (nonRoot.qsort fun a b => ratio a > ratio b).extract 0 8
  let saving (g : Group) : Int := (cands[g.rep]!.proofSizeDag : Int) - cands[g.rep]!.statementSize
  let topSaving := (nonRoot.qsort fun a b => saving a > saving b).extract 0 3
  let mut wantStmt : Std.HashSet Nat := {}
  for g in groups do
    if g.isTarget || g.rep == 0 then wantStmt := wantStmt.insert g.rep
  for g in topRatio ++ topSaving do wantStmt := wantStmt.insert g.rep
  let mut stmts : Array (String × Json) := #[]
  for r in wantStmt.toArray.qsort (· < ·) do
    stmts := stmts.push (toString r, toJson (← statementAt flat cands[r]!.path))
  let gj := groups.map fun g =>
    let c := cands[g.rep]!
    Json.arr #[
      toJson g.rep, toJson g.count, toJson g.minDepth, toJson c.role, toJson c.kind,
      toJson c.stmtIsClass, toJson c.proofSizeDag, toJson c.proofSizeTree, toJson c.statementSize,
      toJson c.statementSizeTree, toJson c.numDeps, toJson c.numPropDeps,
      toJson (hex64 c.stmtHash), toJson g.isTarget, toJson g.underTarget, toJson g.aboveTarget]
  let lStmt ← try pure (← ppExpr lInfo.type).pretty catch _ => pure "<pp failed>"
  let tStmt ← try pure (← ppExpr tInfo.type).pretty catch _ => pure "<pp failed>"
  return [
    ("ok", toJson true),
    ("thmProofDag", toJson (dagSize vT)), ("helperProofDag", toJson (dagSize vL)),
    ("helperStmtDag", toJson (dagSize lInfo.type)),
    ("flatDag", toJson (dagSize flat)), ("flatTree", toJson (treeSize flat)),
    ("sites", toJson ist.sites), ("droppedTags", toJson ist.droppedTags),
    ("lostTags", toJson wst.lost), ("walkSteps", toJson wst.steps),
    ("leakConst", toJson leakConst), ("leakMData", toJson leakMData),
    ("mdataT", toJson (vT0.find? (·.isMData)).isSome), ("mdataL", toJson (vL0.find? (·.isMData)).isSome),
    ("redexT", toJson (countRedexes vT)), ("redexL", toJson (countRedexes vL)),
    ("redexFlat", toJson (countRedexes flat)),
    ("typecheck", toJson tc),
    ("targets", Json.arr tjs),
    ("nCands", toJson cands.size), ("nGroups", toJson groups.size), ("visited", toJson res.visited),
    ("enumErrors", toJson res.errors), ("truncated", toJson res.truncated), ("note", toJson res.note),
    ("helperStatement", toJson lStmt), ("theoremStatement", toJson tStmt),
    ("statements", Json.mkObj stmts.toList),
    ("groupFields", toJson #["rep", "count", "minDepth", "role", "kind", "stmtIsClass",
      "proofSizeDag", "proofSizeTree", "statementSize", "statementSizeTree", "numDeps",
      "numPropDeps", "stmtHash", "isTarget", "underTarget", "aboveTarget"]),
    ("groups", Json.arr gj)]

def run : MetaM Unit := do
  let envNat (k : String) (d : Nat) : IO Nat := do
    return ((← IO.getEnv k).bind (·.toNat?)).getD d
  let corpusPath := (← IO.getEnv "ROSETTE_BENCH_CORPUS").getD "bench/corpus.json"
  let outPath := (← IO.getEnv "ROSETTE_BENCH_OUT").getD "out/bench/raw.jsonl"
  let progress? ← IO.getEnv "ROSETTE_BENCH_PROGRESS"
  let kernelCheck := (← IO.getEnv "ROSETTE_BENCH_NOCHECK").isNone
  let items ← match Json.parse (← IO.FS.readFile corpusPath) with
    | .ok (.arr a) => pure a
    | _ => throwError "cannot parse {corpusPath}"
  let start ← envNat "ROSETTE_BENCH_START" 0
  let stop := min items.size (← envNat "ROSETTE_BENCH_END" items.size)
  -- names are looked up by their printed form (private names contain numeric components)
  let mut wanted : Std.HashSet String := {}
  for it in items do
    for k in ["theoremFullName", "helperFullName"] do
      if let .ok s := it.getObjValAs? String k then wanted := wanted.insert s
  let names := (← getEnv).constants.fold (init := ({} : Std.HashMap String Name)) fun m n _ =>
    let s := n.toString
    if wanted.contains s then m.insert s n else m
  let h ← IO.FS.Handle.mk outPath .append
  let setProgress (s : String) : IO Unit := do
    if let some p := progress? then IO.FS.writeFile p s
  for idx in [start:stop] do
    setProgress s!"{idx} running\n"
    let item := items[idx]!
    let t0 ← IO.monoMsNow
    let fields ← try
        tryCatchRuntimeEx (withBudget 2000000 (runItem item names kernelCheck)) fun ex => do
          pure [("ok", toJson false), ("error", toJson (← ex.toMessageData.toString))]
      catch ex =>
        pure [("ok", toJson false), ("error", toJson (← ex.toMessageData.toString))]
    let t1 ← IO.monoMsNow
    let metaFields := ["theorem", "helper", "theoremFullName", "helperFullName", "module", "area",
      "signal", "helperUseCount", "helperIsPrivate"].filterMap fun k =>
        (item.getObjVal? k).toOption.map fun v => (k, v)
    h.putStrLn (Json.mkObj ([("idx", toJson idx)] ++ metaFields ++ [("ms", toJson (t1 - t0))] ++ fields)).compress
    h.flush
    setProgress s!"{idx} done\n"
  setProgress s!"{stop} finished\n"
  IO.println s!"Rosette.Bench: processed items [{start}, {stop}) -> {outPath}"

end Rosette.Bench

set_option maxHeartbeats 0 in
#eval show MetaM Unit from do
  if (← IO.getEnv "ROSETTE_BENCH").isSome then
    Rosette.Bench.run
  else
    IO.println "Rosette.Bench: set ROSETTE_BENCH=1 to run (see bench/run_bench.sh)"
