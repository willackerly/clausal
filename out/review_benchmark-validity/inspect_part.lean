
/-! ### REVIEW: independent inlining + per-target checks -/

def parsePath (s : String) : Path :=
  if s == "root" then #[] else ((s.splitOn ".").map String.toNat!).toArray

partial def inl2 (L : Name) (lps : List Name) (vL : Expr) (e : Expr) : Expr :=
  e.replace fun x =>
    let f := x.getAppFn
    if f.isConstOf L then
      let args := x.getAppArgs.map (inl2 L lps vL)
      some ((vL.instantiateLevelParams lps f.constLevels!).beta args)
    else none

def inspectItem (idx : Nat) (item : Json) (names : Std.HashMap String Name) (verbose : Bool) :
    MetaM Json := do
  let getS (k : String) : MetaM String :=
    match item.getObjValAs? String k with
    | .ok s => pure s
    | .error e => throwError "corpus item lacks '{k}': {e}"
  let some T := names[← getS "theoremFullName"]? | throwError "unknown theorem"
  let some L := names[← getS "helperFullName"]? | throwError "unknown helper"
  let tInfo ← getConstInfo T
  let lInfo ← getConstInfo L
  let vT := stripMData (← proofOfConst T)
  let vL := stripMData (← proofOfConst L)
  let (tagged, _) := (inlineAux L lInfo.levelParams vL vT).run {}
  let ((), wst) := (walk tagged #[]).run {}
  let flat := stripMData tagged
  let flat2 := inl2 L lInfo.levelParams vL vT
  let b1 ← Core.betaReduce flat
  let b2 ← Core.betaReduce flat2
  let sameFlat := b1 == b2
  -- per-target checks on the ORIGINAL theorem proof at the same path
  let out ← IO.mkRef (#[] : Array Json)
  let exact := wst.tgts.filter (·.via == "exact")
  let hookT : LiftHook := {
    targets := exact.map (·.path)
    onTarget := fun p e => do
      let headIsL := e.getAppFn.isConstOf L
      let tyT := (← inferType e).headBeta
      let eF := inl2 L lInfo.levelParams vL e
      let tyF := (← inferType eF).headBeta
      let syn := tyT == tyF
      let synB := (← Core.betaReduce tyT) == (← Core.betaReduce tyF)
      let deq ← isDefEq tyT tyF
      let iT ← interfaceOf e tyT
      let iF ← interfaceOf eF tyF
      let iFraw ← Rosette.interfaceOf eF tyF
      let sT ← mkForallFVars iT.deps tyT
      let sF ← mkForallFVars iF.deps tyF
      let sFraw ← mkForallFVars iFraw.deps tyF
      let valF ← mkLambdaFVars iF.deps eF
      let env ← getEnv
      let kc := match Kernel.check env {} valF with
        | .ok ty => match Kernel.isDefEq env {} ty sF with
          | .ok true => "ok" | .ok false => "mismatch" | .error _ => "defEqError"
        | .error _ => "reject"
      let mut fields : List (String × Json) := [
        ("path", toJson (pathToString p)), ("headIsL", toJson headIsL), ("nArgs", toJson e.getAppNumArgs),
        ("tySynEq", toJson syn), ("tySynEqBeta", toJson synB), ("tyDefEq", toJson deq),
        ("S_declAtArgs", toJson (dagSize sT)), ("S_inferred", toJson (dagSize sF)), ("S_inferredRaw", toJson (dagSize sFraw)),
        ("deps_T", toJson iT.args.size), ("deps_F", toJson iF.args.size), ("deps_Fraw", toJson iFraw.args.size),
        ("P_site", toJson (dagSize e)), ("P_inlined", toJson (dagSize eF)), ("P_closed", toJson (dagSize valF)),
        ("hashEq", toJson (statementHash sT == statementHash sF)), ("kernel", toJson kc)]
      if verbose then
        fields := fields ++ [("stmtDecl", toJson (← ppExpr sT).pretty), ("stmtInferred", toJson (← ppExpr sF).pretty),
          ("stmtInferredRaw", toJson (← ppExpr sFraw).pretty)]
      out.modify (·.push (Json.mkObj fields))
      return e }
  discard <| ((visit vT #[] none "root" 0).run { cfg := benchCfg, lift? := some hookT }).run' {}
  -- root body: does the dup bug hide a restatement of the theorem?
  let rb ← IO.mkRef Json.null
  if flat.isLambda then
    let hookR : LiftHook := {
      targets := #[#[0]]
      onTarget := fun _ e => do
        let ty := (← inferType e).headBeta
        let i1 ← interfaceOf e ty
        let i0 ← Rosette.interfaceOf e ty
        let s1 ← mkForallFVars i1.deps ty
        let s0 ← mkForallFVars i0.deps ty
        let th := statementHash tInfo.type
        rb.set (Json.mkObj [("depsRaw", toJson i0.args.size), ("depsDedup", toJson i1.args.size),
          ("Sraw", toJson (dagSize s0)), ("Sdedup", toJson (dagSize s1)), ("Sthm", toJson (dagSize tInfo.type)),
          ("rawHashIsThm", toJson (statementHash s0 == th)), ("dedupHashIsThm", toJson (statementHash s1 == th))])
        return e }
    discard <| ((visit flat #[] none "root" 0).run { cfg := benchCfg, lift? := some hookR }).run' {}
  return Json.mkObj [("idx", toJson idx), ("theorem", toJson T.toString), ("helper", toJson L.toString),
    ("sameFlatUpToBeta", toJson sameFlat), ("flatDag", toJson (dagSize flat)), ("flat2Dag", toJson (dagSize flat2)),
    ("nTargets", toJson wst.tgts.size), ("nExact", toJson exact.size),
    ("targets", Json.arr (← out.get)), ("rootBody", ← rb.get)]

def inspectAll : MetaM Unit := do
  let items ← match Json.parse (← IO.FS.readFile "bench/corpus.json") with
    | .ok (.arr a) => pure a
    | _ => throwError "cannot parse corpus"
  let outPath := (← IO.getEnv "ROSETTE_INSPECT_OUT").getD "out/review_benchmark-validity/inspect.jsonl"
  let verboseIds : List Nat := ((← IO.getEnv "ROSETTE_INSPECT_VERBOSE").getD "").splitOn "," |>.filterMap String.toNat?
  let only : List Nat := ((← IO.getEnv "ROSETTE_INSPECT_ONLY").getD "").splitOn "," |>.filterMap String.toNat?
  let mut wanted : Std.HashSet String := {}
  for it in items do
    for k in ["theoremFullName", "helperFullName"] do
      if let .ok s := it.getObjValAs? String k then wanted := wanted.insert s
  let names := (← getEnv).constants.fold (init := ({} : Std.HashMap String Name)) fun m n _ =>
    let s := n.toString
    if wanted.contains s then m.insert s n else m
  let h ← IO.FS.Handle.mk outPath .write
  for idx in [0:items.size] do
    if !only.isEmpty && !only.contains idx then continue
    let j ← try
        tryCatchRuntimeEx (withBudget 2000000 (inspectItem idx items[idx]! names (verboseIds.contains idx))) fun ex => do
          pure (Json.mkObj [("idx", toJson idx), ("error", toJson (← ex.toMessageData.toString))])
      catch ex => pure (Json.mkObj [("idx", toJson idx), ("error", toJson (← ex.toMessageData.toString))])
    h.putStrLn j.compress
    h.flush
  IO.println "inspect done"
