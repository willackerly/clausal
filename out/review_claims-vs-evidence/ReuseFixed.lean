/-
Rosette.Reuse — data collection for hypothesis H2: do closed sub-statements of proofs recur
across *different* theorems?

For every theorem of a few Mathlib slices this file enumerates the Prop-typed subterms of the
proof term (same notion of candidate as `Rosette.Candidates`: same traversal order, same interface
computation, same exact statement hash) and records, per candidate, three keys of its closed
statement `∀ deps, type(e)`:

* `stmtHash` (level E, exact): `Rosette.statementHash` — equal up to bound-variable names, binder
  annotations, `mdata` and names of universe parameters.
* `h1` (level L1, "literals, universes and instances abstracted"): the structural hash of the
  statement in which
    - every literal (`Expr.lit`) is one token `LIT`,
    - every sort and every universe-level argument of a constant is ignored,
    - every argument of a constant-headed application that sits at an instance-implicit (`[..]`)
      binder position of that constant's type is one token `INST`.
  Everything else (constants, bound variables with their de Bruijn indices, binder structure) is
  kept.
* `h2` (level L2, "depth-2 shape"): L1, and in addition
    - every bound variable is one token `VAR`,
    - application nesting is cut at depth 2: writing each hypothesis and the conclusion as
      `c a₁ … aₙ`, the head `c` and the heads of the `aᵢ` are kept, the arguments of the `aᵢ` are
      replaced by one token `HOLE`. Binders (`∀`, `fun`, `let`) and projections do not increase
      the depth.
  L2 is deliberately coarse: it is an upper bound on "the same statement up to generalisation".

To say what an L1 / L2 cluster actually has in common we compute the least general generalisation
(first-order anti-unifier) of its member statements: `lgg a b` keeps the common structure and puts
a hole `◻` wherever the two terms differ (different head, different arity, different leaf).  The
number of holes says how many extra arguments a shared general lemma would need; nothing here
checks that the generalised statement is provable.

"Is it already in Mathlib?" is answered three ways:
* `inLib`: a theorem of the environment whose type has the same exact hash (argument order
  matters, so this undercounts);
* `inLibL1`: same at level L1;
* `exact?`: for the recurring exact statements that are not typeclasses and have no hash match
  (largest gross saving first, up to `ROSETTE_REUSE_EXACT` of them),
  `Lean.Meta.LibrarySearch.librarySearch` is run on the statement with a 20,000k heartbeat budget.
Per candidate we also record `numAuto`, the number of tactic-framework constants in its proof
(certificates of `ring` / `linarith` / `norm_num` / `omega` …, see `isAutoConst`), and
`numThms` = number of distinct theorem constants its proof term mentions
  (`≤ 1` means the proof is a single library-lemma application padded by terms/instances).

Run from the project root (needs `lake build Rosette.Candidates` first):

    ROSETTE_REUSE=1 lake env lean Rosette/Reuse.lean

Environment variables: `ROSETTE_REUSE_OUT` (default `out/reuse`), `ROSETTE_REUSE_MINPROOF`
(minimum DAG size of a theorem's proof, default 800), `ROSETTE_REUSE_MAXDECLS` (cap per slice,
default 0 = none; when set, the theorems with the smallest name hash are kept),
`ROSETTE_REUSE_EXACT` (how many statements to try `exact?` on, default 100000 = all recurring
ones; this is the slow part, about 0.25 s per statement).

Outputs (JSON lines): `candidates.jsonl` (one `decl` record per theorem, then its candidates),
`statements.jsonl` (one record per distinct exact statement), `lgg.jsonl` (one record per L1 / L2
cluster that spans ≥ 2 theorems and ≥ 2 distinct statements), `run.json` (parameters, counts).
Without `ROSETTE_REUSE` the file only elaborates.
-/
import Mathlib
import Rosette.Candidates

open Lean Meta

namespace Rosette.Reuse

/-! ## Slices -/

/-- (label, module-name prefixes). -/
def slices : Array (String × Array String) := #[
  ("measure", #["Mathlib.MeasureTheory.Constructions.", "Mathlib.MeasureTheory.Covering."]),
  ("graph", #["Mathlib.Combinatorics.SimpleGraph."]),
  ("lseries", #["Mathlib.NumberTheory.LSeries."])]

/-! ## Name filter (same rules as `Rosette.Corpus`, which is not importable as a module yet) -/

def generatedSuffixes : List String :=
  ["eq_def", "eq_unfold", "congr_simp", "sizeOf_spec", "injEq", "inj", "noConfusion",
   "noConfusionType", "rec", "recOn", "casesOn", "brecOn", "binductionOn", "below", "ibelow",
   "ctorIdx", "induct", "induct_unfolding", "fun_cases", "fun_cases_unfolding", "elim",
   "ext_iff", "mk_inj", "mk_injEq", "ofNat_ctorIdx", "toCtorIdx", "ind", "omega_nat"]

def isGeneratedComp (s : String) : Bool :=
  s.startsWith "_" || s.startsWith "match_" || s.startsWith "proof_" ||
  s.startsWith "hcongr_" || s.startsWith "inst" ||
  (s.startsWith "eq_" && (s.drop 3).all Char.isDigit && s.length > 3) ||
  generatedSuffixes.contains s

def isAutoName (n : Name) : Bool :=
  let u := privateToUserName n
  u.isAnonymous || go u
where
  go : Name → Bool
    | .anonymous => false
    | .num _ _ => true
    | .str p s => isGeneratedComp s || go p

/-! ## Generalised statement hashes -/

structure GState where
  memo : Std.HashMap (Expr × Nat) UInt64 := {}
  inst : Std.HashMap Name (Array Bool) := {}

/-- For each argument position of constant `n`: is the binder instance-implicit? -/
def instMask (env : Environment) (n : Name) : StateM GState (Array Bool) := do
  if let some m := (← get).inst[n]? then return m
  let m := match env.find? n with
    | some ci => Id.run do
      let mut t := ci.type
      let mut out := #[]
      while t.isForall do
        out := out.push t.bindingInfo!.isInstImplicit
        t := t.bindingBody!
      return out
    | none => #[]
  modify fun s => { s with inst := s.inst.insert n m }
  return m

def tokLit : UInt64 := 1009
def tokSort : UInt64 := 1013
def tokInst : UInt64 := 1019
def tokVar : UInt64 := 1021
def tokHole : UInt64 := 1031

/-- Generalised structural hash. `maxDepth = none` is level L1; `some k` is the depth-`k` shape
(L2 uses `k = 2`). `d` is the current application-nesting depth. -/
partial def gHash (env : Environment) (maxDepth : Option Nat) (e : Expr) (d : Nat) :
    StateM GState UInt64 := do
  let shape := maxDepth.isSome
  if let some k := maxDepth then
    if d ≥ k then return tokHole
  match e with
  | .mdata _ b => gHash env maxDepth b d
  | .lit _ => return tokLit
  | .sort _ => return tokSort
  | .const n _ => return mixHash 47 (hash n)
  | .bvar i => return if shape then tokVar else mixHash 31 (hash i)
  | .fvar id => return mixHash 37 (hash id.name)
  | .mvar id => return mixHash 41 (hash id.name)
  | _ =>
    if let some h := (← get).memo[(e, d)]? then return h
    let h ← match e with
      | .app .. => do
        let f := e.getAppFn
        let args := e.getAppArgs
        let mask ← match f with
          | .const n _ => instMask env n
          | _ => pure #[]
        let mut h := mixHash 61 (mixHash (← gHash env maxDepth f d) (hash args.size))
        for i in [0:args.size] do
          let ha ← if mask.getD i false then pure tokInst else gHash env maxDepth args[i]! (d + 1)
          h := mixHash h ha
        pure h
      | .lam _ t b _ => do
        pure (mixHash 67 (mixHash (← gHash env maxDepth t d) (← gHash env maxDepth b d)))
      | .forallE _ t b _ => do
        pure (mixHash 71 (mixHash (← gHash env maxDepth t d) (← gHash env maxDepth b d)))
      | .letE _ t v b _ => do
        pure (mixHash 73 (mixHash (← gHash env maxDepth t d)
          (mixHash (← gHash env maxDepth v d) (← gHash env maxDepth b d))))
      | .proj s i b => do
        pure (mixHash 79 (mixHash (hash s) (mixHash (hash i) (← gHash env maxDepth b d))))
      | _ => pure 0
    modify fun s => { s with memo := s.memo.insert (e, d) h }
    return h

/-- (L1 hash, L2 hash) of a closed statement. The instance-mask cache is threaded through. -/
def genHashes (env : Environment) (stmt : Expr) (cache : Std.HashMap Name (Array Bool)) :
    (UInt64 × UInt64) × Std.HashMap Name (Array Bool) :=
  let (h1, s1) := (gHash env none stmt 0).run { inst := cache }
  let (h2, s2) := (gHash env (some 2) stmt 0).run { inst := s1.inst }
  ((h1, h2), s2.inst)

/-! ## Anti-unification -/

def holeName : Name := `«◻»
def holeExpr : Expr := .const holeName []
def isHole (e : Expr) : Bool := e.isConstOf holeName

/-- Least general generalisation of two closed terms; the state counts the holes created. -/
partial def lgg (a b : Expr) : StateM Nat Expr := do
  let a := a.consumeMData
  let b := b.consumeMData
  let hole : StateM Nat Expr := do modify (· + 1); pure holeExpr
  if isHole a || isHole b then return ← hole
  match a, b with
  | .app f1 x1, .app f2 x2 =>
    if a.getAppNumArgs != b.getAppNumArgs then return ← hole
    let before ← get
    let f ← lgg f1 f2
    if isHole f then
      set (before + 1); return holeExpr
    return .app f (← lgg x1 x2)
  | .forallE n t1 b1 bi, .forallE _ t2 b2 _ => return .forallE n (← lgg t1 t2) (← lgg b1 b2) bi
  | .lam n t1 b1 bi, .lam _ t2 b2 _ => return .lam n (← lgg t1 t2) (← lgg b1 b2) bi
  | .letE n t1 v1 b1 nd, .letE _ t2 v2 b2 _ =>
    return .letE n (← lgg t1 t2) (← lgg v1 v2) (← lgg b1 b2) nd
  | .proj s i x1, .proj s' i' x2 =>
    if s == s' && i == i' then return .proj s i (← lgg x1 x2) else hole
  | .const n1 _, .const n2 _ => if n1 == n2 then return a else hole
  | .sort _, .sort _ => return a
  | .bvar i, .bvar j => if i == j then return a else hole
  | .lit l1, .lit l2 => if l1 == l2 then return a else hole
  | _, _ => hole

/-- Number of hole occurrences in a term seen as a tree is not what we want; count the holes of
the final anti-unifier (as a tree, each occurrence is one extra lemma argument at most). -/
partial def countHoles (e : Expr) : Nat :=
  match e with
  | .app f a => countHoles f + countHoles a
  | .lam _ t b _ | .forallE _ t b _ => countHoles t + countHoles b
  | .letE _ t v b _ => countHoles t + countHoles v + countHoles b
  | .mdata _ b | .proj _ _ b => countHoles b
  | .const n _ => if n == holeName then 1 else 0
  | _ => 0

/-! ## Candidate enumeration with the extra keys -/

structure Cand where
  id : Nat
  parent : Option Nat
  role : String
  kind : String
  stmtIsClass : Bool
  headConst : Option Name
  conclHead : Option Name
  proofSizeDag : Nat
  proofSizeTree : Nat
  statementSize : Nat
  numDeps : Nat
  numPropDeps : Nat
  numThms : Nat
  /-- distinct tactic-framework constants (`isAutoConst`) the proof mentions. -/
  numAuto : Nat
  stmtHash : UInt64
  h1 : UInt64
  h2 : UInt64
  proofHash : UInt64

structure St where
  cands : Array Cand := #[]
  visited : Nat := 0
  errors : Nat := 0
  truncated : Bool := false
  note : String := ""
  sizes : Std.HashMap Expr Nat := {}
  /-- distinct exact statements seen so far (global across declarations). -/
  stmts : Std.HashMap UInt64 (Expr × String) := {}
  instCache : Std.HashMap Name (Array Bool) := {}

abbrev M := StateRefT St MetaM

def oneLine (s : String) (maxChars : Nat) : String :=
  let s := " ".intercalate ((s.splitOn "\n").map (·.trimAscii.toString))
  if s.length > maxChars then (s.take maxChars).toString ++ " …" else s

private def isAtom : Expr → Bool
  | .app .. | .lam .. | .forallE .. | .letE .. | .mdata .. | .proj .. => false
  | _ => true

private def isTrivialShape (e : Expr) : Bool :=
  let f := e.getAppFn
  (f.isFVar || f.isConst || f.isSort || f.isLit || f.isBVar) && e.getAppArgs.all isAtom

private def kindOf : Expr → String
  | .app .. => "app" | .lam .. => "lam" | .letE (nondep := nd) .. => if nd then "have" else "let"
  | .proj .. => "proj" | _ => "other"

def tsize (e : Expr) : M Nat := do
  let s ← get
  let (n, sizes) := (treeSizeMemo e).run s.sizes
  set { s with sizes := sizes }
  return n

def minProofSize : Nat := 20
def maxVisited : Nat := 300000
def maxCands : Nat := 20000
def maxPpSize : Nat := 1500

/-- Constants that belong to a tactic framework (certificates emitted by `ring`, `linarith`,
`norm_num`, `omega`, `positivity`, `grind`, …). -/
def autoPrefixes : List String :=
  ["Mathlib.Tactic.", "Mathlib.Meta.", "Linarith.", "Nat.Linarith.", "Int.Linarith.",
   "Lean.Omega.", "Int.Linear.", "Nat.Linear.", "Lean.Grind.", "Nat.Simproc.", "Int.Simproc.",
   "Polyrith.", "Lean.RArray.", "Std.Tactic."]

def isAutoConst (n : Name) : Bool :=
  let s := n.toString
  autoPrefixes.any (s.startsWith ·)

/-- `Rosette.interfaceOf` with duplicates removed.  (`interfaceOf` calls `collectFVars st d.type`,
which goes through `CollectFVars.main` and so skips the visited check when `d.type` is a bare
free variable: every dependency `x : α` adds `α` once more, giving statements such as
`∀ {ι : Type u} {ι : Type u} (s : Set ι), …`.) -/
def interfaceDedup (e ty : Expr) : MetaM Interface := do
  let ifc ← Rosette.interfaceOf e ty
  let dedup (xs : Array Expr) : Array Expr :=
    xs.foldl (fun acc x => if acc.contains x then acc else acc.push x) #[]
  return { deps := dedup ifc.deps, args := dedup ifc.args }

def record (e : Expr) (parent : Option Nat) (role : String) (ts : Nat) : M (Option Nat) := do
  if isTrivialShape e then return parent
  try
    let ty ← inferType e
    unless (← isProp ty) do return parent
    let dsize := dagSize e
    if dsize < minProofSize then return parent
    let ty := ty.headBeta
    let ifc ← interfaceDedup e ty
    let stmt ← mkForallFVars ifc.deps ty
    let val ← mkLambdaFVars ifc.deps e
    let ssize := dagSize stmt
    let mut numProp := 0
    for x in ifc.args do
      if ← isProp (← inferType x) then numProp := numProp + 1
    let env ← getEnv
    let sh := statementHash stmt
    let ((h1, h2), cache) := genHashes env stmt (← get).instCache
    modify fun s => { s with instCache := cache }
    unless (← get).stmts.contains sh do
      let str ← if ssize ≤ maxPpSize then
          (do pure (oneLine (← ppExpr stmt).pretty 400)) <|> pure "<pp failed>"
        else pure s!"<statement of {ssize} nodes not printed>"
      modify fun s => { s with stmts := s.stmts.insert sh (stmt, str) }
    let used := e.getUsedConstantsAsSet.toList
    let numThms := (used.filter fun c =>
      match env.find? c with | some (.thmInfo _) => true | _ => false).length
    let numAuto := (used.filter isAutoConst).length
    let stmtIsClass := (← isClass? ty).isSome
    let id := (← get).cands.size
    let c : Cand := {
      id, parent, role, kind := kindOf e, stmtIsClass
      headConst := e.getAppFn.constName?
      conclHead := ty.getForallBody.getAppFn.constName?
      proofSizeDag := dsize, proofSizeTree := ts, statementSize := ssize
      numDeps := ifc.args.size, numPropDeps := numProp, numThms, numAuto
      stmtHash := sh, h1, h2, proofHash := statementHash val }
    modify fun s => { s with cands := s.cands.push c }
    return some id
  catch ex =>
    if ex.isRuntime then throw ex
    modify fun s => { s with errors := s.errors + 1 }
    return parent

/-- Same traversal as `Rosette.visit` in enumeration mode. -/
partial def walk (e : Expr) (parent : Option Nat) (role : String) : M Unit := do
  let ts ← tsize e
  if ts < minProofSize then return
  let s ← get
  if s.truncated then return
  if s.visited ≥ maxVisited then
    modify fun s => { s with truncated := true, note := "maxVisited reached" }; return
  if s.cands.size ≥ maxCands then
    modify fun s => { s with truncated := true, note := "maxCandidates reached" }; return
  Core.checkSystem "rosette"
  modify fun s => { s with visited := s.visited + 1 }
  let mut parent := parent
  unless e.isMData do
    parent ← record e parent role ts
  match e with
  | .app .. =>
    walk e.getAppFn parent "fn"
    for a in e.getAppArgs do walk a parent "arg"
  | .lam .. => lambdaTelescope e fun _ b => walk b parent "lamBody"
  | .letE n t v b nondep =>
    walk v parent (if nondep then "haveValue" else "letValue")
    withLetDecl n t v (nondep := nondep) fun x =>
      walk (b.instantiate1 x) parent (if nondep then "haveBody" else "letBody")
  | .mdata _ b => walk b parent role
  | .proj _ _ b => walk b parent "proj"
  | _ => return

def hex64 (h : UInt64) : String :=
  let s := String.ofList (Nat.toDigits 16 h.toNat)
  "".pushn '0' (16 - s.length) ++ s

def optName : Option Name → Json
  | some n => toJson n.toString
  | none => Json.null

def Cand.toJson (decl : Name) (c : Cand) : Json :=
  Json.mkObj [
    ("record", "candidate"), ("decl", decl.toString), ("id", c.id),
    ("parent", match c.parent with | some p => Lean.toJson p | none => Json.null),
    ("role", c.role), ("kind", c.kind), ("stmtIsClass", c.stmtIsClass),
    ("headConst", optName c.headConst), ("conclHead", optName c.conclHead),
    ("proofSizeDag", c.proofSizeDag), ("proofSizeTree", c.proofSizeTree),
    ("statementSize", c.statementSize), ("numDeps", c.numDeps), ("numPropDeps", c.numPropDeps),
    ("numThms", c.numThms), ("numAuto", c.numAuto), ("stmtHash", hex64 c.stmtHash), ("h1", hex64 c.h1),
    ("h2", hex64 c.h2), ("proofHash", hex64 c.proofHash)]

/-! ## Driver -/

def envNat (var : String) (dflt : Nat) : IO Nat := do
  return ((← IO.getEnv var).bind String.toNat?).getD dflt

/-- Aggregate per key: theorems it occurs in, distinct exact statements, proof sizes. -/
structure Agg where
  decls : Array Name := #[]
  stmts : Array UInt64 := #[]
  sumProof : Nat := 0
  minProof : Nat := 0
  maxProof : Nat := 0
  anyClass : Bool := false
  /-- (theorem, closed proof) pairs already counted: the traversal visits tree positions, so a
  shared subterm is met many times inside one theorem. -/
  seen : Std.HashSet UInt64 := {}

def Agg.add (a : Agg) (d : Name) (sh : UInt64) (p : Nat) (cls : Bool) (ph : UInt64) : Agg :=
  let k := mixHash (hash d) ph
  if a.seen.contains k then a else
  { seen := a.seen.insert k
    decls := if a.decls.contains d then a.decls else a.decls.push d
    stmts := if a.stmts.size ≥ 40 || a.stmts.contains sh then a.stmts else a.stmts.push sh
    sumProof := a.sumProof + p
    minProof := if a.sumProof == 0 then p else min a.minProof p
    maxProof := max a.maxProof p
    anyClass := a.anyClass || cls }

/-- Try to close `stmt` with `exact?`. Returns (status, lemma used). -/
def tryExact (stmt : Expr) (heartbeatsK : Nat) : MetaM (String × Option Name) := do
  let act : MetaM (String × Option Name) := withoutModifyingState <| withBudget heartbeatsK do
    let g ← mkFreshExprMVar stmt
    let (_, g') ← g.mvarId!.intros
    match ← g'.withContext (LibrarySearch.librarySearch g') with
    | none =>
      let pf ← instantiateMVars (mkMVar g')
      return ("closed", pf.getAppFn.constName?)
    | some _ => return ("open", none)
  try
    tryCatchRuntimeEx act fun _ => pure ("timeout", none)
  catch _ => pure ("error", none)

def run : MetaM Unit := do
  let env ← getEnv
  let outDir : System.FilePath := (← IO.getEnv "ROSETTE_REUSE_OUT").getD "out/reuse"
  let minThm ← envNat "ROSETTE_REUSE_MINPROOF" 800
  let maxDecls ← envNat "ROSETTE_REUSE_MAXDECLS" 0
  let nExact ← envNat "ROSETTE_REUSE_EXACT" 100000
  IO.FS.createDirAll outDir
  let modNames := env.header.moduleNames
  let addImages : NameSet :=
    (Mathlib.Tactic.ToAdditive.translations.getState env).get.foldl
      (fun s src info => if info.translation == src then s else s.insert info.translation) {}
  -- 1. select theorems; 2. hash every theorem statement of the environment
  let mut sel : Array (Array (Name × Name × Nat)) := slices.map fun _ => #[]
  let mut libE : Std.HashMap UInt64 (Array Name) := {}
  let mut libL1 : Std.HashMap UInt64 (Array Name) := {}
  let mut instCache : Std.HashMap Name (Array Bool) := {}
  let mut nLib := 0
  for (n, ci) in env.constants.map₁ do
    let .thmInfo t := ci | continue
    nLib := nLib + 1
    let auto := isAutoName n
    -- library table: keep at most 3 names per hash, human names first
    let he := statementHash t.type
    let (h1, s) := (gHash env none t.type 0).run { inst := instCache }
    instCache := s.inst
    let put (m : Std.HashMap UInt64 (Array Name)) (h : UInt64) :=
      let cur := m.getD h #[]
      if cur.size ≥ 3 then m else m.insert h (if auto then cur.push n else #[n] ++ cur)
    libE := put libE he
    libL1 := put libL1 h1
    if auto || addImages.contains n || Meta.isInstanceCore env n then continue
    let some idx := env.getModuleIdxFor? n | continue
    let mn := modNames[idx.toNat]!
    let ms := mn.toString ++ "."
    for i in [0:slices.size] do
      if slices[i]!.2.any (ms.startsWith ·) then
        let sz := dagSize t.value
        if sz ≥ minThm then sel := sel.modify i (·.push (n, mn, sz))
  IO.println s!"library theorems hashed: {nLib}"
  let mut decls : Array (String × Name × Name × Nat) := #[]
  let mut selCounts : Array Json := #[]
  for i in [0:slices.size] do
    let all := sel[i]!
    let mut xs := all.qsort fun a b => a.1.toString < b.1.toString
    if maxDecls > 0 && xs.size > maxDecls then
      xs := (xs.qsort fun a b => hash a.1.toString < hash b.1.toString).extract 0 maxDecls
      xs := xs.qsort fun a b => a.1.toString < b.1.toString
    IO.println s!"slice {slices[i]!.1}: {all.size} theorems with proof ≥ {minThm}, {xs.size} used"
    selCounts := selCounts.push <| Json.mkObj [("slice", slices[i]!.1),
      ("prefixes", toJson slices[i]!.2), ("eligible", all.size), ("used", xs.size)]
    for (n, mn, sz) in xs do decls := decls.push (slices[i]!.1, n, mn, sz)
  -- 3. enumerate
  let ref ← IO.mkRef ({ instCache } : St)
  let h ← IO.FS.Handle.mk (outDir / "candidates.jsonl") .write
  -- per-key aggregates
  let mut aggE : Std.HashMap UInt64 Agg := {}
  let mut aggL1 : Std.HashMap UInt64 Agg := {}
  let mut aggL2 : Std.HashMap UInt64 Agg := {}
  let mut nOk := 0
  let mut nTrunc := 0
  let mut nFail := 0
  let mut nCands := 0
  let t0 ← IO.monoMsNow
  for (slice, n, mn, sz) in decls do
    ref.modify fun s => { s with cands := #[], visited := 0, errors := 0, truncated := false,
                                 note := "", sizes := {} }
    let t1 ← IO.monoMsNow
    let mut ok := true
    let act : MetaM Unit := withBudget 200000 do
      (walk (← proofOfConst n) none "root") ref
    try
      tryCatchRuntimeEx act fun ex => do
        let msg ← ex.toMessageData.toString
        ref.modify fun s => { s with truncated := true, note := oneLine msg 200 }
    catch ex =>
      let msg ← ex.toMessageData.toString
      ok := false
      ref.modify fun s => { s with truncated := true, note := oneLine msg 200 }
    let s ← ref.get
    let t2 ← IO.monoMsNow
    h.putStrLn (Json.mkObj [("record", "decl"), ("decl", n.toString), ("slice", slice),
      ("module", mn.toString), ("proofSizeDag", sz), ("ok", ok),
      ("numCandidates", s.cands.size), ("visited", s.visited), ("errors", s.errors),
      ("truncated", s.truncated), ("note", s.note), ("ms", t2 - t1)]).compress
    if !ok then nFail := nFail + 1 else nOk := nOk + 1
    if s.truncated then nTrunc := nTrunc + 1
    for c in s.cands do
      h.putStrLn (c.toJson n).compress
      nCands := nCands + 1
      -- the root restates the theorem: never a factoring candidate
      if c.role != "root" then
        aggE := aggE.insert c.stmtHash ((aggE.getD c.stmtHash {}).add n c.stmtHash c.proofSizeDag c.stmtIsClass c.proofHash)
        aggL1 := aggL1.insert c.h1 ((aggL1.getD c.h1 {}).add n c.stmtHash c.proofSizeDag c.stmtIsClass c.proofHash)
        aggL2 := aggL2.insert c.h2 ((aggL2.getD c.h2 {}).add n c.stmtHash c.proofSizeDag c.stmtIsClass c.proofHash)
  h.flush
  let t3 ← IO.monoMsNow
  IO.println s!"enumerated {decls.size} theorems ({nOk} ok, {nFail} failed, {nTrunc} truncated), \
    {nCands} candidates, {(t3 - t0) / 1000}s"
  let st ← ref.get
  -- 4. exact? on the top recurring exact statements with no library hash match
  let mut todo : Array (UInt64 × Nat) := #[]
  for (sh, a) in aggE do
    if a.decls.size ≥ 2 && !a.anyClass && !libE.contains sh then
      todo := todo.push (sh, a.sumProof - a.maxProof)
  todo := (todo.qsort fun a b => a.2 > b.2 || (a.2 == b.2 && a.1 < b.1)).extract 0 nExact
  let wantedTxt ← IO.FS.readFile "out/review_claims-vs-evidence/substantive_keys.txt"
  let wanted : Std.HashSet String := Std.HashSet.ofList (wantedTxt.splitOn "\n")
  todo := todo.filter fun (sh, _) => wanted.contains (hex64 sh)
  let mut exactRes : Std.HashMap UInt64 (String × Option Name) := {}
  let t4 ← IO.monoMsNow
  for (sh, _) in todo do
    let some (stmt, _) := st.stmts[sh]? | continue
    exactRes := exactRes.insert sh (← tryExact stmt 20000)
  let t5 ← IO.monoMsNow
  IO.println s!"exact? tried on {todo.size} statements, {(t5 - t4) / 1000}s"
  -- 5. statements
  let hs ← IO.FS.Handle.mk (outDir / "statements.jsonl") .write
  for (sh, (stmt, str)) in st.stmts do
    let ((h1, _), _) := genHashes env stmt st.instCache
    let names (m : Std.HashMap UInt64 (Array Name)) (k : UInt64) : Json :=
      toJson ((m.getD k #[]).map (·.toString))
    let (ex, exLemma) := exactRes.getD sh ("notrun", none)
    hs.putStrLn (Json.mkObj [("stmtHash", hex64 sh), ("statement", str),
      ("inLib", names libE sh), ("inLibL1", names libL1 h1),
      ("exact", ex), ("exactLemma", optName exLemma)]).compress
  hs.flush
  -- 6. anti-unifiers of L1 / L2 clusters
  let hl ← IO.FS.Handle.mk (outDir / "lgg.jsonl") .write
  let mut nLgg := 0
  for (level, agg) in [("L1", aggL1), ("L2", aggL2)] do
    for (k, a) in agg do
      if a.decls.size < 2 || a.stmts.size < 2 then continue
      let es := a.stmts.filterMap fun sh => (st.stmts[sh]?).map (·.1)
      if es.size < 2 then continue
      let g := es.foldl (init := es[0]!) fun g e => ((lgg g e).run 0).1
      let holes := countHoles g
      let gsize := dagSize g
      let str ← if gsize ≤ maxPpSize then
          (do pure (oneLine (← ppExpr g).pretty 400)) <|> pure "<pp failed>"
        else pure s!"<{gsize} nodes>"
      hl.putStrLn (Json.mkObj [("level", level), ("key", hex64 k), ("numStatements", a.stmts.size),
        ("statementsCapped", decide (a.stmts.size ≥ 40)), ("holes", holes), ("lggSize", gsize),
        ("lgg", str)]).compress
      nLgg := nLgg + 1
  hl.flush
  IO.println s!"anti-unifiers written: {nLgg}"
  IO.FS.writeFile (outDir / "run.json") (Json.mkObj [
    ("minTheoremProof", minThm), ("maxDeclsPerSlice", maxDecls), ("minCandidateProof", minProofSize),
    ("slices", Json.arr selCounts), ("theorems", decls.size), ("ok", nOk), ("failed", nFail),
    ("truncated", nTrunc), ("candidates", nCands), ("distinctStatements", st.stmts.size),
    ("libraryTheoremsHashed", nLib), ("exactTried", todo.size),
    ("enumerationSeconds", toJson ((t3 - t0) / 1000)), ("exactSeconds", toJson ((t5 - t4) / 1000)),
    ("leanVersion", Lean.versionString)]).pretty

end Rosette.Reuse

open Rosette.Reuse in
run_meta do
  if (← IO.getEnv "ROSETTE_REUSE").isSome then
    Rosette.Reuse.run
  else
    IO.println "Rosette.Reuse: set ROSETTE_REUSE=1 to run the H2 data collection (see file header)."
