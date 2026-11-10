/-
Lean helper for the definition-centred outline (bench/outline2.py, plan node M2).

Stand-alone program (imports only `Lean`); loads the BUILT environment of `corpora/ns` with
`importModules` and reads everything from `Environment` / `Expr`.  No source text, no regex.
Nothing in the corpus is built or modified.

  outline2 heads <modules.txt> <names.txt> <out.jsonl>
      For every listed declaration: the head constant of each hypothesis, what the conclusion
      "produces" (its head constant, looking through Nonempty / ∃ / ∧ / Σ / subtype / product),
      whether it is a structure, whether a definition is sort-valued (and Prop-valued), the head of a definition's
      body.  Pure `Expr` walks; nothing is pretty-printed.

  outline2 print <modules.txt> <spec.json> <out.jsonl>
      spec.json: [{"name": .., "as": "concept" | "statement", "ns": "<namespace to print in>"}]
      concept   : a structure's fields (types printed by Lean with the parameters and earlier
                  fields in scope, each with its docstring), an inductive's constructors, or a
                  definition's body after stripping its leading binders: ONE level, nothing
                  below it is unfolded.
      statement : the binder telescope, one printed type per binder, and the conclusion.
      Every printed piece also lists the constants it mentions.
-/
import Lean
open Lean Meta

namespace Outline2

def lookThrough : List Name :=
  [``Nonempty, ``And, ``Subtype, ``Sigma, ``PSigma, ``Prod, ``PProd, ``Inhabited, ``Not]

/-- Head constant of a type after dropping leading ∀ binders. -/
partial def headOf : Expr → Option Name
  | .forallE _ _ b _ => headOf b
  | .mdata _ e => headOf e
  | .letE _ _ _ b _ => headOf b
  | e => match e.getAppFn with
    | .const n _ => some n
    | _ => none

/-- Constants a conclusion produces: its head, looking through existence wrappers. -/
partial def produced (e : Expr) (acc : Array Name) (fuel : Nat := 64) : Array Name :=
  if fuel == 0 then acc else
  match e with
  | .mdata _ e => produced e acc fuel
  | .forallE _ _ b _ => produced b acc (fuel - 1)
  | .lam _ _ b _ => produced b acc (fuel - 1)
  | _ =>
    match e.getAppFn with
    | .const n _ =>
      let args := e.getAppArgs
      if n == ``Exists then
        -- ∃ x : T, body : T is produced, and so is whatever the body asserts
        let acc := match args[0]? with
          | some t => produced t acc (fuel - 1)
          | none => acc
        match args[1]? with
        | some b => produced b acc (fuel - 1)
        | none => acc
      else if lookThrough.contains n then
        args.foldl (fun acc a => produced a acc (fuel - 1)) acc
      else acc.push n
    | _ => acc

partial def stripLam : Expr → Expr
  | .lam _ _ b _ => stripLam b
  | .mdata _ e => stripLam e
  | e => e

partial def conclusionOf : Expr → Expr
  | .forallE _ _ b _ => conclusionOf b
  | .mdata _ e => conclusionOf e
  | e => e

partial def binderHeads : Expr → Array Json → Array Json
  | .forallE _ t b bi, acc =>
    let h := match headOf t with | some n => Json.str n.toString | none => Json.null
    let biS := match bi with
      | .default => "default" | .implicit => "implicit"
      | .strictImplicit => "strict" | .instImplicit => "inst"
    binderHeads b (acc.push (Json.mkObj [("head", h), ("bi", biS)]))
  | .mdata _ e, acc => binderHeads e acc
  | _, acc => acc

def headsLine (env : Environment) (s : String) (n : Name) : Json := Id.run do
  let some ci := env.find? n | return Json.mkObj [("name", s), ("missing", true)]
  let concl := conclusionOf ci.type
  let prod := (produced concl #[]).map (·.toString)
  let sortValued := concl.isSort
  let valueHead : Json := match ci.value? with
    | some v => match (stripLam v).getAppFn with
      | .const h _ => Json.str h.toString
      | _ => Json.null
    | none => Json.null
  let isStruct := (getStructureInfo? env n).isSome
  let nFields := if isStruct then (getStructureFields env n).size else 0
  return Json.mkObj [("name", s), ("binders", Json.arr (binderHeads ci.type #[])),
    ("produces", toJson prod), ("sortValued", sortValued), ("propValued", concl.isProp), ("valueHead", valueHead),
    ("isStructure", isStruct), ("nFields", nFields),
    ("conclHead", match headOf concl with | some h => Json.str h.toString | none => Json.null)]

def constsOf (e : Expr) : Json := toJson (e.getUsedConstants.map (·.toString))

def biStr : BinderInfo → String
  | .default => "default" | .implicit => "implicit"
  | .strictImplicit => "strict" | .instImplicit => "inst"

partial def typeBinderInfos : Expr → Array BinderInfo → Array BinderInfo
  | .forallE _ _ b bi, acc => typeBinderInfos b (acc.push bi)
  | .mdata _ e, acc => typeBinderInfos e acc
  | _, acc => acc

def pp (e : Expr) : MetaM String := do
  let f ← Meta.ppExpr e
  return f.pretty 100

/-- Binders of a telescope as JSON: name, binder kind, printed type, constants in the type. -/
def binderJson (xs : Array Expr) : MetaM (Array Json) := do
  let mut out := #[]
  for x in xs do
    let d ← x.fvarId!.getDecl
    let t ← instantiateMVars d.type
    out := out.push (Json.mkObj [("name", d.userName.eraseMacroScopes.toString), ("bi", biStr d.binderInfo),
      ("type", (← pp t)), ("consts", constsOf t), ("isProp", (← isProp t))])
  return out

def docOf (env : Environment) (n : Name) : MetaM Json := do
  match (← findDocString? env n) with
  | some s => return Json.str s
  | none => return Json.null

def printStatement (env : Environment) (s : String) (n : Name) : MetaM Json := do
  let some ci := env.find? n | return Json.mkObj [("name", s), ("missing", true)]
  forallTelescope ci.type fun xs concl => do
    return Json.mkObj [("name", s), ("as", "statement"), ("doc", (← docOf env n)),
      ("binders", Json.arr (← binderJson xs)), ("conclusion", (← pp concl)),
      ("conclusionConsts", constsOf concl), ("levelParams", toJson (ci.levelParams.map (·.toString)))]

def printConcept (env : Environment) (s : String) (n : Name) : MetaM Json := do
  let some ci := env.find? n | return Json.mkObj [("name", s), ("missing", true)]
  let doc ← docOf env n
  let base : List (String × Json) := [("name", Json.str s), ("as", Json.str "concept"), ("doc", doc)]
  match ci with
  | .inductInfo iv =>
    if let some _ := getStructureInfo? env n then
      let ctor := iv.ctors.head!
      let some cinfo := env.find? ctor | return Json.mkObj (base ++ ([("missing", Json.bool true)] : List (String × Json)))
      let fieldNames := getStructureFields env n
      forallTelescope cinfo.type fun xs _ => do
        let params := xs.extract 0 iv.numParams
        let fields := xs.extract iv.numParams xs.size
        -- the constructor makes every parameter implicit; show the binder kinds of the type itself
        let tyBis := typeBinderInfos ci.type #[]
        let pj0 ← binderJson params
        let mut pj := #[]
        for i in [0:pj0.size] do
          pj := pj.push (match tyBis[i]? with
            | some bi => (pj0[i]!).setObjVal! "bi" (biStr bi)
            | none => pj0[i]!)
        let mut fs := #[]
        let fj ← binderJson fields
        for i in [0:fj.size] do
          let fname := fieldNames[i]?.getD .anonymous
          let fdoc ← docOf env (n ++ fname)
          fs := fs.push ((fj[i]!).setObjVal! "doc" fdoc |>.setObjVal! "field" fname.toString)
        let parents := (getStructureParentInfo env n).map (·.structName.toString)
        return Json.mkObj (base ++ ([("form", Json.str "structure"), ("params", Json.arr pj),
          ("fields", Json.arr fs), ("parents", toJson parents), ("isClass", Json.bool (isClass env n)),
          ("resultSort", Json.str (← forallTelescope ci.type fun _ r => pp r))] : List (String × Json)))
    else
      let mut cs := #[]
      for c in iv.ctors do
        let some cinfo := env.find? c | continue
        let j ← forallTelescope cinfo.type fun xs r => do
          let args := xs.extract iv.numParams xs.size
          return Json.mkObj [("ctor", c.toString), ("doc", (← docOf env c)),
            ("args", Json.arr (← binderJson args)), ("result", (← pp r))]
        cs := cs.push j
      let params ← forallTelescope ci.type fun xs r => do
        return Json.mkObj [("b", Json.arr (← binderJson xs)), ("r", (← pp r))]
      return Json.mkObj (base ++ ([("form", Json.str "inductive"), ("signature", params), ("ctors", Json.arr cs)] : List (String × Json)))
  | _ =>
    match ci.value? with
    | none => return Json.mkObj (base ++ ([("form", Json.str "opaque")] : List (String × Json)))
    | some v =>
      lambdaTelescope v fun xs body => do
        let ty ← instantiateForall ci.type xs
        return Json.mkObj (base ++ ([("form", Json.str "def"), ("params", Json.arr (← binderJson xs)),
          ("resultType", Json.str (← pp ty)), ("resultConsts", constsOf ty),
          ("body", Json.str (← pp body)), ("bodyConsts", constsOf body),
          ("isTheorem", Json.bool (match ci with | .thmInfo _ => true | _ => false))] : List (String × Json)))

unsafe def main (args : List String) : IO UInt32 := do
  let [mode, modsFile, inFile, outFile] := args
    | throw <| IO.userError "usage: outline2 heads|print modules.txt input output"
  initSearchPath (← findSysroot)
  enableInitializersExecution
  let modNames := ((← IO.FS.lines modsFile).filter (· ≠ "")).map (·.toName)
  let env ← importModules (modNames.map fun m => { module := m }) {} (trustLevel := 1024) (loadExts := true)
  -- name table: the exports render names with `Name.toString`
  let mut byStr : Std.HashMap String Name := {}
  for (n, _) in env.constants.map₁.toList do
    byStr := byStr.insert n.toString n
  let h ← IO.FS.Handle.mk outFile .write
  if mode == "heads" then
    for s in (← IO.FS.lines inFile) do
      if s == "" then continue
      match byStr[s]? with
      | some n => h.putStrLn (headsLine env s n).compress
      | none => h.putStrLn (Json.mkObj [("name", s), ("missing", true)]).compress
    h.flush
    return 0
  let spec ← IO.ofExcept (Json.parse (← IO.FS.readFile inFile))
  let items ← IO.ofExcept spec.getArr?
  let opts : Options := ({} : Options)
    |>.insert `pp.maxSteps (DataValue.ofNat 2000000)
    |>.insert `pp.deepTerms (DataValue.ofBool true)
    |>.insert `pp.deepTerms.threshold (DataValue.ofNat 1000000)
  for it in items do
    let s := (it.getObjValAs? String "name").toOption.getD ""
    let as := (it.getObjValAs? String "as").toOption.getD "statement"
    let ns := ((it.getObjValAs? String "ns").toOption.getD "").toName
    let coreCtx : Core.Context := { fileName := "<outline2>", fileMap := default, maxHeartbeats := 0,
                                    maxRecDepth := 1000000, options := opts, currNamespace := ns }
    match byStr[s]? with
    | none => h.putStrLn (Json.mkObj [("name", s), ("missing", true)]).compress
    | some n =>
      let act : MetaM Json := if as == "concept" then printConcept env s n else printStatement env s n
      let r ← try
          let (a, _) ← act.run'.toIO coreCtx { env := env }
          pure (a.setObjVal! "ns" ns.toString |>.setObjVal! "module"
            (match env.getModuleIdxFor? n with
             | some i => env.header.moduleNames[i.toNat]!.toString | none => ""))
        catch e => pure (Json.mkObj [("name", s), ("error", toString e)])
      h.putStrLn r.compress
  h.flush
  return 0

end Outline2

unsafe def main (args : List String) : IO UInt32 := Outline2.main args
