import Abs
import F73
import Euler.CylinderSpatialMean
import Euler.LpSmoothFieldJets
import Euler.LpTranslation
import Euler.MeanBoundaryDifference
import Euler.MeanBoundaryTranslation
import Euler.MeanClassicalWordBounds
import Euler.MeanForcingTranslation
import Euler.MeanOperatorTranslation
import Euler.MeanPathSpatialRepresentative
import Euler.MeanSolenoidalTranslation
import Euler.MeanTimeTranslation
import Euler.OrdinaryMollifier
import Euler.OrdinaryWordConstraints
open Lean Elab Command
set_option maxHeartbeats 0
set_option Elab.async false
run_cmd do
  let ts := (← IO.FS.lines "/Users/will/dev/lean-rosette/corpora/families/build/F00073_tr.txt").toList.filter (· != "") |>.map String.toName
  Fam.Abs.transportEqns "F00073" [(`EulerMeanSolenoidal.translation, `Fam.F73.m1)] ts
