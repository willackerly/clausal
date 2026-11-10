/-
Declaration-graph exporter for the machine-generated corpus in `corpora/ns`.

Stand-alone program (imports only `Lean`); it loads the *built* environment of the
corpus with `importModules` and reads everything from `Environment` — no source regex.

Usage (from `corpora/ns`, so that `lake env` supplies LEAN_PATH):
  lake env <exe> <modules.txt> <out.jsonl> <axioms.json> <meta.json> <shard> <nshards> <main1> <main2> ...

Classification of every constant that lives in a project module:
  * primary   – exported as a node
  * body aux  – `_proof_N`, `match_N`, `_unary`, any `_`-prefixed last component, matchers:
                their type/value constants and sizes are folded into the parent's VALUE side
  * ctor      – folded into the parent inductive's TYPE side
  * derived   – recursors, projections, `casesOn`, `noConfusion`, `eq_N`, `injEq`, `ext`… :
                references to them become references to the parent; their own bodies are ignored
  * dropped   – syntax/macro/notation artefacts (ParserDescr etc.)
  * orphan    – auxiliary whose parent chain does not end in a primary project declaration:
                references to it are replaced by its own (recursively resolved) dependencies
-/
import Lean
open Lean Meta

namespace NsExport

def projectRoots : List Name := [`NavierStokes, `Euler, `ComparatorChallenges]

inductive Cls where
  | primary
  | body (parent : Name)
  | ctor (parent : Name)
  | derived (parent : Name)
  | dropped
  | external   -- auxiliary (eq_N, congr_simp, _proof_…) realised here for a NON-project declaration
  | orphan
  deriving Inhabited, BEq

def softNames : List String :=
  ["eq_def", "eq_unfold", "congr_simp", "sizeOf_spec", "injEq", "inj", "ext", "ext_iff",
   "induct", "induct_unfolding", "fun_cases", "fun_cases_unfolding", "mutual_induct",
   "below", "brecOn", "casesOn", "recOn", "noConfusion", "noConfusionType", "ctorIdx",
   "toCtorIdx", "ofNat", "elim", "ctorElim", "ctorElimType", "splitter", "hinj", "binductionOn",
   "rec", "ndrec", "ndrecOn", "inj_iff", "eq_iff", "congr", "match_pattern", "else_eq",
   "ofNat_ctorIdx", "ctorIdx_ofNat", "toCtorIdx_ofNat", "ofNat_toCtorIdx"]

def isEqNum (s : String) : Bool :=
  s.startsWith "eq_" && (s.drop 3).all Char.isDigit && s.length > 3

def droppedTypeHeads : List Name :=
  [`Lean.ParserDescr, `Lean.TrailingParserDescr, `Lean.Macro, `Lean.PrettyPrinter.Unexpander,
   `Lean.Elab.Term.TermElab, `Lean.Elab.Tactic.Tactic, `Lean.Elab.Command.CommandElab,
   `Lean.PrettyPrinter.Delaborator.Delab, `Lean.Parser.Parser, `Lean.Parser.TrailingParser,
   `Lean.PrettyPrinter.Formatter, `Lean.PrettyPrinter.Parenthesizer, `Lean.Meta.Simp.Simproc,
   `Lean.Meta.Simp.DSimproc, `Lean.Parser.Category]

/-- 64-bit, binder-name- and binder-info-invariant structural hash; mdata stripped;
universe parameters replaced by their position in the declaration's parameter list. -/
partial def hashLevel (ps : List Name) : Level → UInt64
  | .zero => 11
  | .succ l => mixHash 13 (hashLevel ps l)
  | .max a b => mixHash 17 (mixHash (hashLevel ps a) (hashLevel ps b))
  | .imax a b => mixHash 19 (mixHash (hashLevel ps a) (hashLevel ps b))
  | .param n => mixHash 23 (hash (ps.idxOf n))
  | .mvar _ => 29

structure Info where
  tree : Nat
  h : UInt64
  deriving Inhabited

abbrev M := StateM (Std.HashMap ExprStructEq Info)

/-- One memoised pass: tree size (Expr node count, mdata not counted) and structural hash.
The number of memo entries afterwards is the DAG size. -/
partial def analyze (ps : List Name) (e : Expr) : M Info := do
  match e with
  | .mdata _ b => analyze ps b
  | _ =>
    if let some r := (← get)[(⟨e⟩ : ExprStructEq)]? then return r
    let r ← match e with
      | .app f a => do
        let x ← analyze ps f; let y ← analyze ps a
        pure (⟨x.tree + y.tree + 1, mixHash 7 (mixHash x.h y.h)⟩ : Info)
      | .lam _ d b _ => do
        let x ← analyze ps d; let y ← analyze ps b
        pure ⟨x.tree + y.tree + 1, mixHash 59 (mixHash x.h y.h)⟩
      | .forallE _ d b _ => do
        let x ← analyze ps d; let y ← analyze ps b
        pure ⟨x.tree + y.tree + 1, mixHash 61 (mixHash x.h y.h)⟩
      | .letE _ t v b _ => do
        let x ← analyze ps t; let y ← analyze ps v; let z ← analyze ps b
        pure ⟨x.tree + y.tree + z.tree + 1, mixHash 67 (mixHash x.h (mixHash y.h z.h))⟩
      | .proj s i b => do
        let x ← analyze ps b
        pure ⟨x.tree + 1, mixHash 71 (mixHash (hash s) (mixHash (hash i) x.h))⟩
      | .bvar i => pure ⟨1, mixHash 3 (hash i)⟩
      | .sort l => pure ⟨1, mixHash 37 (hashLevel ps l)⟩
      | .lit (.natVal n) => pure ⟨1, mixHash 41 (hash n)⟩
      | .lit (.strVal s) => pure ⟨1, mixHash 43 (hash s)⟩
      | .const n ls =>
        pure ⟨1, mixHash 5 (ls.foldl (fun acc l => mixHash acc (hashLevel ps l)) (hash n))⟩
      | _ => pure ⟨1, 47⟩
    modify (·.insert ⟨e⟩ r)
    return r

/-- (treeSize, dagSize, hash).  DAG size = number of structurally distinct subterms. -/
def sizes (ps : List Name) (e : Expr) : Nat × Nat × UInt64 :=
  let (r, m) := (analyze ps e).run {}
  (r.tree, m.size, r.h)

def valueOf? : ConstantInfo → Option Expr
  | .thmInfo v => some v.value
  | .defnInfo v => some v.value
  | .opaqueInfo v => some v.value
  | _ => none

def hexOf (h : UInt64) : String :=
  let s := String.ofList (Nat.toDigits 16 h.toNat)
  "".pushn '0' (16 - s.length) ++ s

structure Ctx where
  env : Environment
  isProj : Name → Bool          -- constant lives in a project module
  cls : Std.HashMap Name Cls

def moduleOf (env : Environment) (n : Name) : Name :=
  match env.getModuleIdxFor? n with
  | some i => env.header.moduleNames[i.toNat]!
  | none => .anonymous

/-- Follow parent links to a primary declaration. -/
partial def resolveRoot (cx : Ctx) (n : Name) (fuel : Nat := 64) : Option Name :=
  if fuel == 0 then none else
  match cx.cls[n]? with
  | some .primary => some n
  | some (.body p) | some (.ctor p) | some (.derived p) => resolveRoot cx p (fuel - 1)
  | _ => none

/-- Project-internal primaries referenced by `consts`, expanding orphans; plus number of
distinct external constants. -/
partial def resolveDeps (cx : Ctx) (self : Name) (consts : Array Name) :
    Std.HashSet Name × Std.HashSet Name := Id.run do
  let mut deps : Std.HashSet Name := {}
  let mut ext : Std.HashSet Name := {}
  let mut seen : Std.HashSet Name := {}
  let mut todo := consts.toList
  while !todo.isEmpty do
    match todo with
    | [] => break
    | c :: rest =>
      todo := rest
      if seen.contains c then continue
      seen := seen.insert c
      if !cx.isProj c || cx.cls[c]? == some Cls.external then
        ext := ext.insert c
        continue
      -- a body auxiliary of ANOTHER declaration (typically a shared `match_N`) is not a
      -- dependency on that declaration's proof: inline the auxiliary's own dependencies
      let foreignBody := match cx.cls[c]? with
        | some (.body _) => resolveRoot cx c != some self
        | _ => false
      match (if foreignBody then none else resolveRoot cx c) with
      | some r => if r != self then deps := deps.insert r
      | none =>
        -- orphan / dropped: inline its own dependencies
        if let some ci := cx.env.find? c then
          todo := ci.type.getUsedConstants.toList ++ todo
          if let some v := valueOf? ci then
            todo := v.getUsedConstants.toList ++ todo
  return (deps, ext)

def sortedNames (s : Std.HashSet Name) : Array String :=
  (s.toArray.map (·.toString (escape := false))).qsort (· < ·)

unsafe def main (args : List String) : IO UInt32 := do
  let modsFile :: outFile :: axFile :: metaFile :: shardS :: nshardS :: mains := args
    | throw <| IO.userError "usage: export modules.txt out.jsonl axioms.json meta.json shard nshards mains.."
  let shard := shardS.toNat!
  let nshards := nshardS.toNat!
  let t0 ← IO.monoMsNow
  initSearchPath (← findSysroot)
  enableInitializersExecution
  let modNames := ((← IO.FS.lines modsFile).filter (· ≠ "")).map (·.toName)
  let env ← importModules (modNames.map fun m => { module := m }) {} (trustLevel := 1024)
    (loadExts := true)
  let t1 ← IO.monoMsNow
  IO.eprintln s!"[shard {shard}] imported {modNames.size} root modules in {t1 - t0} ms; \
    {env.header.moduleNames.size} modules total"
  -- project module indices
  let projIdx : Array Bool := env.header.moduleNames.map fun m => projectRoots.contains m.getRoot
  let isProj (n : Name) : Bool :=
    match env.getModuleIdxFor? n with
    | some i => projIdx[i.toNat]!
    | none => false
  -- all project constants
  let mut projConsts : Array (Name × ConstantInfo) := #[]
  for (n, ci) in env.constants.map₁.toList do
    if isProj n then projConsts := projConsts.push (n, ci)
  projConsts := projConsts.qsort fun a b => a.1.toString < b.1.toString
  IO.eprintln s!"[shard {shard}] project constants (incl. auxiliaries): {projConsts.size}"
  let coreCtx : Core.Context := { fileName := "<export>", fileMap := default,
                                  options := ({} : Options).set `format.width (100 : Nat) }
  let runCore {α} (x : CoreM α) : IO (Option α) := do
    try
      let (a, _) ← x.toIO coreCtx { env := env }
      return some a
    catch _ => return none
  let rangeOf (n : Name) : IO (Option DeclarationRange) := do
    let r ← runCore (findDeclarationRanges? n)
    return (r.join).map (·.range)
  -- candidate parent: the name prefix; a private auxiliary of a public declaration has a
  -- private prefix that is not itself a constant, so fall back to the public spelling
  let parentCand (n : Name) : Name :=
    let pre := n.getPrefix
    if env.contains pre then pre
    else if isPrivateName pre && env.contains (privateToUserName pre) then privateToUserName pre
    else pre
  -- pass 1: classification
  let mut cls : Std.HashMap Name Cls := {}
  for (n, ci) in projConsts do
    let pre := parentCand n
    let preIsProj := isProj pre
    let preIsExt := !preIsProj && env.contains pre
    let c : Cls ← do
      match ci with
      | .ctorInfo v => pure (Cls.ctor v.induct)
      | .recInfo _ => pure (Cls.derived pre)
      | .quotInfo _ => pure Cls.dropped
      | _ =>
        if droppedTypeHeads.contains ci.type.getForallBody.getAppFn.constName then pure Cls.dropped
        else if let some pi := env.getProjectionFnInfo? n then pure (Cls.derived pi.ctorName.getPrefix)
        else if n.hasMacroScopes then pure Cls.orphan
        else if isMatcherCore env n then
          pure (if preIsProj then Cls.body pre else if preIsExt then Cls.external else Cls.orphan)
        else if isAuxRecursor env n || isNoConfusion env n then
          pure (if preIsExt then Cls.external else Cls.derived pre)
        else match n with
          | .num _ _ => pure (if preIsProj then Cls.body pre else if preIsExt then Cls.external else Cls.orphan)
          | .str _ s =>
            if s.startsWith "_" || s.startsWith "match_" || s.startsWith "proof_" then
              pure (if preIsProj then Cls.body pre else if preIsExt then Cls.external else Cls.orphan)
            else if (softNames.contains s || isEqNum s) && preIsExt then pure Cls.external
            else if (softNames.contains s || isEqNum s) && preIsProj then
              -- derived only if it has no source range of its own
              let r ← rangeOf n
              let rp ← rangeOf pre
              match r, rp with
              | none, _ => pure (Cls.derived pre)
              | some a, some b =>
                if a.pos == b.pos && a.endPos == b.endPos then pure (Cls.derived pre)
                else pure Cls.primary
              | some _, none => pure Cls.primary
            else pure Cls.primary
          | .anonymous => pure Cls.dropped
    cls := cls.insert n c
  -- post-pass: a range-less "primary" hanging under a non-primary project constant
  -- (e.g. `T.brecOn.go`, `T.brecOn.eq`) is derived from that constant
  for _ in [0:3] do
    for (n, _) in projConsts do
      if cls[n]! == .primary then
        let pre := parentCand n
        if isProj pre && cls[pre]! != .primary && (← rangeOf n).isNone then
          cls := cls.insert n (Cls.derived pre)
  let cx : Ctx := { env, isProj, cls }
  -- children folded into each primary
  let mut bodyKids : Std.HashMap Name (Array Name) := {}
  let mut ctorKids : Std.HashMap Name (Array Name) := {}
  let mut nPrimary := 0; let mut nBody := 0; let mut nCtor := 0; let mut nDerived := 0
  let mut nDropped := 0; let mut nOrphan := 0; let mut nExternal := 0
  let mut orphanNames : Array String := #[]
  for (n, _) in projConsts do
    match cls[n]! with
    | .primary => nPrimary := nPrimary + 1
    | .dropped => nDropped := nDropped + 1
    | .external => nExternal := nExternal + 1
    | .orphan => nOrphan := nOrphan + 1; orphanNames := orphanNames.push (n.toString (escape := false))
    | c =>
      match resolveRoot cx n with
      | none => nOrphan := nOrphan + 1; orphanNames := orphanNames.push (n.toString (escape := false))
      | some r =>
        match c with
        | .body _ => nBody := nBody + 1; bodyKids := bodyKids.insert r ((bodyKids.getD r #[]).push n)
        | .ctor _ => nCtor := nCtor + 1; ctorKids := ctorKids.insert r ((ctorKids.getD r #[]).push n)
        | _ => nDerived := nDerived + 1
  IO.eprintln s!"[shard {shard}] primary {nPrimary} body {nBody} ctor {nCtor} derived {nDerived} \
    dropped {nDropped} external {nExternal} orphan {nOrphan}"
  -- pass 2: export
  let h ← IO.FS.Handle.mk outFile .write
  let mut idx := 0
  let mut ppFail := 0
  let mut written := 0
  for (n, ci) in projConsts do
    unless cls[n]! == .primary do continue
    idx := idx + 1
    unless idx % nshards == shard do continue
    let ps := ci.levelParams
    let (tTree, tDag, tHash) := sizes ps ci.type
    let mut typeConsts := ci.type.getUsedConstants
    let mut stmtSize := tTree
    let mut stmtDag := tDag
    let ctors := ctorKids.getD n #[]
    for c in ctors do
      if let some cci := env.find? c then
        let (a, b, _) := sizes cci.levelParams cci.type
        stmtSize := stmtSize + a; stmtDag := stmtDag + b
        typeConsts := typeConsts ++ cci.type.getUsedConstants
    let mut valConsts : Array Name := #[]
    let mut proofSize := 0
    let mut proofTree := 0
    if let some v := valueOf? ci then
      let (a, b, _) := sizes ps v
      proofSize := b; proofTree := a
      valConsts := v.getUsedConstants
    let kids := bodyKids.getD n #[]
    let mut auxProofSize := 0
    for k in kids do
      if let some kci := env.find? k then
        let (_, b, _) := sizes kci.levelParams kci.type
        auxProofSize := auxProofSize + b
        valConsts := valConsts ++ kci.type.getUsedConstants
        if let some v := valueOf? kci then
          let (_, b2, _) := sizes kci.levelParams v
          auxProofSize := auxProofSize + b2
          valConsts := valConsts ++ v.getUsedConstants
    let (tDeps, tExt) := resolveDeps cx n typeConsts
    let (vDeps, vExt) := resolveDeps cx n valConsts
    let kind : String :=
      match ci with
      | .axiomInfo _ => "axiom"
      | .thmInfo _ => "theorem"
      | .opaqueInfo _ => "opaque"
      | .defnInfo _ =>
        if isInstanceCore env n || isClass env ci.type.getForallBody.getAppFn.constName
        then "instance" else "def"
      | .inductInfo _ => if isStructure env n then "structure" else "inductive"
      | _ => "other"
    -- statement text
    let ppOne (e : Expr) : IO (Option String) :=
      runCore (do let f ← (Meta.ppExpr e).run'; return f.pretty 100)
    let mut stmt := ""
    let mut ppOk := true
    let sig ← runCore (do
      let f ← (PrettyPrinter.ppSignature n).run'
      return f.fmt.pretty 100)
    match sig with
    | some s => stmt := s
    | none =>
      match ← ppOne ci.type with
      | some s => stmt := s
      | none => ppOk := false
    let typeIsProp := (← runCore ((Meta.isProp ci.type).run')).getD false
    let byRoot (xs : Std.HashSet Name) : Json := Id.run do
      let mut m : Std.HashMap String Nat := {}
      for x in xs do
        let r := (moduleOf env x).getRoot.toString
        m := m.insert r (m.getD r 0 + 1)
      return Json.mkObj ((m.toList.map fun (k, v) => (k, toJson v)))
    for c in ctors do
      if stmt.length > 2000 then break
      if let some cci := env.find? c then
        match ← ppOne cci.type with
        | some s => stmt := stmt ++ "\n| " ++ c.toString (escape := false) ++ " : " ++ s
        | none => ppOk := false
    unless ppOk do ppFail := ppFail + 1
    let stmtLen := stmt.length
    let truncated : Bool := decide (stmtLen > 2000)
    if truncated then stmt := (stmt.take 2000).toString
    let doc ← findDocString? env n
    let range ← rangeOf n
    let mut fields : List (String × Json) := [
      ("name", n.toString (escape := false)),
      ("userName", (privateToUserName n).toString (escape := false)),
      ("module", (moduleOf env n).toString),
      ("kind", kind),
      ("isClass", isClass env n),
      ("instanceAttr", isInstanceCore env n),
      ("isPrivate", isPrivateName n),
      ("hasDocstring", doc.isSome),
      ("statement", stmt),
      ("statementChars", stmtLen),
      ("statementTruncated", truncated),
      ("ppOk", ppOk),
      ("statementSize", stmtSize),
      ("statementDagSize", stmtDag),
      ("proofSize", proofSize),
      ("proofTreeSizeLog2", if proofTree == 0 then 0 else proofTree.log2),
      ("auxProofSize", auxProofSize),
      ("numAux", kids.size),
      ("numCtors", ctors.size),
      ("typeDeps", toJson (sortedNames tDeps)),
      ("valueDeps", toJson (sortedNames vDeps)),
      ("numExtType", tExt.size),
      ("numExtValue", vExt.size),
      ("extTypeByRoot", byRoot tExt),
      ("extValueByRoot", byRoot vExt),
      ("typeIsProp", typeIsProp),
      ("statementHash", hexOf tHash)]
    match range with
    | some r => fields := fields ++ [("line", toJson r.pos.line), ("endLine", toJson r.endPos.line)]
    | none => fields := fields ++ [("line", Json.null), ("endLine", Json.null)]
    h.putStrLn (Json.mkObj fields).compress
    written := written + 1
    if written % 2000 == 0 then
      IO.eprintln s!"[shard {shard}] {written} written, {(← IO.monoMsNow) - t0} ms"
  h.flush
  let t2 ← IO.monoMsNow
  IO.eprintln s!"[shard {shard}] wrote {written} declarations, ppFail {ppFail}, total {t2 - t0} ms"
  if shard == 0 then
    -- axioms of the main theorems
    let mut axs : List (String × Json) := []
    for m in mains do
      let nm := m.toName
      if env.contains nm then
        let r ← runCore (collectAxioms nm)
        match r with
        | some a => axs := axs ++ [(m, toJson ((a.map (·.toString)).qsort (· < ·)))]
        | none => axs := axs ++ [(m, Json.str "collectAxioms failed")]
      else axs := axs ++ [(m, Json.str "not found in environment")]
    IO.FS.writeFile axFile (Json.mkObj axs).pretty
    let projMods := (env.header.moduleNames.filter fun m => projectRoots.contains m.getRoot)
    let metaJ := Json.mkObj [
      ("rootModulesImported", modNames.size),
      ("modulesTotal", env.header.moduleNames.size),
      ("projectModules", projMods.size),
      ("projectConstantsInclAux", projConsts.size),
      ("primary", nPrimary), ("bodyAux", nBody), ("ctor", nCtor), ("derivedAux", nDerived),
      ("dropped", nDropped), ("externalAux", nExternal), ("orphan", nOrphan),
      ("orphanSample", toJson (orphanNames.extract 0 200)),
      ("importMs", t1 - t0)]
    IO.FS.writeFile metaFile metaJ.pretty
  return 0

end NsExport

unsafe def main (args : List String) : IO UInt32 := NsExport.main args
