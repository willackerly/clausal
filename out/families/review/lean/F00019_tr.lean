import Abs
import F19
import NavierStokes.ActualCurrentParticularAssembly
import NavierStokes.ActualMeanPhysicalData
import NavierStokes.ActualPhysicalStageBounds
import NavierStokes.ActualPrimaryCovariance
import NavierStokes.ActualSignedMeanBinding
import NavierStokes.ActualSignedPhysicalData
import NavierStokes.AlignedProfileSpectralCone
import NavierStokes.BaseChartJets
import NavierStokes.BaseContextAssembly
import NavierStokes.BaseRadialJets
import NavierStokes.BaseResidual
import NavierStokes.CorrectionInitialization
import NavierStokes.CorrectionStep
import NavierStokes.HeatTailEdit
import NavierStokes.HeatedOutgoing
import NavierStokes.InitializedPhysicalBackground
import NavierStokes.NaturalCore
import NavierStokes.OutgoingEntranceCone
import NavierStokes.OutgoingHistories
import NavierStokes.ParametricHeatTail
import NavierStokes.PhysicalSignedWave
import NavierStokes.PhysicalStageBounds
import NavierStokes.PulseCone
import NavierStokes.RenormalizedHeatMoment
import NavierStokes.SlowBorelBase
import NavierStokes.SlowExpansionResidual
import NavierStokes.SlowResidualMatching
import NavierStokes.TerminalHistoryBridge
import NavierStokes.TerminalPressure
open Lean Elab Command
set_option maxHeartbeats 0
set_option Elab.async false
run_cmd do
  let ts := (← IO.FS.lines "/Users/will/dev/lean-rosette/corpora/families/build/F00019_tr.txt").toList.filter (· != "") |>.map String.toName
  Fam.Abs.transport "F00019" [(`NavierStokes.CoordinateAlgebra.A, `Fam.F19.halfPlus, none), (`NavierStokes.ExponentLedger.waveExponent, `Fam.F19.halfPlus, none), (`NavierStokes.HeatTailEdit.exponent, `Fam.F19.halfPlus, none), (`NavierStokes.NaturalAxisData.A, `Fam.F19.halfPlus, none), (`NavierStokes.RenormalizedHeatMoment.A, `Fam.F19.halfPlus, none), (`NavierStokes.StressAlgebra.velocityExponent, `Fam.F19.halfPlus, none), (`NavierStokes.TerminalPressure.amplitudeExponent, `Fam.F19.halfPlus, none)] ts
