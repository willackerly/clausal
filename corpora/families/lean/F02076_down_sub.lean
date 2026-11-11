import Tool
import F2076
import NavierStokes.ActualBasePressureBounds
import NavierStokes.ActualPhysicalStageBounds
import NavierStokes.BaseResidual
import NavierStokes.ConstructedSlowBase
import NavierStokes.GenericSupportLocalSummation
import NavierStokes.GenericTupleRealization
import NavierStokes.MixedDiagonalResidual
import Mathlib.Util.CountHeartbeats
set_option Elab.async false  -- so that #count_heartbeats includes the proof

-- REPLAY NavierStokes.GenericTupleRealization.Result.flat_residual_support_local 14 66
run_cmd IO.println "BLOCK NavierStokes.GenericTupleRealization.Result.flat_residual_support_local"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.GenericTupleRealization
open Set Filter ProblemStatement GenericDifferentialPolynomial DiagonalResidual
open GenericRealizationBounds GenericRealization GenericSolenoidalRealization
open scoped Topology ContDiff BigOperators
#count_heartbeats in
theorem Result.flat_residual_support_local_R {κ : Type*} {U : Set SpaceTime} {q : SpaceTime → ℝ}
    {u0 : VelocityField} {s0 : κ → PressureField} {A B : ℕ → VelocityField}
    {R : κ → ℕ → PressureField} {g L : ℕ → ℝ} {a : ℕ → ℕ}
    (H : Result U q u0 s0 A B R g L a) (hU : IsOpen U)
    (hq : ∀ w ∈ U, 0 < q w ∧ q w ≤ 1)
    (hu0 : ContDiffOn ℝ ∞ u0 U) (hs0 : ∀ k, ContDiffOn ℝ ∞ (s0 k) U)
    (hA : ∀ j, 1 ≤ j → ContDiffOn ℝ ∞ (A j) U)
    (hB : ∀ j, 1 ≤ j → ContDiffOn ℝ ∞ (B j) U)
    (hR : ∀ k j, 1 ≤ j → ContDiffOn ℝ ∞ (R k j) U)
    (hgtop : Tendsto g atTop atTop) (P : SupportedPolynomial SpaceTime (Fin 3 ⊕ κ))
    (hconst : ContDiffOn ℝ ∞ P.constant U)
    (region : ((SpaceTime → ℝ) × Expression SpaceTime (Fin 3 ⊕ κ) Empty) → Set SpaceTime)
    (hc : ∀ t ∈ P.terms, ∀ x ∈ U, x ∈ region t → ContDiffAt ℝ ∞ t.1 x)
    (Lc : ((SpaceTime → ℝ) × Expression SpaceTime (Fin 3 ⊕ κ) Empty) → ℕ → ℝ)
    (hcg : ∀ t ∈ P.terms, ∀ m, Fam.F2076.JetRate' (scaleApproach U q ⊓ 𝓟 (region t)) q t.1 m (-Lc t m))
    (hzero : ∀ t ∈ P.terms, ∀ x ∈ U, x ∉ region t →
      t.2.eval (fun k => Empty.elim k) (components (fun j => (a j : ℝ)) q u0 s0 A B R)
        =ᶠ[𝓝 x] (fun _ => 0))
    (hszero : ∀ t ∈ P.terms, ∀ J x, x ∈ U → x ∉ region t →
      t.2.eval (fun k => Empty.elim k) (stageComponents u0 s0 A B R J)
        =ᶠ[𝓝 x] (fun _ => 0))
    (rho : ℕ → ℝ) (hrho : Tendsto rho atTop atTop) (Lres : ℕ → ℝ)
    (hres : ∀ J m, Fam.F2076.JetRate' (scaleApproach U q) q
      (P.eval (stageComponents u0 s0 A B R J)) m (rho J - Lres m)) (m : ℕ) (N : ℝ) :
    ∃ δ C : ℝ, 0 < δ ∧ 0 < C ∧ ∀ x ∈ U, 0 < q x → q x < δ →
      ‖iteratedFDeriv ℝ m (P.eval (components (fun j => (a j : ℝ)) q u0 s0 A B R)) x‖ ≤ C * q x ^ N := by
  have hlU := eventually_domain U q
  have hlq := hlU.mono fun w hw => hq w hw
  have hu : ∀ i, ContDiffOn ℝ ∞ (components (fun j => (a j : ℝ)) q u0 s0 A B R i) U := by
    intro i
    cases i with
    | inl i => exact (EuclideanSpace.proj i).contDiff.comp_contDiffOn H.smooth_velocity
    | inr k => exact H.smooth_scalars k
  have hus : ∀ J i, ContDiffOn ℝ ∞ (stageComponents u0 s0 A B R J i) U := by
    intro J i
    cases i with
    | inl i => exact (EuclideanSpace.proj i).contDiff.comp_contDiffOn (positiveStage_smooth hU hu0 hA hB J)
    | inr k => exact stage_smooth (hs0 k) (hR k) J
  have hgain : Tendsto (fun J => g (J + 1) / 2) atTop atTop :=
    (hgtop.comp (tendsto_add_atTop_nat 1)).atTop_div_const (by norm_num)
  exact uniform_bound_of_rate (P.flat_of_support_local_coefficients hU hlU hlq hu hus hgain hrho
    (fun i => (H.approximation i).some) hconst region hc Lc hcg hzero hszero Lres hres m N)
end NavierStokes.GenericTupleRealization
end
end

-- REPLAY NavierStokes.GenericTupleRealization.Result.flat_residual 70 122
run_cmd IO.println "BLOCK NavierStokes.GenericTupleRealization.Result.flat_residual"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.GenericTupleRealization
open Set Filter ProblemStatement DiagonalResidual GenericRealizationBounds GenericDifferentialPolynomial
open GenericSolenoidalRealization GenericRealization
open scoped Topology ContDiff BigOperators
#count_heartbeats in
theorem Result.flat_residual_R {κ : Type*} {U : Set SpaceTime} {q : SpaceTime → ℝ}
    {u0 : VelocityField} {s0 : κ → PressureField} {A B : ℕ → VelocityField}
    {R : κ → ℕ → PressureField} {g L : ℕ → ℝ} {a : ℕ → ℕ}
    (H : Result U q u0 s0 A B R g L a) (hU : IsOpen U)
    (hq : ∀ w ∈ U, 0 < q w ∧ q w ≤ 1)
    (hu0 : ContDiffOn ℝ ∞ u0 U) (hs0 : ∀ k, ContDiffOn ℝ ∞ (s0 k) U)
    (hA : ∀ j, 1 ≤ j → ContDiffOn ℝ ∞ (A j) U)
    (hB : ∀ j, 1 ≤ j → ContDiffOn ℝ ∞ (B j) U)
    (hR : ∀ k j, 1 ≤ j → ContDiffOn ℝ ∞ (R k j) U)
    (hgtop : Tendsto g atTop atTop) (P : SupportedPolynomial SpaceTime (Fin 3 ⊕ κ))
    (hconst : ContDiffOn ℝ ∞ P.constant U)
    (hc : ∀ t ∈ P.terms, ContDiffOn ℝ ∞ t.1 U)
    (region : ((SpaceTime → ℝ) × Expression SpaceTime (Fin 3 ⊕ κ) Empty) → Set SpaceTime)
    (Lc : ((SpaceTime → ℝ) × Expression SpaceTime (Fin 3 ⊕ κ) Empty) → ℕ → ℝ)
    (hcg : ∀ t ∈ P.terms, ∀ m, Fam.F2076.JetRate' (scaleApproach U q ⊓ 𝓟 (region t)) q t.1 m (-Lc t m))
    (hzero : ∀ t ∈ P.terms, ∀ x ∈ U, x ∉ region t →
      t.2.eval (fun k => Empty.elim k) (components (fun j => (a j : ℝ)) q u0 s0 A B R)
        =ᶠ[𝓝 x] (fun _ => 0))
    (hszero : ∀ t ∈ P.terms, ∀ J x, x ∈ U → x ∉ region t →
      t.2.eval (fun k => Empty.elim k) (stageComponents u0 s0 A B R J)
        =ᶠ[𝓝 x] (fun _ => 0))
    (rho : ℕ → ℝ) (hrho : Tendsto rho atTop atTop) (Lres : ℕ → ℝ)
    (hres : ∀ J m, Fam.F2076.JetRate' (scaleApproach U q) q
      (P.eval (stageComponents u0 s0 A B R J)) m (rho J - Lres m)) (m : ℕ) (N : ℝ) :
    ∃ δ C : ℝ, 0 < δ ∧ 0 < C ∧ ∀ x ∈ U, 0 < q x → q x < δ →
      ‖iteratedFDeriv ℝ m (P.eval (components (fun j => (a j : ℝ)) q u0 s0 A B R)) x‖ ≤ C * q x ^ N := by
  have hlU := eventually_domain U q
  have hlq := hlU.mono fun w hw => hq w hw
  have hu : ∀ i, ContDiffOn ℝ ∞ (components (fun j => (a j : ℝ)) q u0 s0 A B R i) U := by
    intro i
    cases i with
    | inl i => exact (EuclideanSpace.proj i).contDiff.comp_contDiffOn H.smooth_velocity
    | inr k => exact H.smooth_scalars k
  have hus : ∀ J i, ContDiffOn ℝ ∞ (stageComponents u0 s0 A B R J i) U := by
    intro J i
    cases i with
    | inl i => exact (EuclideanSpace.proj i).contDiff.comp_contDiffOn (positiveStage_smooth hU hu0 hA hB J)
    | inr k => exact stage_smooth (hs0 k) (hR k) J
  have hgain : Tendsto (fun J => g (J + 1) / 2) atTop atTop :=
    (hgtop.comp (tendsto_add_atTop_nat 1)).atTop_div_const (by norm_num)
  exact uniform_bound_of_rate (P.flat_of_local_coefficients hU hlU hlq hu hus hgain hrho
    (fun i => (H.approximation i).some) hconst hc region Lc hcg hzero hszero Lres hres m N)
end NavierStokes.GenericTupleRealization
end
end

-- REPLAY NavierStokes.ActualPhysicalStageBounds.initialIncrement_rate 126 182
run_cmd IO.println "BLOCK NavierStokes.ActualPhysicalStageBounds.initialIncrement_rate"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ActualPhysicalStageBounds
open Set Function Filter ProblemStatement DiagonalResidual
open scoped Topology ContDiff BigOperators
section JetAlgebra
variable {V : Type*} [NormedAddCommGroup V] [NormedSpace ℝ V]
  {h qbig : ℝ} {f g : SpaceTime → V} {m : ℕ} {r s : ℝ}
end JetAlgebra
section Increments
variable {h : ℝ}
  {DP DS : Type} [NormedAddCommGroup DP] [NormedSpace ℝ DP]
  [NormedAddCommGroup DS] [NormedSpace ℝ DS] {IP KP IS KS : Type*}
end Increments
namespace CycleInputs
variable {h : ℝ}
  {DP DS : Type} [NormedAddCommGroup DP] [NormedSpace ℝ DP]
  [NormedAddCommGroup DS] [NormedSpace ℝ DS] {IP KP IS KS : Type*}
  (D : CycleInputs h DP IP KP DS IS KS)
end CycleInputs
namespace CycleInputs
variable {h κ qbig : ℝ}
  {DP DS : Type} [NormedAddCommGroup DP] [NormedSpace ℝ DP]
  [NormedAddCommGroup DS] [NormedSpace ℝ DS] {IP KP IS KS : Type*}
  (D : CycleInputs h DP IP KP DS IS KS)
end CycleInputs
section RawTransfer
variable {V : Type*} [NormedAddCommGroup V] [NormedSpace ℝ V]
  {h qbig : ℝ} {f g : SpaceTime → V} {m : ℕ} {r : ℝ}
end RawTransfer
namespace CycleInputs
variable {h κ qbig : ℝ}
  {DP DS : Type} [NormedAddCommGroup DP] [NormedSpace ℝ DP]
  [NormedAddCommGroup DS] [NormedSpace ℝ DS] {IP KP IS KS : Type*}
  (D : CycleInputs h DP IP KP DS IS KS)
end CycleInputs
open InitializedPhysicalBackground (seedPotentialLoss seedDirectLoss initialLoss)
section InitialIncrement
variable {h : ℝ} {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D] {I K : Type*}
#count_heartbeats in
theorem initialIncrement_rate_R (W : PhysicalStageBounds.WaveData h D I K (Fin 3))
    (MT MR : MeanInput h (CoordinateAlgebra.A h - 1 / 2))
    (hh : 0 < h) (hh1 : h < 1 / 2) {qbig : ℝ} (hqbig : 0 < qbig)
    (hqT : qbig ≤ ChartScales.Q MT.firstBand) (hqR : qbig ≤ ChartScales.Q MR.firstBand) (m : ℕ) :
    Fam.F2076.JetRate' ActualBaseVelocityBounds.endpoint (PhysicalWaveSum.physicalQ h)
      (initialIncrement W MT MR) m
      (-seedPotentialLoss h W.alpha W.shift (min MT.alpha MR.alpha) m) := by
  obtain ⟨C, hC, hb⟩ := initialIncrement_bound W MT MR hh hh1 hqT hqR m
  refine ⟨C, hC, ?_⟩
  filter_upwards [InitializedPhysicalBackground.endpoint_sublevel hh hh1 hqbig,
    ActualBaseVelocityBounds.endpoint_q_small hh hh1] with w hw hqw
  exact hb w hw hqw.2
end InitialIncrement
end NavierStokes.ActualPhysicalStageBounds
end
end

-- REPLAY NavierStokes.ConstructedSlowBase.modified_jetRate 186 223
run_cmd IO.println "BLOCK NavierStokes.ConstructedSlowBase.modified_jetRate"
section
set_option linter.all false
noncomputable section
open Set Filter Function
open scoped ContDiff Topology BigOperators
namespace NavierStokes.ConstructedSlowBase
open GlobalSlowProfiles AssembledSlowBase SlowBorelBase
section RepairedFamily
variable {S : Set ℝ} {h C rho inner : ℝ} {U : Set ℂ}
  {base : Fin 5 → SimilarityProfile.InnerProfile} {s : Scheme S h C}
  {A : SlowRecursion.LocalHierarchy rho U h C base}
  (L : Localization s A inner) (B0 : BaseAgreement s A inner)
  (Z0 : ZeroOrderSolved s inner) (hI : Icc (-1 : ℝ) 1 ⊆ S)
end RepairedFamily
section Nominal
variable {F : OutgoingProfile.Profile} (W : NominalProfile.Witness F)
include W
end Nominal
section Modified
variable {F : OutgoingProfile.Profile} (W : NominalProfile.Witness F)
  {D : ProfileHistories.RadialDomain} (Q : ProfileHistories.Profiles D)
  {S : Set ℝ} {lo hi : ℝ} (M : FiniteModification W Q S lo hi)
include M
#count_heartbeats in
theorem modified_jetRate_R {l : Filter ProblemStatement.SpaceTime} {a : ℕ → ℕ} {upper : ℝ}
    (P : BaseResidual.PhysicalApproach l F.data.h 0 upper)
    (ha : AdmissibleScales F.data.h
      (coefficientBundle W.axis.normalization (modifiedCoefficients W Q M)) (innerBox 0 upper) a)
    (m : ℕ) (n : ℝ) (hn : 0 ≤ n) :
    Fam.F2076.JetRate' l (fun z => (cartesianChart F.data.h z).1)
      (BaseResidual.baseResidual a F.data.h W.axis.normalization (modifiedCoefficients W Q M)) m n :=
  repaired_jetRate (modifiedLocalization W Q M) (modifiedBaseAgreement W Q M)
    (modifiedZeroOrder W Q M) M.contains (height_pos W) (height_lt_half W) P ha
    (modified_finiteIdentities W Q M) m n hn
end Modified
end NavierStokes.ConstructedSlowBase
end
end

-- REPLAY NavierStokes.BaseResidual.finiteRate_fderiv 227 265
run_cmd IO.println "BLOCK NavierStokes.BaseResidual.finiteRate_fderiv"
section
set_option linter.all false
noncomputable section
open Set Filter Function
open scoped Topology ContDiff BigOperators
namespace NavierStokes.BaseResidual
open SlowBorelBase
section Axis
variable {V : Type} [NormedAddCommGroup V] [NormedSpace ℝ V]
end Axis
section Monomials
open PhysicalCoordinateBounds
end Monomials
section CartesianMonomials
open ProblemStatement
end CartesianMonomials
section FixedPrefixRates
open ProblemStatement DiagonalResidual
end FixedPrefixRates
section RateAlgebra
open DiagonalResidual
variable {D E F G : Type}
  [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup F] [NormedSpace ℝ F]
  [NormedAddCommGroup G] [NormedSpace ℝ G]
#count_heartbeats in
theorem finiteRate_fderiv_R {l : Filter D} {q : D → ℝ} {f : D → E} {M : ℕ} {r : ℝ}
    (hf : Fam.F2076.FiniteJetRate' l q f (M + 1) r) :
    Fam.F2076.FiniteJetRate' l q (fderiv ℝ f) M r := by
  obtain ⟨C, hC, hb⟩ := hf
  refine ⟨C, hC, hb.mono ?_⟩
  intro x hx m hm
  rw [norm_iteratedFDeriv_fderiv]
  exact hx (m + 1) (Nat.add_le_add_right hm 1)
end RateAlgebra
end NavierStokes.BaseResidual
end
end

-- REPLAY NavierStokes.BaseResidual.cartesian_prefix_growth 269 330
run_cmd IO.println "BLOCK NavierStokes.BaseResidual.cartesian_prefix_growth"
section
set_option linter.all false
noncomputable section
open Set Filter Function
open scoped Topology ContDiff BigOperators
namespace NavierStokes.BaseResidual
open SlowBorelBase
section Axis
variable {V : Type} [NormedAddCommGroup V] [NormedSpace ℝ V]
end Axis
section Monomials
open PhysicalCoordinateBounds
end Monomials
section CartesianMonomials
open ProblemStatement
end CartesianMonomials
section FixedPrefixRates
open ProblemStatement DiagonalResidual
end FixedPrefixRates
section RateAlgebra
open DiagonalResidual
variable {D E F G : Type}
  [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup F] [NormedSpace ℝ F]
  [NormedAddCommGroup G] [NormedSpace ℝ G]
end RateAlgebra
section PotentialRates
open ProblemStatement DiagonalResidual
end PotentialRates
section CurlRates
open ProblemStatement DiagonalResidual ResidualStability
end CurlRates
section PrefixGrowth
open ProblemStatement DiagonalResidual SlowExpansionResidual
#count_heartbeats in
theorem cartesian_prefix_growth_R {l : Filter SpaceTime} {h lo hi : ℝ}
    (hh : 0 < h) (hh1 : h < 1 / 2) (A : PhysicalApproach l h lo hi)
    {f : ℕ → Inner → ℝ} (hf : ∀ j, ContDiff ℝ ∞ (f j)) (b : ℝ) (J M : ℕ) :
    Fam.F2076.FiniteJetRate' l (fun z => (cartesianChart h z).1) (cartesianUncutPrefix h b f J)
      M (b - M) := by
  have hq := A.positive_small hh hh1
  apply finiteJetRate_of_jetRate (hq.mono (fun _ hz => hz.1))
  intro m hm
  obtain ⟨C, hC, hb⟩ := cartesian_finite_monomials_bound hh hh1 isOpen_univ
    (innerBox_isCompact lo hi) (subset_univ _) (fun i : Fin (J + 1) => f i)
    (fun i => (hf i).contDiffOn) (fun i => b + slowOrder h i) b lo hi
    (fun i => le_add_of_nonneg_right (by unfold slowOrder; positivity)) A.compact m
  have hr : Fam.F2076.JetRate' l (fun z => (cartesianChart h z).1)
      (fun z => ∑ i : Fin (J + 1), cartesianMonomial h (b + slowOrder h i) (f i) z)
      m (b - m) := by
    refine ⟨C, hC.le, ?_⟩
    filter_upwards [A.in_carrier, A.past, A.radial, hq] with z hz ht hX hqz
    exact hb z hz ht hqz.2 hX (physicalChart_inner_mem hh hh1 ht hX)
  have he := hr.congr_on past_isOpen
    (A.past.mono (fun _ ht => ⟨ht, mem_univ _⟩))
    (fun z hz => (cartesianUncutPrefix_eq_sum hh hh1 b f J hz.1).symm)
  exact he.weaken hq (sub_le_sub_left (by exact_mod_cast hm) b)
end PrefixGrowth
end NavierStokes.BaseResidual
end
end

-- REPLAY NavierStokes.ActualBasePressureBounds.pressure_rate 334 365
run_cmd IO.println "BLOCK NavierStokes.ActualBasePressureBounds.pressure_rate"
section
set_option linter.all false
noncomputable section
open Set Filter Function
open scoped Topology ContDiff
namespace NavierStokes.ActualBasePressureBounds
open ProblemStatement SlowBorelBase BaseResidual DiagonalResidual ActualBaseVelocityBounds
section Actual
variable {F : OutgoingProfile.Profile} {W : NominalProfile.Witness F}
  (H : NominalConeAssembly.Certificate W) {ld : ModulatedProfileAssembly.LoopData W}
  (v : ModulatedProfileAssembly.Witness ld)
#count_heartbeats in
theorem pressure_rate_R (upper : ℝ) (B m : ℕ) :
    Fam.F2076.JetRate' endpoint (PhysicalWaveSum.physicalQ F.data.h) (FinalSlowBase.pressure H v upper B)
      m (-pressureLoss m) := by
  apply pressure_rate_of_heat H v upper B m
  intro l hl hR
  obtain ⟨C, hC, hb⟩ := WholeDomainHeatBounds.heat_pressure_bound
    (BaseExterior.nominalHeatNormalization W) F.data.h_pos F.data.h_lt_half
    (BaseExterior.nominalExteriorRadius_pos W) m
  refine ⟨C, hC, ?_⟩
  filter_upwards [endpoint_past.filter_mono hl,
    (endpoint_q_small F.data.h_pos F.data.h_lt_half).filter_mono hl, hR] with w hw hq hRw
  exact (hb w hw hq.2 hRw).trans (mul_le_mul_of_nonneg_left
    (Real.rpow_le_rpow_of_exponent_ge hq.1 hq.2 (by
      unfold pressureLoss WholeDomainHeatBounds.heatLoss
      have hm : 0 ≤ (m : ℝ) := by positivity
      linarith)) hC)
end Actual
end NavierStokes.ActualBasePressureBounds
end
end

-- REPLAY NavierStokes.BaseResidual.finiteRate_mono 369 403
run_cmd IO.println "BLOCK NavierStokes.BaseResidual.finiteRate_mono"
section
set_option linter.all false
noncomputable section
open Set Filter Function
open scoped Topology ContDiff BigOperators
namespace NavierStokes.BaseResidual
open SlowBorelBase
section Axis
variable {V : Type} [NormedAddCommGroup V] [NormedSpace ℝ V]
end Axis
section Monomials
open PhysicalCoordinateBounds
end Monomials
section CartesianMonomials
open ProblemStatement
end CartesianMonomials
section FixedPrefixRates
open ProblemStatement DiagonalResidual
end FixedPrefixRates
section RateAlgebra
open DiagonalResidual
variable {D E F G : Type}
  [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup F] [NormedSpace ℝ F]
  [NormedAddCommGroup G] [NormedSpace ℝ G]
#count_heartbeats in
theorem finiteRate_mono_R {l : Filter D} {q : D → ℝ} {f : D → E} {M N : ℕ} {r : ℝ}
    (hf : Fam.F2076.FiniteJetRate' l q f M r) (hNM : N ≤ M) : Fam.F2076.FiniteJetRate' l q f N r := by
  obtain ⟨C, hC, hb⟩ := hf
  exact ⟨C, hC, hb.mono (fun x hx m hm => hx m (hm.trans hNM))⟩
end RateAlgebra
end NavierStokes.BaseResidual
end
end

-- REPLAY NavierStokes.BaseResidual.stressForce_rate 407 515
run_cmd IO.println "BLOCK NavierStokes.BaseResidual.stressForce_rate"
section
set_option linter.all false
noncomputable section
open Set Filter Function
open scoped Topology ContDiff BigOperators
namespace NavierStokes.BaseResidual
open SlowBorelBase
section Axis
variable {V : Type} [NormedAddCommGroup V] [NormedSpace ℝ V]
end Axis
section Monomials
open PhysicalCoordinateBounds
end Monomials
section CartesianMonomials
open ProblemStatement
end CartesianMonomials
section FixedPrefixRates
open ProblemStatement DiagonalResidual
end FixedPrefixRates
section RateAlgebra
open DiagonalResidual
variable {D E F G : Type}
  [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup F] [NormedSpace ℝ F]
  [NormedAddCommGroup G] [NormedSpace ℝ G]
end RateAlgebra
section PotentialRates
open ProblemStatement DiagonalResidual
end PotentialRates
section CurlRates
open ProblemStatement DiagonalResidual ResidualStability
end CurlRates
section PrefixGrowth
open ProblemStatement DiagonalResidual SlowExpansionResidual
end PrefixGrowth
section ProfileDerivatives
open ProblemStatement DiagonalResidual
end ProfileDerivatives
section AnnularFactors
open ProblemStatement DiagonalResidual
end AnnularFactors
section StressOperator
open ProblemStatement DiagonalResidual
#count_heartbeats in
theorem stressForce_rate_R {l : Filter SpaceTime} {h lo hi : ℝ}
    (hh : 0 < h) (hh1 : h < 1 / 2) (A : PhysicalApproach l h lo hi) (hlo : 0 < lo)
    {theta axial : Chart → ℝ} (ht : ContDiffOn ℝ ∞ theta profilePast)
    (ha : ContDiffOn ℝ ∞ axial profilePast) (M : ℕ) (r : ℝ)
    (htv : Fam.F2076.FiniteJetRate' l (fun z => (cartesianChart h z).1) (liftProfile theta) M r)
    (hav : Fam.F2076.FiniteJetRate' l (fun z => (cartesianChart h z).1) (liftProfile axial) M r)
    (htd : Fam.F2076.FiniteJetRate' l (fun z => (cartesianChart h z).1)
      (cartesianDerivative (0, (1, 0)) theta) M r)
    (had : Fam.F2076.FiniteJetRate' l (fun z => (cartesianChart h z).1)
      (cartesianDerivative (0, (1, 0)) axial) M r) :
    Fam.F2076.FiniteJetRate' l (fun z => (cartesianChart h z).1) (stressForce theta axial)
      M (r - 1 - M) := by
  have hq := A.positive_small hh hh1
  have hq0 := hq.mono (fun _ hx => hx.1)
  have hU := annularPast_isOpen
  have hlU := A.in_annularPast hh hh1 hlo
  have hts := (liftProfile_smooth ht).mono annularPast_subset
  have has := (liftProfile_smooth ha).mono annularPast_subset
  have htds := (cartesianDerivative_smooth ht (0, (1, 0))).mono annularPast_subset
  have hads := (cartesianDerivative_smooth ha (0, (1, 0))).mono annularPast_subset
  have hr0 := radialPower_rate hh hh1 A hlo (-1) M
  have hrp := finiteRate_weaken (radialPower_rate hh hh1 A hlo (1 / 2) M) hq
    (show -1 - (M : ℝ) ≤ 1 / 2 - M by linarith)
  have hrn := finiteRate_weaken (radialPower_rate hh hh1 A hlo (-(1 / 2)) M) hq
    (show -1 - (M : ℝ) ≤ -(1 / 2) - M by linarith)
  have hpt := finiteRate_bilinear hr0 htv hU hlU hq0 (radialPower_smooth (-1)) hts
    (ContinuousLinearMap.mul ℝ ℝ)
  have hpa := finiteRate_bilinear hrp had hU hlU hq0 (radialPower_smooth (1 / 2)) hads
    (ContinuousLinearMap.mul ℝ ℝ)
  have hqa := finiteRate_bilinear hrn hav hU hlU hq0 (radialPower_smooth (-(1 / 2))) has
    (ContinuousLinearMap.mul ℝ ℝ)
  have hexp : -1 - (M : ℝ) + r = r - 1 - M := by ring
  rw [hexp] at hpt hpa hqa
  have hpt2 := scalarConst_rate hpt hU hlU ((radialPower_smooth (-1)).mul hts) 2
  have hdt := finiteRate_weaken htd hq (show r - 1 - M ≤ r by
    have := Nat.cast_nonneg (α := ℝ) M; linarith)
  have hs0 := scalarConst_rate (finiteRate_add hdt hpt2 hU hlU htds
    (contDiffOn_const.mul ((radialPower_smooth (-1)).mul hts))) hU hlU
    (htds.add (contDiffOn_const.mul ((radialPower_smooth (-1)).mul hts))) (-2)
  have hs1 := scalarConst_rate (finiteRate_add hpa hqa hU hlU
    ((radialPower_smooth (1 / 2)).mul hads) ((radialPower_smooth (-(1 / 2))).mul has)) hU hlU
    (((radialPower_smooth (1 / 2)).mul hads).add ((radialPower_smooth (-(1 / 2))).mul has)) (-1)
  have hsc0 : ContDiffOn ℝ ∞ (stressAngularScalar theta) annularPast :=
    contDiffOn_const.mul (htds.add ((contDiffOn_const.mul (radialPower_smooth (-1))).mul hts))
  have hsc1 : ContDiffOn ℝ ∞ (stressAxialScalar axial) annularPast :=
    (((radialPower_smooth (1 / 2)).mul hads).add ((radialPower_smooth (-(1 / 2))).mul has)).neg
  have hs0' : Fam.F2076.FiniteJetRate' l (fun z => (cartesianChart h z).1) (stressAngularScalar theta)
      M (r - 1 - M) := by
        convert! hs0 using 1
        funext z
        change -2 * (_ + 2 * radialPower (-1) z * liftProfile theta z) = -2 * (_ + 2 * (_ * _))
        ring
  have hs1' : Fam.F2076.FiniteJetRate' l (fun z => (cartesianChart h z).1) (stressAxialScalar axial)
      M (r - 1 - M) := by
    simp only [neg_one_mul] at hs1 ⊢
    exact hs1
  have hb := potentialFromScalars_rate hU hlU hq0 A.compact A.in_carrier hsc0 hsc1 hs0' hs1'
  apply finiteRate_congr_on hb hU hlU
  intro z hz
  exact (stressForce_eq_scalars theta axial hz.2).symm
end StressOperator
end NavierStokes.BaseResidual
end
end

-- REPLAY NavierStokes.MixedDiagonalResidual.exists_physical_schedule_residual_zero 519 595
run_cmd IO.println "BLOCK NavierStokes.MixedDiagonalResidual.exists_physical_schedule_residual_zero"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.MixedDiagonalResidual
open ProblemStatement Set Filter DiagonalResidual ResidualStability
open scoped Topology ContDiff BigOperators
#count_heartbeats in
theorem exists_physical_schedule_residual_zero_R {h qbig : ℝ}
    (hh : 0 < h) (hh1 : h < 1 / 2) (hqbig : 0 < qbig)
    {S : Set SpaceTime} (hSopen : IsOpen S) (hS : S ⊆ PhysicalWaveSum.preterminal)
    (hlS : ∀ᶠ z in 𝓝[SpacetimeEndpoint.openPast 1] (1, (0 : Space)), z ∈ S)
    {A B : ℕ → VelocityField} {P : ℕ → PressureField}
    (hA : ∀ j, ContDiffOn ℝ ∞ (A j) (CutStageEstimates.physicalSublevel h qbig))
    (hB : ∀ j, ContDiffOn ℝ ∞ (B j) (CutStageEstimates.physicalSublevel h qbig))
    (hP : ∀ j, ContDiffOn ℝ ∞ (P j) (CutStageEstimates.physicalSublevel h qbig))
    (g LA LB LP Lbg Lres : ℕ → ℝ) (CA CB CP pA pB pP : ℕ → ℕ → ℝ)
    (rawA : CutStageEstimates.RawStageBounds (PhysicalWaveSum.physicalQ h) A g LA CA pA
      (S ∩ CutStageEstimates.physicalSublevel h qbig))
    (rawB : CutStageEstimates.RawStageBounds (PhysicalWaveSum.physicalQ h) B g LB CB pB
      (S ∩ CutStageEstimates.physicalSublevel h qbig))
    (rawP : CutStageEstimates.RawStageBounds (PhysicalWaveSum.physicalQ h) P g LP CP pP
      (S ∩ CutStageEstimates.physicalSublevel h qbig))
    (hg0 : 0 ≤ g 0) (hg : ∀ j, 1 ≤ j → 0 < g j)
    (hgmono : Monotone g) (hgtop : Tendsto g atTop atTop)
    (hbg : ∀ J m, Fam.F2076.JetRate' (𝓝[SpacetimeEndpoint.openPast 1] (1, (0 : Space)))
      (PhysicalWaveSum.physicalQ h) (uncutVelocity A B J) m (-Lbg m))
    (hres : ∀ J m, Fam.F2076.JetRate' (𝓝[SpacetimeEndpoint.openPast 1] (1, (0 : Space)))
      (PhysicalWaveSum.physicalQ h)
      (fun z => navierStokesResidual (uncutVelocity A B J)
        (DiagonalJetBounds.uncutPrefix P (J + 1)) z.1 z.2) m (g J - Lres m))
    (lower : ℕ) :
    ∃ a : ℕ → ℕ, lower ≤ a 0 ∧ (∀ j, 0 < a j) ∧
      (∀ j, 2 * a j ≤ a (j + 1)) ∧ StrictMono a ∧
      Tendsto (fun j => (a j : ℝ)) atTop atTop ∧
      (∀ j, 1 / (a j : ℝ) < qbig) ∧
      MixedDiagonalSchedule.ThreeCutBounds a h A B P (fun j => g j / 2)
        (MixedDiagonalSchedule.commonLoss LA LB LP) S ∧
      MixedDiagonalSchedule.ThreeSmoothSums a h A B P ∧
      JointResidualLimits.VanishingJointJets
        (residual (fun j => (a j : ℝ)) (PhysicalWaveSum.physicalQ h) A B P) := by
  obtain ⟨a, hal, hap, had, ham, hat, hrecip, hb, hs⟩ :=
    MixedDiagonalSchedule.exists_three_component_local_schedule hh hh1 hqbig hS
      hA hB hP g LA LB LP CA CB CP pA pB pP rawA rawB rawP hg lower
  refine ⟨a, hal, hap, had, ham, hat, hrecip, hb, hs, ?_⟩
  let U := S ∩ CutStageEstimates.physicalSublevel h qbig
  have hU : IsOpen U := hSopen.inter (CutStageEstimates.physicalSublevel_open hh hh1 qbig)
  have hUp : U ⊆ PhysicalWaveSum.preterminal := fun _ hx => hS hx.1
  have hqzero := AnnularEndpoint.physicalQ_tendsto_zero hh hh1 (x := (0 : Space)) rfl
  have hlU : ∀ᶠ z in 𝓝[SpacetimeEndpoint.openPast 1] (1, (0 : Space)), z ∈ U := by
    filter_upwards [hlS, hqzero.eventually (gt_mem_nhds hqbig)] with z hz hqz
    exact ⟨hz, hS hz, hqz⟩
  have hlq : ∀ᶠ z in 𝓝[SpacetimeEndpoint.openPast 1] (1, (0 : Space)),
      0 < PhysicalWaveSum.physicalQ h z ∧ PhysicalWaveSum.physicalQ h z ≤ 1 := by
    filter_upwards [hlS, hqzero.eventually (gt_mem_nhds (show (0 : ℝ) < 1 by norm_num))]
      with z hz hqz
    exact ⟨PhysicalWaveSum.physicalQ_pos hh hh1 (hS hz), hqz.le⟩
  have hhalfmono : Monotone (fun j => g j / 2) := by
    intro i j hij
    exact div_le_div_of_nonneg_right (hgmono hij) (by norm_num)
  have hhalftop : Tendsto (fun j => g j / 2) atTop atTop := by
    apply tendsto_atTop.2
    intro r
    filter_upwards [hgtop.eventually (eventually_ge_atTop (2 * r))] with j hj
    linarith
  have hnonneg (J : ℕ) : 0 ≤ g J := hg0.trans (hgmono (Nat.zero_le J))
  apply physical_vanishingJointJets (Lbg := Lbg) (Lres := Lres) hh hh1 hat hU hUp hlU
    (fun j => (hA j).mono inter_subset_right)
    (fun j => (hB j).mono inter_subset_right)
    (fun j => (hP j).mono inter_subset_right) hhalfmono hhalftop
    (fun j hj m hm z hz => hb.potential j hj m hm z hz.1)
    (fun j hj m hm z hz => hb.direct j hj m hm z hz.1)
    (fun j hj m hm z hz => hb.pressure j hj m hm z hz.1) hbg
  intro J m
  exact (hres J m).weaken hlq (by linarith [hnonneg J])
end NavierStokes.MixedDiagonalResidual
end
end

