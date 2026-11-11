import Abs
import F42
import Euler.FiniteEnergyTruncation
import Euler.MeanHarmonicInterior
import Euler.MeanScalarProductDerivatives
import Euler.MeanWeakCurl
import NavierStokes.ActivationHolomorphic
import NavierStokes.ActivationStocks
import NavierStokes.AxisSourceRegularity
import NavierStokes.BasePrefixIdentity
import NavierStokes.GlobalSlowProfiles
import NavierStokes.LeadingStress
import NavierStokes.MeanChartCompatibility
import NavierStokes.NaturalCoefficientBridge
import NavierStokes.ParametricTorusInverse
import NavierStokes.PositiveAxisSystem
import NavierStokes.PositiveOrderMoments
import NavierStokes.PressureStream
import NavierStokes.ProfileHistories
import NavierStokes.ReferenceBounds
import NavierStokes.ReferenceJetBounds
import NavierStokes.SimilarityProfile
import NavierStokes.SlowBorelBase
import NavierStokes.SlowExpansionResidual
import NavierStokes.SlowRecursion
import NavierStokes.SlowResidualMatching
import NavierStokes.SmoothFourierData
import NavierStokes.StateMomentBalances
open Lean Elab Command
set_option maxHeartbeats 0
set_option Elab.async false
run_cmd do
  let ts := (← IO.FS.lines "/Users/will/dev/lean-rosette/corpora/families/build/F00042_tr.txt").toList.filter (· != "") |>.map String.toName
  Fam.Abs.transportEqns "F00042" [(`EulerMeanVectorIdentities.vectorPartial, `Fam.F42.m01), (`EulerPacketGraphHessian.angularDerivative, `Fam.F42.m02), (`EulerSmoothSobolev.coordinateDerivative, `Fam.F42.m03), (`EulerVectorCalculus.partialDerivative, `Fam.F42.m04), (`NavierStokes.IntegratedMeanBalances.parameterPartial, `Fam.F42.m05), (`NavierStokes.ParametricTorusInverse.parameterPartial, `Fam.F42.m06), (`NavierStokes.PressureStream.graphDr, `Fam.F42.m07), (`NavierStokes.PressureStream.graphDz, `Fam.F42.m08), (`NavierStokes.ProfileHistories.parameterPartial, `Fam.F42.m09), (`NavierStokes.ProfileHistories.radialPartial, `Fam.F42.m10), (`NavierStokes.RadialAlias.directionalDeriv, `Fam.F42.m11), (`NavierStokes.RadialAlias.slowDeriv, `Fam.F42.m12), (`NavierStokes.SimilarityProfile.partialEta, `Fam.F42.m13), (`NavierStokes.SimilarityProfile.partialX, `Fam.F42.m14), (`NavierStokes.SmoothFamilyTorusInverse.directionalPartial, `Fam.F42.m15), (`NavierStokes.SmoothFourierData.partialX, `Fam.F42.m16), (`NavierStokes.StateMomentBalances.radialPartial, `Fam.F42.m17), (`NavierStokes.TemporalMeanUpdate.partialY, `Fam.F42.m18)] ts
