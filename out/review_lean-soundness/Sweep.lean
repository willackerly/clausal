import Mathlib
import Rosette.Lift
open Lean Meta Elab Command Rosette
set_option maxHeartbeats 0

namespace Rev

def canonLevels (stmt : Expr) : Expr :=
  let ps := (collectLevelParams {} stmt).params
  stmt.instantiateLevelParams ps.toList ((List.range ps.size).map fun i => Level.param (Name.mkNum `u i))

/-- independent, de-duplicated interface -/
def myInterface (e ty : Expr) : MetaM (Array Expr) := do
  let lctx ← getLCtx
  let mut seen : Std.HashSet FVarId := {}
  let mut work : Array FVarId := (collectFVars (collectFVars {} e) ty).fvarIds
  let mut i := 0
  let mut out : Array LocalDecl := #[]
  while i < work.size do
    let f := work[i]!
    i := i + 1
    if seen.contains f then continue
    seen := seen.insert f
    let some d := lctx.find? f | throwError "unknown fvar"
    out := out.push d
    work := work ++ (collectFVars {} d.type).fvarIds
    if let some v := d.value? then work := work ++ (collectFVars {} v).fvarIds
  let sorted := out.qsort (·.index < ·.index)
  return sorted.map (·.toExpr)

def log (h : IO.FS.Handle) (s : String) : IO Unit := do
  h.putStrLn s; h.flush

def thmDeclOf (env : Environment) (n : Name) : Option Declaration :=
  match env.find? n with
  | some (.thmInfo t) => some (.thmDecl t)
  | _ => none

/-- lift with a config, then verify everything independently. returns (ok, message, nLemmas, dupArgLemmas, truncated, subErrs) -/
def liftAndVerify (n : Name) (cfg : LiftConfig) : MetaM (Bool × String × Nat × Nat × Bool × Nat) := do
  let saved ← getEnv
  let info ← getConstInfo n
  try
    let r ← liftConst n cfg
    let env ← getEnv
    let mut problems : Array String := #[]
    let some (.thmInfo main) := env.find? r.main | throwError "main not a theorem"
    unless main.type == info.type do problems := problems.push "main type differs"
    unless main.levelParams == info.levelParams do problems := problems.push "main lparams differ"
    let lemNames := r.lemmas.map (·.name)
    if main.value.getUsedConstantsAsSet.contains n then problems := problems.push "main calls original"
    -- axioms
    let ax0 ← collectAxioms n
    for d in lemNames.push r.main do
      for a in (← collectAxioms d) do
        unless ax0.contains a do problems := problems.push s!"new axiom {a} in {d}"
    -- independent kernel replay on the pre-lift kernel environment
    let mut kenv := saved.toKernelEnv
    for d in lemNames.push r.main do
      match thmDeclOf env d with
      | none => problems := problems.push s!"{d} not a theorem"
      | some decl =>
        if let .thmDecl t := decl then
          if t.value.getUsedConstantsAsSet.contains n && d != r.main then
            problems := problems.push s!"{d} calls original"
          if t.type.hasFVar || t.type.hasMVar || t.value.hasFVar || t.value.hasMVar || t.value.hasSorry then
            problems := problems.push s!"{d} has fvar/mvar/sorry"
        match kenv.addDeclCore 0 0 decl none with
        | .ok k => kenv := k
        | .error _ => problems := problems.push s!"kernel replay rejected {d}"
    -- duplicated arguments at call sites
    let mut dup := 0
    for l in r.lemmas do
      let hit := (main.value.find? fun s =>
        s.isApp && s.getAppFn.isConstOf l.name && s.getAppNumArgs == l.numArgs &&
          (let as := s.getAppArgs
           (List.range as.size).any fun i => (List.range i).any fun j => as[i]! == as[j]!)).isSome
      if hit then dup := dup + 1
    setEnv saved
    return (problems.isEmpty, "; ".intercalate problems.toList, r.lemmas.size, dup,
      r.enumeration.truncated, r.enumeration.errors)
  catch ex =>
    setEnv saved
    let m ← ex.toMessageData.toString
    return (false, "EXCEPTION " ++ (m.take 300).toString, 0, 0, false, 0)

end Rev

open Rev in
run_meta do
  let h ← IO.FS.Handle.mk "out/review_lean-soundness/sweep.log" .write
  let env ← getEnv
  let seed : UInt64 := 20261109
  let mut pool : Array (UInt64 × Name) := #[]
  for (n, ci) in env.constants.map₁.toList do
    if let .thmInfo _ := ci then
      if n.isInternalDetail then continue
      let hn := mixHash (hash n) seed
      if hn % 53 != 7 then continue
      let some mi := env.getModuleIdxFor? n | continue
      unless (`Mathlib).isPrefixOf env.header.moduleNames[mi.toNat]! do continue
      pool := pool.push (mixHash hn 977, n)
  let poolS := pool.qsort fun a b => a.1 < b.1
  let mut names : Array Name := #[]
  for (_, n) in poolS do
    if names.size ≥ 50 then break
    let p ← proofOfConst n
    if dagSize p ≥ 1000 then names := names.push n
  log h s!"pool={poolS.size} selected={names.size}"
  -- phase 1 counters
  let mut okDefault := 0; let mut okAgg := 0
  let mut lemDefault := 0; let mut lemAgg := 0; let mut dupDefault := 0; let mut dupAgg := 0
  let mut truncN := 0; let mut subErrs := 0
  -- phase 2 counters
  let mut cTotal := 0; let mut cChecked := 0; let mut cKernelFail := 0; let mut cException := 0
  let mut cNotClosed := 0; let mut cDup := 0; let mut cSizeMismatch := 0; let mut cHashMismatch := 0
  let mut cProofMismatch := 0
  let mut sumStmt := 0; let mut sumStmtDedup := 0
  let mut dupTriples := 0
  let mut hashTab : Std.HashMap UInt64 Expr := {}
  let mut collisions := 0
  for n in names do
    let t0 ← IO.monoMsNow
    let info ← getConstInfo n
    let proof ← proofOfConst n
    let (ok1, m1, l1, d1, tr1, se1) ← liftAndVerify n { k := 5 }
    let (ok2, m2, l2, d2, _, _) ← liftAndVerify n
      { k := 12, minProofSize := 20, maxStatementSize := 1000000, maxFraction := 0.95, suffix := "agg" }
    if ok1 then okDefault := okDefault + 1
    if ok2 then okAgg := okAgg + 1
    lemDefault := lemDefault + l1; lemAgg := lemAgg + l2
    dupDefault := dupDefault + d1; dupAgg := dupAgg + d2
    if tr1 then truncN := truncN + 1
    subErrs := subErrs + se1
    let t1 ← IO.monoMsNow
    -- phase 2
    let r ← candidatesOfExprCore proof { ppStatements := false }
    cTotal := cTotal + r.cands.size
    -- duplicate candidates (same statement hash, same proof sizes)
    let mut seenT : Std.HashSet (UInt64 × Nat × Nat) := {}
    for c in r.cands do
      let key := (c.stmtHash, c.proofSizeDag, c.proofSizeTree)
      if seenT.contains key then dupTriples := dupTriples + 1 else seenT := seenT.insert key
    -- sample up to 40 candidates
    let idxs := (Array.range r.cands.size).qsort fun a b =>
      mixHash (hash a) seed < mixHash (hash b) seed
    let kenv := (← getEnv).toKernelEnv
    let mut thisFail := 0; let mut thisDup := 0
    for i in idxs.extract 0 40 do
      let c := r.cands[i]!
      let res ← IO.mkRef (none : Option (Bool × Bool × Nat × Nat × UInt64 × Nat × Nat × Expr))
      let onTarget (_ : Path) (e : Expr) : MetaM Expr := do
        let ty := (← inferType e).headBeta
        let ifc ← interfaceOf e ty
        let (stmt, val) ← closeOver ifc e ty
        let closed := !(stmt.hasFVar || stmt.hasMVar || stmt.hasLooseBVars ||
          val.hasFVar || val.hasMVar || val.hasLooseBVars)
        let used := (collectLevelParams (collectLevelParams {} stmt) val).params
        let lps := info.levelParams.filter used.contains
        let kok := match kenv.addDeclCore 0 0
            (.thmDecl { name := `Rev.tmpCandidate, levelParams := lps, type := stmt, value := val }) none with
          | .ok _ => true
          | .error _ => false
        let mine ← myInterface e ty
        let stmt2 ← mkForallFVars mine ty
        res.set (some (closed, kok, ifc.deps.size - mine.size, dagSize stmt, statementHash stmt,
          dagSize stmt2, dagSize e, canonLevels stmt))
        return e
      try
        let st ← IO.mkRef ({} : Rosette.State)
        let hook : LiftHook := { targets := #[c.path], onTarget }
        discard <| ((visit proof #[] none "root" 0).run { cfg := {}, lift? := some hook }) st
        match ← res.get with
        | none => cException := cException + 1; log h s!"  NOTREACHED {n} #{c.id}"
        | some (closed, kok, dup, ssize, shash, ssize2, psize, cstmt) =>
          cChecked := cChecked + 1
          unless closed do cNotClosed := cNotClosed + 1
          unless kok do
            cKernelFail := cKernelFail + 1; thisFail := thisFail + 1
            log h s!"  KERNELFAIL {n} #{c.id} path={pathToString c.path} role={c.role} kind={c.kind} dag={c.proofSizeDag} stmt={c.statementSize}"
          if dup > 0 then cDup := cDup + 1; thisDup := thisDup + 1
          if ssize != c.statementSize then cSizeMismatch := cSizeMismatch + 1
          if shash != c.stmtHash then cHashMismatch := cHashMismatch + 1
          if psize != c.proofSizeDag then cProofMismatch := cProofMismatch + 1
          sumStmt := sumStmt + ssize; sumStmtDedup := sumStmtDedup + ssize2
          match hashTab[shash]? with
          | some other =>
            unless other == cstmt do
              collisions := collisions + 1
              log h s!"  HASHCOLLISION {n} #{c.id}"
          | none => hashTab := hashTab.insert shash cstmt
      catch ex =>
        cException := cException + 1
        log h s!"  EXC {n} #{c.id}: {((← ex.toMessageData.toString).take 200).toString}"
    let t2 ← IO.monoMsNow
    log h s!"{n} dag={dagSize proof} cands={r.cands.size} visited={r.visited} trunc={r.truncated} errs={r.errors} | default ok={ok1} lem={l1} dupArgs={d1} {m1} | agg ok={ok2} lem={l2} dupArgs={d2} {m2} | sampleKernelFail={thisFail} sampleDupDeps={thisDup} | ms lift={t1-t0} cand={t2-t1}"
  log h s!"SUMMARY theorems={names.size} defaultOk={okDefault} aggOk={okAgg} lemmasDefault={lemDefault} lemmasAgg={lemAgg} lemmasWithDupArgs default={dupDefault} agg={dupAgg} truncated={truncN} subErrs={subErrs}"
  log h s!"SUMMARY2 candsTotal={cTotal} dupTriples={dupTriples} checked={cChecked} kernelFail={cKernelFail} exceptions={cException} notClosed={cNotClosed} withDupDeps={cDup} sizeMismatch={cSizeMismatch} hashMismatch={cHashMismatch} proofSizeMismatch={cProofMismatch} sumStmt={sumStmt} sumStmtDedup={sumStmtDedup} hashCollisions={collisions} distinctHashes={hashTab.size}"
