/-
Constant-threading experiment: measurement.  One JSON line per declaration, Expr level, with the same size
measures as the corpus exports (tree node count; number of distinct subterms under structural equality),
plus the axioms of every new declaration and a structural check that `Back.X` states exactly the original.
-/
import Equiv

open Lean Meta Elab Command

namespace Lesssim.Measure

partial def treeSize (e : Expr) : StateM (Std.HashMap ExprStructEq Nat) Nat := do
  match e with
  | .mdata _ b => treeSize b
  | _ =>
    if let some r := (← get)[(⟨e⟩ : ExprStructEq)]? then return r
    let r ← match e with
      | .app f a => do pure ((← treeSize f) + (← treeSize a) + 1)
      | .lam _ d b _ => do pure ((← treeSize d) + (← treeSize b) + 1)
      | .forallE _ d b _ => do pure ((← treeSize d) + (← treeSize b) + 1)
      | .letE _ t v b _ => do pure ((← treeSize t) + (← treeSize v) + (← treeSize b) + 1)
      | .proj _ _ b => do pure ((← treeSize b) + 1)
      | _ => pure 1
    modify (·.insert ⟨e⟩ r)
    return r

/-- (tree size, number of distinct subterms) -/
def sizes (e : Expr) : Nat × Nat :=
  let (r, m) := (treeSize e).run {}
  (r, m.size)

partial def stripLams : Expr → Expr
  | .lam _ _ b _ => stripLams b
  | .mdata _ b => stripLams b
  | e => e

/-- binders a reader meets in the conclusion: `∀`, `∃`, `fun` (unshared count) -/
partial def quantCount (e : Expr) : Nat × Nat × Nat :=
  let add (a b : Nat × Nat × Nat) := (a.1 + b.1, a.2.1 + b.2.1, a.2.2 + b.2.2)
  match e with
  | .mdata _ b => quantCount b
  | .app f a =>
    let r := add (quantCount f) (quantCount a)
    if e.isAppOfArity ``Exists 2 then add r (0, 1, 0) else r
  | .lam _ d b _ =>
    -- the lambda directly under `Exists` is the ∃ binder itself, not a function a reader sees
    add (add (quantCount d) (quantCount b)) (0, 0, 1)
  | .forallE _ d b _ => add (add (quantCount d) (quantCount b)) (1, 0, 0)
  | .letE _ t v b _ => add (add (quantCount t) (quantCount v)) (quantCount b)
  | .proj _ _ b => quantCount b
  | _ => (0, 0, 0)

def auxOf (env : Environment) (n : Name) (e : Expr) : Array Name :=
  e.getUsedConstants.filter fun c => n.isPrefixOf c && c != n && (env.find? c).isSome

def measure (group : String) (n : Name) : CommandElabM Json := do
  let env ← getEnv
  let some ci := env.find? n | throwError "missing {n}"
  let (st, sd) := sizes ci.type
  let (nb, nh, nexp, ct, cd, q) ← liftTermElabM <| forallTelescope ci.type fun xs body => do
    let mut nh : Nat := 0; let mut nexp : Nat := 0
    for x in xs do
      let d ← x.fvarId!.getDecl
      let isP ← isProp d.type
      if isP && !d.binderInfo.isInstImplicit then nh := nh + 1
      if d.binderInfo == .default then nexp := nexp + 1
    let (ct, cd) := sizes body
    return (xs.size, nh, nexp, ct, cd, quantCount body)
  -- matchers and other auxiliaries of the statement
  let tAux := auxOf env n ci.type
  let mut tAuxDag : Nat := 0
  for a in tAux do
    if let some ai := env.find? a then
      tAuxDag := tAuxDag + (sizes ai.type).2
      if let some av := ai.value? (allowOpaque := true) then tAuxDag := tAuxDag + (sizes av).2
  let mut fields : List (String × Json) := [("group", group), ("name", toJson n.toString), ("statementTree", toJson st),
    ("statementDag", toJson sd), ("binders", toJson nb), ("hyps", toJson nh), ("explicit", toJson nexp),
    ("conclTree", toJson ct), ("conclDag", toJson cd), ("conclForall", toJson q.1),
    ("conclExists", toJson q.2.1), ("conclLam", toJson (q.2.2 - q.2.1)),
    ("statementAux", toJson tAux.size), ("statementAuxDag", toJson tAuxDag)]
  if let some v := ci.value? (allowOpaque := true) then
    let (vt, vd) := sizes v
    let auxs := (auxOf env n v).filter fun c => !tAux.contains c
    let mut auxDag : Nat := 0
    for a in auxs do
      if let some ai := env.find? a then
        if let some av := ai.value? (allowOpaque := true) then auxDag := auxDag + (sizes av).2
    let uses (p : Name) := (v.getUsedConstants.filter fun c => p.isPrefixOf c).size
    fields := fields ++ [("valueDag", toJson vd), ("valueTreeLog2", toJson (Nat.log2 vt)), ("aux", toJson auxs.size),
      ("auxDag", toJson auxDag), ("distinctConsts", toJson v.getUsedConstants.size),
      ("bodyDag", toJson (sizes (stripLams v)).2),
      ("usesLib", toJson ((v.getUsedConstants.filter fun c => c.getPrefix == `Lesssim).size)),
      ("usesNative", toJson (uses `Lesssim.Native)),
      ("usesAsymptotics", toJson (uses `Asymptotics)),
      ("libConsts", toJson ((v.getUsedConstants.filter fun c => c.getPrefix == `Lesssim).map (·.toString))),
      ("asymptoticsConsts", toJson ((v.getUsedConstants.filter fun c => (`Asymptotics).isPrefixOf c).map (·.toString)))]
  if group != "orig" then
    let ax ← liftCoreM <| collectAxioms n
    fields := fields ++ [("axioms", toJson (ax.map (·.toString)))]
    if ax.contains ``sorryAx then throwError "sorry in {n}"
  return Json.mkObj fields

def family : List (Name × Name) := [
  (`NavierStokes.WeightedRadialPrimitive.weight_uniform_bound, `weight_uniform_bound),
  (`NavierStokes.PhysicalClassBounds.flat_edge_uniform, `flat_edge_uniform),
  (`NavierStokes.PhysicalClassBounds.FlatGeometry.uniform, `FlatGeometry.uniform),
  (`NavierStokes.PhysicalClassBounds.UniformClass.edge_absorbed, `UniformClass.edge_absorbed),
  (`NavierStokes.LocalPhysicalCopyBounds.LocalSourceBounds.chart_bound, `LocalSourceBounds.chart_bound),
  (`NavierStokes.LocalPhysicalCopyBounds.commonChart_amplitude_bound, `commonChart_amplitude_bound),
  (`NavierStokes.LocalPhysicalCopyBounds.localStrippedClass_of_weighted, `localStrippedClass_of_weighted),
  (`NavierStokes.LocalPhysicalCopyBounds.physical_sum_jet_bound_of_weighted, `physical_sum_jet_bound_of_weighted),
  (`NavierStokes.LocalPhysicalCopyBounds.physical_vector_sum_jet_bound_of_weighted, `physical_vector_sum_jet_bound_of_weighted),
  (`NavierStokes.PhysicalStageBounds.WaveData.vector_bound, `WaveData.vector_bound),
  (`NavierStokes.PhysicalStageBounds.WaveData.vector_bound_with_gain, `WaveData.vector_bound_with_gain),
  (`NavierStokes.ActualPhysicalStageBounds.potentialIncrement_bound, `potentialIncrement_bound),
  (`NavierStokes.ActualPhysicalStageBounds.CycleInputs.potential_bound, `CycleInputs.potential_bound)]

def lib : List Name := [`isBigO_of_bound_on, `exists_bound_on, `isBigO_on_iff, `mono_set, `congr_on, `congr_left_on,
  `congr_right_on, `comp_mapsTo, `isBigO_of_le_on, `exists_bound_on_finset, `exists_bound_on_le, `isBigO_rpow_of_le,
  `jet_add, `jet_comp, `uniformClass_isBigO]

def shapes : List Name := [`back1, `fwd1, `back3, `fwd3]

run_cmd do
  let env ← getEnv
  for (o, s) in family do
    IO.println ("MEASURE " ++ (← measure "orig" o).compress)
    IO.println ("MEASURE " ++ (← measure "native" (`Lesssim.Native ++ s)).compress)
    IO.println ("MEASURE " ++ (← measure "back" (`Lesssim.Back ++ s)).compress)
    if (env.find? (`Lesssim.Fwd ++ s)).isSome then
      IO.println ("MEASURE " ++ (← measure "fwd" (`Lesssim.Fwd ++ s)).compress)
    -- Back.X states EXACTLY the original; Fwd.X states exactly the native statement
    let some oc := env.find? o | throwError "missing"
    let some bc := env.find? (`Lesssim.Back ++ s) | throwError "missing"
    let same := oc.type == bc.type.instantiateLevelParams bc.levelParams (oc.levelParams.map Level.param)
    let mut fsame : Json := Json.null
    if let some fc := env.find? (`Lesssim.Fwd ++ s) then
      let some nc := env.find? (`Lesssim.Native ++ s) | throwError "missing"
      fsame := toJson (nc.type == fc.type.instantiateLevelParams fc.levelParams (nc.levelParams.map Level.param))
    let usesOrig (n : Name) : Bool := match env.find? n with
      | some ci => (ci.value? (allowOpaque := true)).any fun v => (family.any fun (o', _) => v.getUsedConstants.contains o')
      | none => false
    IO.println ("MEASURE " ++ (Json.mkObj [("group", "check"), ("name", toJson s.toString), ("backSameStatement", toJson same),
      ("fwdSameStatement", fsame), ("nativeUsesOriginalFamily", toJson (usesOrig (`Lesssim.Native ++ s))),
      ("backUsesOriginalFamily", toJson (usesOrig (`Lesssim.Back ++ s)))]).compress)
  for l in lib do
    IO.println ("MEASURE " ++ (← measure "lib" (`Lesssim ++ l)).compress)
  for l in shapes do
    IO.println ("MEASURE " ++ (← measure "shape" (`Lesssim ++ l)).compress)

end Lesssim.Measure
