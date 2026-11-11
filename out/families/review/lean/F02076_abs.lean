import Abs
import NavierStokes.ActualBasePressureBounds
import NavierStokes.ActualBaseVelocityBounds
import NavierStokes.ActualCycleResidualBounds
import NavierStokes.ActualInitialExcluded
import NavierStokes.ActualPhysicalStageBounds
import NavierStokes.BaseResidual
import NavierStokes.ConstructedSlowBase
import NavierStokes.DiagonalResidual
import NavierStokes.FinalSlowBase
import NavierStokes.GenericDifferentialPolynomial
import NavierStokes.GenericJetRateAlgebra
import NavierStokes.GenericRealization
import NavierStokes.GenericRealizationBounds
import NavierStokes.GenericSummationRealization
import NavierStokes.GenericSupportLocalCoefficients
import NavierStokes.GenericSupportLocalSummation
import NavierStokes.GenericSupportedPolynomial
import NavierStokes.GenericTupleRealization
import NavierStokes.GenericTupleSupport
import NavierStokes.GenericVelocityRates
import NavierStokes.GlobalBaseError
import NavierStokes.InitializedPhysicalBackground
import NavierStokes.LocalResidualFlatness
import NavierStokes.LocalScaleApproach
import NavierStokes.MixedDiagonalResidual
import NavierStokes.MixedFiniteBackground
import NavierStokes.PhysicalResidualJetBounds
import NavierStokes.SimilarityApproach
import NavierStokes.WholeDomainBaseBounds
import NavierStokes.WholeDomainCompactBounds
import NavierStokes.WholeDomainHeatCompact
open Lean Elab Command
set_option maxHeartbeats 0
set_option Elab.async false
run_cmd do
  let ts := (← IO.FS.lines "/Users/will/dev/lean-rosette/corpora/families/build/F02076_abs.txt").toList.filter (· != "") |>.map String.toName
  Fam.Abs.go "F02076" [`NavierStokes.DiagonalResidual.FiniteJetRate, `NavierStokes.DiagonalResidual.JetRate] ts
