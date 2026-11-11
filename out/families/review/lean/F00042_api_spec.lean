import Tool
import Euler.MeanScalarProductDerivatives
import Euler.MeanWeakCurl
import NavierStokes.ActivationHolomorphic
import NavierStokes.ActivationStocks
import NavierStokes.AxisSourceRegularity
import NavierStokes.BasePrefixIdentity
import NavierStokes.GlobalSlowProfiles
import NavierStokes.MeanChartCompatibility
import NavierStokes.NaturalCoefficientBridge
import NavierStokes.ParametricTorusInverse
import NavierStokes.PositiveAxisSystem
import NavierStokes.PressureStream
import NavierStokes.ProfileHistories
import NavierStokes.ReferenceBounds
import NavierStokes.ReferenceJetBounds
import NavierStokes.SimilarityProfile
import NavierStokes.SlowBorelBase
import NavierStokes.SlowExpansionResidual
import NavierStokes.SlowRecursion
import NavierStokes.SmoothFourierData
import NavierStokes.StateMomentBalances
import Mathlib.Util.CountHeartbeats
set_option Elab.async false  -- so that #count_heartbeats includes the proof

-- REPLAY EulerMeanHarmonic.partialDerivative_mul 27 41
run_cmd IO.println "BLOCK EulerMeanHarmonic.partialDerivative_mul"
section
set_option linter.all false
noncomputable section
namespace EulerMeanHarmonic
open InnerProductSpace EulerSmoothLimit EulerVectorCalculus
open scoped ContDiff
#count_heartbeats in
theorem partialDerivative_mul_S {f g : Space → ℝ} {x : Space}
    (hf : DifferentiableAt ℝ f x) (hg : DifferentiableAt ℝ g x) (i : Fin 3) :
    partialDerivative (f * g) i x = g x * partialDerivative f i x + f x * partialDerivative g i x := by
  rw [← gradient_coordinate, gradient_mul hf hg]
  simp only [PiLp.add_apply, PiLp.smul_apply, smul_eq_mul, gradient_coordinate]
end EulerMeanHarmonic
end
end

-- REPLAY EulerMeanHarmonic.secondPartial_mul 45 79
run_cmd IO.println "BLOCK EulerMeanHarmonic.secondPartial_mul"
section
set_option linter.all false
noncomputable section
namespace EulerMeanHarmonic
open InnerProductSpace EulerSmoothLimit EulerVectorCalculus
open scoped ContDiff
#count_heartbeats in
theorem secondPartial_mul_S (f g : Space → ℝ) (hf : ContDiff ℝ ∞ f)
    (hg : ContDiff ℝ ∞ g) (i : Fin 3) (x : Space) :
    partialDerivative (partialDerivative (f * g) i) i x =
      g x * partialDerivative (partialDerivative f i) i x +
        2 * partialDerivative f i x * partialDerivative g i x +
        f x * partialDerivative (partialDerivative g i) i x := by
  have heq : partialDerivative (f * g) i =
      g * partialDerivative f i + f * partialDerivative g i := by
    funext y
    exact partialDerivative_mul ((hf.differentiable (by simp)).differentiableAt)
      ((hg.differentiable (by simp)).differentiableAt) i
  have hdf := contDiff_partialDerivative f hf i
  have hdg := contDiff_partialDerivative g hg i
  have h₁ : DifferentiableAt ℝ (g * partialDerivative f i) x :=
    ((hg.mul hdf).differentiable (by simp)).differentiableAt
  have h₂ : DifferentiableAt ℝ (f * partialDerivative g i) x :=
    ((hf.mul hdg).differentiable (by simp)).differentiableAt
  rw [heq, partialDerivative_add h₁ h₂ i,
    partialDerivative_mul (f := g) (g := partialDerivative f i)
      ((hg.differentiable (by simp)).differentiableAt)
      ((hdf.differentiable (by simp)).differentiableAt),
    partialDerivative_mul (f := f) (g := partialDerivative g i)
      ((hf.differentiable (by simp)).differentiableAt)
      ((hdg.differentiable (by simp)).differentiableAt)]
  ring
end EulerMeanHarmonic
end
end

-- REPLAY EulerMeanPressure.skewTest_inner 83 97
run_cmd IO.println "BLOCK EulerMeanPressure.skewTest_inner"
section
set_option linter.all false
noncomputable section
namespace EulerMeanPressure
open MeasureTheory InnerProductSpace EulerSmoothLimit EulerVectorCalculus EulerMeanSolenoidal
open scoped ContDiff
#count_heartbeats in
theorem skewTest_inner_S (i j : Fin 3) (ψ : Space → ℝ) (x v : Space) :
    ⟪v, skewTest i j ψ x⟫_ℝ = v i * partialDerivative ψ j x - v j * partialDerivative ψ i x := by
  simp only [skewTest, inner_sub_right, inner_smul_right,
    EuclideanSpace.inner_single_right, RCLike.conj_to_real, one_mul]
  ring
end EulerMeanPressure
end
end

-- REPLAY NavierStokes.ActivationHolomorphic.radial_ofReal 101 122
run_cmd IO.println "BLOCK NavierStokes.ActivationHolomorphic.radial_ofReal"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ActivationHolomorphic
open Set Filter Metric MeasureTheory Complex
open scoped Topology ContDiff
section CompactIntegral
variable {H : Type*} [NormedAddCommGroup H] [NormedSpace ℝ H] [ProperSpace H]
    {s : Set H} {G : H × ℝ → ℂ}
end CompactIntegral
#count_heartbeats in
theorem radial_ofReal_S {S : Set ℝ} (hS : IsOpen S) {G : CField} {g : ProfileHistories.Field}
    {x η : ℝ} (hx : x ∈ S) (hg : ContDiffAt ℝ ∞ g (x,η))
    (heq : ∀ y ∈ S, G (y,(η : ℂ)) = (g (y,η) : ℂ)) :
    radial G (x,(η : ℂ)) = (ProfileHistories.radialPartial g (x,η) : ℂ) := by
  have he : (fun y => G (y,(η : ℂ))) =ᶠ[𝓝 x] (fun y => (g (y,η) : ℂ)) := by
    filter_upwards [hS.mem_nhds hx] with y hy
    exact heq y hy
  exact he.deriv_eq.trans (ReferenceJetBounds.radial_deriv hg).ofReal_comp.deriv
end NavierStokes.ActivationHolomorphic
end
end

-- REPLAY NavierStokes.ActivationStocks.parameterPartial_natural_field 126 166
run_cmd IO.println "BLOCK NavierStokes.ActivationStocks.parameterPartial_natural_field"
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
theorem parameterPartial_natural_field_S {G : Field} (hG : ContDiffOn ℝ ∞ G (domain Λ))
    {p : Point} (hp : p ∈ domain Λ) : parameterPartial G p = partialEta G p :=
  (parameterPartial_hasDerivAt (naturalDomain hΛ) hG hp).deriv.symm
end NaturalHistories
end NavierStokes.ActivationStocks
end
end

-- REPLAY NavierStokes.ActivationStocks.radialPartial_natural_field 170 210
run_cmd IO.println "BLOCK NavierStokes.ActivationStocks.radialPartial_natural_field"
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
theorem radialPartial_natural_field_S {G : Field} (hG : ContDiffOn ℝ ∞ G (domain Λ))
    {p : Point} (hp : p ∈ domain Λ) : radialPartial G p = partialY G p :=
  (radialPartial_hasDerivAt (naturalDomain hΛ) hG hp).deriv.symm
end NaturalHistories
end NavierStokes.ActivationStocks
end
end

-- REPLAY NavierStokes.AxisSourceRegularity.partialEta_smooth 214 226
run_cmd IO.println "BLOCK NavierStokes.AxisSourceRegularity.partialEta_smooth"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.AxisSourceRegularity
open SimilarityProfile Set Filter
open scoped BigOperators Topology ContDiff
#count_heartbeats in
theorem partialEta_smooth_S {v : InnerProfile} {w : InnerPoint}
    (hv : ContDiffAt ℝ ∞ v w) : ContDiffAt ℝ ∞ (partialEta v) w :=
  partialEta_smoothAt hv (by simp)
end NavierStokes.AxisSourceRegularity
end
end

-- REPLAY NavierStokes.AxisSourceRegularity.partialX_smooth 230 242
run_cmd IO.println "BLOCK NavierStokes.AxisSourceRegularity.partialX_smooth"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.AxisSourceRegularity
open SimilarityProfile Set Filter
open scoped BigOperators Topology ContDiff
#count_heartbeats in
theorem partialX_smooth_S {v : InnerProfile} {w : InnerPoint}
    (hv : ContDiffAt ℝ ∞ v w) : ContDiffAt ℝ ∞ (partialX v) w :=
  partialX_smoothAt hv (by simp)
end NavierStokes.AxisSourceRegularity
end
end

-- REPLAY NavierStokes.AxisSourceRegularity.radial_advection_axisFactor 246 265
run_cmd IO.println "BLOCK NavierStokes.AxisSourceRegularity.radial_advection_axisFactor"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.AxisSourceRegularity
open SimilarityProfile Set Filter
open scoped BigOperators Topology ContDiff
#count_heartbeats in
theorem radial_advection_axisFactor_S {vi vj : InnerProfile} {w : InnerPoint}
    (hvj : DifferentiableAt ℝ vj w) :
    axisFactor vi w * (partialX (axisFactor vj) w - axisFactor vj w / (2 * w.1)) =
      w.1 * (vi w * (vj w / 2 + w.1 * partialX vj w)) := by
  rw [partialX_axisFactor hvj]
  unfold axisFactor
  by_cases hX : w.1 = 0
  · simp [hX]
  · field_simp [hX]
    ring
end NavierStokes.AxisSourceRegularity
end
end

-- REPLAY NavierStokes.BasePrefixIdentity.partialS_physicalUncutPrefix 269 287
run_cmd IO.println "BLOCK NavierStokes.BasePrefixIdentity.partialS_physicalUncutPrefix"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.BasePrefixIdentity
open Set Filter
open scoped Topology ContDiff
open SlowBorelBase (Inner Chart Coefficients SmoothCoefficients)
#count_heartbeats in
theorem partialS_physicalUncutPrefix_S {h b : ℝ} (hh : 0 < h) (hh1 : h < 1 / 2)
    (J : ℕ) (f : ℕ → Inner → ℝ) {p : Chart} (hp : p.1 < 1)
    (hf : ∀ n ≤ J, DifferentiableAt ℝ (f n) (SimilarityProfile.inner h p)) :
    AxisymmetricFields.partialS (SlowBorelBase.physicalUncutPrefix h b f J) p =
      SlowExpansionResidual.finiteProfile J h (b - 1) (fun n => SimilarityProfile.partialX (f n)) p := by
  change fderiv ℝ _ p (0, (1, 0)) = _
  rw [(physicalUncutPrefix_germ hh hh1 b f J hp).fderiv_eq]
  exact SlowExpansionResidual.partialS_finiteProfile hh hh1 J f hp hf
end NavierStokes.BasePrefixIdentity
end
end

-- REPLAY NavierStokes.GlobalSlowProfiles.xProfile_partialEta 291 305
run_cmd IO.println "BLOCK NavierStokes.GlobalSlowProfiles.xProfile_partialEta"
section
set_option linter.all false
noncomputable section
open Set Filter Function MeasureTheory
open scoped ContDiff Topology BigOperators
namespace NavierStokes.GlobalSlowProfiles
#count_heartbeats in
theorem xProfile_partialEta_S {S : Set ℝ} (hS : IsOpen S) (f : EvenProfile S)
    {w : ℝ × ℝ} (hX : 0 < w.1) (heta : w.2 ∈ S) :
    SimilarityProfile.partialEta (xProfile f) w = xProfile (etaDerivative hS f) w :=
  (partialEta_hasDerivAt ((xProfile_contDiffAt hS f hX heta).differentiableAt (by simp))).unique
    (parameter_derivative hS f.smooth heta (Real.sqrt (2 * w.1)))
end NavierStokes.GlobalSlowProfiles
end
end

-- REPLAY NavierStokes.GlobalSlowProfiles.xProfile_partialX 309 339
run_cmd IO.println "BLOCK NavierStokes.GlobalSlowProfiles.xProfile_partialX"
section
set_option linter.all false
noncomputable section
open Set Filter Function MeasureTheory
open scoped ContDiff Topology BigOperators
namespace NavierStokes.GlobalSlowProfiles
#count_heartbeats in
theorem xProfile_partialX_S {S : Set ℝ} (hS : IsOpen S) (f : EvenProfile S)
    {w : ℝ × ℝ} (hX : 0 < w.1) (heta : w.2 ∈ S) :
    SimilarityProfile.partialX (xProfile f) w = xProfile (xDerivative hS f) w := by
  let R := Real.sqrt (2 * w.1)
  have hR : R ≠ 0 := ne_of_gt (Real.sqrt_pos.mpr (mul_pos (by norm_num) hX))
  have hd := ProfileHistories.radialPartial_hasDerivAt (PositiveOrderMoments.parameterDomain S hS)
    f.smooth (p := (R, w.2)) ⟨mem_univ _, heta⟩
  have hs : HasDerivAt (fun X : ℝ => Real.sqrt (2 * X)) (1 / R) w.1 := by
    convert! (Real.hasDerivAt_sqrt (ne_of_gt (mul_pos (by norm_num) hX))).scomp w.1
      ((hasDerivAt_id w.1).const_mul 2) using 1
    dsimp [R]
    field_simp
  have hc := hd.scomp w.1 hs
  have hx := radius_mul_xDerivative hS f heta R
  change R * xDerivative hS f (R, w.2) = ProfileHistories.radialPartial f (R, w.2) at hx
  rw [← hx] at hc
  have he : (1 / R) • (R * xDerivative hS f (R, w.2)) = xDerivative hS f (R, w.2) := by
    rw [smul_eq_mul]
    field_simp
  rw [he] at hc
  exact (partialX_hasDerivAt ((xProfile_contDiffAt hS f hX heta).differentiableAt (by simp))).unique hc
end NavierStokes.GlobalSlowProfiles
end
end

-- REPLAY NavierStokes.MeanChartCompatibility.pressureAlias_eq_source_sub_derivative 343 393
run_cmd IO.println "BLOCK NavierStokes.MeanChartCompatibility.pressureAlias_eq_source_sub_derivative"
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
#count_heartbeats in
theorem pressureAlias_eq_source_sub_derivative_S {d a b M : ℝ}
    (ha : 0 < a) (hab : a < b) (hd : 0 < d) (v : Plane)
    {f : PressureStream.Lift S → ℝ} (hf : ContDiff ℝ ∞ f)
    (hs : RadialAlias.RadiallySupported a b f) (z : PressureStream.Lift S) :
    PressureStream.pressureAlias d a b M hab v f z =
      PressureStream.pressureSource a b hab f z -
        PressureStream.graphDr (PressureStream.physicalSpeed d M) ((0 : S), v)
          (PressureStream.meanPressure d a b M hab v f) z := by
  have he := PressureStream.meanPressure_radial_residual_global (M := M) ha hab hd v hf hs z
  unfold PressureStream.pressureSource
  linarith
end PressureAlias
end
end NavierStokes.MeanChartCompatibility
end

-- REPLAY NavierStokes.NaturalCoefficientBridge.partialEta_const_mul 397 412
run_cmd IO.println "BLOCK NavierStokes.NaturalCoefficientBridge.partialEta_const_mul"
section
set_option linter.all false
noncomputable section
open Set Filter
open scoped Topology ContDiff
namespace NavierStokes.NaturalCoefficientBridge
open SimilarityProfile (InnerPoint InnerProfile partialX partialEta T Z)
open SlowExpansionResidual
#count_heartbeats in
theorem partialEta_const_mul_S (C : ℝ) {f : InnerProfile} {w : InnerPoint}
    (hf : DifferentiableAt ℝ f w) :
    partialEta (fun p => C * f p) w = C * partialEta f w := by
  simp only [partialEta, fderiv_const_mul hf, _root_.smul_apply, smul_eq_mul]
end NavierStokes.NaturalCoefficientBridge
end
end

-- REPLAY NavierStokes.NaturalCoefficientBridge.partialX_const_mul 416 431
run_cmd IO.println "BLOCK NavierStokes.NaturalCoefficientBridge.partialX_const_mul"
section
set_option linter.all false
noncomputable section
open Set Filter
open scoped Topology ContDiff
namespace NavierStokes.NaturalCoefficientBridge
open SimilarityProfile (InnerPoint InnerProfile partialX partialEta T Z)
open SlowExpansionResidual
#count_heartbeats in
theorem partialX_const_mul_S (C : ℝ) {f : InnerProfile} {w : InnerPoint}
    (hf : DifferentiableAt ℝ f w) :
    partialX (fun p => C * f p) w = C * partialX f w := by
  simp only [partialX, fderiv_const_mul hf, _root_.smul_apply, smul_eq_mul]
end NavierStokes.NaturalCoefficientBridge
end
end

-- REPLAY NavierStokes.NaturalCoefficientBridge.secondX_const_mul 435 452
run_cmd IO.println "BLOCK NavierStokes.NaturalCoefficientBridge.secondX_const_mul"
section
set_option linter.all false
noncomputable section
open Set Filter
open scoped Topology ContDiff
namespace NavierStokes.NaturalCoefficientBridge
open SimilarityProfile (InnerPoint InnerProfile partialX partialEta T Z)
open SlowExpansionResidual
#count_heartbeats in
theorem secondX_const_mul_S (C : ℝ) {f : InnerProfile} {w : InnerPoint}
    (hf : ContDiffAt ℝ ∞ f w) :
    partialX (partialX (fun p => C * f p)) w = C * partialX (partialX f) w := by
  rw [secondX_eq_slice (contDiffAt_const.mul hf), secondX_eq_slice hf]
  exact iteratedDeriv_const_mul
    C ((hf.comp w.1 (contDiffAt_id.prodMk contDiffAt_const)).of_le (nat_le_infty 2))
end NavierStokes.NaturalCoefficientBridge
end
end

-- REPLAY NavierStokes.ParametricTorusInverse.coefficient_hasDerivAt 456 488
run_cmd IO.println "BLOCK NavierStokes.ParametricTorusInverse.coefficient_hasDerivAt"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ParametricTorusInverse
open Set Filter MeasureTheory
open TorusInverse
open scoped Topology ContDiff BigOperators
#count_heartbeats in
theorem coefficient_hasDerivAt_S {f : Source} (hf : ContDiff ℝ ∞ f)
    (k : Frequency) (p : ℝ) :
    HasDerivAt (fun q => coefficient f q k) (coefficient (parameterPartial f) p k) p := by
  let inner : ℝ × ℝ → ℂ := fun q => ∫ x in (0 : ℝ)..1, weightedSource k f (q, x)
  let innerD : ℝ × ℝ → ℂ := fun q => ∫ x in (0 : ℝ)..1,
    weightedSource k (parameterPartial f) (q, x)
  have hi : ContDiff ℝ ∞ inner :=
    TransportPrimitive.parameterIntegral_contDiff (weightedSource_smooth hf k) 0 1
  have hd : ∀ q y, HasDerivAt (fun u => inner (u, y)) (innerD (q, y)) q := by
    intro q y
    have hy : ContDiff ℝ ∞ (fun z : ℝ × ℝ => weightedSource k f ((z.1, y), z.2)) :=
      ((weightedSource_smooth hf k).comp
        ((contDiff_fst.prodMk contDiff_const).prodMk contDiff_snd))
    exact integral_hasDerivAt
      (g' := fun z : ℝ × ℝ => weightedSource k (parameterPartial f) ((z.1, y), z.2))
      hy (fun u x => by
        simpa only [weightedSource] using
          (parameter_slice_hasDerivAt hf u (x, y)).const_mul
            (SmoothFourierData.kernel k (x, y))) 0 1 q
  have ho := integral_hasDerivAt hi hd 0 1 p
  simpa only [coefficient, SmoothFourierData.coefficient_eq_doubleIntegral, slice,
    inner, innerD, weightedSource] using ho
end NavierStokes.ParametricTorusInverse
end
end

-- REPLAY NavierStokes.ParametricTorusInverse.parameter_slice_hasDerivAt 492 507
run_cmd IO.println "BLOCK NavierStokes.ParametricTorusInverse.parameter_slice_hasDerivAt"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ParametricTorusInverse
open Set Filter MeasureTheory
open TorusInverse
open scoped Topology ContDiff BigOperators
#count_heartbeats in
theorem parameter_slice_hasDerivAt_S {f : Source} (hf : ContDiff ℝ ∞ f)
    (p : ℝ) (Y : Plane) :
    HasDerivAt (fun q => f (q, Y)) (parameterPartial f (p, Y)) p := by
  exact ((hf.differentiable (by simp)) (p, Y)).hasFDerivAt.comp_hasDerivAt p
    ((hasDerivAt_id p).prodMk (hasDerivAt_const p Y))
end NavierStokes.ParametricTorusInverse
end
end

-- REPLAY NavierStokes.PositiveAxisSystem.hasDerivAt_parameterProfile 511 532
run_cmd IO.println "BLOCK NavierStokes.PositiveAxisSystem.hasDerivAt_parameterProfile"
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
theorem hasDerivAt_parameterProfile_S {f : InnerProfile} {X eta : ℝ}
    (hf : DifferentiableAt ℝ f (X, eta)) :
    HasDerivAt (fun z => f (X, z)) (partialEta f (X, eta)) eta := by
  have hc := hf.hasFDerivAt.comp_hasDerivAt eta
    ((hasDerivAt_const eta X).prodMk (hasDerivAt_id eta))
  simpa [fderiv_inner_apply, Function.comp_def] using hc
end ActualProfiles
end NavierStokes.PositiveAxisSystem
end
end

-- REPLAY NavierStokes.PressureStream.meanPressure_radial_residual_global 536 577
run_cmd IO.println "BLOCK NavierStokes.PressureStream.meanPressure_radial_residual_global"
section
set_option linter.all false
noncomputable section
open Set Filter Function MeasureTheory
open scoped Topology ContDiff Interval
namespace NavierStokes.PressureStream
open TransportPrimitive
section Average
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
end Average
section Graph
variable {E : Type} [NormedAddCommGroup E] [NormedSpace ℝ E]
end Graph
section Pressure
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
end Pressure
section Stream
variable {E : Type} [NormedAddCommGroup E] [NormedSpace ℝ E]
end Stream
section BarIdentities
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
end BarIdentities
section GlobalStream
variable {E : Type} [NormedAddCommGroup E] [NormedSpace ℝ E]
end GlobalStream
section FinalBar
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
#count_heartbeats in
theorem meanPressure_radial_residual_global_S {d a b M : ℝ} (ha : 0 < a) (hab : a < b)
    (hd : 0 < d) (v : Plane) {f : Lift S → ℝ} (hf : ContDiff ℝ ∞ f)
    (hs : RadialAlias.RadiallySupported a b f) (p : Lift S) :
    graphDr (physicalSpeed d M) (0, v) (meanPressure d a b M hab v f) p - f p =
      -rho a b hab p.1 * pressureMass f p.2.1 - pressureAlias d a b M hab v f p := by
  rw [graphDr_eq_physical, meanPressure,
    RadialPullback.physicalGraphDeriv_physicalCompact_global ha hab hd
      (pressureSource_contDiff hab hf hs) (pressureSource_supported hab hs) M (0, v) p]
  unfold pressureAlias pressureSource
  ring
end FinalBar
end NavierStokes.PressureStream
end
end

-- REPLAY NavierStokes.ProfileHistories.Profiles.W_formula 581 603
run_cmd IO.println "BLOCK NavierStokes.ProfileHistories.Profiles.W_formula"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ProfileHistories
open Set MeasureTheory Filter Metric
open scoped Topology ContDiff
section CompactParameterIntegral
variable {s : Set Point} {G : Point → ℝ → ℝ}
end CompactParameterIntegral
namespace Profiles
open StressAlgebra
variable {D : RadialDomain} (P : Profiles D)
#count_heartbeats in
theorem W_formula_S (h : ℝ) {p : Point} (hp : p ∈ D.carrier) :
    P.W h p = 1 - 2 * axialExponent h * p.2 * P.Ubar p -
      coordinateFactor p.2 * parameterPartial P.Ubar p := by
  rw [show parameterPartial P.Ubar p = average (parameterPartial P.U) p from
    parameterPartial_average D P.U_smooth hp]
  rfl
end Profiles
end NavierStokes.ProfileHistories
end
end

-- REPLAY NavierStokes.ProfileHistories.parameterPartial_smooth 607 619
run_cmd IO.println "BLOCK NavierStokes.ProfileHistories.parameterPartial_smooth"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ProfileHistories
open Set MeasureTheory Filter Metric
open scoped Topology ContDiff
#count_heartbeats in
theorem parameterPartial_smooth_S (D : RadialDomain) {F : Field}
    (hF : ContDiffOn ℝ ∞ F D.carrier) : ContDiffOn ℝ ∞ (parameterPartial F) D.carrier := by
  exact (hF.fderiv_of_isOpen D.isOpen (by simp)).clm_apply contDiffOn_const
end NavierStokes.ProfileHistories
end
end

-- REPLAY NavierStokes.ProfileHistories.radialPartial_smooth 623 635
run_cmd IO.println "BLOCK NavierStokes.ProfileHistories.radialPartial_smooth"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ProfileHistories
open Set MeasureTheory Filter Metric
open scoped Topology ContDiff
#count_heartbeats in
theorem radialPartial_smooth_S (D : RadialDomain) {F : Field}
    (hF : ContDiffOn ℝ ∞ F D.carrier) : ContDiffOn ℝ ∞ (radialPartial F) D.carrier := by
  exact (hF.fderiv_of_isOpen D.isOpen (by simp)).clm_apply contDiffOn_const
end NavierStokes.ProfileHistories
end
end

-- REPLAY NavierStokes.ReferenceBounds.H_radialPartial 639 658
run_cmd IO.println "BLOCK NavierStokes.ReferenceBounds.H_radialPartial"
section
set_option linter.all false
noncomputable section
open Set Filter Function MeasureTheory
open scoped Topology ContDiff BigOperators
namespace NavierStokes.ReferenceBounds
open ProfileHistories
section Histories
variable {D : RadialDomain} (P : Profiles D)
#count_heartbeats in
theorem H_radialPartial_S {p : Point} (hp : p ∈ D.carrier) :
    radialPartial P.H p = 2 * P.f p + 2 * p.1 * radialPartial P.f p := by
  have h := ((hasDerivAt_id p.1).const_mul 2).mul
    (radialPartial_hasDerivAt D P.f_smooth hp)
  have he := (radialPartial_hasDerivAt D P.H_smooth hp).unique h
  simpa only [one_mul, mul_one, id_eq, Prod.eta] using he
end Histories
end NavierStokes.ReferenceBounds
end
end

-- REPLAY NavierStokes.ReferenceBounds.parameterPartial_natural 662 687
run_cmd IO.println "BLOCK NavierStokes.ReferenceBounds.parameterPartial_natural"
section
set_option linter.all false
noncomputable section
open Set Filter Function MeasureTheory
open scoped Topology ContDiff BigOperators
namespace NavierStokes.ReferenceBounds
open ProfileHistories
section Histories
variable {D : RadialDomain} (P : Profiles D)
end Histories
open NaturalAxisCoefficients
section ActualModels
variable {D : RadialDomain} (P : Profiles D)
end ActualModels
section NaturalAgreement
open NaturalAxisBridge NaturalProfile ReferencePath
#count_heartbeats in
theorem parameterPartial_natural_S {F : ProfileHistories.Field} {p : Point}
    (hF : ContDiffAt ℝ ∞ F p) : parameterPartial F p = partialEta F p := by
  have hd := (hF.differentiableAt (by simp)).hasFDerivAt.comp_hasDerivAt p.2
    ((hasDerivAt_const p.2 p.1).prodMk (hasDerivAt_id p.2))
  exact hd.deriv.symm
end NaturalAgreement
end NavierStokes.ReferenceBounds
end
end

-- REPLAY NavierStokes.ReferenceBounds.radialPartial_natural 691 716
run_cmd IO.println "BLOCK NavierStokes.ReferenceBounds.radialPartial_natural"
section
set_option linter.all false
noncomputable section
open Set Filter Function MeasureTheory
open scoped Topology ContDiff BigOperators
namespace NavierStokes.ReferenceBounds
open ProfileHistories
section Histories
variable {D : RadialDomain} (P : Profiles D)
end Histories
open NaturalAxisCoefficients
section ActualModels
variable {D : RadialDomain} (P : Profiles D)
end ActualModels
section NaturalAgreement
open NaturalAxisBridge NaturalProfile ReferencePath
#count_heartbeats in
theorem radialPartial_natural_S {F : ProfileHistories.Field} {p : Point}
    (hF : ContDiffAt ℝ ∞ F p) : radialPartial F p = partialY F p := by
  have hd := (hF.differentiableAt (by simp)).hasFDerivAt.comp_hasDerivAt p.1
    ((hasDerivAt_id p.1).prodMk (hasDerivAt_const p.1 p.2))
  exact hd.deriv.symm
end NaturalAgreement
end NavierStokes.ReferenceBounds
end
end

-- REPLAY NavierStokes.ReferenceJetBounds.first_parameter_difference 720 742
run_cmd IO.println "BLOCK NavierStokes.ReferenceJetBounds.first_parameter_difference"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ReferenceJetBounds
open Set Filter MeasureTheory
open scoped Topology ContDiff
open ProfileHistories NaturalAxisCoefficients NaturalAxisBridge NaturalProfile NaturalEntrance
section Natural
variable {h j σ Λ C : ℝ} {P0 : ℝ → ℝ} {d : AnalyticInputs h j σ P0}
variable (F : CoefficientProfile d Λ C)
end Natural
#count_heartbeats in
theorem first_parameter_difference_S {F G : ProfileHistories.Field} {x y η : ℝ}
    (hF : ContDiffAt ℝ ∞ F (x, η)) (hG : ContDiffAt ℝ ∞ G (y, η)) :
    iteratedDeriv 1 (fun z => F (x, z) - G (y, z)) η =
      parameterPartial F (x, η) - parameterPartial G (y, η) := by
  rw [iteratedDeriv_one]
  have hdF : HasDerivAt (fun z => F (x, z)) (parameterPartial F (x, η)) η := parameter_deriv hF
  have hdG : HasDerivAt (fun z => G (y, z)) (parameterPartial G (y, η)) η := parameter_deriv hG
  exact (hdF.sub hdG).deriv
end NavierStokes.ReferenceJetBounds
end
end

-- REPLAY NavierStokes.ReferenceJetBounds.natural_U_parameter 746 771
run_cmd IO.println "BLOCK NavierStokes.ReferenceJetBounds.natural_U_parameter"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ReferenceJetBounds
open Set Filter MeasureTheory
open scoped Topology ContDiff
open ProfileHistories NaturalAxisCoefficients NaturalAxisBridge NaturalProfile NaturalEntrance
section Natural
variable {h j σ Λ C : ℝ} {P0 : ℝ → ℝ} {d : AnalyticInputs h j σ P0}
variable (F : CoefficientProfile d Λ C)
#count_heartbeats in
theorem natural_U_parameter_S (hΛ : Λ ≠ 0) {p : Point} (hp : p ∈ domain Λ) :
    Λ * (parameterPartial F.family.U p - 4) =
      NaturalAxisBridge.partialEta (AxisEvaluation.profile window d.coefficients.epsilon F.coefficients.2)
        (rescalePoint Λ p) := by
  have hpart : parameterPartial F.family.U p = NaturalAxisBridge.partialEta F.family.U p :=
    parameterPartial_eq_partialEta (F.family.natural.U_smooth.contDiffAt ((domain_isOpen Λ).mem_nhds hp))
  rw [hpart, F.U_eq]
  rw [axialField, affineProfile_partialEta
    (AxisEvaluation.profile_smooth window d.coefficients.epsilon_pos F.coefficients.2)
    (1 / Λ) Λ hp (uStar_hasDerivAt j p.2)]
  field_simp ; ring
end Natural
end NavierStokes.ReferenceJetBounds
end
end

-- REPLAY NavierStokes.ReferenceJetBounds.parameterPartial_eq_partialEta 775 787
run_cmd IO.println "BLOCK NavierStokes.ReferenceJetBounds.parameterPartial_eq_partialEta"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ReferenceJetBounds
open Set Filter MeasureTheory
open scoped Topology ContDiff
open ProfileHistories NaturalAxisCoefficients NaturalAxisBridge NaturalProfile NaturalEntrance
#count_heartbeats in
theorem parameterPartial_eq_partialEta_S {F : ProfileHistories.Field} {p : Point} (hF : ContDiffAt ℝ ∞ F p) :
    parameterPartial F p = NaturalAxisBridge.partialEta F p := (parameter_deriv hF).deriv.symm
end NavierStokes.ReferenceJetBounds
end
end

-- REPLAY NavierStokes.ReferenceJetBounds.radialPartial_eq_partialY 791 803
run_cmd IO.println "BLOCK NavierStokes.ReferenceJetBounds.radialPartial_eq_partialY"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ReferenceJetBounds
open Set Filter MeasureTheory
open scoped Topology ContDiff
open ProfileHistories NaturalAxisCoefficients NaturalAxisBridge NaturalProfile NaturalEntrance
#count_heartbeats in
theorem radialPartial_eq_partialY_S {F : ProfileHistories.Field} {p : Point} (hF : ContDiffAt ℝ ∞ F p) :
    radialPartial F p = NaturalAxisBridge.partialY F p := (radial_deriv hF).deriv.symm
end NavierStokes.ReferenceJetBounds
end
end

-- REPLAY NavierStokes.SimilarityProfile.hasDerivAt_pullback_s 807 831
run_cmd IO.println "BLOCK NavierStokes.SimilarityProfile.hasDerivAt_pullback_s"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.SimilarityProfile
open Set Filter
open scoped Topology ContDiff
#count_heartbeats in
theorem hasDerivAt_pullback_s_S {h b : ℝ} {f : InnerProfile}
    (hh : 0 < h) (hh1 : h < 1 / 2) {p : PhysicalPoint} (hp : p.1 < 1)
    (hf : DifferentiableAt ℝ f (inner h p)) :
    HasDerivAt (fun s => pullback h b f (p.1, (s, p.2.2)))
      (pullback h (b - 1) (partialX f) p) p.2.1 := by
  have hx : HasDerivAt (fun s => s / q h p) (1 / q h p) p.2.1 :=
    (hasDerivAt_id p.2.1).div_const _
  have hc := hf.hasFDerivAt.comp_hasDerivAt p.2.1 (hx.prodMk (hasDerivAt_const p.2.1 (eta h p)))
  have hm := hc.const_mul (q h p ^ b)
  rw [fderiv_inner_apply] at hm
  have he : q h p ^ b * (partialX f (inner h p) * (1 / q h p) + partialEta f (inner h p) * 0) =
      pullback h (b - 1) (partialX f) p := by
    rw [pullback, Real.rpow_sub_one (q_pos hh hh1 hp).ne']
    ring
  exact hm.congr_deriv he
end NavierStokes.SimilarityProfile
end
end

-- REPLAY NavierStokes.SimilarityProfile.partialEta_smoothAt 835 847
run_cmd IO.println "BLOCK NavierStokes.SimilarityProfile.partialEta_smoothAt"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.SimilarityProfile
open Set Filter
open scoped Topology ContDiff
#count_heartbeats in
theorem partialEta_smoothAt_S {f : InnerProfile} {w : InnerPoint} {m n : WithTop ℕ∞}
    (hf : ContDiffAt ℝ n f w) (hmn : m + 1 ≤ n) : ContDiffAt ℝ m (partialEta f) w :=
  (hf.fderiv_right hmn).clm_apply contDiffAt_const
end NavierStokes.SimilarityProfile
end
end

-- REPLAY NavierStokes.SimilarityProfile.partialX_smoothAt 851 863
run_cmd IO.println "BLOCK NavierStokes.SimilarityProfile.partialX_smoothAt"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.SimilarityProfile
open Set Filter
open scoped Topology ContDiff
#count_heartbeats in
theorem partialX_smoothAt_S {f : InnerProfile} {w : InnerPoint} {m n : WithTop ℕ∞}
    (hf : ContDiffAt ℝ n f w) (hmn : m + 1 ≤ n) : ContDiffAt ℝ m (partialX f) w :=
  (hf.fderiv_right hmn).clm_apply contDiffAt_const
end NavierStokes.SimilarityProfile
end
end

-- REPLAY NavierStokes.SlowBorelBase.partialS_physicalProfile 867 890
run_cmd IO.println "BLOCK NavierStokes.SlowBorelBase.partialS_physicalProfile"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.SlowBorelBase
open Set Filter Function
open scoped Topology ContDiff BigOperators
variable {V : Type} [NormedAddCommGroup V] [NormedSpace ℝ V]
section PhysicalCoordinates
end PhysicalCoordinates
section PhysicalProfiles
#count_heartbeats in
theorem partialS_physicalProfile_S {a : ℕ → ℕ} (ha : StrictMono a) {h : ℝ}
    (hh : 0 < h) (hh1 : h < 1 / 2) {f : ℕ → Inner → ℝ}
    (hf : ∀ j, ContDiff ℝ ∞ (f j)) (b : ℝ) {p : Chart} (hp : p.1 < 1) :
    AxisymmetricFields.partialS (physicalProfile a h b f) p =
      physicalProfile a h (b - 1) (fun j => SimilarityProfile.partialX (f j)) p := by
  have hd := ((physicalProfile_smoothAt ha hh hh1 hf b hp).differentiableAt (by simp)).hasFDerivAt
  have hc := hd.comp_hasDerivAt p.2.1 ((hasDerivAt_const p.2.1 p.1).prodMk
    ((hasDerivAt_id p.2.1).prodMk (hasDerivAt_const p.2.1 p.2.2)))
  exact hc.unique (hasDerivAt_physicalProfile_s ha hh hh1 hf b hp)
end PhysicalProfiles
end NavierStokes.SlowBorelBase
end
end

-- REPLAY NavierStokes.SlowExpansionResidual.partialSS_finiteProfile 894 919
run_cmd IO.println "BLOCK NavierStokes.SlowExpansionResidual.partialSS_finiteProfile"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.SlowExpansionResidual
open AxisymmetricFields
open SimilarityProfile (InnerProfile InnerPoint pullback partialX T Z)
open scoped BigOperators Topology ContDiff
#count_heartbeats in
theorem partialSS_finiteProfile_S {h b : ℝ} (hh : 0 < h) (hh1 : h < 1 / 2)
    (N : ℕ) (f : ℕ → InnerProfile) {p : ProfilePoint} (hp : p.1 < 1)
    (hf : ∀ n ≤ N, ContDiffAt ℝ 2 (f n) (SimilarityProfile.inner h p)) :
    partialS (partialS (finiteProfile N h b f)) p =
      finiteProfile N h (b - 2) (fun n => partialX (partialX (f n))) p := by
  unfold finiteProfile
  change derivativeAlong (0, (1, 0)) (derivativeAlong (0, (1, 0)) _) p = _
  rw [secondAlong_sum _ _ _ _ _ (fun n hn => SimilarityProfile.pullback_smoothAt
    hh hh1 hp (hf n (by have := Finset.mem_range.mp hn; omega)))]
  apply Finset.sum_congr rfl
  intro n hn
  change SimilarityProfile.partialS (SimilarityProfile.partialS _) p = _
  rw [SimilarityProfile.partialS_partialS_pullback hh hh1 hp
    (hf n (by have := Finset.mem_range.mp hn; omega))]
  rw [show b + slowOrder h n - 2 = b - 2 + slowOrder h n by ring]
end NavierStokes.SlowExpansionResidual
end
end

-- REPLAY NavierStokes.SlowRecursion.parameterDerivative_value 923 944
run_cmd IO.println "BLOCK NavierStokes.SlowRecursion.parameterDerivative_value"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.SlowRecursion
open Set Filter
open scoped Topology ContDiff
#count_heartbeats in
theorem parameterDerivative_value_S {R : ℝ} (hR : 0 < R) {U : Set ℂ} (hU : IsOpen U)
    (F : AxisFunction R U) {X eta : ℝ} (hX : X ∈ Ioo (0 : ℝ) (R ^ 2))
    (heta : (eta : ℂ) ∈ U) :
    complexProfile (parameterDerivative hU F) (X, (eta : ℂ)) =
      (SimilarityProfile.partialEta (profile F) (X, eta) : ℂ) := by
  have hr := sqrt_mem hR ⟨hX.1.le, hX.2⟩
  have hdC := ((F.2.holomorphic _ hr).differentiableAt (hU.mem_nhds heta)).hasDerivAt
  have hdR := PositiveAxisSystem.hasDerivAt_parameterProfile
    ((profile_contDiffAt hR hU F hX heta).differentiableAt (by simp))
  apply Complex.ext
  · exact hdC.real_of_complex.deriv.symm.trans hdR.deriv
  · exact parameterDerivative_real hU F hr heta
end NavierStokes.SlowRecursion
end
end

-- REPLAY NavierStokes.SlowRecursion.radialDerivative_value 948 972
run_cmd IO.println "BLOCK NavierStokes.SlowRecursion.radialDerivative_value"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.SlowRecursion
open Set Filter
open scoped Topology ContDiff
#count_heartbeats in
theorem radialDerivative_value_S {R : ℝ} (hR : 0 < R) {U : Set ℂ} (hU : IsOpen U)
    (F : AxisFunction R U) {X eta : ℝ} (hX : X ∈ Ioo (0 : ℝ) (R ^ 2))
    (heta : (eta : ℂ) ∈ U) :
    complexProfile (radialDerivative hR hU F) (X, (eta : ℂ)) =
      (SimilarityProfile.partialX (profile F) (X, eta) : ℂ) := by
  have hb := BoundaryAxisJets.axisJet_eq_ordinary_full hR hU F.2.smooth F.2.even 1 hX heta
  have hd := ((profile_contDiffAt hR hU F hX heta).differentiableAt (by simp)).hasFDerivAt.comp_hasDerivAt X
    ((hasDerivAt_id X).prodMk (hasDerivAt_const X eta))
  change HasDerivAt (fun Y => profile F (Y, eta)) (SimilarityProfile.partialX (profile F) (X, eta)) X at hd
  have he : (fun Y => F (Real.sqrt Y, (eta : ℂ))) =ᶠ[𝓝 X]
      (fun Y => (profile F (Y, eta) : ℂ)) := by
    filter_upwards [isOpen_Ioo.mem_nhds hX] with Y hY
    exact complexProfile_real hR F ⟨hY.1.le, hY.2⟩ heta
  simp only [iteratedDeriv_one, he.deriv_eq, hd.ofReal_comp.deriv] at hb
  exact hb
end NavierStokes.SlowRecursion
end
end

-- REPLAY NavierStokes.SmoothFourierData.hasDerivAt_slice 976 991
run_cmd IO.println "BLOCK NavierStokes.SmoothFourierData.hasDerivAt_slice"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.SmoothFourierData
open Set Function MeasureTheory TorusInverse
open scoped BigOperators ContDiff Interval Topology
local instance : Fact ((0 : ℝ) < 1) := ⟨by norm_num⟩
#count_heartbeats in
theorem hasDerivAt_slice_S {f : Plane → ℂ} {x y : ℝ}
    (hf : DifferentiableAt ℝ f (x, y)) :
    HasDerivAt (fun t => f (t, y)) (partialX f (x, y)) x := by
  exact hf.hasFDerivAt.comp_hasDerivAt x
    ((hasDerivAt_id x).prodMk (hasDerivAt_const x y))
end NavierStokes.SmoothFourierData
end
end

-- REPLAY NavierStokes.SmoothFourierData.partialX_smooth 995 1009
run_cmd IO.println "BLOCK NavierStokes.SmoothFourierData.partialX_smooth"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.SmoothFourierData
open Set Function MeasureTheory TorusInverse
open scoped BigOperators ContDiff Interval Topology
local instance : Fact ((0 : ℝ) < 1) := ⟨by norm_num⟩
#count_heartbeats in
theorem partialX_smooth_S {f : Plane → ℂ} (hf : ContDiff ℝ ∞ f) :
    ContDiff ℝ ∞ (partialX f) :=
  (ContinuousLinearMap.apply ℝ ℂ (1, 0)).contDiff.comp
    (hf.fderiv_right (by simp))
end NavierStokes.SmoothFourierData
end
end

-- REPLAY NavierStokes.StateMomentBalances.native_dr_lift 1013 1035
run_cmd IO.println "BLOCK NavierStokes.StateMomentBalances.native_dr_lift"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.StateMomentBalances
open Set Filter MeasureTheory CorrectionState
open scoped BigOperators ContDiff Topology
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
namespace AuxiliaryAverage
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
end AuxiliaryAverage
namespace AuxiliaryAverage
end AuxiliaryAverage
#count_heartbeats in
theorem native_dr_lift_S (r : ReconstructionData) (ε fast : ℕ → ℝ) (z t : S)
    (v : PressureStream.Plane) {F : ℕ → ℝ × S → ℝ} (hF : ∀ n, ContDiff ℝ ∞ (F n)) :
    (nativeOperators r ε fast z t v).dr (liftSlow F) = liftSlow (fun n => radialPartial (F n)) := by
  funext n x
  simp only [MeanIncrementBounds.Operators.dr, WeightedClasses.graphDerivative,
    nativeOperators, graphOperators, fderiv_liftSlow hF]
  simp [liftSlow, radialPartial, show ((0 : ℝ), (0 : S)) = (0 : ℝ × S) from rfl]
end NavierStokes.StateMomentBalances
end
end

