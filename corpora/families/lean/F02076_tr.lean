import Abs
import F2076
import NavierStokes.ActualBasePressureBounds
import NavierStokes.ActualBaseVelocityBounds
import NavierStokes.ActualPhysicalStageBounds
import NavierStokes.BaseResidual
import NavierStokes.ConstructedSlowBase
import NavierStokes.DiagonalResidual
import NavierStokes.GenericSupportLocalSummation
import NavierStokes.GenericTupleRealization
import NavierStokes.MixedDiagonalResidual
open Lean Elab Command
set_option maxHeartbeats 0
set_option Elab.async false
run_cmd do
  let ts := (← IO.FS.lines "/Users/will/dev/lean-rosette/corpora/families/build/F02076_tr.txt").toList.filter (· != "") |>.map String.toName
  Fam.Abs.transport "F02076" [(`NavierStokes.DiagonalResidual.JetRate, `Fam.F2076.JetRate', some `Fam.F2076.jetRate_eq), (`NavierStokes.DiagonalResidual.FiniteJetRate, `Fam.F2076.FiniteJetRate', some `Fam.F2076.finiteJetRate_eq)] ts
