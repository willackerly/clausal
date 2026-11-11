/-
M9 families, F00019: the exponent `1/2 + h`, defined seven times.  Primitive: ONE DEFINITION, no parameter beyond
the members' own argument (the lightest form: the members are already the same function).
-/
import Tool
import NavierStokes.CoordinateAlgebra
import NavierStokes.ExponentLedger
import NavierStokes.HeatTailEdit
import NavierStokes.NaturalAxisData
import NavierStokes.RenormalizedHeatMoment
import NavierStokes.StressAlgebra
import NavierStokes.TerminalPressure
import Mathlib.Util.CountHeartbeats
set_option Elab.async false

namespace Fam.F19

#count_heartbeats in
/-- THE PRIMITIVE -/
noncomputable def halfPlus (h : ℝ) : ℝ := 1 / 2 + h

open NavierStokes in
#count_heartbeats in
theorem members_eq :
    CoordinateAlgebra.A = halfPlus ∧ ExponentLedger.waveExponent = halfPlus ∧ HeatTailEdit.exponent = halfPlus ∧
    NaturalAxisData.A = halfPlus ∧ RenormalizedHeatMoment.A = halfPlus ∧ StressAlgebra.velocityExponent = halfPlus ∧
    TerminalPressure.amplitudeExponent = halfPlus :=
  ⟨rfl, rfl, rfl, rfl, rfl, rfl, rfl⟩

end Fam.F19
