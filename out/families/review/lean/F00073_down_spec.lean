import Tool
import Euler.CylinderSpatialMean
import Euler.LpTranslation
import Euler.MeanBoundaryDifference
import Euler.MeanBoundaryTranslation
import Euler.MeanForcingTranslation
import Euler.MeanOperatorTranslation
import Euler.MeanSolenoidalTranslation
import Euler.MeanTimeTranslation
import Mathlib.Util.CountHeartbeats
set_option Elab.async false  -- so that #count_heartbeats includes the proof

-- REPLAY EulerMeanOperatorTranslation.translateOperator_apply 14 27
run_cmd IO.println "BLOCK EulerMeanOperatorTranslation.translateOperator_apply"
section
set_option linter.all false
noncomputable section
namespace EulerMeanOperatorTranslation
open Set MeasureTheory InnerProductSpace ContinuousLinearMap EulerSmoothLimit
  EulerMeanSolenoidal EulerTimeLp EulerTerminalTimePrimitive EulerTimeLpBoundedMap
  EulerMeanTimeTranslation EulerVolterraConvolution EulerMeanVariationalInverse
  EulerTimeH1OperatorProduct
#count_heartbeats in
theorem translateOperator_apply_S (a : Space) (A : L2 →L[ℝ] L2) (u : L2) :
    translateOperator a A u = translation a (A (translation (-a) u)) := rfl
end EulerMeanOperatorTranslation
end
end

-- REPLAY EulerMeanBoundary.cutoffCurl_translation 31 49
run_cmd IO.println "BLOCK EulerMeanBoundary.cutoffCurl_translation"
section
set_option linter.all false
noncomputable section
namespace EulerMeanBoundary
open MeasureTheory InnerProductSpace EulerSmoothLimit EulerVectorCalculus
  EulerMeanSolenoidal EulerMeanCutoffCurl EulerMeanGradientTest
open scoped ContDiff
#count_heartbeats in
theorem cutoffCurl_translation_S (a : Space) (χ : Cutoff) (u : homogeneousSpace) :
    translation a (cutoffCurl χ u) = cutoffCurl (χ.translate a) (homogeneousTranslation a u) := by
  refine homogeneousGradient_dense.induction_on u ?_ ?_
  · exact isClosed_eq ((translation a).continuous.comp (cutoffCurl χ).continuous)
      ((cutoffCurl (χ.translate a)).continuous.comp (homogeneousTranslation a).continuous)
  · intro f
    rw [homogeneousTranslation_test, cutoffCurl_on_test, cutoffCurl_on_test]
    exact testCurl_translated a χ f
end EulerMeanBoundary
end
end

-- REPLAY EulerMeanBoundary.mixedBoundaryOperator_differenceCommutator 53 73
run_cmd IO.println "BLOCK EulerMeanBoundary.mixedBoundaryOperator_differenceCommutator"
section
set_option linter.all false
noncomputable section
namespace EulerMeanBoundary
open MeasureTheory InnerProductSpace EulerSmoothLimit EulerMeanSolenoidal EulerMeanGradientTest
  EulerMeanCutoffCurl
open scoped ENNReal
#count_heartbeats in
theorem mixedBoundaryOperator_differenceCommutator_S (a : Space) (h : ℝ) (χ ψ : Cutoff) :
    (spatialDifference a h).comp (mixedBoundaryOperator χ ψ) -
        (mixedBoundaryOperator χ ψ).comp (spatialDifference a h) =
      (mixedBoundaryOperator (χ.differenceQuotient a h) (ψ.translate (h • a)) +
        mixedBoundaryOperator χ (ψ.differenceQuotient a h)).comp
          (translation (h • a)).toContinuousLinearMap := by
  rw [spatialDifference_commutator, mixedBoundaryOperator_translationCommutator]
  unfold Cutoff.differenceQuotient
  rw [mixedBoundaryOperator_scale_left, mixedBoundaryOperator_scale_right]
  simp only [ContinuousLinearMap.add_comp, ContinuousLinearMap.smul_comp, smul_add]
end EulerMeanBoundary
end
end

-- REPLAY EulerMeanForcing.orbitJet_memLp 77 95
run_cmd IO.println "BLOCK EulerMeanForcing.orbitJet_memLp"
section
set_option linter.all false
noncomputable section
namespace EulerMeanForcing
open MeasureTheory EulerSmoothLimit EulerLpTranslation EulerLpDerivative
  EulerTimeLp EulerTimeLpBoundedMap EulerLpSmoothFamily Filter
open scoped ContDiff Topology
variable {V : Type*} [NormedAddCommGroup V] [NormedSpace ℝ V]
#count_heartbeats in
theorem orbitJet_memLp_S (T : ℝ) (A : ℝ → SmoothL2Field V)
    (hA : ∀ n, MemLp (fun t => (A t).jetLp n) 2 (timeMeasure T)) (n : ℕ) (a : Space) :
    MemLp (fun t => iteratedFDeriv ℝ n (fun b : Space => translation b (A t).toLp) a)
      2 (timeMeasure T) := by
  have h := ((hA n).continuousLinearMap_comp (translation (V := Space [×n]→L[ℝ] V) a).toContinuousLinearMap).continuousLinearMap_comp
    (multilinearBundling (P := Space) (V := V) volume n)
  exact h.ae_eq (Eventually.of_forall (fun t => (A t).iteratedFDeriv_translation_eq n a |>.symm))
end EulerMeanForcing
end
end

-- REPLAY EulerCylinderSpatialMean.mean_translate 99 119
run_cmd IO.println "BLOCK EulerCylinderSpatialMean.mean_translate"
section
set_option linter.all false
noncomputable section
namespace EulerCylinderSpatialMean
open Set MeasureTheory ContinuousLinearMap InnerProductSpace EulerSmoothLimit EulerLiftedGradientSpace
  EulerLpCylinderTranslation EulerCylinderSpatialEmbedding EulerCylinderAngleAverage
variable (P : ℝ) [Fact (0 < P)]
  {V : Type*} [NormedAddCommGroup V] [InnerProductSpace ℝ V] [CompleteSpace V]
#count_heartbeats in
theorem mean_translate_S (a : LiftTangent) (u : CylinderL2 P V) :
    mean P (translate P a u) = EulerLpTranslation.translation a.1 (mean P u) := by
  apply ext_inner_right ℝ
  intro v
  rw [mean_apply, real_inner_smul_left, ContinuousLinearMap.adjoint_inner_left,
    cylinder_translation_inner, embedding_translate, spatial_translation_inner]
  change P⁻¹*inner ℝ u (embedding P (EulerLpTranslation.translation (-a.1) v)) =
    inner ℝ (P⁻¹ • (embedding P).adjoint u) (EulerLpTranslation.translation (-a.1) v)
  rw [real_inner_smul_left, ContinuousLinearMap.adjoint_inner_left]
end EulerCylinderSpatialMean
end
end

-- REPLAY EulerMeanSolenoidal.translated_generator 123 141
run_cmd IO.println "BLOCK EulerMeanSolenoidal.translated_generator"
section
set_option linter.all false
noncomputable section
namespace EulerMeanSolenoidal
open MeasureTheory InnerProductSpace EulerSmoothLimit
open scoped ContDiff
#count_heartbeats in
theorem translated_generator_S (a : Space) {g : L2} (hg : g ∈ gradientGenerators) :
    translation a g ∈ gradientGenerators := by
  obtain ⟨φ, hc, hs, hg⟩ := hg
  refine ⟨fun x => φ (x + a), hc.comp_homeomorph (Homeomorph.addRight a),
    hs.comp (contDiff_id.add contDiff_const), ?_⟩
  filter_upwards [translation_ae a g,
    (measurePreserving_add_right (volume : Measure Space) a).quasiMeasurePreserving.ae hg]
    with x hx hy
  rw [hx, hy, gradient_translated]
end EulerMeanSolenoidal
end
end

-- REPLAY EulerMeanBoundary.testCurl_translated 145 163
run_cmd IO.println "BLOCK EulerMeanBoundary.testCurl_translated"
section
set_option linter.all false
noncomputable section
namespace EulerMeanBoundary
open MeasureTheory InnerProductSpace EulerSmoothLimit EulerVectorCalculus
  EulerMeanSolenoidal EulerMeanCutoffCurl EulerMeanGradientTest
open scoped ContDiff
#count_heartbeats in
theorem testCurl_translated_S (a : Space) (χ : Cutoff) (f : Test) :
    translation a (testCurl χ f) = testCurl (χ.translate a) (translatedTest a f) := by
  apply Lp.ext
  filter_upwards [translation_ae a (testCurl χ f),
    (measurePreserving_add_right (volume : Measure Space) a).quasiMeasurePreserving.ae
      (testCurl_ae χ f), testCurl_ae (χ.translate a) (translatedTest a f)] with x ha hχ ht
  rw [ha, hχ, ht]
  exact (vectorCurl_translated a (fun y => χ.field y • (f : Space → Space) y) x).symm
end EulerMeanBoundary
end
end

-- REPLAY EulerMeanTimeTranslation.timeTranslation_ae 167 179
run_cmd IO.println "BLOCK EulerMeanTimeTranslation.timeTranslation_ae"
section
set_option linter.all false
noncomputable section
namespace EulerMeanTimeTranslation
open Set MeasureTheory InnerProductSpace ContinuousLinearMap EulerSmoothLimit
  EulerMeanSolenoidal EulerTimeLp EulerTerminalTimePrimitive EulerTimeLpBoundedMap
#count_heartbeats in
theorem timeTranslation_ae_S (T : ℝ) (a : Space) (u : TimeLp T L2) :
    timeTranslation T a u =ᵐ[timeMeasure T] fun t => translation a (u t) :=
  timeLift_ae T (translation a).toContinuousLinearMap u
end EulerMeanTimeTranslation
end
end

-- REPLAY EulerLpTranslation.translation_add 183 200
run_cmd IO.println "BLOCK EulerLpTranslation.translation_add"
section
set_option linter.all false
noncomputable section
namespace EulerLpTranslation
open MeasureTheory EulerSmoothLimit Filter
open scoped Topology
variable {V : Type*} [NormedAddCommGroup V] [NormedSpace ℝ V]
#count_heartbeats in
theorem translation_add_S (a b : Space) (u : L2Space V) :
    translation a (translation b u) = translation (a+b) u := by
  apply Lp.ext
  filter_upwards [translation_ae a (translation b u),
    (measurePreserving_add_right (volume : Measure Space) a).quasiMeasurePreserving.ae (translation_ae b u),
    translation_ae (a+b) u] with x ha hb hab
  rw [ha, hb, hab, add_assoc]
end EulerLpTranslation
end
end

-- REPLAY EulerMeanSolenoidal.translation_gradient_mem 204 223
run_cmd IO.println "BLOCK EulerMeanSolenoidal.translation_gradient_mem"
section
set_option linter.all false
noncomputable section
namespace EulerMeanSolenoidal
open MeasureTheory InnerProductSpace EulerSmoothLimit
open scoped ContDiff
#count_heartbeats in
theorem translation_gradient_mem_S (a : Space) {g : L2} (hg : g ∈ gradientSpace) :
    translation a g ∈ gradientSpace := by
  let τ := (translation a).toContinuousLinearMap
  have hspan : Submodule.span ℝ gradientGenerators ≤ gradientSpace.comap τ.toLinearMap := by
    apply Submodule.span_le.2
    intro f hf
    exact (Submodule.span ℝ gradientGenerators).le_topologicalClosure
      (Submodule.subset_span (translated_generator a hf))
  exact (Submodule.span ℝ gradientGenerators).topologicalClosure_minimal hspan
    (gradientSpace_closed.preimage τ.continuous) hg
end EulerMeanSolenoidal
end
end

