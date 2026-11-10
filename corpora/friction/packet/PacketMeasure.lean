/-
Packet experiment: measurement.  Prints one JSON line per declaration (Expr level, same size
measures as the corpus exports: tree node count; number of distinct subterms under structural
equality) and the axioms each new theorem depends on.
-/
import PacketWrap
import PacketDirect
import PacketApi

open Lean Meta Elab Command

namespace FrictionPacket.Measure

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

def countConst (e : Expr) (p : Name → Bool) : Nat :=
  (e.foldConsts (init := (0 : Nat)) fun n acc => if p n then acc + 1 else acc)

/-- occurrences (in the unshared tree) of constants satisfying `p` -/
partial def occ (p : Name → Bool) (e : Expr) : StateM (Std.HashMap ExprStructEq Nat) Nat := do
  if let some r := (← get)[(⟨e⟩ : ExprStructEq)]? then return r
  let r ← match e with
    | .const n _ => pure (if p n then 1 else 0)
    | .app f a => do pure ((← occ p f) + (← occ p a))
    | .lam _ d b _ => do pure ((← occ p d) + (← occ p b))
    | .forallE _ d b _ => do pure ((← occ p d) + (← occ p b))
    | .letE _ t v b _ => do pure ((← occ p t) + (← occ p v) + (← occ p b))
    | .proj _ _ b => occ p b
    | .mdata _ b => occ p b
    | _ => pure 0
  modify (·.insert ⟨e⟩ r)
  return r

partial def stripLams : Expr → Expr
  | .lam _ _ b _ => stripLams b
  | .mdata _ b => stripLams b
  | e => e

def measure (group : String) (n : Name) : CommandElabM Json := do
  let env ← getEnv
  let some ci := env.find? n | throwError "missing {n}"
  let (st, sd) := sizes ci.type
  let (nb, nh, nexp, nterm) ← liftTermElabM <| forallTelescope ci.type fun xs _ => do
    let mut nh : Nat := 0; let mut nexp : Nat := 0; let mut nterm : Nat := 0
    for x in xs do
      let d ← x.fvarId!.getDecl
      let isP ← isProp d.type
      if isP && !d.binderInfo.isInstImplicit then nh := nh + 1
      if d.binderInfo == .default then nexp := nexp + 1
      if !isP && !d.binderInfo.isInstImplicit then nterm := nterm + 1
    return (xs.size, nh, nexp, nterm)
  let isProjOfFrame (c : Name) : Bool := c.getPrefix == ``FrictionPacket.Frame && (c.getString! == "hT" || c.getString! == "hc" || c.getString! == "hQ" || c.getString! == "hd")
  let projOcc := ((occ isProjOfFrame ci.type).run {}).1
  let mut fields : List (String × Json) := [("group", group), ("name", toJson n.toString), ("statementTree", toJson st),
    ("statementDag", toJson sd), ("binders", toJson nb), ("hyps", toJson nh), ("explicit", toJson nexp), ("dataBinders", toJson nterm),
    ("frameProjOccInStatement", toJson projOcc)]
  if let some v := ci.value? (allowOpaque := true) then
    let (vt, vd) := sizes v
    -- own auxiliaries (names extending the declaration's name)
    let auxs := v.getUsedConstants.filter fun c => n.isPrefixOf c && c != n
    let mut auxDag : Nat := 0
    for a in auxs do
      if let some ai := env.find? a then
        if let some av := ai.value? (allowOpaque := true) then auxDag := auxDag + (sizes av).2
    fields := fields ++ [("valueDag", toJson vd), ("valueTreeLog2", toJson (Nat.log2 vt)), ("aux", toJson auxs.size),
      ("auxDag", toJson auxDag), ("distinctConsts", toJson v.getUsedConstants.size),
      ("frameProjOccInValue", toJson ((occ isProjOfFrame v).run {}).1),
      ("bodyDag", toJson (sizes (stripLams v)).2),
      ("usesOriginalCluster", toJson (v.getUsedConstants.filter fun c => c.getPrefix == `EulerFixedEndpointStrong).size),
      ("usesWrap", toJson (v.getUsedConstants.filter fun c => c.getPrefix == `FrictionPacket.Wrap).size),
      ("usesDirect", toJson (v.getUsedConstants.filter fun c => c.getPrefix == `FrictionPacket.Direct).size)]
  if group != "orig" then
    let ax ← liftCoreM <| collectAxioms n
    fields := fields ++ [("axioms", toJson (ax.map (·.toString)))]
    if ax.contains ``sorryAx then throwError "sorry in {n}"
  return Json.mkObj fields

def cluster : List String := ["fixedEndpointDerivative_weak", "coordinateSlope_range", "coordinateSlope_ae",
  "coordinate_equation", "coordinateSlope_h1", "continuousCoordinateVelocity_eq", "historyVelocity_eq",
  "continuousCoordinateVelocity_hasDerivWithinAt_generator", "continuousCoordinateVelocity_eq_forward"]

def glue : List String := ["initialTrace", "primitiveTimeLp", "momentum", "initialMomentumForcing", "affineTrial",
  "fixedEndpointDerivative", "coordinateSlope", "coordinateAcceleration", "continuousCoordinateVelocity",
  "historyVelocity", "coordinateVelocityPath", "initialCoordinates", "generator", "extendPathU", "Evolution",
  "coordinates", "zero"]

run_cmd do
  for s in cluster do
    for (g, pre) in [("orig", `EulerFixedEndpointStrong), ("wrap", `FrictionPacket.Wrap), ("back", `FrictionPacket.Back),
                     ("direct", `FrictionPacket.Direct), ("api", `FrictionPacket.Api)] do
      IO.println ("MEASURE " ++ (← measure g (pre ++ Name.mkSimple s)).compress)
  -- the converse theorems state EXACTLY the original statements (structural equality of the types)
  for s in cluster do
    let env ← getEnv
    let some o := env.find? (`EulerFixedEndpointStrong ++ Name.mkSimple s) | throwError "missing"
    let some b := env.find? (`FrictionPacket.Back ++ Name.mkSimple s) | throwError "missing"
    let same := o.type == b.type.instantiateLevelParams b.levelParams (o.levelParams.map Level.param)
    IO.println ("MEASURE " ++ (Json.mkObj [("group", "backcheck"), ("name", s), ("sameStatement", toJson same),
      ("levelParams", toJson (o.levelParams.length == b.levelParams.length))]).compress)
  for s in glue do
    IO.println ("MEASURE " ++ (← measure "glue" (`FrictionPacket.Frame ++ Name.mkSimple s)).compress)
  for s in ["hT", "hc", "hQ", "hd", "mk"] do
    IO.println ("MEASURE " ++ (← measure "struct" (`FrictionPacket.Frame ++ Name.mkSimple s)).compress)
  IO.println ("MEASURE " ++ (← measure "struct" `FrictionPacket.Frame).compress)

end FrictionPacket.Measure
