import Euler.CompactCurlBounds
import Euler.ComparatorLocalCompactVorticity
import Euler.CylinderCompactTranslation
import Euler.DivCurlRecovery
import Euler.EulerFiniteLifespan
import Euler.EulerProof
import Euler.FiniteEnergyTruncation
import Euler.LocalFlowTrap
import Euler.LpCylinderTranslation
import Euler.LpSpatialCutoff
import Euler.LpSupportedTranslation
import Euler.MeanBoundaryDerivative
import Euler.PacketCommonScaleChoice
import Euler.PacketExactGlobalChoice
import Euler.PacketForwardInitializedChildShear
import Euler.PacketForwardInitializedCorrectionChoice
import Euler.PacketForwardInitializedCorrectionEstimates
import Euler.PacketForwardInitializedExactLifted
import Euler.PacketForwardInitializedFlowAndShear
import Euler.PacketForwardInitializedFlowBounds
import Euler.PacketGeometrySourceGrowth
import Euler.PacketInitializedChildBounds
import Euler.PacketInitializedCorrectionChoice
import Euler.PacketInitializedCorrectionEstimateChoice
import Euler.PacketInitializedExactLifted
import Euler.PacketInitializedFlowAndShear
import Euler.PacketInitializedHessianChoice
import Euler.PacketInitializedPhysicalChoice
import Euler.PacketInitializedPhysicalFieldsChoice
import Euler.PacketInitializedPointwiseChoice
import Euler.PacketSourceGeometryData
import Euler.PacketSourceScaleGuards
import Euler.ParentPacketChildChoice
import Euler.ParentPacketForwardChildChoice
import Euler.Solution
import Euler.UniformHeatLocal
import Euler.VolterraUniqueness
import Euler.WeakTimeContinuity
import NavierStokes.ActivationBounds
import NavierStokes.ActivationCone
import NavierStokes.ActivationContinuation
import NavierStokes.ActivationHolomorphic
import NavierStokes.ActivationStocks
import NavierStokes.ActiveAnnulusWeight
import NavierStokes.ActualBaseVelocityBounds
import NavierStokes.ActualCurrentParticularBounds
import NavierStokes.ActualCycleResidualBounds
import NavierStokes.ActualGaussianCoverage
import NavierStokes.ActualInitialExcluded
import NavierStokes.ActualParticularControl
import NavierStokes.ActualParticularPhysicalData
import NavierStokes.ActualPhaseJetBounds
import NavierStokes.ActualPhysicalPrefixFields
import NavierStokes.ActualPhysicalStageBounds
import NavierStokes.ActualSignedNativeRegularity
import NavierStokes.ActualSignedPhysicalData
import NavierStokes.ActualSignedPhysicalGeometry
import NavierStokes.ActualSignedWaveData
import NavierStokes.ActualSlowAxis
import NavierStokes.AllBandBaseJets
import NavierStokes.AngularMomentReset
import NavierStokes.AssembledSlowBase
import NavierStokes.AxisContraction
import NavierStokes.AxisHolomorphic
import NavierStokes.AxisHolomorphicJoint
import NavierStokes.AxisReference
import NavierStokes.BaseAngularGrowth
import NavierStokes.BaseChartJets
import NavierStokes.BaseExterior
import NavierStokes.BasePhaseGeometry
import NavierStokes.BaseResidual
import NavierStokes.BaseStressClasses
import NavierStokes.BorelExtension
import NavierStokes.CandidateConsequences
import NavierStokes.CandidateFromLimits
import NavierStokes.ClosedIntervalJetAlgebra
import NavierStokes.CompactForceDecay
import NavierStokes.CompactSpatialForceDecay
import NavierStokes.ConstructedSlowBase
import NavierStokes.CorrectedPressureBounds
import NavierStokes.CorrectedPulseAmplitude
import NavierStokes.CutStageEstimates
import NavierStokes.DependentSignedPhysicalFamily
import NavierStokes.DiagonalJetBounds
import NavierStokes.DiagonalJetBoundsNoOptions
import NavierStokes.EdgeWeightJets
import NavierStokes.ExtendedHeatDebts
import NavierStokes.ExtendedHeatedOutgoing
import NavierStokes.FinalSlowBase
import NavierStokes.FiveProfileMoments
import NavierStokes.FiveRowRank
import NavierStokes.FlatCovariance
import NavierStokes.FlatKernelBounds
import NavierStokes.FlatPrimitivePaper
import NavierStokes.FourierAlias
import NavierStokes.GaugeAliasDecay
import NavierStokes.GaussianEnvelope
import NavierStokes.GaussianTailFlat
import NavierStokes.GenericRealization
import NavierStokes.GenericSummationRealization
import NavierStokes.GenericSupportLocalSummation
import NavierStokes.GenericTupleRealization
import NavierStokes.GenericTupleSupport
import NavierStokes.GluedStageEstimates
import NavierStokes.HeatProfileExtension
import NavierStokes.HeatSwitchCone
import NavierStokes.HeatedOutgoing
import NavierStokes.InitialHarmonicContinuation
import NavierStokes.LabelCounting
import NavierStokes.LeadingStressWeights
import NavierStokes.LiftedMeanResidual
import NavierStokes.LinearWaveBounds
import NavierStokes.LocalAngularGrowth
import NavierStokes.LocalHeatFormula
import NavierStokes.LocalJetBounds
import NavierStokes.LocalMeanPhysicalBounds
import NavierStokes.LocalPaperHeat
import NavierStokes.LocalPhysicalCopyBounds
import NavierStokes.LocalRankDefect
import NavierStokes.LocalScaleApproach
import NavierStokes.LocalizedGaussianBounds
import NavierStokes.LocalizedMomentRepair
import NavierStokes.LoopVariance
import NavierStokes.MatchingConeBounds
import NavierStokes.MatchingDebtBounds
import NavierStokes.MaximalLifespan
import NavierStokes.MeanRankUpdate
import NavierStokes.ModulatedCone
import NavierStokes.ModulatedHistories
import NavierStokes.ModulatedProfileJetRates
import NavierStokes.ModulatedStockBounds
import NavierStokes.NaturalAxisBridge
import NavierStokes.NaturalAxisCoefficients
import NavierStokes.NaturalAxisData
import NavierStokes.NaturalAxisJointAnalytic
import NavierStokes.NaturalAxisRange
import NavierStokes.NaturalCore
import NavierStokes.NaturalEntrance
import NavierStokes.NaturalExitBounds
import NavierStokes.NaturalExitParameterJets
import NavierStokes.NaturalProfile
import NavierStokes.NominalConeAssembly
import NavierStokes.NominalProfile
import NavierStokes.OffplaneJetExtensions
import NavierStokes.OutgoingCone
import NavierStokes.OutgoingDilation
import NavierStokes.OutgoingEntranceCone
import NavierStokes.OutgoingNegativeSlopeCone
import NavierStokes.OutgoingProfile
import NavierStokes.OutgoingPulseBounds
import NavierStokes.ParametricFlatFactor
import NavierStokes.ParametricHeatTail
import NavierStokes.ParametricKernelBounds
import NavierStokes.ParametricModulation
import NavierStokes.ParametricTerminalCompensation
import NavierStokes.ParametricTorusInverse
import NavierStokes.PeriodicPaperTheorem
import NavierStokes.PeriodicUniqueness
import NavierStokes.PeriodizedWaveBounds
import NavierStokes.PhysicalClassBounds
import NavierStokes.PhysicalCoordinateBounds
import NavierStokes.PhysicalCopyBounds
import NavierStokes.PhysicalGraphBounds
import NavierStokes.PhysicalMeanDomain
import NavierStokes.PhysicalMeanJetBounds
import NavierStokes.PhysicalResidualJetBounds
import NavierStokes.PhysicalStageBounds
import NavierStokes.PhysicalStageSupport
import NavierStokes.PhysicalWaveSum
import NavierStokes.PositiveRepresentatives
import NavierStokes.PositiveTimeSignedData
import NavierStokes.PrimaryCopyBounds
import NavierStokes.PrimaryCovarianceBounds
import NavierStokes.PrimaryMaterialDefect
import NavierStokes.PrimaryODE
import NavierStokes.PrimaryRepresentatives
import NavierStokes.PrimaryTargetBounds
import NavierStokes.ProfileSpectralCone
import NavierStokes.PulseAmplitude
import NavierStokes.PulseCone
import NavierStokes.PulseCovariance
import NavierStokes.PulseLag
import NavierStokes.R3.CandidateBreakdown
import NavierStokes.R3.CompactComparisonBounds
import NavierStokes.R3.CompactForceBound
import NavierStokes.R3.ComparisonCutoffs
import NavierStokes.R3.ComparisonFiniteEnergy
import NavierStokes.R3.ComparisonGronwall
import NavierStokes.R3.ComparisonRateBound
import NavierStokes.R3.ComparisonTimeAverages
import NavierStokes.R3.ComparisonYoung
import NavierStokes.R3.LocalizedFluxEstimates
import NavierStokes.R3.PressureFlux
import NavierStokes.R3.PressureFunctionals
import NavierStokes.R3.PressureRecovery
import NavierStokes.R3.PressureTestBounds
import NavierStokes.R3.RadialKernelBounds
import NavierStokes.R3.RieszSymbolRegularity
import NavierStokes.R3AbsorbedBoundary
import NavierStokes.R3EnergyAbsorption
import NavierStokes.R3StressPressureEstimate
import NavierStokes.R3UniformBounds
import NavierStokes.RadialModulation
import NavierStokes.RadialPullback
import NavierStokes.RankStateBounds
import NavierStokes.ReferenceBounds
import NavierStokes.ReferenceEndpointRate
import NavierStokes.ReferenceJetBounds
import NavierStokes.ReferencePath
import NavierStokes.ReleaseMoments
import NavierStokes.RenormalizedHeatMoment
import NavierStokes.RepairConeBounds
import NavierStokes.ResetEnergyBounds
import NavierStokes.SchedulePressure
import NavierStokes.ScheduledProfileChoice
import NavierStokes.SeedConePaper
import NavierStokes.SeedHandbackJets
import NavierStokes.ShapeTransition
import NavierStokes.SharpCurrentModeJets
import NavierStokes.SharpCurrentParticularBounds
import NavierStokes.SharpGraphBounds
import NavierStokes.SharpLogWeights
import NavierStokes.SharpMeanJetBounds
import NavierStokes.SharpMeanStageBounds
import NavierStokes.SharpParticularGluing
import NavierStokes.SharpPhysicalCarrier
import NavierStokes.SharpPhysicalCopyBounds
import NavierStokes.SharpPhysicalLoss
import NavierStokes.SharpWaveStageBounds
import NavierStokes.SignedStressPrimitive
import NavierStokes.SimilarityCoordinates
import NavierStokes.SlotColoring
import NavierStokes.SlotGeometry
import NavierStokes.SlowBorelBase
import NavierStokes.SlowFirstOrderEdge
import NavierStokes.SlowResidualMatching
import NavierStokes.SlowStressSupport
import NavierStokes.SmoothCovariance
import NavierStokes.SmoothCutoffs
import NavierStokes.SmoothExponentialMomentMatrix
import NavierStokes.SmoothFamilyTorusInverse
import NavierStokes.SmoothMomentRepair
import NavierStokes.SmoothPowerMomentMatrix
import NavierStokes.SpatialBorelExtension
import NavierStokes.SquaredPartition
import NavierStokes.StressActivation
import NavierStokes.TailCone
import NavierStokes.TemporalMeanUpdate
import NavierStokes.TerminalCompensation
import NavierStokes.TerminalEdgeFactor
import NavierStokes.TerminalEdgePaper
import NavierStokes.TorusAverages
import NavierStokes.TransitionRamp
import NavierStokes.TransportPrimitive
import NavierStokes.TrueConeLoop
import NavierStokes.TrueConeLoopPaper
import NavierStokes.UniformAngularReset
import NavierStokes.UniformCone
import NavierStokes.UniformFourierAlias
import NavierStokes.VariableGaugeMean
import NavierStokes.VolterraRegularity
import NavierStokes.WaveEdgeExtension
import NavierStokes.WaveEnvelopeTransport
import NavierStokes.WeightedRadialPrimitive
import NavierStokes.WholeDomainActualStageBounds
import NavierStokes.WholeDomainBaseBounds
import NavierStokes.WholeDomainCompactBounds
import NavierStokes.WholeDomainHeatBounds
import NavierStokes.WholeDomainHeatCompact
import NavierStokes.WholeDomainPhysicalStageTheorem
import NavierStokes.WholeDomainStageBounds

/-
Constant-threading experiment: which of the corpus's `∃ C` theorems have the shape the relation covers.
Generated header above imports every module holding a census producer.  For each producer the conclusion
is opened (`∃`, `∧`, `∀`/`→`) and every atom that mentions a real `∃`-bound variable is classified.
-/
open Lean Meta Elab Command

namespace Lesssim.Shape

def occ (x : FVarId) (e : Expr) : Nat :=
  match e with
  | .fvar y => if x == y then 1 else 0
  | .app f a => occ x f + occ x a
  | .lam _ d b _ => occ x d + occ x b
  | .forallE _ d b _ => occ x d + occ x b
  | .letE _ t v b _ => occ x t + occ x v + occ x b
  | .proj _ _ b => occ x b
  | .mdata _ b => occ x b
  | _ => 0

partial def factors (e : Expr) : Array Expr :=
  let e := e.consumeMData
  if e.isAppOfArity ``HMul.hMul 6 then factors (e.getArg! 4) ++ factors (e.getArg! 5) else #[e]

structure Acc where
  realEx : Nat := 0
  natEx : Nat := 0
  otherEx : Nat := 0
  signed : Nat := 0
  atoms : Array String := #[]
  hypMentions : Nat := 0

def isReal (t : Expr) : Bool := t.consumeMData.isConstOf ``Real

/-- class of an atom that mentions the real ∃-variables `cs` -/
def classify (cs : Array FVarId) (a : Expr) : MetaM String := do
  let a := a.consumeMData
  let present := cs.filter fun c => occ c a > 0
  if present.size > 1 then return "multi"
  let c := present[0]!
  -- normalise ≥ / > to ≤ / <
  let rel? : Option (Expr × Expr × Expr) :=
    if a.isAppOfArity ``LE.le 4 || a.isAppOfArity ``LT.lt 4 then some (a.getArg! 0, a.getArg! 2, a.getArg! 3)
    else if a.isAppOfArity ``GE.ge 4 || a.isAppOfArity ``GT.gt 4 then some (a.getArg! 0, a.getArg! 3, a.getArg! 2)
    else none
  let some (ty, lhs, rhs) := rel? | return "other"
  if !isReal ty then return "nonreal"
  let rhs := rhs.consumeMData
  let lhs := lhs.consumeMData
  -- sign atom: literal on the left, the variable alone on the right
  if rhs.isFVarOf c && !lhs.hasFVar then return "sign"
  if occ c lhs > 0 then
    return (if occ c rhs > 0 then "both-sides" else "lower")
  if rhs.isFVarOf c then return "O1"
  let fs := factors rhs
  let withC := fs.filter fun f => occ c f > 0
  if withC.size == 1 && withC[0]!.isFVarOf c then
    return (if fs[0]!.isFVarOf c then "O" else "Oprod")
  return "upper-other"

partial def walk (cs : Array FVarId) (e : Expr) (acc : Acc) : MetaM Acc := do
  let e := e.consumeMData
  if e.isAppOfArity ``Exists 2 then
    let ty := e.getArg! 0
    let body := e.getArg! 1
    let .lam n _ b _ := body.consumeMData | return { acc with atoms := acc.atoms.push "other" }
    withLocalDeclD n ty fun x => do
      let acc := if isReal ty then { acc with realEx := acc.realEx + 1 }
        else if ty.consumeMData.isConstOf ``Nat then { acc with natEx := acc.natEx + 1 }
        else { acc with otherEx := acc.otherEx + 1 }
      walk (if isReal ty then cs.push x.fvarId! else cs) (b.instantiate1 x) acc
  else if e.isAppOfArity ``And 2 then
    walk cs (e.getArg! 1) (← walk cs (e.getArg! 0) acc)
  else if let .forallE n d b bi := e then
    let acc := if cs.any (fun c => occ c d > 0) then { acc with hypMentions := acc.hypMentions + 1 } else acc
    withLocalDecl n bi d fun x => walk cs (b.instantiate1 x) acc
  else if cs.any (fun c => occ c e > 0) then
    let k ← classify cs e
    return (if k == "sign" then { acc with signed := acc.signed + 1 } else { acc with atoms := acc.atoms.push k })
  else return acc

run_cmd do
  let names := (← IO.FS.lines "../../../out/corpus/lesssim/producers.txt").filter (· ≠ "")
  let env ← getEnv
  let mut out : Array String := #[]
  let mut missing := 0
  for s in names do
    -- names are printed with `toString`; private names need the stored Name, so search by string
    let n := s.toName
    let some ci := env.find? n | do missing := missing + 1; out := out.push (Json.mkObj [("name", s), ("missing", true)]).compress; continue
    let acc ← liftTermElabM <| forallTelescope ci.type fun _ body => walk #[] body {}
    out := out.push (Json.mkObj [("name", s), ("realEx", acc.realEx), ("natEx", acc.natEx), ("otherEx", acc.otherEx),
      ("signed", acc.signed), ("hypMentions", acc.hypMentions), ("atoms", toJson acc.atoms)]).compress
  IO.FS.writeFile "../../../out/corpus/lesssim/shape.jsonl" ("\n".intercalate out.toList ++ "\n")
  IO.println s!"SHAPE {names.size} missing {missing}"

end Lesssim.Shape
