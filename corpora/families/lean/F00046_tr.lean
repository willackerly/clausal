import Abs
import F46
import NavierStokes.ActualStageEstimates
import NavierStokes.ActualWaveRegularityData
import NavierStokes.BaseContextAssembly
import NavierStokes.BaseStressClasses
import NavierStokes.CorrectionInitialization
import NavierStokes.CorrectionStep
import NavierStokes.CurlClassBounds
import NavierStokes.CurrentSignedCurl
import NavierStokes.DefectIncrementBounds
import NavierStokes.GaugeAliasDecay
import NavierStokes.GaugeDebtIncrement
import NavierStokes.HarmonicCovariance
import NavierStokes.HarmonicWaveInteraction
import NavierStokes.LocalSignedRequest
import NavierStokes.MeanIncrementBounds
import NavierStokes.MeanMomentBounds
import NavierStokes.MovingMomentBounds
import NavierStokes.ParticularWaveAssembly
import NavierStokes.PhysicalMeanDomain
import NavierStokes.PrimaryMaterialDefect
import NavierStokes.SignedStressPrimitive
import NavierStokes.TemporalMeanUpdate
import NavierStokes.VariableGaugeMean
import NavierStokes.WaveInteractionBounds
import NavierStokes.WeightedClasses
open Lean Elab Command
set_option maxHeartbeats 0
set_option Elab.async false
run_cmd do
  let ts := (← IO.FS.lines "/Users/will/dev/lean-rosette/corpora/families/build/F00046_tr.txt").toList.filter (· != "") |>.map String.toName
  Fam.Abs.transportEqns "F00046" [(`NavierStokes.WeightedClasses.MeanClass, `Fam.F46.m1), (`NavierStokes.WeightedClasses.UnweightedClass, `Fam.F46.m2), (`NavierStokes.WeightedClasses.WaveClass, `Fam.F46.m3), (`NavierStokes.CurrentSignedCurl.AmplitudeBound, `Fam.F46.m4)] ts
