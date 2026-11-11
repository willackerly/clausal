import F00079_re
import F00015_re
import F00042_re
import F00046_re
import F00073_re
import F02076_re
import F46
import F73
import F79
open Lean Meta Elab Command

/-- transitive closure of constants used by `n`, following only constants defined in corpus or Fam modules -/
partial def revClosure (env : Environment) (start : Name) : Std.HashSet Name := Id.run do
  let mut seen : Std.HashSet Name := {}
  let mut stack : Array Name := #[start]
  while h : stack.size > 0 do
    let c := stack.back
    stack := stack.pop
    if seen.contains c then continue
    seen := seen.insert c
    let some ci := env.find? c | continue
    let inCorpus := match env.getModuleIdxFor? c with
      | some i => let m := env.header.moduleNames[i.toNat]!; (`NavierStokes).isPrefixOf m || (`Euler).isPrefixOf m || m.toString.startsWith "F" || m.toString.startsWith "Tool"
      | none => true
    if !inCorpus then continue
    let mut used := ci.type.getUsedConstants
    if let some v := ci.value? (allowOpaque := true) then used := used ++ v.getUsedConstants
    for u in used do
      if !seen.contains u then stack := stack.push u
  return seen

run_cmd do
  let env ← getEnv
  let pairs : List (Name × Name) := [
  (`NavierStokes.WeightedClasses.MemClass.map, `NavierStokes.WeightedClasses.MemClass.map_R),
  (`NavierStokes.WeightedClasses.MemClass.fderiv, `NavierStokes.WeightedClasses.MemClass.fderiv_R),
  (`NavierStokes.WeightedClasses.MemClass.bilinear, `NavierStokes.WeightedClasses.MemClass.bilinear_R),
  (`NavierStokes.WeightedClasses.MemClass.mul, `NavierStokes.WeightedClasses.MemClass.mul_R),
  (`NavierStokes.CurlClassBounds.class_neg, `NavierStokes.CurlClassBounds.class_neg_R),
  (`NavierStokes.CurlClassBounds.class_sub, `NavierStokes.CurlClassBounds.class_sub_R),
  (`NavierStokes.LabelSumBounds.UniformClass.map, `NavierStokes.LabelSumBounds.UniformClass.map_R),
  (`NavierStokes.LabelSumBounds.UniformClass.neg, `NavierStokes.LabelSumBounds.UniformClass.neg_R),
  (`NavierStokes.LabelSumBounds.UniformClass.bilinear, `NavierStokes.LabelSumBounds.UniformClass.bilinear_R),
  (`NavierStokes.UniformPrimaryWeights.fderiv_class, `NavierStokes.UniformPrimaryWeights.fderiv_class_R),
  (`NavierStokes.UniformHarmonicInteraction.cmul, `NavierStokes.UniformHarmonicInteraction.cmul_R),
  (`NavierStokes.PeriodizedWaveBounds.LocalJets.bilinear, `NavierStokes.PeriodizedWaveBounds.LocalJets.bilinear_R),
  (`NavierStokes.WeightedClasses.MemClass.add, `NavierStokes.WeightedClasses.MemClass.add_R),
  (`NavierStokes.WeightedClasses.MemClass.zero, `NavierStokes.WeightedClasses.MemClass.zero_R),
  (`NavierStokes.WeightedClasses.MemClass.mono_exponent, `NavierStokes.WeightedClasses.MemClass.mono_exponent_R),
  (`NavierStokes.WeightedClasses.MemClass.mono_weight, `NavierStokes.WeightedClasses.MemClass.mono_weight_R),
  (`NavierStokes.WeightedClasses.MemClass.smul, `NavierStokes.WeightedClasses.MemClass.smul_R),
  (`NavierStokes.WeightedClasses.MemClass.band_smul, `NavierStokes.WeightedClasses.MemClass.band_smul_R),
  (`NavierStokes.WeightedClasses.MemClass.directional, `NavierStokes.WeightedClasses.MemClass.directional_R),
  (`NavierStokes.LabelSumBounds.UniformClass.add, `NavierStokes.LabelSumBounds.UniformClass.add_R),
  (`NavierStokes.LabelSumBounds.UniformClass.sub, `NavierStokes.LabelSumBounds.UniformClass.sub_R),
  (`NavierStokes.LabelSumBounds.UniformClass.zero, `NavierStokes.LabelSumBounds.UniformClass.zero_R),
  (`NavierStokes.LabelSumBounds.UniformClass.mono_exponent, `NavierStokes.LabelSumBounds.UniformClass.mono_exponent_R),
  (`NavierStokes.LabelSumBounds.UniformClass.mono_weight, `NavierStokes.LabelSumBounds.UniformClass.mono_weight_R),
  (`NavierStokes.LabelSumBounds.UniformClass.congr, `NavierStokes.LabelSumBounds.UniformClass.congr_R),
  (`NavierStokes.PeriodizedWaveBounds.LocalJets.add, `NavierStokes.PeriodizedWaveBounds.LocalJets.add_R),
  (`NavierStokes.PeriodizedWaveBounds.LocalJets.band_smul, `NavierStokes.PeriodizedWaveBounds.LocalJets.band_smul_R),
  (`NavierStokes.PeriodizedWaveBounds.LocalJets.smul, `NavierStokes.PeriodizedWaveBounds.LocalJets.smul_R),
  (`NavierStokes.ActualCyclePeriodicity.CoefficientsTranslation.sub, `NavierStokes.ActualCyclePeriodicity.CoefficientsTranslation.sub_R),
  (`NavierStokes.CorrectionStep.GaugeSupported.sub, `NavierStokes.CorrectionStep.GaugeSupported.sub_R),
  (`NavierStokes.DefectIncrementBounds.Shell.sub, `NavierStokes.DefectIncrementBounds.Shell.sub_R),
  (`NavierStokes.GaugeDebtIncrement.Regular.sub, `NavierStokes.GaugeDebtIncrement.Regular.sub_R),
  (`NavierStokes.MeanStateRegularity.MovingField.sub, `NavierStokes.MeanStateRegularity.MovingField.sub_R),
  (`NavierStokes.HarmonicResidual.band_sub, `NavierStokes.HarmonicResidual.band_sub_R),
  (`NavierStokes.HarmonicResidual.SmoothCoefficients.sub, `NavierStokes.HarmonicResidual.SmoothCoefficients.sub_R),
  (`NavierStokes.HarmonicSourceSupport.NonzeroSupported.sub, `NavierStokes.HarmonicSourceSupport.NonzeroSupported.sub_R),
  (`NavierStokes.LocalRankDefect.LocalShell.sub, `NavierStokes.LocalRankDefect.LocalShell.sub_R),
  (`NavierStokes.MeanIncrementBounds.SmoothOn.sub, `NavierStokes.MeanIncrementBounds.SmoothOn.sub_R),
  (`NavierStokes.MeanStateRegularity.Periodic.sub, `NavierStokes.MeanStateRegularity.Periodic.sub_R),
  (`NavierStokes.MovingMomentBounds.Support.sub, `NavierStokes.MovingMomentBounds.Support.sub_R),
  (`NavierStokes.PhysicalResidualNaturality.CoefficientsOn.sub, `NavierStokes.PhysicalResidualNaturality.CoefficientsOn.sub_R),
  (`NavierStokes.PhysicalResidualNaturality.ScalarOn.sub, `NavierStokes.PhysicalResidualNaturality.ScalarOn.sub_R),
  (`NavierStokes.PrimaryCopyBounds.NativeJets.sub, `NavierStokes.PrimaryCopyBounds.NativeJets.sub_R),
  (`NavierStokes.SimilarityProfile.partialX_smoothAt, `NavierStokes.SimilarityProfile.partialX_smoothAt_R),
  (`NavierStokes.SimilarityProfile.partialEta_smoothAt, `NavierStokes.SimilarityProfile.partialEta_smoothAt_R),
  (`NavierStokes.AxisSourceRegularity.partialX_smooth, `NavierStokes.AxisSourceRegularity.partialX_smooth_R),
  (`NavierStokes.AxisSourceRegularity.partialEta_smooth, `NavierStokes.AxisSourceRegularity.partialEta_smooth_R),
  (`NavierStokes.NaturalCoefficientBridge.partialX_const_mul, `NavierStokes.NaturalCoefficientBridge.partialX_const_mul_R),
  (`NavierStokes.NaturalCoefficientBridge.partialEta_const_mul, `NavierStokes.NaturalCoefficientBridge.partialEta_const_mul_R),
  (`NavierStokes.PositiveAxisSystem.hasDerivAt_parameterProfile, `NavierStokes.PositiveAxisSystem.hasDerivAt_parameterProfile_R),
  (`NavierStokes.ProfileHistories.radialPartial_smooth, `NavierStokes.ProfileHistories.radialPartial_smooth_R),
  (`NavierStokes.ProfileHistories.parameterPartial_smooth, `NavierStokes.ProfileHistories.parameterPartial_smooth_R),
  (`NavierStokes.SmoothFourierData.partialX_smooth, `NavierStokes.SmoothFourierData.partialX_smooth_R),
  (`NavierStokes.SmoothFourierData.hasDerivAt_slice, `NavierStokes.SmoothFourierData.hasDerivAt_slice_R),
  (`NavierStokes.ParametricTorusInverse.parameter_slice_hasDerivAt, `NavierStokes.ParametricTorusInverse.parameter_slice_hasDerivAt_R),
  (`EulerMeanHarmonic.partialDerivative_mul, `EulerMeanHarmonic.partialDerivative_mul_R),
  (`NavierStokes.MeanIncrementBounds.Class.neg, `NavierStokes.MeanIncrementBounds.Class.neg_R),
  (`NavierStokes.MeanIncrementBounds.Class.sub, `NavierStokes.MeanIncrementBounds.Class.sub_R),
  (`EulerMeanSolenoidal.translation_ae, `EulerMeanSolenoidal.translation_ae_R),
  (`EulerMeanSolenoidal.translation_add, `EulerMeanSolenoidal.translation_add_R),
  (`EulerMeanSolenoidal.translation_zero, `EulerMeanSolenoidal.translation_zero_R),
  (`EulerMeanTimeTranslation.translation_continuous, `EulerMeanTimeTranslation.translation_continuous_R),
  (`NavierStokes.DiagonalResidual.JetRate.weaken, `NavierStokes.DiagonalResidual.JetRate.weaken_R),
  (`NavierStokes.DiagonalResidual.JetRate.add, `NavierStokes.DiagonalResidual.JetRate.add_R),
  (`NavierStokes.DiagonalResidual.JetRate.congr_on, `NavierStokes.DiagonalResidual.JetRate.congr_on_R),
  (`NavierStokes.BaseResidual.finiteRate_weaken, `NavierStokes.BaseResidual.finiteRate_weaken_R),
  (`NavierStokes.BaseResidual.finiteRate_congr_on, `NavierStokes.BaseResidual.finiteRate_congr_on_R),
  (`NavierStokes.BaseResidual.finiteRate_add, `NavierStokes.BaseResidual.finiteRate_add_R)]
  let mut bad := 0
  for (o, r) in pairs do
    let cl := revClosure env r
    if cl.contains o then
      bad := bad + 1
      IO.println s!"CIRCULAR {r} depends on {o}"
  IO.println s!"checked {pairs.length} pairs, circular {bad}"
