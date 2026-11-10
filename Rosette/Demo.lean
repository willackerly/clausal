/-
Rosette.Demo — the artifact a mathematician would look at.

For three long, monolithic Mathlib proofs this file
  1. lifts lemmas out of the proof term with `Rosette.liftConst`, *hierarchically*: after lifting
     `X.lifted_i` out of `X`, it lifts again inside each `X.lifted_i` (giving
     `X.lifted_i.lifted_j`), so the result is a small dependency tree, not a flat list;
  2. checks that every new declaration is a kernel-checked theorem, that `X.lifted` has
     syntactically the same statement as `X`, and that no axiom was added;
  3. writes `out/demo/generated/<X>.<config>.md`: the original signature, the tree (mermaid +
     nested list) of lifted statements printed with `ppSignature` (what `#check` shows), and the
     list of the `have` statements the human author wrote, with their rank under hidingRatio.

Everything in `out/demo/generated/` is produced by Lean. The assessments in `out/demo/*.md` are
hand-written prose around those generated blocks.

  lake build Rosette.Lift && lake env lean Rosette/Demo.lean      (about 1.5 minutes)
  python3 out/demo/assemble.py                                    (rebuilds out/demo/<X>.md)

Three configurations are run for each theorem (see `cfgDefault`, `cfgFiltered`, `cfgWide`):
  * `lifted`: `Rosette.Lift` exactly as shipped (score = hidingRatio, statement ≤ 150 nodes);
  * `filtered`: same, but typeclass-instance proofs, rewriting plumbing, tactic-internal
    lemmas and statements in tactic-internal vocabulary are never selected. This tests the
    first remedies proposed in `out/demo/README.md`;
  * `wide`: `filtered` with the statement bound relaxed to 500 nodes and picks limited to half
    of the parent proof.
-/
import Mathlib
import Rosette.Lift

open Lean Meta Rosette

namespace Rosette.Demo

/-- One lifted lemma in the recovered tree. -/
structure Node where
  name : Name
  /-- `ppSignature`, i.e. what `#check` prints. -/
  sig : String
  proofDag : Nat
  proofTree : Nat
  stmtSize : Nat
  ratio : Float
  numArgs : Nat
  /-- arguments that are proofs. -/
  numHyps : Nat
  /-- arguments that are typeclass instances. -/
  numInst : Nat
  role : String
  isClass : Bool
  uses : Nat
  /-- head constant of the lifted proof term. -/
  head : Option Name
  /-- DAG size of this lemma's closed proof (`fun deps => e`) before and after *its own*
  children were lifted out of it. (The closed proof is measured with bound variables, so
  `ownBefore` differs slightly from `proofDag`, which is measured in context.) -/
  ownBefore : Nat
  ownAfter : Nat
  children : Array Node

private def fmt2 (x : Float) : String :=
  let n := (x * 100).round.toUInt64.toNat
  s!"{n / 100}.{if n % 100 < 10 then "0" else ""}{n % 100}"

/-- (number of hypotheses, number of instance arguments) among the binders of a closed
statement. Unlike `forallTelescope` this also walks through `let` binders, so hypotheses that
come after a `let n := …;` in the statement are counted. -/
partial def countArgs (type : Expr) : MetaM (Nat × Nat) := do
  match type with
  | .forallE n d b bi =>
    withLocalDecl n bi d fun x => do
      let (nh, ni) ← countArgs (b.instantiate1 x)
      if ← isProp d then return (nh + 1, ni)
      else if (← isClass? d).isSome then return (nh, ni + 1)
      else return (nh, ni)
  | .letE n t v b nondep => withLetDecl n t v (nondep := nondep) fun x => countArgs (b.instantiate1 x)
  | .mdata _ b => countArgs b
  | _ => return (0, 0)

def sigOf (n : Name) : MetaM String := do
  return (← PrettyPrinter.ppSignature n).fmt.pretty 100

/-- Lift with `k = ks.head` at this level, then recurse into each lifted lemma with `ks.tail`. -/
partial def liftRec (n : Name) (cfg : LiftConfig) (ks : List Nat) :
    MetaM (LiftResult × Array Node) := do
  let k :: rest := ks | throwError "liftRec: empty level list"
  -- `Rosette.selectCandidates` has no score threshold. To let a config *exclude* candidates by
  -- giving them score ≤ 0, run the selection once to count how many picks have positive score
  -- (they are always selected first) and cap `k` at that count.
  let info ← getConstInfo n
  let proof ← proofOfConst n
  let enum ← candidatesOfExprCore proof cfg.enum
  let pre := selectCandidates enum (dagSize proof) (statementHash info.type) { cfg with k }
  let k := (pre.filter (cfg.score · > 0)).size
  let r ← liftConst n { cfg with k }
  let mut nodes := #[]
  for l in r.lemmas do
    let own := dagSize (← proofOfConst l.name)
    let (children, ownAfter) ←
      if rest.isEmpty then pure (#[], own) else do
        let (r', ch) ← liftRec l.name cfg rest
        pure (ch, r'.newProofSize)
    let (numHyps, numInst) ← countArgs (← getConstInfo l.name).type
    nodes := nodes.push {
      name := l.name, sig := ← sigOf l.name
      proofDag := l.cand.proofSizeDag, proofTree := l.cand.proofSizeTree
      stmtSize := l.cand.statementSize, ratio := l.cand.hidingRatio
      numArgs := l.numArgs, numHyps, numInst
      role := l.cand.role, isClass := l.cand.stmtIsClass, uses := l.uses
      head := l.cand.headConst, ownBefore := own, ownAfter, children }
  return (r, nodes)

partial def Node.all (n : Node) : Array Node :=
  n.children.foldl (fun acc c => acc ++ c.all) #[n]

/-- Kernel/axiom invariants for one lifted theorem and its whole tree. Throws on failure and
returns the axioms of `X.lifted`. -/
def verify (orig : Name) (main : Name) (nodes : Array Node) : MetaM (Array Name) := do
  let env ← getEnv
  let o ← getConstInfo orig
  let some (.thmInfo m) := env.find? main | throwError "{main} is missing or not a theorem"
  unless m.type == o.type do throwError "{main}: statement differs from {orig}"
  for nd in nodes.flatMap (·.all) do
    let some (.thmInfo _) := env.find? nd.name | throwError "{nd.name} is not a theorem"
  -- every top-level lemma is really called by the rewritten main proof
  let used := m.value.getUsedConstantsAsSet
  for nd in nodes do
    unless used.contains nd.name do throwError "{main} does not call {nd.name}"
  let ax0 ← collectAxioms orig
  let ax1 ← collectAxioms main
  for a in ax1 do
    unless ax0.contains a do throwError "{main} uses new axiom {a}"
  return ax1

private def short (root n : Name) : String :=
  (n.toString.drop (root.toString.length + 1)).toString

private def nodeStats (nd : Node) : String :=
  s!"hides {nd.proofDag} proof nodes (tree {nd.proofTree}) · statement {nd.stmtSize} nodes · \
    hidingRatio {fmt2 nd.ratio} · binders: {nd.numHyps} hypotheses, {nd.numInst} instances \
    ({nd.numArgs} supplied from the caller's context) · was `{nd.role}` in its parent proof, \
    head `{nd.head.getD `«(none)»}`\
    {if nd.isClass then " · statement is a typeclass" else ""}\
    {if nd.uses > 1 then s!" · REUSED at {nd.uses} call sites" else ""}\
    {if nd.children.isEmpty then "" else s!" · own proof {nd.ownBefore} → {nd.ownAfter} nodes after lifting its children"}"

private partial def nodeList (root : Name) (nd : Node) (ind : String) : String := Id.run do
  let body := ("\n" ++ ind ++ "  ").intercalate (nd.sig.splitOn "\n")
  let mut s := s!"{ind}- **`{short root nd.name}`** — {nodeStats nd}\n\n{ind}  ```lean\n{ind}  {body}\n{ind}  ```\n"
  for c in nd.children do
    s := s ++ nodeList root c (ind ++ "  ")
  return s

private def mmId (root n : Name) : String :=
  "L" ++ ((short root n).replace "." "_")

private partial def nodeMermaid (root : Name) (parentId : String) (nd : Node) : String := Id.run do
  let id := mmId root nd.name
  let mut s := s!"  {parentId} --> {id}[\"{short root nd.name}<br/>hides {nd.proofDag} · \
    {nd.numHyps} hyps · ratio {fmt2 nd.ratio}\"]\n"
  for c in nd.children do
    s := s ++ nodeMermaid root id c
  return s

/-- Run one configuration on one theorem and write `dir/<name>.<label>.md`. -/
def runOne (dir : System.FilePath) (n : Name) (label : String) (cfg : LiftConfig)
    (ks : List Nat) (withHaves : Bool) : MetaM Unit := do
  let cfg := { cfg with suffix := label }
  let (r, nodes) ← liftRec n cfg ks
  let axioms ← verify n r.main nodes
  let all := nodes.flatMap (·.all)
  let mut s := s!"<!-- GENERATED by Rosette/Demo.lean (config `{label}`); do not edit. -->\n\n"
  s := s ++ s!"### Original statement\n\n```lean\n{← sigOf n}\n```\n\n"
  s := s ++ s!"- proof term: **{r.origProofSize}** nodes as a DAG (shared subterms once), \
    **{treeSize (← proofOfConst n)}** as a tree\n"
  s := s ++ s!"- candidate boundaries enumerated (Prop-typed subterms of DAG size ≥ 20): \
    {r.enumeration.cands.size}, of which {(r.enumeration.cands.filter (·.stmtIsClass)).size} \
    are typeclass-instance proofs and {(r.enumeration.cands.filter (·.role == "haveValue")).size} \
    are values of a `have`{if r.enumeration.truncated then " (TRUNCATED)" else ""}\n"
  s := s ++ s!"- config `{label}`: levels k = {ks}, minProof {cfg.minProofSize}, \
    maxStmt {cfg.maxStatementSize}, maxFraction {cfg.maxFraction}\n"
  s := s ++ s!"- result: {all.size} lemmas in the tree ({nodes.size} called directly by the \
    main proof); main proof {r.origProofSize} → **{r.newProofSize}** nodes\n"
  s := s ++ s!"- kernel check: `{r.main}` and all {all.size} lemmas were added with `addDecl` \
    (synchronous kernel check) and are `theorem`s; `{r.main}` has the identical statement; \
    axioms of the lifted version: {axioms.toList} (no new axiom)\n\n"
  s := s ++ s!"### Recovered skeleton\n\n```mermaid\ngraph TD\n  \
    T[\"{n}<br/>{r.origProofSize} nodes, {r.newProofSize} left\"]\n"
  for nd in nodes do s := s ++ nodeMermaid r.main "T" nd
  s := s ++ "```\n\n"
  for nd in nodes do s := s ++ nodeList r.main nd ""
  if withHaves then
    -- the boundaries the human chose: values of `have` in the original proof term
    let e ← candidatesOfConstCore n { maxStmtChars := 700 }
    let sorted := sortByRatio e.cands
    let total := sorted.size
    s := s ++ s!"\n### The `have` boundaries in the original proof term\n\n\
      Every value of a `have` (non-dependent `let`) in the elaborated term with proof DAG size \
      ≥ 20, in source order (a value that occurs at several positions is listed once). \
      `rank` is the position among all {total} distinct candidates sorted by \
      hidingRatio (1 = best). The statement shown is the *closed* one: all hypotheses the \
      proof of the `have` actually uses are quantified.\n\n"
    for c in e.cands do
      if c.role != "haveValue" then continue
      let some rank := sorted.findIdx? (·.id == c.id) | continue
      s := s ++ s!"- rank {rank + 1}/{total} · ratio {fmt2 c.hidingRatio} · proof {c.proofSizeDag} · \
        statement {c.statementSize} · {c.numPropDeps} hyps{if c.stmtIsClass then " · typeclass" else ""}\
        {if c.occurrences > 1 then s!" · the same term was met at {c.occurrences} positions" else ""}\n\n  \
        ```lean\n  {c.statement}\n  ```\n"
  IO.FS.createDirAll dir
  IO.FS.writeFile (dir / s!"{n}.{label}.md") s
  logInfo m!"{n} [{label}]: {r.origProofSize} → {r.newProofSize} nodes, {all.size} lemmas \
    ({nodes.size} top-level), kernel-checked, axioms {axioms}"

/-- `default`: `Rosette.Lift` exactly as shipped. -/
def cfgDefault : LiftConfig := {}

/-- Heads of proof terms that are congruence/rewriting plumbing produced by `simp`, `rw`,
`congr`, `convert`: the term proves an equation between propositions or between normal forms,
never a step the author stated. -/
def plumbingHeads : List Name := [
  ``congrArg, ``congr, ``congrFun, ``Eq.trans, ``Eq.symm, ``eq_true, ``eq_false, ``propext,
  ``implies_congr, ``forall_congr, ``funext, ``eq_self, ``Eq.refl, ``HEq.refl, ``eq_of_heq,
  ``heq_of_eq, ``iff_of_eq, ``eq_true_intro, ``eq_false_intro, ``Eq.mpr_prop, ``id,
  ``congrFun', ``congr_arg₂, ``congrArg₂, ``rfl]

/-- Namespaces of tactic-internal lemmas (`ring`, `field_simp`, `norm_num`, `linarith`,
`omega`, `grind`, `positivity` certificates). -/
def tacticNamespaces : List Name :=
  [`Mathlib.Tactic, `Mathlib.Meta, `Lean, `Nat.Linear, `Int.Linear, `Linarith, `Std.Tactic]

/-- Notation that only appears in statements about tactic internals: `≍` (`HEq`, from the
congruence lemmas `convert`/`congr!` build inline), `ring`'s `rawCast` numerals and
`field_simp`'s normal-form lists. This is a crude *textual* stand-in for a proper vocabulary
check on the statement term ("mentions a constant from a tactic namespace, or `HEq`"), which
needs a field `Rosette.Candidate` does not have. -/
def internalMarkers : List String := ["≍", "rawCast", "::ᵣ", "NF.eval", "Mathlib.Tactic", "Mathlib.Meta"]

def isNoise (c : Candidate) : Bool :=
  c.stmtIsClass || c.role == "fn" ||
  internalMarkers.any (fun m => (c.statement.splitOn m).length > 1) ||
  match c.headConst with
  | some h => plumbingHeads.contains h || tacticNamespaces.any (·.isPrefixOf h) ||
      -- auto-generated simp lemmas `Foo._simp_1`
      (match h with | .str _ s => s.startsWith "_simp_" | _ => false)
  | none => false

/-- `filtered`: same bounds and same ranking as `default`, but never select a typeclass-instance
proof, a term in function position, a proof whose head is rewriting plumbing or a
tactic-internal lemma, or a statement written in tactic-internal vocabulary. -/
def cfgFiltered : LiftConfig := {
  enum := { ppStatements := true, maxStmtChars := 100000 }
  score := fun c => if isNoise c then 0 else c.hidingRatio }

/-- `wide`: `filtered`, with the statement bound relaxed from 150 to 500 nodes and each pick
limited to half of its parent proof, to see what the long `have` statements of an analysis proof
look like when they are allowed in. -/
def cfgWide : LiftConfig := {
  maxStatementSize := 500
  maxFraction := 0.5
  enum := { ppStatements := true, maxStmtChars := 100000 }
  score := fun c => if isNoise c then 0 else c.hidingRatio }

/-- The three demo theorems. They were chosen by hand, one each from analysis, number theory and
combinatorics, from a list of the longest single-declaration tactic proofs in the Mathlib source
(a line-count script); they are an illustration, not a sample. -/
def demoDecls : List Name := [
  -- analysis / PDE-adjacent: Gagliardo–Nirenberg–Sobolev inequality (119-line tactic proof)
  ``MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq_inner,
  -- number theory: existence of a nontrivial solution of Pell's equation (63 lines)
  ``Pell.exists_of_not_isSquare,
  -- combinatorics: Erdős–Ginzburg–Ziv over ℤ (69 lines)
  ``Int.erdos_ginzburg_ziv]

end Rosette.Demo

/-- All three configurations on one theorem. -/
def Rosette.Demo.runAll (n : Name) : MetaM Unit := do
  runOne "out/demo/generated" n "lifted" cfgDefault [6, 3] (withHaves := true)
  runOne "out/demo/generated" n "filtered" cfgFiltered [6, 3] (withHaves := false)
  runOne "out/demo/generated" n "wide" cfgWide [6, 3] (withHaves := false)

-- The default 200k-heartbeat budget of a command is too small for enumerating, pretty-printing
-- and re-checking these proofs several times over; each enumeration still has its own budget
-- (`Rosette.Config.maxHeartbeats`) and reports truncation.
set_option maxHeartbeats 0 in
open Rosette.Demo in
run_meta do
  for n in demoDecls do runAll n
