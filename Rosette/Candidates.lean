/-
Rosette.Candidates — enumerate candidate lemma boundaries inside an elaborated proof term.

For every subterm `e` of a proof term that is itself a proof (its type is a `Prop`) we compute
  * the interface: the local hypotheses/variables `e` really depends on (closed under the
    dependencies of their types),
  * the closed statement `∀ deps, type(e)`,
  * sizes of proof and statement (DAG size = shared subterms counted once, and tree size),
  * hidingRatio = proofSizeDag / statementSize.

Everything is computed on kernel terms; nothing here looks at tactic text.
The same traversal (`visit`) is reused by `Rosette.Lift` in "rebuild" mode to replace selected
subterms by calls to freshly added auxiliary theorems.
-/
import Lean

open Lean Meta Elab Command

namespace Rosette

/-- Position of a subterm, as a sequence of child indices.
* application spine `f a₁ … aₙ`: `0` is `f`, `i` is `aᵢ`;
* `fun x₁ … xₙ => b` (maximal lambda telescope): `0` is `b`;
* `let/have x := v; b`: `0` is `v`, `1` is `b`;
* `mdata`/`proj`: `0` is the inner term. -/
abbrev Path := Array Nat

def pathToString (p : Path) : String :=
  if p.isEmpty then "root" else ".".intercalate (p.toList.map toString)

/-- `p` is a (non-strict) prefix of `q`. -/
def pathIsPrefix (p q : Path) : Bool :=
  p.size ≤ q.size && (List.range p.size).all fun i => p[i]! == q[i]!

/-- One candidate lemma boundary. -/
structure Candidate where
  /-- index in the result array (pre-order). -/
  id : Nat
  /-- id of the closest enclosing candidate, if any. -/
  parent : Option Nat
  path : Path
  /-- nesting depth in the expression tree (= `path.size`). -/
  depth : Nat
  /-- number of local binders (lambda / let / have) in scope at the subterm. -/
  binderDepth : Nat
  /-- how the subterm sits in its parent: root | fn | arg | lamBody | haveValue | letValue |
  haveBody | letBody | proj. `haveValue` marks a human-written `have` boundary. -/
  role : String
  /-- constructor of the subterm: app | lam | let | have | proj | other. -/
  kind : String
  /-- the (unclosed) statement is a typeclass, e.g. `DenselyOrdered ℝ`: such proofs come from
  instance synthesis, not from a step the author wrote. -/
  stmtIsClass : Bool
  /-- head constant of the application spine, if any. -/
  headConst : Option Name
  /-- number of distinct subterms of the proof (shared subterms counted once). -/
  proofSizeDag : Nat
  /-- number of nodes of the proof seen as a tree. -/
  proofSizeTree : Nat
  /-- DAG size of the closed statement `∀ deps, type`. -/
  statementSize : Nat
  statementSizeTree : Nat
  /-- number of arguments the lifted lemma takes. -/
  numDeps : Nat
  /-- how many of those arguments are proofs (hypotheses). -/
  numPropDeps : Nat
  /-- `proofSizeDag / statementSize`. -/
  hidingRatio : Float
  /-- pretty-printed closed statement (single line, truncated). -/
  statement : String
  /-- structural hash of the closed statement: invariant under bound-variable names, binder
  annotations, `mdata` and the names of universe parameters. -/
  stmtHash : UInt64
  /-- number of tree positions at which the traversal met this very subterm (same term, same
  local variables). The traversal is DAG-aware: a repeated subterm is one candidate, recorded at
  its first position. Copies that sit inside a larger repeated subterm are not counted, because
  the traversal does not enter that larger subterm a second time. -/
  occurrences : Nat := 1
  deriving Inhabited

structure Config where
  /-- only subterms whose DAG size is at least this are reported. -/
  minProofSize : Nat := 20
  /-- stop after this many candidates. -/
  maxCandidates : Nat := 20000
  /-- stop after visiting this many subterms. -/
  maxVisited : Nat := 400000
  /-- heartbeat budget (in thousands, like the `maxHeartbeats` option) per declaration. -/
  maxHeartbeats : Nat := 400000
  /-- pretty-print statements (the slow part); statements larger than `maxPpSize` nodes are
  not printed. -/
  ppStatements : Bool := true
  maxPpSize : Nat := 1500
  /-- truncate pretty-printed statements to this many characters. -/
  maxStmtChars : Nat := 400

/-- Result of enumerating one proof term. -/
structure Result where
  cands : Array Candidate := #[]
  /-- subterms visited. -/
  visited : Nat := 0
  /-- subterms for which type inference / abstraction threw (they are skipped). -/
  errors : Nat := 0
  /-- a budget (candidates / visited / heartbeats) was hit: `cands` is incomplete. -/
  truncated : Bool := false
  /-- reason for truncation or failure, if any. -/
  note : String := ""

/-! ### Sizes and hashes -/

private def isAtom : Expr → Bool
  | .app .. | .lam .. | .forallE .. | .letE .. | .mdata .. | .proj .. => false
  | _ => true

/-- Tree size with a memo table (so it is linear in the DAG size). `mdata` nodes are free. -/
partial def treeSizeMemo (e : Expr) : StateM (Std.HashMap Expr Nat) Nat := do
  if isAtom e then return 1
  if let some n := (← get)[e]? then return n
  let n ← match e with
    | .app f a => do pure (1 + (← treeSizeMemo f) + (← treeSizeMemo a))
    | .lam _ t b _ | .forallE _ t b _ => do pure (1 + (← treeSizeMemo t) + (← treeSizeMemo b))
    | .letE _ t v b _ => do pure (1 + (← treeSizeMemo t) + (← treeSizeMemo v) + (← treeSizeMemo b))
    | .mdata _ b => treeSizeMemo b
    | .proj _ _ b => do pure (1 + (← treeSizeMemo b))
    | _ => pure 1
  modify fun m => m.insert e n
  return n

private partial def dagSizeAux (e : Expr) : StateM (Std.HashSet Expr) Unit := do
  match e with
  | .mdata _ b => dagSizeAux b
  | _ =>
    if (← get).contains e then return
    modify fun s => s.insert e
    match e with
    | .app f a => dagSizeAux f; dagSizeAux a
    | .lam _ t b _ | .forallE _ t b _ => dagSizeAux t; dagSizeAux b
    | .letE _ t v b _ => dagSizeAux t; dagSizeAux v; dagSizeAux b
    | .proj _ _ b => dagSizeAux b
    | _ => pure ()

/-- Number of distinct subterms (up to alpha-equivalence) of `e`. -/
def dagSize (e : Expr) : Nat :=
  ((dagSizeAux e).run {}).2.size

def treeSize (e : Expr) : Nat :=
  ((treeSizeMemo e).run {}).1

private partial def levelHash : Level → UInt64
  | .zero => 11
  | .succ l => mixHash 13 (levelHash l)
  | .max a b => mixHash 17 (mixHash (levelHash a) (levelHash b))
  | .imax a b => mixHash 19 (mixHash (levelHash a) (levelHash b))
  | .param n => mixHash 23 (hash n)
  | .mvar _ => 29

private partial def structHashAux (e : Expr) : StateM (Std.HashMap Expr UInt64) UInt64 := do
  match e with
  | .bvar i => return mixHash 31 (hash i)
  | .fvar id => return mixHash 37 (hash id.name)
  | .mvar id => return mixHash 41 (hash id.name)
  | .sort l => return mixHash 43 (levelHash l)
  | .const n ls => return ls.foldl (fun h l => mixHash h (levelHash l)) (mixHash 47 (hash n))
  | .lit (.natVal n) => return mixHash 53 (hash n)
  | .lit (.strVal s) => return mixHash 59 (hash s)
  | .mdata _ b => structHashAux b
  | _ =>
    if let some h := (← get)[e]? then return h
    let h ← match e with
      | .app f a => do pure (mixHash 61 (mixHash (← structHashAux f) (← structHashAux a)))
      | .lam _ t b _ => do pure (mixHash 67 (mixHash (← structHashAux t) (← structHashAux b)))
      | .forallE _ t b _ => do pure (mixHash 71 (mixHash (← structHashAux t) (← structHashAux b)))
      | .letE _ t v b _ => do
        pure (mixHash 73 (mixHash (← structHashAux t)
          (mixHash (← structHashAux v) (← structHashAux b))))
      | .proj s i b => do pure (mixHash 79 (mixHash (hash s) (mixHash (hash i) (← structHashAux b))))
      | _ => pure 0
    modify fun m => m.insert e h
    return h

/-- 64-bit structural hash of a closed statement. Ignores binder names, binder annotations and
`mdata`; universe parameters are renamed in order of first occurrence, so the same statement
proved in two declarations with differently named universes gets the same hash. -/
def statementHash (stmt : Expr) : UInt64 :=
  let ps := (collectLevelParams {} stmt).params
  let canon := (List.range ps.size).map fun i => Level.param (Name.mkNum `u i)
  let stmt := stmt.instantiateLevelParams ps.toList canon
  ((structHashAux stmt).run {}).1

/-! ### Interfaces -/

/-- The interface of a subterm: local declarations it depends on. -/
structure Interface where
  /-- all local fvars `e` (and its type) depend on, transitively, in local-context order. -/
  deps : Array Expr
  /-- the subset that becomes lemma arguments (everything except dependent `let` variables,
  which stay as `let` binders inside the lemma). -/
  args : Array Expr

/-- `collectFVars` that never records a variable twice. (`Lean.collectFVars s x` is
`CollectFVars.main x s`, and `main` on a *bare* free variable pushes it without consulting
`fvarSet`/`visitedExpr`; calling it on a dependency's type `ι` therefore used to add `ι` once per
dependency `x : ι`, giving statements like `∀ {ι} {ι} (s : Set ι), …`.) -/
private def collectFVarsOnce (st : CollectFVars.State) (x : Expr) : CollectFVars.State :=
  match x with
  | .fvar id =>
    if st.fvarSet.contains id then st
    else { st.add id with visitedExpr := st.visitedExpr.insert x }
  | _ => collectFVars st x

/-- Compute the interface of `e : ty` in the current local context. Every local variable occurs
at most once. -/
def interfaceOf (e ty : Expr) : MetaM Interface := do
  let lctx ← getLCtx
  let mut st : CollectFVars.State := collectFVarsOnce (collectFVarsOnce {} e) ty
  let mut i := 0
  while i < st.fvarIds.size do
    let fvarId := st.fvarIds[i]!
    let some d := lctx.find? fvarId | throwError "rosette: unknown free variable in subterm"
    st := collectFVarsOnce st d.type
    -- only the value of a *dependent* let is visible to the body
    if let some v := d.value? then st := collectFVarsOnce st v
    i := i + 1
  -- belt and braces: drop any repeated id
  let mut seen : FVarIdSet := {}
  let mut ids : Array FVarId := #[]
  for id in st.fvarIds do
    unless seen.contains id do
      seen := seen.insert id
      ids := ids.push id
  let decls := ids.filterMap lctx.find?
  let decls := decls.qsort fun a b => a.index < b.index
  return { deps := decls.map (·.toExpr), args := (decls.filter (!·.isLet)).map (·.toExpr) }

/-- Closed statement and closed proof of `e : ty` over its interface.
`have`-bound variables become ordinary hypotheses; dependent `let`s stay `let`s. -/
def closeOver (ifc : Interface) (e ty : Expr) : MetaM (Expr × Expr) := do
  let stmt ← mkForallFVars ifc.deps ty
  let val ← mkLambdaFVars ifc.deps e
  return (stmt, val)

/-! ### Traversal -/

/-- Extra behaviour for `Rosette.Lift`: called on the subterm at a selected path, returns the
replacement term. -/
structure LiftHook where
  targets : Array Path
  onTarget : Path → Expr → MetaM Expr

structure Ctx where
  cfg : Config
  /-- when set, run in rebuild mode: no candidates are recorded, only subterms on the way to a
  target are visited, and the rewritten term is returned. -/
  lift? : Option LiftHook := none

structure State where
  res : Result := {}
  sizes : Std.HashMap Expr Nat := {}
  /-- enumeration mode: subterms already visited ↦ the candidate recorded for them (if any). A
  subterm met again (same term, same local variables) would give exactly the same closed statement
  and sizes, so it is not visited again; only its `occurrences` count goes up. -/
  seen : Std.HashMap Expr (Option Nat) := {}
  /-- rebuild mode: original subterm ↦ rewritten subterm, for everything on the way to a target.
  Used to rewrite the other (identical) occurrences of a lifted subterm as well. -/
  rebuilt : Std.HashMap Expr Expr := {}

abbrev M := ReaderT Ctx (StateRefT State MetaM)

private def sizeOf' (e : Expr) : M Nat := do
  let s ← get
  let (n, sizes) := (treeSizeMemo e).run s.sizes
  set { s with sizes := sizes }
  return n

private def markTruncated (why : String) : M Unit :=
  modify fun s => if s.res.truncated then s else
    { s with res := { s.res with truncated := true, note := why } }

/-- `c x₁ … xₙ` / bare variables and constants: nothing to hide. -/
private def isTrivialShape (e : Expr) : Bool :=
  let f := e.getAppFn
  (f.isFVar || f.isConst || f.isSort || f.isLit || f.isBVar) && e.getAppArgs.all isAtom

private def kindOf : Expr → String
  | .app .. => "app" | .lam .. => "lam" | .letE (nondep := nd) .. => if nd then "have" else "let"
  | .proj .. => "proj" | _ => "other"

private def oneLine (s : String) (maxChars : Nat) : String :=
  let s := " ".intercalate ((s.splitOn "\n").map (·.trimAscii.toString))
  if s.length > maxChars then (s.take maxChars).toString ++ " …" else s

/-- Try to record `e` as a candidate. Returns the id of the new candidate, if `e` was recorded. -/
private def record (e : Expr) (path : Path) (parent : Option Nat) (role : String)
    (binderDepth : Nat) (tsize : Nat) : M (Option Nat) := do
  let cfg := (← read).cfg
  if isTrivialShape e then return none
  try
    let ty ← inferType e
    unless (← isProp ty) do return none
    let dsize := dagSize e
    if dsize < cfg.minProofSize then return none
    let ty := ty.headBeta
    let ifc ← interfaceOf e ty
    let stmt ← mkForallFVars ifc.deps ty
    let ssize := dagSize stmt
    let stsize ← sizeOf' stmt
    let mut numProp := 0
    for x in ifc.args do
      if ← isProp (← inferType x) then numProp := numProp + 1
    let str ←
      if cfg.ppStatements && ssize ≤ cfg.maxPpSize then
        pure (oneLine (← ppExpr stmt).pretty cfg.maxStmtChars)
      else if cfg.ppStatements then pure s!"<statement of {ssize} nodes not printed>"
      else pure ""
    let stmtIsClass := (← isClass? ty).isSome
    let id := (← get).res.cands.size
    let c : Candidate := {
      id, parent, path, depth := path.size, binderDepth, role, kind := kindOf e
      stmtIsClass, headConst := e.getAppFn.constName?
      proofSizeDag := dsize, proofSizeTree := tsize
      statementSize := ssize, statementSizeTree := stsize
      numDeps := ifc.args.size, numPropDeps := numProp
      hidingRatio := dsize.toFloat / ssize.toFloat
      statement := str, stmtHash := statementHash stmt }
    modify fun s => { s with res := { s.res with cands := s.res.cands.push c } }
    return some id
  catch ex =>
    if ex.isRuntime then throw ex
    modify fun s => { s with res := { s.res with errors := s.res.errors + 1 } }
    return none

/-- Visit `e` (all bound variables already replaced by local fvars). In enumeration mode returns
`e` unchanged; in rebuild mode returns `e` with the target subterms replaced. -/
partial def visit (e : Expr) (path : Path) (parent : Option Nat) (role : String)
    (binderDepth : Nat) : M Expr := do
  let ctx ← read
  let cfg := ctx.cfg
  let mut parent := parent
  match ctx.lift? with
  | some hook =>
    if hook.targets.contains path then
      let r ← hook.onTarget path e
      modify fun s => { s with rebuilt := s.rebuilt.insert e r }
      return r
    unless hook.targets.any (pathIsPrefix path ·) do
      -- off the way to any target: nothing to lift here, but identical copies of subterms that
      -- were already rewritten (shared subterms occur at several tree positions) are rewritten
      -- the same way, so that a lifted proof does not survive at its other positions
      let rb := (← get).rebuilt
      if rb.isEmpty then return e
      return e.replace fun x => rb[x]?
  | none =>
    let tsize ← sizeOf' e
    -- a subterm smaller than the threshold cannot contain a candidate
    if tsize < cfg.minProofSize then return e
    let s ← get
    if s.res.truncated then return e
    unless e.isMData do
      if let some c? := s.seen[e]? then
        -- same subterm again: count the position; a `have` value keeps its `haveValue` role
        if let some id := c? then
          modify fun s => { s with res := { s.res with cands := s.res.cands.modify id fun c =>
            { c with occurrences := c.occurrences + 1
                     role := if role == "haveValue" then role else c.role } } }
        return e
    if s.res.visited ≥ cfg.maxVisited then
      markTruncated s!"maxVisited = {cfg.maxVisited} reached"; return e
    if s.res.cands.size ≥ cfg.maxCandidates then
      markTruncated s!"maxCandidates = {cfg.maxCandidates} reached"; return e
    Core.checkSystem "rosette"
    modify fun s => { s with res := { s.res with visited := s.res.visited + 1 } }
    unless e.isMData do
      let rec? ← record e path parent role binderDepth tsize
      modify fun s => { s with seen := s.seen.insert e rec? }
      if rec?.isSome then parent := rec?
  let rebuild := ctx.lift?.isSome
  let r ← match e with
    | .app .. => do
      let f := e.getAppFn
      let args := e.getAppArgs
      let f' ← visit f (path.push 0) parent "fn" binderDepth
      let mut args' := Array.mkEmpty args.size
      for h : i in [0:args.size] do
        args' := args'.push (← visit args[i] (path.push (i + 1)) parent "arg" binderDepth)
      pure (if rebuild then mkAppN f' args' else e)
    | .lam .. =>
      lambdaTelescope e fun xs b => do
        let b' ← visit b (path.push 0) parent "lamBody" (binderDepth + xs.size)
        if rebuild then mkLambdaFVars xs b' else pure e
    | .letE n t v b nondep => do
      let v' ← visit v (path.push 0) parent (if nondep then "haveValue" else "letValue") binderDepth
      withLetDecl n t v (nondep := nondep) fun x => do
        let b' ← visit (b.instantiate1 x) (path.push 1) parent
          (if nondep then "haveBody" else "letBody") (binderDepth + 1)
        pure (if rebuild then .letE n t v' (b'.abstract #[x]) nondep else e)
    | .mdata d b => do
      let b' ← visit b (path.push 0) parent role binderDepth
      pure (if rebuild then .mdata d b' else e)
    | .proj s i b => do
      let b' ← visit b (path.push 0) parent "proj" binderDepth
      pure (if rebuild then .proj s i b' else e)
    | _ => pure e
  if rebuild then modify fun s => { s with rebuilt := s.rebuilt.insert e r }
  return r

/-- Run `x` with its own heartbeat budget. -/
def withBudget (maxHeartbeats : Nat) (x : MetaM α) : MetaM α :=
  withCurrHeartbeats <|
    withTheReader Core.Context (fun c => { c with maxHeartbeats := maxHeartbeats * 1000 }) x

/-- Enumerate the candidates of a proof term in the current local context. Never throws on
budget exhaustion: the partial result is returned with `truncated := true`. -/
def candidatesOfExprCore (e : Expr) (cfg : Config := {}) : MetaM Result := do
  let ref ← IO.mkRef ({} : State)
  let act : MetaM Unit := withBudget cfg.maxHeartbeats do
    discard <| ((visit e #[] none "root" 0).run { cfg }) ref
  -- the state lives in `ref`, so whatever was found before an exception survives
  try
    tryCatchRuntimeEx act fun ex => do
      let msg ← ex.toMessageData.toString
      ref.modify fun s => { s with res := { s.res with truncated := true, note := oneLine msg 200 } }
  catch ex =>
    let msg ← ex.toMessageData.toString
    ref.modify fun s => { s with res := { s.res with truncated := true, note := oneLine msg 200 } }
  return (← ref.get).res

def candidatesOfExpr (e : Expr) (cfg : Config := {}) : MetaM (Array Candidate) :=
  return (← candidatesOfExprCore e cfg).cands

/-- The proof term of a theorem (or the value of a definition). -/
def proofOfConst (n : Name) : MetaM Expr := do
  let info ← getConstInfo n
  match info.value? (allowOpaque := true) with
  | some v => return v
  | none => throwError "rosette: '{n}' has no value (axiom, constructor, recursor, …)"

def candidatesOfConstCore (n : Name) (cfg : Config := {}) : MetaM Result := do
  candidatesOfExprCore (← proofOfConst n) cfg

/-- All candidate lemma boundaries of the proof of `n`. -/
def candidatesOfConst (n : Name) : MetaM (Array Candidate) :=
  return (← candidatesOfConstCore n).cands

/-! ### JSON -/

private def hex64 (h : UInt64) : String :=
  let s := String.ofList (Nat.toDigits 16 h.toNat)
  "".pushn '0' (16 - s.length) ++ s

def Candidate.toJson (decl : Name) (c : Candidate) : Json :=
  Json.mkObj [
    ("record", "candidate"),
    ("decl", Lean.toJson decl),
    ("id", Lean.toJson c.id),
    ("parent", match c.parent with | some p => Lean.toJson p | none => Json.null),
    ("path", Lean.toJson (pathToString c.path)),
    ("depth", Lean.toJson c.depth),
    ("binderDepth", Lean.toJson c.binderDepth),
    ("role", Lean.toJson c.role),
    ("kind", Lean.toJson c.kind),
    ("stmtIsClass", Lean.toJson c.stmtIsClass),
    ("headConst", match c.headConst with | some h => Lean.toJson h | none => Json.null),
    ("proofSizeDag", Lean.toJson c.proofSizeDag),
    ("proofSizeTree", Lean.toJson c.proofSizeTree),
    ("statementSize", Lean.toJson c.statementSize),
    ("statementSizeTree", Lean.toJson c.statementSizeTree),
    ("numDeps", Lean.toJson c.numDeps),
    ("numPropDeps", Lean.toJson c.numPropDeps),
    ("hidingRatio", Lean.toJson c.hidingRatio),
    ("statement", Lean.toJson c.statement),
    -- 64-bit value, as hex text: JSON numbers lose precision above 2^53
    ("stmtHash", Lean.toJson (hex64 c.stmtHash)),
    ("occurrences", Lean.toJson c.occurrences)]

/-- One summary line per declaration (`"record": "decl"`), so consumers know about truncation and
failures instead of silently seeing fewer rows. -/
def Result.summaryJson (decl : Name) (r : Result) (ok : Bool) : Json :=
  Json.mkObj [
    ("record", "decl"), ("decl", toJson decl), ("ok", toJson ok),
    ("numCandidates", toJson r.cands.size), ("visited", toJson r.visited),
    ("errors", toJson r.errors), ("truncated", toJson r.truncated), ("note", toJson r.note)]

/-- Append the candidates of each declaration to `path` as JSON lines: one `"record": "decl"`
summary line per declaration followed by one `"record": "candidate"` line per candidate. Declarations that fail
(no value, exception) get a summary line with `"ok": false`. Returns (#decls ok, #candidates). -/
def dumpCandidatesJsonl (decls : Array Name) (path : System.FilePath) (cfg : Config := {})
    (append : Bool := false) : MetaM (Nat × Nat) := do
  let h ← IO.FS.Handle.mk path (if append then .append else .write)
  let mut nOk := 0
  let mut nCands := 0
  for d in decls do
    let r? ← try
        let r ← candidatesOfConstCore d cfg
        pure (Except.ok r)
      catch ex => pure (Except.error (← ex.toMessageData.toString))
    match r? with
    | .ok r =>
      h.putStrLn (r.summaryJson d true).compress
      for c in r.cands do h.putStrLn (c.toJson d).compress
      nOk := nOk + 1
      nCands := nCands + r.cands.size
    | .error msg =>
      h.putStrLn (({ note := oneLine msg 200 } : Result).summaryJson d false).compress
  h.flush
  return (nOk, nCands)

/-! ### Commands -/

private def fmtRatio (x : Float) : String :=
  let n := (x * 100).round.toUInt64.toNat
  let frac := n % 100
  s!"{n / 100}.{if frac < 10 then "0" else ""}{frac}"

def Candidate.format (c : Candidate) : String :=
  s!"#{c.id} ratio={fmtRatio c.hidingRatio} proof(dag={c.proofSizeDag}, tree={c.proofSizeTree}) \
    stmt={c.statementSize} deps={c.numDeps} (props={c.numPropDeps}) depth={c.depth} \
    {c.role}/{c.kind} @{pathToString c.path}{if c.occurrences > 1 then s!" (x{c.occurrences})" else ""}\n    {c.statement}"

/-- Candidates sorted by decreasing hiding ratio. -/
def sortByRatio (cs : Array Candidate) : Array Candidate :=
  cs.qsort fun a b => a.hidingRatio > b.hidingRatio

/-- `#rosette_candidates Foo.bar` prints the 10 candidate lemma boundaries of the proof of
`Foo.bar` with the highest hiding ratio; `#rosette_candidates Foo.bar 25` prints 25. -/
elab "#rosette_candidates " id:ident n:(num)? : command => do
  let name ← liftCoreM <| realizeGlobalConstNoOverloadWithInfo id
  let top := (n.map (·.getNat)).getD 10
  let r ← liftTermElabM <| candidatesOfConstCore name
  let sorted := sortByRatio r.cands
  let mut msg := s!"{name}: {r.cands.size} candidates ({r.visited} subterms visited, \
    {r.errors} skipped on error{if r.truncated then s!", TRUNCATED: {r.note}" else ""})"
  for c in sorted.extract 0 top do
    msg := msg ++ "\n" ++ c.format
  logInfo msg

/-- `#rosette_dump "out/file.jsonl" Foo.bar Baz.qux …` writes the candidates of the listed
declarations as JSON lines. -/
elab "#rosette_dump " path:str ids:(ppSpace ident)+ : command => do
  let names ← ids.mapM fun id => liftCoreM <| realizeGlobalConstNoOverloadWithInfo id
  let (nOk, nCands) ← liftTermElabM <| dumpCandidatesJsonl names path.getString
  logInfo s!"wrote {nCands} candidates of {nOk}/{names.size} declarations to {path.getString}"

end Rosette
