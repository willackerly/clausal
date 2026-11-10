/-
ExportDecls: dump the declaration graph of a built Lean project as JSON lines.

Run from inside the corpus project (so LEAN_PATH points at its .lake build):
  lake env lean --run ../tools/ExportDecls.lean <outDir> <rootPrefixes,comma> <importModules,comma> [mainTheorem ...]

Writes <outDir>/decls.jsonl, modules.jsonl, axioms.json, export_meta.json.
All data comes from the loaded environment; nothing is read from source text.
-/
import Lean
open Lean Meta

namespace ExportDecls

/-- structural info of an expression: binder-name-invariant hash, tree size. -/
structure Info where
  hash : UInt64
  tree : Nat
  deriving Inhabited

abbrev SizeM := StateM (Std.HashMap Expr Info)

def bump (tag : UInt64) (hs : List UInt64) : UInt64 :=
  hs.foldl (fun a h => mixHash a h) (mixHash 0x9e3779b97f4a7c15 tag)

/-- Visit `e`; mdata is transparent; binder names and binder infos are ignored. -/
partial def visit (e : Expr) : SizeM Info := do
  match e with
  | .mdata _ b => visit b
  | _ =>
  if let some i := (← get)[e]? then return i
  let i ← match e with
    | .bvar n => pure ⟨bump 1 [hash n], 1⟩
    | .fvar id => pure ⟨bump 2 [hash id.name], 1⟩
    | .mvar id => pure ⟨bump 3 [hash id.name], 1⟩
    | .sort l => pure ⟨bump 4 [hash l], 1⟩
    | .const n ls => pure ⟨bump 5 [hash n, hash ls], 1⟩
    | .app f a => do
        let x ← visit f; let y ← visit a
        pure ⟨bump 6 [x.hash, y.hash], x.tree + y.tree + 1⟩
    | .lam _ t b _ => do
        let x ← visit t; let y ← visit b
        pure ⟨bump 7 [x.hash, y.hash], x.tree + y.tree + 1⟩
    | .forallE _ t b _ => do
        let x ← visit t; let y ← visit b
        pure ⟨bump 8 [x.hash, y.hash], x.tree + y.tree + 1⟩
    | .letE _ t v b _ => do
        let x ← visit t; let y ← visit v; let z ← visit b
        pure ⟨bump 9 [x.hash, y.hash, z.hash], x.tree + y.tree + z.tree + 1⟩
    | .lit (.natVal n) => pure ⟨bump 10 [hash n], 1⟩
    | .lit (.strVal s) => pure ⟨bump 11 [hash s], 1⟩
    | .proj s i b => do
        let x ← visit b
        pure ⟨bump 12 [hash s, hash i, x.hash], x.tree + 1⟩
    | .mdata _ b => visit b
  modify (·.insert e i)
  return i

/-- (hash, treeSize, dagSize) where dagSize = number of distinct subterms up to binder names. -/
def measure (e : Expr) : UInt64 × Nat × Nat :=
  let (i, m) := (visit e).run {}
  (i.hash, i.tree, m.size)

/-- rename universe parameters positionally so the hash does not depend on their names. -/
def normLevels (ci : ConstantInfo) (e : Expr) : Expr :=
  let ps := ci.levelParams
  e.instantiateLevelParams ps ((List.range ps.length).map fun i => Level.param (Name.mkNum `u i))

def digitsToHash (s : String) : String :=
  String.ofList (s.toList.map fun c => if c.isDigit then '#' else c)

def lastComp : Name → String
  | .str _ s => digitsToHash s
  | .num p _ => lastComp p ++ ".#"
  | .anonymous => ""

partial def chainParent (isPrimary : Name → Bool) : Name → Option Name
  | .str p _ | .num p _ => if isPrimary p then some p else chainParent isPrimary p
  | .anonymous => none

def rootStr (m : Name) : String := m.getRoot.toString

def trunc (s : String) (n : Nat) : String := if s.length > n then (s.take n).toString ++ "…" else s

structure Deps where
  typeDeps : NameSet := {}
  valueDeps : NameSet := {}
  extType : NameSet := {}
  extValue : NameSet := {}
  axioms : NameSet := {}
  visited : NameSet := {}
  auxSize : Nat := 0
  numAux : Nat := 0

end ExportDecls
open ExportDecls

unsafe def main (args : List String) : IO UInt32 := do
  let outDir :: rootsS :: importsS :: mains := args
    | IO.eprintln "usage: <outDir> <roots> <imports> [mains...]"; return 1
  let t0 ← IO.monoMsNow
  let roots := (rootsS.splitOn ",").map String.toName
  let imports := (importsS.splitOn ",").map String.toName
  initSearchPath (← findSysroot)
  enableInitializersExecution
  let env ← importModules (imports.toArray.map fun m => {module := m}) {} (trustLevel := 1024) (loadExts := true)
  let t1 ← IO.monoMsNow
  IO.eprintln s!"imported in {t1 - t0} ms"
  let modNames := env.header.moduleNames
  let isProjMod (m : Name) : Bool := roots.any (·.isPrefixOf m)
  let modOf (n : Name) : Option Name := (env.getModuleIdxFor? n).map fun i => modNames[i.toNat]!
  let inProject (n : Name) : Bool := match modOf n with | some m => isProjMod m | none => false
  -- modules
  let hMod ← IO.FS.Handle.mk (outDir ++ "/modules.jsonl") .write
  let mut nMods := 0
  for i in [0:modNames.size] do
    let m := modNames[i]!
    if isProjMod m then
      nMods := nMods + 1
      let imps := env.header.moduleData[i]!.imports.map (·.module)
      hMod.putStrLn (Json.compress <| Json.mkObj [
        ("module", m.toString),
        ("imports", toJson (imps.filter isProjMod |>.map (·.toString))),
        ("numExternalImports", toJson (imps.filter (!isProjMod ·)).size)])
  hMod.flush
  let opts : Options := ({} : Options) |>.setBool `pp.unicode.fun true
  let ctx : Core.Context := { fileName := "<export>", fileMap := default, options := opts, maxHeartbeats := 0 }
  let act : MetaM (Json) := do
    -- pass 1: classify project constants
    let projConsts : Array (Name × ConstantInfo) := env.constants.fold (init := #[]) fun acc n ci =>
      if inProject n then acc.push (n, ci) else acc
    let mut primary : NameSet := {}
    let mut autoHist : Std.HashMap String Nat := {}
    let mut autoList : Array Name := #[]
    for (n, ci) in projConsts do
      let un := (privateToUserName? n).getD n
      let isSyntaxObj := ci.type.getUsedConstants.any fun c =>
        c == ``Lean.ParserDescr || c == ``Lean.TrailingParserDescr || c == ``Lean.Macro
          || c == ``Lean.PrettyPrinter.Unexpander || c == ``Lean.PrettyPrinter.Delaborator.Delab
      let structural := un.isInternalDetail || isSyntaxObj || isAuxRecursor env n || isNoConfusion env n
        || env.isProjectionFn n || (match ci with | .ctorInfo _ | .recInfo _ => true | _ => false)
      let mut why := ""
      if structural then
        why := match ci with
          | .ctorInfo _ => "<ctor>" | .recInfo _ => "<rec>"
          | _ => if env.isProjectionFn n then "<proj>" else if isSyntaxObj then "<syntax>" else lastComp n
      else if (← findDeclarationRanges? n).isNone then
        why := "<norange>:" ++ lastComp n
      if why == "" then primary := primary.insert n
      else
        autoList := autoList.push n
        autoHist := autoHist.insert why (autoHist.getD why 0 + 1)
    let isPrimary (n : Name) : Bool := primary.contains n
    let parentOf (n : Name) : Option Name :=
      let direct : Option Name := match env.find? n with
        | some (.ctorInfo v) => some v.induct
        | some (.recInfo v) => v.all.head?
        | _ => match env.getProjectionFnInfo? n with
          | some pi => (match env.find? pi.ctorName with | some (.ctorInfo v) => some v.induct | _ => none)
          | none => none
      match direct with
      | some p => if isPrimary p then some p else chainParent isPrimary p
      | none =>
        match chainParent isPrimary n with
        | some p => some p
        | none => if isPrivateName n then
            (match privateToUserName? n with | some u => chainParent isPrimary u | none => none) else none
    let mut orphan := 0
    let mut orphanEx : Array String := #[]
    for n in autoList do
      if (parentOf n).isNone then
        orphan := orphan + 1
        if orphanEx.size < 40 then orphanEx := orphanEx.push n.toString
    -- every project constant, with its classification and parent
    let hAll ← IO.FS.Handle.mk (outDir ++ "/all_names.jsonl") .write
    for (n, _) in projConsts do
      hAll.putStrLn (Json.compress <| Json.mkObj [
        ("name", n.toString), ("userName", ((privateToUserName? n).getD n).toString),
        ("auto", !isPrimary n),
        ("parent", match (if isPrimary n then none else parentOf n) with | some p => Json.str p.toString | none => Json.null)])
    hAll.flush
    -- existence check for externally supplied names (e.g. blueprint \lean tags)
    if let some f ← IO.getEnv "EXPORT_CHECK_NAMES" then
      let mut chk : Array (String × Json) := #[]
      for l in (← IO.FS.lines f) do
        let s := l.trimAscii.toString
        if s.isEmpty then continue
        let nm := s.toName
        chk := chk.push (s, Json.mkObj [("exists", env.contains nm),
          ("module", match modOf nm with | some m => Json.str m.toString | none => Json.null)])
      IO.FS.writeFile (outDir ++ "/name_check.json") (Json.compress (Json.mkObj chk.toList))
    -- pass 2: export
    let h ← IO.FS.Handle.mk (outDir ++ "/decls.jsonl") .write
    let mut kindHist : Std.HashMap String Nat := {}
    let mut ppFail := 0
    let mut nEdgesT := 0
    let mut nEdgesV := 0
    let sorted := projConsts.filter (fun p => isPrimary p.1) |>.qsort (fun a b => a.1.toString < b.1.toString)
    for (n, ci) in sorted do
      -- dependency collection with expansion of own / orphan auxiliaries
      let rec go (fuel : Nat) (isVal : Bool) (e : Expr) (d : Deps) : Deps := Id.run do
        let mut d := d
        for c in e.getUsedConstants do
          if c == n then continue
          match env.find? c with
          | none => continue
          | some cci =>
          if cci matches .axiomInfo _ then d := { d with axioms := d.axioms.insert c }
          if !inProject c then
            d := if isVal then { d with extValue := d.extValue.insert c } else { d with extType := d.extType.insert c }
          else if isPrimary c then
            d := if isVal then { d with valueDeps := d.valueDeps.insert c } else { d with typeDeps := d.typeDeps.insert c }
          else
            match parentOf c with
            | some p =>
              if p != n then
                d := if isVal then { d with valueDeps := d.valueDeps.insert p } else { d with typeDeps := d.typeDeps.insert p }
              else if !d.visited.contains c && fuel > 0 then
                d := { d with visited := d.visited.insert c }
                d := go (fuel - 1) isVal cci.type d
                if let some v := cci.value? (allowOpaque := true) then
                  if isVal then
                    d := { d with auxSize := d.auxSize + (measure v).2.2, numAux := d.numAux + 1 }
                  d := go (fuel - 1) isVal v d
            | none =>
              if !d.visited.contains c && fuel > 0 then
                d := { d with visited := d.visited.insert c }
                d := go (fuel - 1) isVal cci.type d
                if let some v := cci.value? (allowOpaque := true) then
                  if isVal then
                    d := { d with auxSize := d.auxSize + (measure v).2.2, numAux := d.numAux + 1 }
                  d := go (fuel - 1) isVal v d
        return d
      let mut d : Deps := {}
      d := go 64 false ci.type d
      let mut fieldsSize := 0
      let mut numCtors := 0
      if let .inductInfo iv := ci then
        for cn in iv.ctors do
          if let some cc := env.find? cn then
            numCtors := numCtors + 1
            fieldsSize := fieldsSize + (measure cc.type).2.2
            d := go 64 false cc.type d
      let val? := ci.value? (allowOpaque := true)
      let mut proofSize := 0
      let mut proofTree := 0
      if let some v := val? then
        let (_, t, dg) := measure v
        proofSize := dg; proofTree := t
        d := go 64 true v d
      let (hsh, stTree, stDag) := measure (normLevels ci ci.type)
      let isInst ← isInstance n
      let constKind : String := match ci with
        | .thmInfo _ => "theorem" | .defnInfo _ => "def" | .axiomInfo _ => "axiom"
        | .opaqueInfo _ => "opaque"
        | .inductInfo _ => if isStructure env n then "structure" else "inductive"
        | .quotInfo _ => "quot" | .ctorInfo _ => "ctor" | .recInfo _ => "rec"
      let kind : String := if isInst then "instance" else constKind
      kindHist := kindHist.insert kind (kindHist.getD kind 0 + 1)
      let stmt ← try
          let f ← PrettyPrinter.ppSignature n
          pure (f.fmt.pretty 100)
        catch _ =>
          try pure ((← ppExpr ci.type).pretty 100)
          catch _ => ppFail := ppFail + 1; pure "<pp failed>"
      let isPropTy ← try isProp ci.type catch _ => pure false
      let rng ← findDeclarationRanges? n
      let doc ← findDocString? env n
      let extCounts (s : NameSet) : Json := Id.run do
        let mut m : Std.HashMap String Nat := {}
        for c in s do
          let r := match modOf c with | some mm => rootStr mm | none => "?"
          m := m.insert r (m.getD r 0 + 1)
        return Json.mkObj (m.toList.map fun (k, v) => (k, toJson v))
      let names (s : NameSet) : Json := toJson (s.toList.map (·.toString) |>.toArray.qsort (· < ·))
      nEdgesT := nEdgesT + d.typeDeps.size
      nEdgesV := nEdgesV + d.valueDeps.size
      let userName := (privateToUserName? n).getD n
      h.putStrLn (Json.compress <| Json.mkObj [
        ("name", n.toString),
        ("userName", userName.toString),
        ("module", ((modOf n).getD .anonymous).toString),
        ("kind", kind),
        ("constKind", constKind),
        ("isClass", isClass env n),
        ("isPrivate", isPrivateName n),
        ("isUnsafe", ci.isUnsafe),
        ("typeIsProp", isPropTy),
        ("usesLeanMeta", decide (d.extType.any fun c => (`Lean).isPrefixOf c)),
        ("hasDocstring", doc.isSome),
        ("statement", trunc stmt 2000),
        ("statementTruncated", decide (stmt.length > 2000)),
        ("statementSize", stTree),
        ("statementDagSize", stDag),
        ("statementHash", toString hsh),
        ("proofSize", proofSize),
        ("proofTreeSize", proofTree),
        ("auxProofSize", d.auxSize),
        ("numAux", d.numAux),
        ("numCtors", numCtors),
        ("fieldsSize", fieldsSize),
        ("typeDeps", names d.typeDeps),
        ("valueDeps", names d.valueDeps),
        ("numExtType", d.extType.size),
        ("numExtValue", d.extValue.size),
        ("extTypeByRoot", extCounts d.extType),
        ("extValueByRoot", extCounts d.extValue),
        ("directAxioms", names d.axioms),
        ("line", match rng with | some r => toJson r.range.pos.line | none => Json.null),
        ("endLine", match rng with | some r => toJson r.range.endPos.line | none => Json.null)])
    h.flush
    -- axioms of main theorems
    let mut axs : Array (String × Json) := #[]
    for m in mains do
      let nm := m.toName
      if env.contains nm then
        let a ← collectAxioms nm
        axs := axs.push (m, toJson (a.map (·.toString) |>.qsort (· < ·)))
      else
        axs := axs.push (m, Json.null)
    IO.FS.writeFile (outDir ++ "/axioms.json") (Json.pretty (Json.mkObj axs.toList))
    return Json.mkObj [
      ("numProjectConstants", projConsts.size),
      ("numExported", sorted.size),
      ("numAuto", autoList.size),
      ("numAutoOrphan", orphan),
      ("autoOrphanExamples", toJson orphanEx),
      ("kindCounts", Json.mkObj (kindHist.toList.map fun (k, v) => (k, toJson v))),
      ("autoBySuffix", Json.mkObj ((autoHist.toArray.qsort (fun a b => a.2 > b.2)).toList.map fun (k, v) => (k, toJson v))),
      ("ppFailures", ppFail),
      ("typeEdges", nEdgesT),
      ("valueEdges", nEdgesV)]
  let (res, _) ← act.run'.toIO ctx { env }
  let t2 ← IO.monoMsNow
  let metaJ := res.mergeObj (Json.mkObj [
    ("numProjectModules", nMods),
    ("leanVersion", Lean.versionString),
    ("roots", toJson rootsS), ("imports", toJson importsS),
    ("importMs", t1 - t0), ("exportMs", t2 - t1)])
  IO.FS.writeFile (outDir ++ "/export_meta.json") (Json.pretty metaJ)
  IO.eprintln s!"done in {t2 - t0} ms"
  return 0
