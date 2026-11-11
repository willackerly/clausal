import Tool
import Euler.FiniteEnergyTruncation
import Euler.MeanHarmonicInterior
import NavierStokes.ActivationStocks
import NavierStokes.LeadingStress
import NavierStokes.MeanChartCompatibility
import NavierStokes.PositiveAxisSystem
import NavierStokes.PositiveOrderMoments
import NavierStokes.ReferenceJetBounds
import NavierStokes.SlowResidualMatching
import Mathlib.Util.CountHeartbeats
set_option Elab.async false  -- so that #count_heartbeats includes the proof

-- REPLAY NavierStokes.SlowResidualMatching.partialXX_swirlRadius 15 57
run_cmd IO.println "BLOCK NavierStokes.SlowResidualMatching.partialXX_swirlRadius"
section
set_option linter.all false
noncomputable section
open Set Filter
open scoped BigOperators Topology ContDiff
namespace NavierStokes.SlowResidualMatching
open SimilarityProfile (InnerPoint InnerProfile PhysicalPoint PhysicalProfile
  partialX partialEta T Z pullback)
open SlowExpansionResidual
open AxisymmetricFields (radialEnergy profilePoint)
#count_heartbeats in
theorem partialXX_swirlRadius_S (C : ℝ) {f : InnerProfile} {w : InnerPoint}
    (hf : ContDiffAt ℝ 2 f (radiusPoint w)) :
    partialX (partialX (swirlRadius C f)) w =
      3 * w.1 / C * partialX f (radiusPoint w) +
        w.1 ^ 3 / C * partialX (partialX f) (radiusPoint w) := by
  have he : partialX (swirlRadius C f) =ᶠ[𝓝 w]
      (fun y => toRadius f y / C + y.1 ^ 2 / C * toRadius (partialX f) y) := by
    have hh := radiusPoint_smooth.continuous.continuousAt (hf.eventually (by norm_num))
    filter_upwards [hh] with y hy
    change ContDiffAt ℝ 2 f (radiusPoint y) at hy
    exact partialX_swirlRadius C (hy.differentiableAt (by norm_num))
  have hf' := hf.differentiableAt (by norm_num)
  have hfx := (PositiveAxisSystem.partialX_contDiffAt hf).differentiableAt (by norm_num)
  have hG : DifferentiableAt ℝ
      (fun y : InnerPoint => toRadius f y / C + y.1 ^ 2 / C * toRadius (partialX f) y) w := by
    simpa only [div_eq_mul_inv] using ((toRadius_differentiableAt hf').mul_const C⁻¹).fun_add
      (((show DifferentiableAt ℝ (fun y : InnerPoint => y.1) w from
          differentiableAt_fst).fun_pow 2).mul_const C⁻¹ |>.fun_mul (toRadius_differentiableAt hfx))
  have hd := ((LeadingStress.partialX_hasDerivAt (toRadius_differentiableAt hf')).div_const C).fun_add
    ((((hasDerivAt_id w.1).fun_pow 2).div_const C).fun_mul
      (LeadingStress.partialX_hasDerivAt (toRadius_differentiableAt hfx)))
  have hv := (LeadingStress.partialX_hasDerivAt hG).unique hd
  change (fderiv ℝ (partialX (swirlRadius C f)) w) (1, 0) = _
  rw [he.fderiv_eq]
  change partialX (fun y : InnerPoint => toRadius f y / C +
    y.1 ^ 2 / C * toRadius (partialX f) y) w = _
  rw [hv, partialX_toRadius hf', partialX_toRadius hfx]
  simp only [toRadius, id_eq, Nat.cast_ofNat, Nat.reduceSub, pow_one, mul_one]
  ring
end NavierStokes.SlowResidualMatching
end
end

-- REPLAY NavierStokes.LeadingStress.radialDivergence_physicalStressTheta 61 89
run_cmd IO.println "BLOCK NavierStokes.LeadingStress.radialDivergence_physicalStressTheta"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.LeadingStress
open ProfileHistories
open SimilarityProfile (partialX partialEta pullback inner)
open CoordinateAlgebra (A L)
open scoped Topology ContDiff
variable {Ω : RadialDomain} (P : Profiles Ω)
#count_heartbeats in
theorem radialDivergence_physicalStressTheta_S {h : ℝ} (hh : 0 < h) (hh1 : h < 1 / 2)
    {p : SimilarityProfile.PhysicalPoint} (hp : p.1 < 1) (hs : 0 < p.2.1)
    (hw : inner h p ∈ Ω.carrier) (hf : P.f (inner h p) ≠ 0) :
    radialDivergence 2 (physicalStressTheta P h) p =
      SimilarityProfile.q h p ^ (-A h - 1) * (Real.sqrt (2 * (inner h p).1) *
        (P.f (inner h p) * sourceTheta P h (inner h p) / L h (inner h p).2 +
          2 * ((inner h p).1 * partialX (partialX P.f) (inner h p) +
            2 * partialX P.f (inner h p)))) := by
  have hX := inner_X_pos hh hh1 hp hs
  have hL : L h (inner h p).2 ≠ 0 := (SimilarityProfile.L_pos hh hh1 hp).ne'
  unfold physicalStressTheta
  rw [radialDivergence_pullback hh hh1 2 hp
    ((theta_smoothAt P h hw hX.ne' hf hL).differentiableAt (by simp)),
    sqrt_radial_two hX, theta_divergence P h hw hX hf hL]
  congr 2
  ring
end NavierStokes.LeadingStress
end
end

-- REPLAY Euler.ComparatorBridge.partialDerivative_mul 93 108
run_cmd IO.println "BLOCK Euler.ComparatorBridge.partialDerivative_mul"
section
set_option linter.all false
noncomputable section
open Set MeasureTheory Filter EulerSmoothLimit EulerVectorCalculus
open scoped ContDiff Topology
namespace Euler.ComparatorBridge
#count_heartbeats in
theorem partialDerivative_mul_S (f g : Space → ℝ)
    (hf : Differentiable ℝ f) (hg : Differentiable ℝ g) (j : Fin 3) (x : Space) :
    partialDerivative (fun y => f y * g y) j x =
      f x * partialDerivative g j x + partialDerivative f j x * g x := by
  rw [partialDerivative, fderiv_fun_mul (hf x) (hg x)]
  simp [partialDerivative, mul_comm]
end Euler.ComparatorBridge
end
end

-- REPLAY NavierStokes.ReferenceJetBounds.radial_deriv 112 127
run_cmd IO.println "BLOCK NavierStokes.ReferenceJetBounds.radial_deriv"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ReferenceJetBounds
open Set Filter MeasureTheory
open scoped Topology ContDiff
open ProfileHistories NaturalAxisCoefficients NaturalAxisBridge NaturalProfile NaturalEntrance
#count_heartbeats in
theorem radial_deriv_S {F : ProfileHistories.Field} {p : Point} (hF : ContDiffAt ℝ ∞ F p) :
    HasDerivAt (fun X => F (X, p.2)) (radialPartial F p) p.1 := by
  simpa only [radialPartial, Function.comp_def, id_eq, Prod.eta] using
    (hF.differentiableAt (by simp)).hasFDerivAt.comp_hasDerivAt p.1
      ((hasDerivAt_id p.1).prodMk (hasDerivAt_const p.1 p.2))
end NavierStokes.ReferenceJetBounds
end
end

-- REPLAY NavierStokes.PositiveOrderMoments.massHistory_parameterPartial 131 148
run_cmd IO.println "BLOCK NavierStokes.PositiveOrderMoments.massHistory_parameterPartial"
section
set_option linter.all false
noncomputable section
open Set Function MeasureTheory
open scoped BigOperators ContDiff
namespace NavierStokes.PositiveOrderMoments
section SmoothParameters
variable {P : Type*} [NormedAddCommGroup P] [NormedSpace ℝ P]
end SmoothParameters
section PhysicalHistories
#count_heartbeats in
theorem massHistory_parameterPartial_S {u : JointProfile} (hu : ContDiff ℝ ∞ u) (w : ℝ × ℝ) :
    ProfileHistories.parameterPartial (massHistory u) w = parameterMassHistory u w :=
  ProfileHistories.parameterPartial_primitive globalDomain (weightedAxial_contDiff hu).contDiffOn (mem_univ w)
end PhysicalHistories
end NavierStokes.PositiveOrderMoments
end
end

-- REPLAY NavierStokes.MeanChartCompatibility.physicalFast_naturality 152 225
run_cmd IO.println "BLOCK NavierStokes.MeanChartCompatibility.physicalFast_naturality"
section
set_option linter.all false
namespace NavierStokes.MeanChartCompatibility
noncomputable section
open Set Function Filter MeasureTheory
open scoped Topology ContDiff BigOperators Interval
section RadialScale
end RadialScale
section Pullback
variable {E F : Type} [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup F] [NormedSpace ℝ F]
end Pullback
section TorusPullback
open TorusInverse
variable {S T : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
  [NormedAddCommGroup T] [NormedSpace ℝ T]
end TorusPullback
section RankScaling
end RankScaling
section CommonTemporalBounds
open TorusInverse
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
variable [FiniteDimensional ℝ S]
end CommonTemporalBounds
section PhysicalFamilies
open TorusInverse
end PhysicalFamilies
section ReconstructedStream
variable {E F : Type} [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup F] [NormedSpace ℝ F]
end ReconstructedStream
section PressureAlias
open TorusInverse
variable {S T : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
  [NormedAddCommGroup T] [NormedSpace ℝ T]
end PressureAlias
section CommonTemporalReconstruction
open TorusInverse
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
variable [FiniteDimensional ℝ S]
end CommonTemporalReconstruction
section PhysicalTemporalFields
open TorusInverse
#count_heartbeats in
theorem physicalFast_naturality_S (h : ℝ) (n i : ℕ) {f : PressureStream.Lift Plane → ℝ}
    (hf : ContDiff ℝ ∞ f) (z : PressureStream.Lift Plane) :
    fieldOnPhysical h n i (2 * CoordinateAlgebra.A h + 1 / 2) (fastAtIndex h n i f) z =
      PressureStream.graphDz ((0 : Plane), vector .temporal)
        (fieldOnPhysical h n i (CoordinateAlgebra.A h) f) z := by
  have he := graphDz_pull (chartScale n) (physicalAuxiliary h n i)
    (ChartScales.Q n ^ (-CoordinateAlgebra.A h)) (ChartScales.Tg ^ i)
    ((0 : Plane), vector .temporal) ((0 : Plane), vector .temporal)
    ((hf.differentiable (by simp)) (physicalToChart h n i z)) (physicalAuxiliary_temporal h n i)
  change PressureStream.graphDz _ (fieldOnPhysical h n i (CoordinateAlgebra.A h) f) z = _ at he
  rw [he, fieldOnPhysical_apply, fastAtIndex]
  have hunit : ChartScales.Q n ^ (-(2 * CoordinateAlgebra.A h + 1 / 2)) *
      ChartScales.Q n ^ (1 + h) = ChartScales.Q n ^ (-CoordinateAlgebra.A h) := by
    rw [← Real.rpow_add (ChartScales.Q_pos n)]
    congr 1
    unfold CoordinateAlgebra.A
    ring
  change ChartScales.Q n ^ (-(2 * CoordinateAlgebra.A h + 1 / 2)) *
    ((ChartScales.Tg ^ i * ChartScales.Q n ^ (1 + h)) *
      PressureStream.graphDz _ f (physicalToChart h n i z)) = _
  rw [show ChartScales.Q n ^ (-(2 * CoordinateAlgebra.A h + 1 / 2)) *
      ((ChartScales.Tg ^ i * ChartScales.Q n ^ (1 + h)) *
        PressureStream.graphDz ((0 : Plane), vector .temporal) f (physicalToChart h n i z)) =
      (ChartScales.Q n ^ (-(2 * CoordinateAlgebra.A h + 1 / 2)) * ChartScales.Q n ^ (1 + h)) *
        ChartScales.Tg ^ i * PressureStream.graphDz _ f (physicalToChart h n i z) by ring, hunit]
  rfl
end PhysicalTemporalFields
end
end NavierStokes.MeanChartCompatibility
end

-- REPLAY NavierStokes.SlowResidualMatching.partialX_toRadius_zero 229 249
run_cmd IO.println "BLOCK NavierStokes.SlowResidualMatching.partialX_toRadius_zero"
section
set_option linter.all false
noncomputable section
open Set Filter
open scoped BigOperators Topology ContDiff
namespace NavierStokes.SlowResidualMatching
open SimilarityProfile (InnerPoint InnerProfile PhysicalPoint PhysicalProfile
  partialX partialEta T Z pullback)
open SlowExpansionResidual
open AxisymmetricFields (radialEnergy profilePoint)
#count_heartbeats in
theorem partialX_toRadius_zero_S {f : InnerProfile} {eta : ℝ}
    (hf : DifferentiableAt ℝ (toRadius f) (0, eta)) : partialX (toRadius f) (0, eta) = 0 := by
  have he : Function.Even (fun R => toRadius f (R, eta)) := by
    intro R
    simp [toRadius, radiusPoint]
  exact (LeadingStress.partialX_hasDerivAt hf).deriv.symm.trans
    (EvenSmoothDescent.deriv_zero_of_even he)
end NavierStokes.SlowResidualMatching
end
end

-- REPLAY EulerMeanHarmonic.localized_second_norm_le 253 270
run_cmd IO.println "BLOCK EulerMeanHarmonic.localized_second_norm_le"
section
set_option linter.all false
noncomputable section
namespace EulerMeanHarmonic
open MeasureTheory InnerProductSpace Laplacian EulerSmoothLimit EulerVectorCalculus EulerSobolev
open scoped ContDiff
#count_heartbeats in
theorem localized_second_norm_le_S (h : Space → ℝ) (hh : ContDiff ℝ ∞ h)
    (hLp : MemLp h 2 volume) (hharmonic : ∀ x ∈ Metric.ball 0 (1 : ℝ), Δ h x = 0)
    (i : Fin 3) :
    lpNorm (partialDerivative (partialDerivative (innerCutoff * h) i) i) 2 volume ≤
      Real.sqrt interiorSecondEnergyConstant * lpNorm h 2 volume := by
  apply (sq_le_sq₀ lpNorm_nonneg (mul_nonneg (Real.sqrt_nonneg _) lpNorm_nonneg)).1
  rw [mul_pow, Real.sq_sqrt interiorSecondEnergyConstant_nonneg]
  exact localized_second_energy_le h hh hLp hharmonic i
end EulerMeanHarmonic
end
end

-- REPLAY NavierStokes.PositiveAxisSystem.hasDerivAt_squareProfile_radial 274 298
run_cmd IO.println "BLOCK NavierStokes.PositiveAxisSystem.hasDerivAt_squareProfile_radial"
section
set_option linter.all false
noncomputable section
open Set
open scoped BigOperators ContDiff
namespace NavierStokes.PositiveAxisSystem
section Algebra
variable {K : Type*} [Field K] [CharZero K]
end Algebra
section ActualProfiles
open SimilarityProfile
#count_heartbeats in
theorem hasDerivAt_squareProfile_radial_S {f : InnerProfile} {r eta : ℝ}
    (hf : ContDiffAt ℝ 2 f (r ^ 2, eta)) :
    HasDerivAt (fun s => 2 * s * partialX f (s ^ 2, eta))
      (2 * partialX f (r ^ 2, eta) + 4 * r ^ 2 * partialX (partialX f) (r ^ 2, eta)) r := by
  have hc := ((hasDerivAt_id r).const_mul 2).mul
    (hasDerivAt_squareProfile ((partialX_contDiffAt hf).differentiableAt (by norm_num)))
  convert! hc using 1
  simp only [id_eq]
  ring
end ActualProfiles
end NavierStokes.PositiveAxisSystem
end
end

-- REPLAY NavierStokes.ActivationStocks.naturalHistories_pressure_derivative 302 347
run_cmd IO.println "BLOCK NavierStokes.ActivationStocks.naturalHistories_pressure_derivative"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ActivationStocks
open Set Filter ProfileHistories StressActivation
open scoped Topology ContDiff
section SmoothPairs
variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
namespace SmoothPair
variable {Ω : Set E} {w : E → ℝ}
end SmoothPair
end SmoothPairs
namespace FromReference
open ReferencePath
variable (N : ReferencePath.Input)
end FromReference
open ActivationBounds (ScaledPoint scaledDomain scaledDistance)
section ConstructedFactors
variable (h : ℝ) {X0 : ℝ} (hX0 : 0 < X0) (initial : HistoryRow → ℝ → ℝ)
    {J : Set ℝ} (hJ : IsOpen J) {L U : Field}
    (hL : ContDiffOn ℝ ∞ L (logDomain J hJ).carrier)
    (hU : ContDiffOn ℝ ∞ U (logDomain J hJ).carrier)
    (hi : ∀ r, ContDiffOn ℝ ∞ (initial r) J)
    (hcoef : ∀ η ∈ J, NaturalAxisData.L h η ≠ 0)
end ConstructedFactors
namespace FromReference
open ReferencePath
variable (N : ReferencePath.Input)
end FromReference
section NaturalHistories
open NaturalProfile NaturalAxisBridge
variable {h j σ Λ C : ℝ} {P0 : ℝ → ℝ} {d : NaturalAxisCoefficients.AnalyticInputs h j σ P0}
    (F : ProfileFamily d Λ C) (hΛ : 0 < Λ) (hP0 : ContDiff ℝ ∞ P0)
#count_heartbeats in
theorem naturalHistories_pressure_derivative_S {p : Point} (hp : p ∈ domain Λ) :
    parameterPartial (naturalHistories F hΛ hP0).pressure p = partialEta F.Pi p := by
  have he : (naturalHistories F hΛ hP0).pressure =ᶠ[𝓝 p] F.Pi := by
    filter_upwards [(domain_isOpen Λ).mem_nhds hp] with q hq
    exact naturalHistories_pressure F hΛ hP0 hq
  change fderiv ℝ _ p (0, 1) = _
  rw [he.fderiv_eq]
  exact parameterPartial_natural_field hΛ F.natural.pressure_smooth hp
end NaturalHistories
end NavierStokes.ActivationStocks
end
end

