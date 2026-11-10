/- Measurement of the sample and of the projection variants; same functions as `Measure.lean`. -/
import Measure
import Sample
import SampleS8
import Variants

open Lean Meta Elab Command Lesssim.Measure

def Lesssim.sampleDone : List (Name × Name) := [
  (`NavierStokes.BaseStressClasses.correction_weighted_jets, `correction_weighted_jets),
  (`NavierStokes.PositiveTimeSignedData.potential_physical_bound, `potential_physical_bound),
  (`NavierStokes.SmoothFamilyTorusInverse.exists_uniform_coefficient_bound, `exists_uniform_coefficient_bound),
  (`NavierStokes.SmoothFamilyTorusInverse.uniform_multiplied_coeff_bound, `uniform_multiplied_coeff_bound)]

run_cmd do
  let env ← getEnv
  for (o, s) in Lesssim.sampleDone do
    IO.println ("MEASURE " ++ (← measure "orig" o).compress)
    IO.println ("MEASURE " ++ (← measure "native" (`Lesssim.Sample.Native ++ s)).compress)
    IO.println ("MEASURE " ++ (← measure "back" (`Lesssim.Sample.Back ++ s)).compress)
    IO.println ("MEASURE " ++ (← measure "fwd" (`Lesssim.Sample.Fwd ++ s)).compress)
    let some oc := env.find? o | throwError "missing"
    let some bc := env.find? (`Lesssim.Sample.Back ++ s) | throwError "missing"
    let some nc := env.find? (`Lesssim.Sample.Native ++ s) | throwError "missing"
    let some fc := env.find? (`Lesssim.Sample.Fwd ++ s) | throwError "missing"
    let same := oc.type == bc.type.instantiateLevelParams bc.levelParams (oc.levelParams.map Level.param)
    let fsame := nc.type == fc.type.instantiateLevelParams fc.levelParams (nc.levelParams.map Level.param)
    let usesO (n : Name) : Bool := match env.find? n with
      | some ci => (ci.value? (allowOpaque := true)).any fun v => v.getUsedConstants.contains o
      | none => false
    IO.println ("MEASURE " ++ (Json.mkObj [("group", "check"), ("name", toJson s.toString), ("backSameStatement", toJson same),
      ("fwdSameStatement", toJson fsame), ("nativeUsesOriginal", toJson (usesO (`Lesssim.Sample.Native ++ s))),
      ("backUsesOriginal", toJson (usesO (`Lesssim.Sample.Back ++ s)))]).compress)
  IO.println ("MEASURE " ++ (← measure "orig" `NavierStokes.ParametricKernelBounds.profile_comp_derivative_bound).compress)
  IO.println ("MEASURE " ++ (← measure "native-universe0" `Lesssim.Sample.Native.profile_comp_derivative_bound).compress)
  IO.println ("MEASURE " ++ (← measure "iff" `Lesssim.Sample.waveClass_sourceArgument_bound_iff).compress)
  IO.println ("MEASURE " ++ (← measure "iff" `Lesssim.Sample.graphRestriction_jet_bound_iff).compress)
  IO.println ("MEASURE " ++ (← measure "orig" `NavierStokes.WaveEnvelopeTransport.waveClass_sourceArgument_bound).compress)
  IO.println ("MEASURE " ++ (← measure "orig" `NavierStokes.SharpGraphBounds.graphRestriction_jet_bound).compress)
  for s in [`UniformClass.edge_absorbed, `LocalSourceBounds.chart_bound, `commonChart_amplitude_bound] do
    IO.println ("MEASURE " ++ (← measure "variant" (`Lesssim.Variant ++ s)).compress)
