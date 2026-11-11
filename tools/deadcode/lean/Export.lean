/-
deadcode/Export: everything the dead-code tool needs to know about a built Lean project, read from Lean.

  lean --run Export.lean <outDir> <rootPrefixes,comma> <modulesFile> <srcRoot> [shard numShards]

with LEAN_PATH pointing at the project's build output and that of its packages (the Python driver
sets it; no Lake call is involved).  Imports only `Lean`, so it runs on the toolchain of the project
it inspects.  Tested on Lean 4.34.0-rc2 and 4.36.0-rc1/rc2.

Written to <outDir> (shard k of n writes decls.<k>.jsonl; shard 0 writes the other files):

  decls.jsonl     one line per source-level declaration ("primary" constant): kind, module, Lean's
                  declaration range, term dependencies (constants in the statement / in the value, with
                  auto-generated constants folded into the declaration they belong to), a statement shape
                  hash for clone detection, and what Lean's tables say about it:
                    simpSets      every registered simp set that contains it (simp, push_cast, field_simps ...)
                    instance      registered in the instance table
                    reducibility  reducible / irreducible / instances / semireducible
                    ext           registered `@[ext]` theorem
                    unexpander    target of an `app_unexpander` (what `notation ... => f ...` generates)
                    isClass
                  and what Lean's own parser reads at the start of the declaration range:
                    attrs         each attribute instance as written, with its syntax kind
                    declKw, mods  the declaration keyword and modifiers
  autos.jsonl     every other project constant: why it is not a source-level declaration and the
                  declaration it was folded into (null = orphan)
  meta.jsonl      orphan auto-generated constants (notation, macro, syntax, elaborator, deriving output ...)
                  with the source-level declarations they mention: uses that no declaration's term shows
  modules.jsonl   project modules, their project imports
  extensions.json for every persistent environment extension, how many entries the project modules
                  contributed (a footprint of all attribute / elaboration tables, decoded or not)
  clashes.json    constants that a project module's own .olean declares but that the combined environment
                  attributes to another module (same name declared twice; one of the two is dropped on import)
  export_meta.json
-/
import Lean
open Lean Meta

namespace DeadcodeExport

abbrev HashM := StateM (Std.HashMap Expr UInt64)

def mix (tag : UInt64) (hs : List UInt64) : UInt64 :=
  hs.foldl (fun a h => mixHash a h) (mixHash 0x9e3779b97f4a7c15 tag)

def lastStr : Name → String
  | .str _ s => s
  | .num p _ => lastStr p
  | .anonymous => ""

/-- Shape hash: binder names, binder kinds and metadata ignored; a project constant counts as the last
component of its name (so a namespace-renamed copy has the same shape), any other constant as itself. -/
partial def shape (isProj : Name → Bool) (e : Expr) : HashM UInt64 := do
  match e with
  | .mdata _ b => shape isProj b
  | _ =>
  if let some i := (← get)[e]? then return i
  let i ← match e with
    | .bvar n => pure (mix 1 [hash n])
    | .fvar id => pure (mix 2 [hash id.name])
    | .mvar id => pure (mix 3 [hash id.name])
    | .sort _ => pure (mix 4 [])
    | .const n _ =>
        if isProj n then pure (mix 13 [hash (lastStr ((privateToUserName? n).getD n))]) else pure (mix 5 [hash n])
    | .app f a => do let x ← shape isProj f; let y ← shape isProj a; pure (mix 6 [x, y])
    | .lam _ t b _ => do let x ← shape isProj t; let y ← shape isProj b; pure (mix 7 [x, y])
    | .forallE _ t b _ => do let x ← shape isProj t; let y ← shape isProj b; pure (mix 8 [x, y])
    | .letE _ t v b _ => do
        let x ← shape isProj t; let y ← shape isProj v; let z ← shape isProj b; pure (mix 9 [x, y, z])
    | .lit (.natVal n) => pure (mix 10 [hash n])
    | .lit (.strVal s) => pure (mix 11 [hash s])
    | .proj _ i b => do let x ← shape isProj b; pure (mix 12 [hash i, x])
    | .mdata _ b => shape isProj b
  modify (·.insert e i)
  return i

def shapeOf (isProj : Name → Bool) (e : Expr) : UInt64 × Nat :=
  let (h, m) := (shape isProj e).run {}
  (h, m.size)

def digitsToHash (s : String) : String :=
  String.ofList (s.toList.map fun c => if c.isDigit then '#' else c)

def lastComp : Name → String
  | .str _ s => digitsToHash s
  | .num p _ => lastComp p ++ ".#"
  | .anonymous => ""

partial def chainParent (isPrimary : Name → Bool) : Name → Option Name
  | .str p _ | .num p _ => if isPrimary p then some p else chainParent isPrimary p
  | .anonymous => none

structure Deps where
  typeDeps : NameSet := {}
  valueDeps : NameSet := {}
  visited : NameSet := {}

def namesJson (s : NameSet) : Json := toJson (s.toList.map (·.toString) |>.toArray.qsort (· < ·))

def isIdRest (c : Char) : Bool := c.isAlphanum || c == '_' || c == '\''

/-- First word of `s` (letters, digits, `_`, `'`, `#`). -/
def firstWord (s : String) : String :=
  String.ofList ((s.toList.dropWhile Char.isWhitespace).takeWhile fun c => isIdRest c || c == '#')

/-- Text of a syntax node as written, without leading/trailing trivia. -/
def stxText (stx : Syntax) : String :=
  match stx.reprint with
  | some s => String.ofList ((s.toList.dropWhile Char.isWhitespace).reverse.dropWhile Char.isWhitespace).reverse
  | none => ""

/-- Run Lean's `declModifiers` parser at the start of a declaration range. Returns the attribute
instances (syntax kind and text), the modifier keywords and the declaration keyword. -/
def parseHead (env : Environment) (src : String) (fm : FileMap) (fileName : String) (line col : Nat) :
    Option (Array (String × String) × Array String × String) := Id.run do
  let ictx := Parser.mkInputContext src fileName
  let pmctx : Parser.ParserModuleContext := { env := env, options := {} }
  let p := fm.ofPosition ⟨line, col⟩
  let s0 := (Parser.mkParserState src).setPos p
  let s := (Parser.Command.declModifiers false).fn.run ictx pmctx (Parser.getTokenTable env) s0
  if s.hasError then return none
  let stx := s.stxStack.back
  let mut attrs : Array (String × String) := #[]
  let mut mods : Array String := #[]
  -- children: doc?, attributes?, visibility?, protected?, (meta|noncomputable)?, unsafe?, (partial|nonrec)?
  let args := stx.getArgs
  for i in [0:args.size] do
    let a := args[i]!
    if a.isNone then continue
    if i == 1 then
      -- optional(Term.attributes): "@[" sepBy1 attrInstance "]"
      for attrsNode in a.getArgs do
        let insts := attrsNode[1].getSepArgs
        for inst in insts do
          -- attrInstance: attrKind attr
          let attr := inst[1]
          attrs := attrs.push (attr.getKind.toString, stxText inst)
    else if i >= 2 then
      mods := mods.push (firstWord (stxText a))
  -- the declaration keyword: the first ASCII word after the modifiers
  let bytes := src.toUTF8
  let mut i := s.pos.byteIdx
  while i < bytes.size && (bytes[i]! == 32 || bytes[i]! == 10 || bytes[i]! == 13 || bytes[i]! == 9) do i := i + 1
  -- `local instance` / `scoped instance`: the attribute kind precedes the keyword
  let mut kw := ""
  for _ in [0:3] do
    while i < bytes.size && (bytes[i]! == 32 || bytes[i]! == 10 || bytes[i]! == 13 || bytes[i]! == 9) do i := i + 1
    let mut kwc : Array Char := #[]
    while i < bytes.size && bytes[i]! < 128 && (isIdRest (Char.ofNat bytes[i]!.toNat) || bytes[i]! == 35) do
      kwc := kwc.push (Char.ofNat bytes[i]!.toNat)
      i := i + 1
    kw := String.ofList kwc.toList
    if kw == "local" || kw == "scoped" then mods := mods.push kw else break
  return some (attrs, mods, kw)

/-- Decode a `Name` literal term (`Name.mkStr`, `Name.mkStrN`, `Name.mkSimple`), as found in the
compiled body of a syntax quotation. -/
partial def nameLit? (e : Expr) : Option Name :=
  let fn := e.getAppFn
  let args := e.getAppArgs
  let strs (as : Array Expr) : Option (List String) :=
    as.toList.mapM fun a => match a with | .lit (.strVal s) => some s | _ => none
  match fn with
  | .const c _ =>
    if c == ``Lean.Name.anonymous then some .anonymous
    else if c == ``Lean.Name.mkStr && args.size == 2 then
      match nameLit? args[0]!, args[1]! with
      | some p, .lit (.strVal s) => some (.str p s)
      | _, _ => none
    else if c == ``Lean.Name.mkSimple || c == ``Lean.Name.mkStr1 || c == ``Lean.Name.mkStr2
        || c == ``Lean.Name.mkStr3 || c == ``Lean.Name.mkStr4 || c == ``Lean.Name.mkStr5
        || c == ``Lean.Name.mkStr6 || c == ``Lean.Name.mkStr7 || c == ``Lean.Name.mkStr8 then
      (strs args).map fun ss => ss.foldl (fun n s => Name.str n s) .anonymous
    else none
  | _ => none

/-- All `Name` literals occurring in a term. -/
partial def nameLits (e : Expr) : StateM (Std.HashSet Expr × NameSet) Unit := do
  if (← get).1.contains e then return
  modify fun (v, ns) => (v.insert e, ns)
  if let some n := nameLit? e then
    if !n.isAnonymous then modify fun (v, ns) => (v, ns.insert n)
  match e with
  | .app f a => nameLits f; nameLits a
  | .lam _ t b _ | .forallE _ t b _ => nameLits t; nameLits b
  | .letE _ t v b _ => nameLits t; nameLits v; nameLits b
  | .mdata _ b | .proj _ _ b => nameLits b
  | _ => pure ()

end DeadcodeExport
open DeadcodeExport

unsafe def main (args : List String) : IO UInt32 := do
  let outDir :: rootsS :: modsFile :: srcRoot :: rest := args
    | IO.eprintln "usage: <outDir> <rootPrefixes> <modulesFile> <srcRoot> [shard numShards]"; return 1
  let (shard, nShards) := match rest with
    | [a, b] => (a.toNat!, b.toNat!)
    | _ => (0, 1)
  let t0 ← IO.monoMsNow
  let roots := (rootsS.splitOn ",").map String.toName
  let imports := ((← IO.FS.lines modsFile).filter (· ≠ "")).map String.toName
  initSearchPath (← findSysroot)
  enableInitializersExecution
  let env ← importModules (imports.map fun m => {module := m}) {} (trustLevel := 1024) (loadExts := true)
  let t1 ← IO.monoMsNow
  IO.eprintln s!"imported in {t1 - t0} ms"
  let modNames := env.header.moduleNames
  let isProjMod (m : Name) : Bool := roots.any (·.isPrefixOf m)
  let modOf (n : Name) : Option Name := (env.getModuleIdxFor? n).map fun i => modNames[i.toNat]!
  let inProject (n : Name) : Bool := match modOf n with | some m => isProjMod m | none => false
  if shard == 0 then
    let hMod ← IO.FS.Handle.mk (outDir ++ "/modules.jsonl") .write
    for i in [0:modNames.size] do
      let m := modNames[i]!
      if isProjMod m then
        let imps := env.header.moduleData[i]!.imports.map (·.module)
        hMod.putStrLn (Json.compress <| Json.mkObj [
          ("module", m.toString),
          ("imports", toJson (imps.filter isProjMod |>.map (·.toString))),
          ("numExternalImports", toJson (imps.filter (!isProjMod ·)).size)])
    hMod.flush
    -- footprint of every persistent environment extension
    let pExts ← persistentEnvExtensionsRef.get
    let mut extRows : Array (String × Json) := #[]
    for ext in pExts do
      let mut total := 0
      let mut nMods := 0
      for i in [0:modNames.size] do
        if isProjMod modNames[i]! then
          let k := (ext.getModuleEntries env i).size
          if k > 0 then
            total := total + k
            nMods := nMods + 1
      if total > 0 then
        extRows := extRows.push (ext.name.toString, Json.mkObj [("entries", toJson total), ("modules", toJson nMods)])
    IO.FS.writeFile (outDir ++ "/extensions.json") (Json.pretty (Json.mkObj extRows.toList))
  let simpMap ← simpExtensionMapRef.get
  let simpSets : Array (String × SimpTheorems) := simpMap.toArray.map fun (n, ext) => (n.toString, ext.getState env)
  let insts := (instanceExtension.getState env).instanceNames
  let extThms : NameSet := (Lean.Meta.Ext.extExtension.getState env).tree.foldValues
    (fun (s : NameSet) t => s.insert t.declName) {}
  let ctx : Core.Context := { fileName := "<export>", fileMap := default, options := {}, maxHeartbeats := 0 }
  let act : MetaM Json := do
    let projConsts : Array (Name × ConstantInfo) := env.constants.fold (init := #[]) fun acc n ci =>
      if inProject n then acc.push (n, ci) else acc
    let mut primary : NameSet := {}
    let mut autoList : Array (Name × String) := #[]
    for (n, ci) in projConsts do
      let un := (privateToUserName? n).getD n
      let isSyntaxObj := ci.type.getUsedConstants.any fun c =>
        c == ``Lean.ParserDescr || c == ``Lean.TrailingParserDescr || c == ``Lean.Macro
          || c == ``Lean.PrettyPrinter.Unexpander || c == ``Lean.PrettyPrinter.Delaborator.Delab
      let structural := un.isInternalDetail || isSyntaxObj || isAuxRecursor env n || isNoConfusion env n
        || env.isProjectionFn n || (match ci with | .ctorInfo _ | .recInfo _ => true | _ => false)
      -- a user theorem called `eq_6_3_35` looks like an equation lemma (`eq_1`) to `isInternalDetail`;
      -- real equation lemmas carry no declaration range
      let eqLike := match un with
        | .str _ s => s.startsWith "eq_" && !(s.startsWith "eq_def")
        | _ => false
      let hasRange := (← findDeclarationRanges? n).isSome
      let userEq := eqLike && hasRange && !un.hasMacroScopes && !isSyntaxObj && !isAuxRecursor env n
        && !isNoConfusion env n && !env.isProjectionFn n
        && (match ci with | .thmInfo _ | .defnInfo _ => true | _ => false)
      let structural := structural && !userEq
      let mut why := ""
      if structural then
        why := match ci with
          | .ctorInfo _ => "<ctor>" | .recInfo _ => "<rec>"
          | _ => if env.isProjectionFn n then "<proj>" else if isSyntaxObj then "<syntax>" else lastComp n
      else if (← findDeclarationRanges? n).isNone then
        why := "<norange>:" ++ lastComp n
      if why == "" then primary := primary.insert n
      else autoList := autoList.push (n, why)
    let isPrimary (n : Name) : Bool := primary.contains n
    -- Name clashes.  When two imported modules declare the same name, `importModules` may keep one constant
    -- and say nothing (Lean 4.36 does for theorems; 4.34 refuses most such imports).  The other module's
    -- declaration is then invisible to everything below.  Each project module's own .olean is read again and
    -- every constant the environment attributes to a different module is listed.
    if shard == 0 then
      let mut clashRows : Array Json := #[]
      for m in imports do
        let (md, _) ← readModuleData (← findOLean m)
        for n in md.constNames do
          match modOf n with
          | some m' =>
            if m' != m then
              clashRows := clashRows.push (Json.mkObj [
                ("name", n.toString), ("module", m.toString), ("attributedTo", m'.toString),
                ("sourceLevel", isPrimary n)])
          | none => clashRows := clashRows.push (Json.mkObj [
                ("name", n.toString), ("module", m.toString), ("attributedTo", Json.null), ("sourceLevel", false)])
      IO.FS.writeFile (outDir ++ "/clashes.json") (Json.compress (Json.arr clashRows))
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
    let isBodyAux (c : Name) : Bool :=
      match env.find? c with
      | some (.ctorInfo _) | some (.recInfo _) => false
      | _ =>
        if env.isProjectionFn c || isAuxRecursor env c || isNoConfusion env c then false
        else if c.hasMacroScopes || Lean.Meta.isMatcherCore env c then true
        else match c with
          | .num _ _ => true
          | .str _ s => s.startsWith "_" || s.startsWith "match_" || s.startsWith "proof_"
          | .anonymous => false
    -- dependency collection; auto-generated constants are folded (see corpora/tools/ExportDecls.lean,
    -- whose rule this is): a derived object (constructor, projection, recursor, equation lemma) stands
    -- for its parent; a body auxiliary of ANOTHER declaration is inlined.
    let rec go (n : Name) (fuel : Nat) (isVal : Bool) (e : Expr) (d : Deps) : Deps := Id.run do
      let mut d := d
      for c in e.getUsedConstants do
        if c == n then continue
        match env.find? c with
        | none => continue
        | some cci =>
        if !inProject c then continue
        if isPrimary c then
          d := if isVal then { d with valueDeps := d.valueDeps.insert c } else { d with typeDeps := d.typeDeps.insert c }
        else
          let par := if isBodyAux c then (match parentOf c with | some p => if p == n then some p else none | none => none)
                     else parentOf c
          match par with
          | some p =>
            if p != n then
              d := if isVal then { d with valueDeps := d.valueDeps.insert p } else { d with typeDeps := d.typeDeps.insert p }
              -- the derived object's own term is needed too (it can mention more than its parent does)
              if !d.visited.contains c && fuel > 0 then
                d := { d with visited := d.visited.insert c }
                d := go n (fuel - 1) isVal cci.type d
                if let some v := cci.value? (allowOpaque := true) then
                  d := go n (fuel - 1) isVal v d
            else if !d.visited.contains c && fuel > 0 then
              d := { d with visited := d.visited.insert c }
              d := go n (fuel - 1) isVal cci.type d
              if let some v := cci.value? (allowOpaque := true) then
                d := go n (fuel - 1) isVal v d
          | none =>
            if !d.visited.contains c && fuel > 0 then
              d := { d with visited := d.visited.insert c }
              d := go n (fuel - 1) isVal cci.type d
              if let some v := cci.value? (allowOpaque := true) then
                d := go n (fuel - 1) isVal v d
      return d
    if shard == 0 then
      let hAuto ← IO.FS.Handle.mk (outDir ++ "/autos.jsonl") .write
      let hMeta ← IO.FS.Handle.mk (outDir ++ "/meta.jsonl") .write
      for (n, why) in autoList do
        let par := parentOf n
        hAuto.putStrLn (Json.compress <| Json.mkObj [
          ("name", n.toString), ("why", why),
          ("parent", match par with | some p => Json.str p.toString | none => Json.null)])
        if par.isNone then
          if let some ci := env.find? n then
            let mut d : Deps := {}
            d := go n 64 false ci.type d
            if let some v := ci.value? (allowOpaque := true) then d := go n 64 true v d
            -- names quoted inside a notation / macro body are Name literals, not constants
            let mut quoted : NameSet := {}
            if let some v := ci.value? (allowOpaque := true) then
              let (_, (_, lits)) := (nameLits v).run ({}, {})
              for q in lits do
                if inProject q then
                  if isPrimary q then quoted := quoted.insert q
                  else if let some p := parentOf q then quoted := quoted.insert p
            let rng ← findDeclarationRanges? n
            hMeta.putStrLn (Json.compress <| Json.mkObj [
              ("name", n.toString), ("why", why), ("module", ((modOf n).getD .anonymous).toString),
              ("instance", insts.contains n),
              ("line", match rng with | some r => toJson r.range.pos.line | none => Json.null),
              ("deps", namesJson (d.typeDeps.toList.foldl (fun s x => s.insert x) d.valueDeps)),
              ("quoted", namesJson quoted)])
      hAuto.flush
      hMeta.flush
    let suffix := if nShards == 1 then "" else s!".{shard}"
    let h ← IO.FS.Handle.mk (outDir ++ s!"/decls{suffix}.jsonl") .write
    let sorted := projConsts.filter (fun p => isPrimary p.1) |>.qsort (fun a b => a.1.toString < b.1.toString)
    let mut srcCache : Std.HashMap Name (String × FileMap) := {}
    let mut parseFail := 0
    let mut idx := 0
    for (n, ci) in sorted do
      idx := idx + 1
      if idx % nShards != shard then continue
      let mut d : Deps := {}
      d := go n 64 false ci.type d
      if let .inductInfo iv := ci then
        for cn in iv.ctors do
          if let some cc := env.find? cn then d := go n 64 false cc.type d
      if let some v := ci.value? (allowOpaque := true) then d := go n 64 true v d
      let isInst := insts.contains n
      let constKind : String := match ci with
        | .thmInfo _ => "theorem" | .defnInfo _ => "def" | .axiomInfo _ => "axiom"
        | .opaqueInfo _ => "opaque"
        | .inductInfo _ => if isStructure env n then "structure" else "inductive"
        | .quotInfo _ => "quot" | .ctorInfo _ => "ctor" | .recInfo _ => "rec"
      let kind : String := if isInst then "instance" else constKind
      let rng ← findDeclarationRanges? n
      let m := (modOf n).getD .anonymous
      let (sh, stSize) := shapeOf inProject ci.type
      let mut inSets : Array String := #[]
      for (sn, st) in simpSets do
        if st.lemmaNames.contains (.decl n) || st.lemmaNames.contains (.decl n false) || st.toUnfold.contains n then
          inSets := inSets.push sn
      let red := match getReducibilityStatusCore env n with
        | .reducible => "reducible" | .irreducible => "irreducible" | .semireducible => "semireducible"
        | _ => "instances"
      let unexp := !(Lean.PrettyPrinter.Delaborator.appUnexpanderAttribute.getValues env n).isEmpty
      -- Lean's parser on the head of the declaration range
      let mut attrsJ : Json := Json.null
      let mut modsJ : Json := Json.null
      let mut kw : String := ""
      if let some r := rng then
        let path := srcRoot ++ "/" ++ (m.toString.replace "." "/") ++ ".lean"
        if !srcCache.contains m then
          let txt ← try IO.FS.readFile path catch _ => pure ""
          srcCache := srcCache.insert m (txt, FileMap.ofString txt)
        let (txt, fm) := srcCache[m]!
        if txt != "" then
          match parseHead env txt fm path r.range.pos.line r.range.pos.column with
          | some (as, ms, k) =>
            attrsJ := toJson (as.map fun (k, t) => Json.mkObj [("kind", k), ("text", t)])
            modsJ := toJson ms
            kw := k
          | none => parseFail := parseFail + 1
      h.putStrLn (Json.compress <| Json.mkObj [
        ("name", n.toString),
        ("userName", ((privateToUserName? n).getD n).toString),
        ("module", m.toString),
        ("kind", kind),
        ("constKind", constKind),
        ("isClass", isClass env n),
        ("isPrivate", isPrivateName n),
        ("typeDeps", namesJson d.typeDeps),
        ("valueDeps", namesJson d.valueDeps),
        ("shape", toString sh),
        ("statementDagSize", stSize),
        ("simpSets", toJson inSets),
        ("instance", isInst),
        ("reducibility", red),
        ("ext", extThms.contains n),
        ("unexpander", unexp),
        ("attrs", attrsJ), ("mods", modsJ), ("declKw", kw),
        ("line", match rng with | some r => toJson r.range.pos.line | none => Json.null),
        ("col", match rng with | some r => toJson r.range.pos.column | none => Json.null),
        ("endLine", match rng with | some r => toJson r.range.endPos.line | none => Json.null),
        ("endCol", match rng with | some r => toJson r.range.endPos.column | none => Json.null)])
    h.flush
    return Json.mkObj [
      ("numProjectConstants", projConsts.size),
      ("numPrimary", sorted.size),
      ("numAuto", autoList.size),
      ("headParseFailures", parseFail),
      ("simpSetsRegistered", simpSets.size)]
  let (res, _) ← act.run'.toIO ctx { env }
  let t2 ← IO.monoMsNow
  if shard == 0 then
    let metaJ := res.mergeObj (Json.mkObj [
      ("leanVersion", Lean.versionString),
      ("roots", toJson rootsS), ("shards", nShards),
      ("importMs", t1 - t0), ("exportMs", t2 - t1)])
    IO.FS.writeFile (outDir ++ "/export_meta.json") (Json.pretty metaJ)
  IO.eprintln s!"shard {shard}/{nShards} done in {t2 - t0} ms"
  return 0
