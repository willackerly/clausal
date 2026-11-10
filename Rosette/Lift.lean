/-
Rosette.Lift — turn selected candidate boundaries into real, kernel-checked lemmas.

`#rosette_lift Foo.bar (k := 5)` picks up to `k` non-overlapping proof subterms of `Foo.bar`
with the best score, adds each one to the environment as an auxiliary theorem
`Foo.bar.lifted_i : ∀ deps, type` (value: the subterm abstracted over its interface), rebuilds
the main proof so that it *calls* those lemmas, and adds it as `Foo.bar.lifted` with the original
statement. Every declaration goes through `addDecl`, i.e. through the kernel, synchronously.
No text is spliced anywhere: this is extraction on proof terms.
-/
import Rosette.Candidates

open Lean Meta Elab Command

namespace Rosette

structure LiftConfig where
  /-- maximum number of lemmas to lift. -/
  k : Nat := 5
  /-- a lifted proof must have at least this DAG size. -/
  minProofSize : Nat := 40
  /-- a lifted statement must have at most this DAG size. -/
  maxStatementSize : Nat := 150
  /-- a lifted proof may contain at most this fraction of the whole proof (otherwise the top
  pick is always "the theorem itself minus its first step"). -/
  maxFraction : Float := 0.8
  /-- ranking; higher is better. -/
  score : Candidate → Float := (·.hidingRatio)
  /-- suffix of the new declarations: `Foo.bar.<suffix>` and `Foo.bar.<suffix>_i`. -/
  suffix : String := "lifted"
  enum : Config := { ppStatements := false }
  /-- after lifting, check that the new main theorem depends on no axiom the original did not
  (in particular not on `sorryAx`). -/
  checkAxioms : Bool := true

structure LiftedLemma where
  name : Name
  /-- closed statement, pretty-printed. -/
  statement : String
  cand : Candidate
  /-- number of lemma arguments at the call site. -/
  numArgs : Nat
  /-- number of selected subterms this one lemma replaced. Since proofs are irrelevant, two
  selected subterms with the same closed statement share a single lemma. -/
  uses : Nat := 1

structure LiftResult where
  orig : Name
  main : Name
  statement : String
  /-- DAG size of the original proof and of the rewritten main proof. -/
  origProofSize : Nat
  newProofSize : Nat
  lemmas : Array LiftedLemma
  enumeration : Result
  /-- the candidate enumeration hit a budget: the lemmas were selected from a partial list. The
  lift itself is still kernel-checked. -/
  truncated : Bool := false

/-- Greedy selection: best score first, skipping anything that overlaps (is nested in or
contains) an earlier pick, restates the theorem itself, or violates the size bounds. -/
def selectCandidates (r : Result) (rootProofSize : Nat) (rootStmtHash : UInt64)
    (cfg : LiftConfig) : Array Candidate := Id.run do
  let sorted := r.cands.qsort fun a b => cfg.score a > cfg.score b
  let mut chosen : Array Candidate := #[]
  for c in sorted do
    if chosen.size ≥ cfg.k then break
    if c.path.isEmpty then continue
    if c.proofSizeDag < cfg.minProofSize then continue
    if c.statementSize > cfg.maxStatementSize then continue
    if c.proofSizeDag.toFloat > cfg.maxFraction * rootProofSize.toFloat then continue
    if c.stmtHash == rootStmtHash then continue
    if chosen.any fun d => pathIsPrefix d.path c.path || pathIsPrefix c.path d.path then continue
    chosen := chosen.push c
  return chosen

/-- Add a theorem and have the kernel check it *now* (not in a background task), so that a
kernel rejection is an exception right here. -/
def addTheoremChecked (name : Name) (levelParams : List Name) (type value : Expr) : MetaM Unit := do
  if (← getEnv).contains name then
    throwError "rosette: '{name}' already exists"
  -- synchronous, and with the kernel type checker on whatever the ambient options say
  withOptions (fun o => debug.skipKernelTC.set (Elab.async.set o false) false) do
    addDecl <| .thmDecl { name, levelParams, type, value }
  -- `addDecl` falls back to an axiom when the kernel rejects a theorem (and throws); make sure
  -- what we ended up with really is a theorem.
  match (← getEnv).find? name with
  | some (.thmInfo _) => pure ()
  | _ => throwError "rosette: '{name}' was not added as a theorem"

/-- Lift up to `cfg.k` lemmas out of the proof of `n`. All new declarations are kernel-checked;
on any failure the environment is restored and the error rethrown. -/
def liftConst (n : Name) (cfg : LiftConfig := {}) : MetaM LiftResult := do
  let info ← getConstInfo n
  let proof ← proofOfConst n
  unless ← isProp info.type do
    throwError "rosette: '{n}' is not a theorem (its type is not a proposition)"
  let enumeration ← candidatesOfExprCore proof cfg.enum
  let rootSize := dagSize proof
  let chosen := selectCandidates enumeration rootSize (statementHash info.type) cfg
  let mainName := n ++ Name.mkSimple cfg.suffix
  let lemmasRef ← IO.mkRef (#[] : Array LiftedLemma)
  -- closed statement ↦ (lemma, its universe parameters), for reuse within this declaration
  let addedRef ← IO.mkRef (#[] : Array (Expr × Name × List Name))
  let onTarget (path : Path) (e : Expr) : MetaM Expr := do
    let some idx := chosen.findIdx? (·.path == path) | throwError "rosette: unexpected target"
    let cand := chosen[idx]!
    let ty := (← inferType e).headBeta
    let ifc ← interfaceOf e ty
    let (stmt, val) ← closeOver ifc e ty
    -- same closed statement as an earlier pick (up to bound-variable names): call that lemma
    if let some (_, name, lps) := (← addedRef.get).find? (·.1 == stmt) then
      lemmasRef.modify fun ls => ls.map fun l => if l.name == name then { l with uses := l.uses + 1 } else l
      return mkAppN (mkConst name (lps.map mkLevelParam)) ifc.args
    let used := (collectLevelParams (collectLevelParams {} stmt) val).params
    let lps := info.levelParams.filter used.contains
    let name := n ++ Name.mkSimple s!"{cfg.suffix}_{idx + 1}"
    addTheoremChecked name lps stmt val
    addedRef.modify (·.push (stmt, name, lps))
    let statement := (← ppExpr stmt).pretty
    lemmasRef.modify (·.push { name, statement, cand, numArgs := ifc.args.size })
    return mkAppN (mkConst name (lps.map mkLevelParam)) ifc.args
  let env ← getEnv
  try
    let hook : LiftHook := { targets := chosen.map (·.path), onTarget }
    let state ← IO.mkRef ({} : State)
    let newProof ← ((visit proof #[] none "root" 0).run { cfg := cfg.enum, lift? := some hook }) state
    let lemmas := (← lemmasRef.get).qsort fun a b => a.name.toString < b.name.toString
    let sites := lemmas.foldl (· + ·.uses) 0
    unless sites == chosen.size do
      throwError "rosette: internal error, {chosen.size} targets selected but {sites} reached"
    let usedConsts := newProof.getUsedConstantsAsSet
    for l in lemmas do
      unless usedConsts.contains l.name do
        throwError "rosette: internal error, rewritten proof does not call {l.name}"
    addTheoremChecked mainName info.levelParams info.type newProof
    if cfg.checkAxioms then
      let ax0 ← collectAxioms n
      for a in ← collectAxioms mainName do
        unless ax0.contains a do
          throwError "rosette: '{mainName}' depends on axiom '{a}', which '{n}' does not"
    return {
      truncated := enumeration.truncated
      orig := n, main := mainName, statement := (← ppExpr info.type).pretty
      origProofSize := rootSize, newProofSize := dagSize newProof, lemmas, enumeration }
  catch ex =>
    setEnv env
    throw ex

private def fmt2 (x : Float) : String :=
  let n := (x * 100).round.toUInt64.toNat
  s!"{n / 100}.{if n % 100 < 10 then "0" else ""}{n % 100}"

private def indent (s : String) (pre : String) : String :=
  ("\n" ++ pre).intercalate (s.splitOn "\n")

/-- Readable skeleton: main statement, then each lifted lemma's statement with its sizes. -/
def LiftResult.skeleton (r : LiftResult) : String := Id.run do
  let e := r.enumeration
  let mut s := s!"theorem {r.main} :\n    {indent r.statement "    "}\n  \
    -- kernel-checked. proof: {r.origProofSize} nodes originally, {r.newProofSize} after lifting \
    {r.lemmas.size} lemma(s); chosen among {e.cands.size} distinct candidates\
    {if e.truncated then s!" (enumeration TRUNCATED: {e.note})" else ""}"
  for l in r.lemmas do
    let c := l.cand
    s := s ++ s!"\n\nlemma {l.name} :\n    {indent l.statement "    "}\n  \
      -- kernel-checked. hides proof of {c.proofSizeDag} nodes (tree {c.proofSizeTree}) behind a \
      statement of {c.statementSize} nodes: hidingRatio {fmt2 c.hidingRatio}; \
      {l.numArgs} argument(s), {c.numPropDeps} of them hypotheses; was {c.role} at \
      {pathToString c.path}\
      {if l.uses > 1 then s!"; REUSED at {l.uses} call sites" else ""}"
  if r.lemmas.isEmpty then
    s := s ++ "\n\n(no candidate satisfied the size bounds: nothing lifted, proof re-checked as is)"
  return s

syntax rosetteLiftOpt := " (" ident " := " num ")"

/-- `#rosette_lift Foo.bar (k := 5) (minProof := 40) (maxStmt := 150) (maxPct := 80)`:
lift up to `k` lemmas out of the proof of `Foo.bar`, adding kernel-checked theorems
`Foo.bar.lifted_i` and `Foo.bar.lifted`, and print the resulting skeleton. -/
elab "#rosette_lift " id:ident opts:rosetteLiftOpt* : command => do
  let name ← liftCoreM <| realizeGlobalConstNoOverloadWithInfo id
  let mut cfg : LiftConfig := {}
  for o in opts do
    match o with
    | `(rosetteLiftOpt| ($key:ident := $v:num)) =>
      let v := v.getNat
      match key.getId with
      | `k => cfg := { cfg with k := v }
      | `minProof => cfg := { cfg with minProofSize := v }
      | `maxStmt => cfg := { cfg with maxStatementSize := v }
      | `maxPct => cfg := { cfg with maxFraction := v.toFloat / 100 }
      | _ => throwErrorAt key "unknown option, expected one of: k, minProof, maxStmt, maxPct"
    | _ => throwUnsupportedSyntax
  let r ← liftTermElabM <| liftConst name cfg
  logInfo r.skeleton

end Rosette
