import Tool
import F2076
import NavierStokes.ActualBaseVelocityBounds
import NavierStokes.ActualPhysicalStageBounds
import NavierStokes.BaseResidual
import NavierStokes.DiagonalResidual
import NavierStokes.MixedDiagonalResidual
import Mathlib.Util.CountHeartbeats
set_option Elab.async false  -- so that #count_heartbeats includes the proof

-- REPLAY NavierStokes.ActualBaseVelocityBounds.actual_outer_rate 12 52
run_cmd IO.println "BLOCK NavierStokes.ActualBaseVelocityBounds.actual_outer_rate"
section
set_option linter.all false
noncomputable section
open Set Filter Function
open scoped Topology ContDiff BigOperators
namespace NavierStokes.ActualBaseVelocityBounds
open ProblemStatement SlowBorelBase BaseResidual DiagonalResidual
section Actual
variable {F : OutgoingProfile.Profile} {W : NominalProfile.Witness F}
  (H : NominalConeAssembly.Certificate W) {ld : ModulatedProfileAssembly.LoopData W}
  (v : ModulatedProfileAssembly.Witness ld)
#count_heartbeats in
theorem actual_outer_rate_R (upper : ℝ) (B : ℕ) {l : Filter SpaceTime}
    (hl : l ≤ endpoint)
    (houter : ∀ᶠ z in l, AssembledSlowBase.nominalOuterX W < (cartesianChart F.data.h z).2.1)
    (m : ℕ) :
    Fam.F2076.JetRate' l (PhysicalWaveSum.physicalQ F.data.h) (FinalSlowBase.velocity H v upper B)
      m (-heatLoss m) := by
  let S : Set SpaceTime := {z | (cartesianChart F.data.h z).2.1 ≤ BaseExterior.nominalExteriorRadius W}
  have hq := (endpoint_q_small F.data.h_pos F.data.h_lt_half).filter_mono hl
  apply rate_glue (S := S) (hq.mono (fun _ hz => hz.1))
  · have hl' : l ⊓ 𝓟 S ≤ endpoint := inf_le_left.trans hl
    have hR : ∀ᶠ z in l ⊓ 𝓟 S,
        (cartesianChart F.data.h z).2.1 ≤ BaseExterior.nominalExteriorRadius W := restricted_mem l S
    have hr := actual_middle_rate H v upper B hl' hR (houter.filter_mono inf_le_left) m
    exact (finiteRate_at hr le_rfl).weaken (hq.filter_mono inf_le_left)
      (heatLoss_controls_middle F.data.h_lt_half m)
  · have hl' : l ⊓ 𝓟 Sᶜ ≤ endpoint := inf_le_left.trans hl
    have hR : ∀ᶠ z in l ⊓ 𝓟 Sᶜ,
        BaseExterior.nominalExteriorRadius W < (cartesianChart F.data.h z).2.1 :=
      (restricted_mem l Sᶜ).mono (fun _ hz => lt_of_not_ge hz)
    have hr := heat_velocity_rate hl' F.data.h_pos F.data.h_lt_half
      (BaseExterior.nominalExteriorRadius_pos W) hR (BaseExterior.nominalHeatNormalization W) m
    have ha := finiteRate_congr_on hr
      (BaseExterior.cartesianExterior_isOpen F.data.h_pos F.data.h_lt_half _)
      ((endpoint_past.filter_mono hl').and hR) (FinalSlowBase.exterior_fields_eq_heat H v upper B).1.symm
    exact finiteRate_at ha le_rfl
end Actual
end NavierStokes.ActualBaseVelocityBounds
end
end

-- REPLAY NavierStokes.ActualBaseVelocityBounds.heat_velocity_rate 56 129
run_cmd IO.println "BLOCK NavierStokes.ActualBaseVelocityBounds.heat_velocity_rate"
section
set_option linter.all false
noncomputable section
open Set Filter Function
open scoped Topology ContDiff BigOperators
namespace NavierStokes.ActualBaseVelocityBounds
open ProblemStatement SlowBorelBase BaseResidual DiagonalResidual
#count_heartbeats in
theorem heat_velocity_rate_R {l : Filter SpaceTime} (hl : l ≤ endpoint)
    {h R : ℝ} (hh : 0 < h) (hh1 : h < 1 / 2) (hR : 0 < R)
    (hlR : ∀ᶠ z in l, R < (cartesianChart h z).2.1) (C : ℝ) (m : ℕ) :
    Fam.F2076.FiniteJetRate' l (PhysicalWaveSum.physicalQ h) (BaseExterior.heatVelocity C h)
      m (-heatLoss m) := by
  let q := PhysicalWaveSum.physicalQ h
  have hq := (endpoint_q_small hh hh1).filter_mono hl
  have hq0 := hq.mono (fun _ hz => hz.1)
  have hK := endpoint_compact.filter_mono hl
  have hlow : ∀ᶠ z in l, R * q z ≤ physicalEnergy z := by
    filter_upwards [hlR, hq] with z hz hqz
    exact ((lt_div_iff₀ hqz.1).mp (by simpa only [X_eq] using hz)).le
  have hlU : ∀ᶠ z in l, z ∈ positiveRadius := by
    filter_upwards [hlow, hq] with z hz hqz
    exact (mul_pos hR hqz.1).trans_le hz
  have hi := finiteRate_negative_power physicalEnergy_smooth (isCompact_closedBall _ _) hK hq
    hR hlow (p := -1) (by constructor <;> norm_num) m
  have ht := finiteRate_compact (q := q) heatTime_smooth (isCompact_closedBall _ _) hK m
  have hr : Fam.F2076.FiniteJetRate' l q heatRatio m (-powerLoss m) := by
    have he := finiteRate_mul ht hi positiveRadius_isOpen hlU hq0
      heatTime_smooth.contDiffOn (energyPower_smooth (-1))
    simp only [zero_add] at he
    exact he
  obtain ⟨A, hA, ha⟩ := extension_uniform_jets (by linarith : 1 < 1 + h) m
  have he := finiteRate_uniform_comp positiveRadius_isOpen hlU heatRatio_smooth
    (HeatProfileExtension.extension (1 + h)) (HeatProfileExtension.extension_contDiff (by linarith))
    (powerLoss_nonneg m) hA ha hq hr
  have hp := finiteRate_negative_power physicalEnergy_smooth (isCompact_closedBall _ _) hK hq
    hR hlow (p := RadialHeatProfile.spatialExponent (1 + h))
    (by unfold RadialHeatProfile.spatialExponent; constructor <;> linarith) m
  have hs := (energyPower_smooth (RadialHeatProfile.spatialExponent (1 + h))).mul
    ((HeatProfileExtension.extension_contDiff (by linarith : 1 < 1 + h)).comp_contDiffOn
      heatRatio_smooth)
  have hpe := finiteRate_mul hp he positiveRadius_isOpen hlU hq0 (energyPower_smooth _)
    ((HeatProfileExtension.extension_contDiff (by linarith : 1 < 1 + h)).comp_contDiffOn
      heatRatio_smooth)
  have hC := scalarConst_rate hpe positiveRadius_isOpen hlU hs C
  have hlow2 : ∀ᶠ z in l, (2 * R) * q z ≤ 2 * physicalEnergy z := by
    filter_upwards [hlow] with z hz
    nlinarith
  have hd := finiteRate_negative_power (contDiff_const.mul physicalEnergy_smooth)
    (isCompact_closedBall _ _) hK hq (mul_pos (by norm_num) hR) hlow2
    (p := -(1 / 2 : ℝ)) (by constructor <;> norm_num) m
  have hc : Fam.F2076.FiniteJetRate' l q (heatModelCoefficient C h) m (-heatLoss m) := by
    convert! finiteRate_mul hC hd positiveRadius_isOpen hlU hq0
      (contDiffOn_const.mul hs) (doubleEnergyPower_smooth _) using 1
    dsimp only [heatModelCoefficient, heatLoss, Function.comp_apply]
    ring
  have hv : Fam.F2076.FiniteJetRate' l q (heatModelVelocity C h) m (-heatLoss m) := by
    have he := finiteRate_bilinear hc
      (finiteRate_compact (q := q) angularVector_smooth (isCompact_closedBall _ _) hK m)
      positiveRadius_isOpen hlU hq0 (heatModelCoefficient_smooth C hh)
      angularVector_smooth.contDiffOn (ContinuousLinearMap.lsmul ℝ ℝ)
    simp only [add_zero] at he
    exact he
  apply finiteRate_congr_on hv (BaseExterior.cartesianExterior_isOpen hh hh1 R)
    (show ∀ᶠ z in l, z ∈ BaseExterior.cartesianExterior h R from
      (endpoint_past.filter_mono hl).and hlR)
  intro z hz
  have hpq := PhysicalWaveSum.physicalQ_pos hh hh1 hz.1
  have hxs : 0 < physicalEnergy z := (mul_pos hR hpq).trans
    ((lt_div_iff₀ hpq).mp (by simpa only [X_eq] using hz.2))
  exact heatModelVelocity_eq C h hz.1 hxs
end NavierStokes.ActualBaseVelocityBounds
end
end

-- REPLAY NavierStokes.ActualBaseVelocityBounds.rate_glue 133 159
run_cmd IO.println "BLOCK NavierStokes.ActualBaseVelocityBounds.rate_glue"
section
set_option linter.all false
noncomputable section
open Set Filter Function
open scoped Topology ContDiff BigOperators
namespace NavierStokes.ActualBaseVelocityBounds
open ProblemStatement SlowBorelBase BaseResidual DiagonalResidual
#count_heartbeats in
theorem rate_glue_R {D E : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    {l : Filter D} {q : D → ℝ} {f : D → E} {S : Set D} {m : ℕ} {r : ℝ}
    (hq : ∀ᶠ z in l, 0 < q z)
    (hleft : Fam.F2076.JetRate' (l ⊓ 𝓟 S) q f m r)
    (hright : Fam.F2076.JetRate' (l ⊓ 𝓟 Sᶜ) q f m r) : Fam.F2076.JetRate' l q f m r := by
  obtain ⟨A, hA, ha⟩ := hleft
  obtain ⟨B, hB, hb⟩ := hright
  refine ⟨A + B, add_nonneg hA hB, ?_⟩
  filter_upwards [hq, eventually_inf_principal.mp ha, eventually_inf_principal.mp hb]
    with z hz hza hzb
  by_cases hs : z ∈ S
  · exact (hza hs).trans (mul_le_mul_of_nonneg_right (le_add_of_nonneg_right hB)
      (Real.rpow_nonneg hz.le _))
  · exact (hzb hs).trans (mul_le_mul_of_nonneg_right (le_add_of_nonneg_left hA)
      (Real.rpow_nonneg hz.le _))
end NavierStokes.ActualBaseVelocityBounds
end
end

-- REPLAY NavierStokes.ActualBaseVelocityBounds.velocity_rate 163 192
run_cmd IO.println "BLOCK NavierStokes.ActualBaseVelocityBounds.velocity_rate"
section
set_option linter.all false
noncomputable section
open Set Filter Function
open scoped Topology ContDiff BigOperators
namespace NavierStokes.ActualBaseVelocityBounds
open ProblemStatement SlowBorelBase BaseResidual DiagonalResidual
section Actual
variable {F : OutgoingProfile.Profile} {W : NominalProfile.Witness F}
  (H : NominalConeAssembly.Certificate W) {ld : ModulatedProfileAssembly.LoopData W}
  (v : ModulatedProfileAssembly.Witness ld)
#count_heartbeats in
theorem velocity_rate_R (upper : ℝ) (B m : ℕ) :
    Fam.F2076.JetRate' endpoint (PhysicalWaveSum.physicalQ F.data.h) (FinalSlowBase.velocity H v upper B)
      m (-heatLoss m) := by
  let S : Set SpaceTime := {z | (cartesianChart F.data.h z).2.1 ≤ FinalSlowBase.boxRadius W upper}
  have hq := endpoint_q_small F.data.h_pos F.data.h_lt_half
  apply rate_glue (S := S) (hq.mono (fun _ hz => hz.1))
  · have hr := actual_bounded_rate H v upper B (show endpoint ⊓ 𝓟 S ≤ endpoint from inf_le_left)
      (show ∀ᶠ z in endpoint ⊓ 𝓟 S,
        (cartesianChart F.data.h z).2.1 ≤ FinalSlowBase.boxRadius W upper from restricted_mem endpoint S) m
    exact (finiteRate_at hr le_rfl).weaken (hq.filter_mono inf_le_left)
      (heatLoss_controls_core F.data.h_lt_half m)
  · apply actual_outer_rate H v upper B inf_le_left _ m
    exact (restricted_mem endpoint Sᶜ).mono (fun _ hz =>
      (outer_lt_box (W := W) upper).trans (lt_of_not_ge hz))
end Actual
end NavierStokes.ActualBaseVelocityBounds
end
end

-- REPLAY NavierStokes.ActualPhysicalStageBounds.initialDirect_rate 196 252
run_cmd IO.println "BLOCK NavierStokes.ActualPhysicalStageBounds.initialDirect_rate"
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
omit [NormedAddCommGroup D] [NormedSpace ℝ D] in
#count_heartbeats in
theorem initialDirect_rate_R (MB : MeanInput h (CoordinateAlgebra.A h))
    (hh : 0 < h) (hh1 : h < 1 / 2) {qbig : ℝ} (hqbig : 0 < qbig)
    (hq : qbig ≤ ChartScales.Q MB.firstBand) (m : ℕ) :
    Fam.F2076.JetRate' ActualBaseVelocityBounds.endpoint (PhysicalWaveSum.physicalQ h)
      MB.family.angularField m (-seedDirectLoss h MB.alpha m) := by
  obtain ⟨C, hC, hb⟩ := MB.angular_bound_with_gain (g := 0) (delta := -(h * MB.alpha))
    hh hh1 hq (by linarith) m
  refine ⟨C, hC, ?_⟩
  filter_upwards [InitializedPhysicalBackground.endpoint_sublevel hh hh1 hqbig,
    ActualBaseVelocityBounds.endpoint_q_small hh hh1] with w hw hqw
  simpa only [seedDirectLoss, PhysicalStageBounds.directLoss, zero_sub] using hb w hw hqw.2
end InitialIncrement
end NavierStokes.ActualPhysicalStageBounds
end
end

-- REPLAY NavierStokes.BaseResidual.finiteRate_add 256 298
run_cmd IO.println "BLOCK NavierStokes.BaseResidual.finiteRate_add"
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
theorem finiteRate_add_R {l : Filter D} {q : D → ℝ} {f g : D → E} {M : ℕ} {r : ℝ}
    {U : Set D} (hf : Fam.F2076.FiniteJetRate' l q f M r) (hg : Fam.F2076.FiniteJetRate' l q g M r)
    (hU : IsOpen U) (hlU : ∀ᶠ x in l, x ∈ U)
    (hsf : ContDiffOn ℝ ∞ f U) (hsg : ContDiffOn ℝ ∞ g U) :
    Fam.F2076.FiniteJetRate' l q (fun x => f x + g x) M r := by
  obtain ⟨A, hA, ha⟩ := hf
  obtain ⟨B, hB, hb⟩ := hg
  refine ⟨A + B, add_nonneg hA hB, ?_⟩
  filter_upwards [hlU, ha, hb] with x hx hax hbx
  intro m hm
  exact (ResidualStability.norm_jet_add_le hU hsf hsg hx m).trans
    ((add_le_add (hax m hm) (hbx m hm)).trans_eq (by ring))
end RateAlgebra
end NavierStokes.BaseResidual
end
end

-- REPLAY NavierStokes.BaseResidual.finiteRate_congr_on 302 341
run_cmd IO.println "BLOCK NavierStokes.BaseResidual.finiteRate_congr_on"
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
theorem finiteRate_congr_on_R {l : Filter D} {q : D → ℝ} {f g : D → E} {M : ℕ} {r : ℝ}
    {U : Set D} (hf : Fam.F2076.FiniteJetRate' l q f M r) (hU : IsOpen U)
    (hlU : ∀ᶠ x in l, x ∈ U) (hfg : EqOn f g U) : Fam.F2076.FiniteJetRate' l q g M r := by
  obtain ⟨C, hC, hb⟩ := hf
  refine ⟨C, hC, ?_⟩
  filter_upwards [hlU, hb] with x hx hbx
  intro m hm
  rw [← ResidualStability.iteratedFDeriv_eqOn hU hfg m hx]
  exact hbx m hm
end RateAlgebra
end NavierStokes.BaseResidual
end
end

-- REPLAY NavierStokes.BaseResidual.finiteRate_weaken 345 381
run_cmd IO.println "BLOCK NavierStokes.BaseResidual.finiteRate_weaken"
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
theorem finiteRate_weaken_R {l : Filter D} {q : D → ℝ} {f : D → E} {M : ℕ} {r s : ℝ}
    (hf : Fam.F2076.FiniteJetRate' l q f M r) (hq : ∀ᶠ x in l, 0 < q x ∧ q x ≤ 1) (hsr : s ≤ r) :
    Fam.F2076.FiniteJetRate' l q f M s := by
  apply finiteJetRate_of_jetRate (hq.mono (fun _ hx => hx.1))
  intro m hm
  exact (finiteRate_at hf hm).weaken hq hsr
end RateAlgebra
end NavierStokes.BaseResidual
end
end

-- REPLAY NavierStokes.BaseResidual.potentialFromScalars_rate 385 444
run_cmd IO.println "BLOCK NavierStokes.BaseResidual.potentialFromScalars_rate"
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
#count_heartbeats in
theorem potentialFromScalars_rate_R {l : Filter SpaceTime} {q : SpaceTime → ℝ}
    {H K : SpaceTime → ℝ} {U B : Set SpaceTime} {M : ℕ} {r : ℝ}
    (hU : IsOpen U) (hlU : ∀ᶠ z in l, z ∈ U) (hq : ∀ᶠ z in l, 0 < q z)
    (hB : IsCompact B) (hlB : ∀ᶠ z in l, z ∈ B)
    (hH : ContDiffOn ℝ ∞ H U) (hK : ContDiffOn ℝ ∞ K U)
    (hrH : Fam.F2076.FiniteJetRate' l q H M r) (hrK : Fam.F2076.FiniteJetRate' l q K M r) :
    Fam.F2076.FiniteJetRate' l q (potentialFromScalars H K) M r := by
  let c0 : SpaceTime → ℝ := fun z => (-(1 / 2 : ℝ)) * z.2 1
  let c1 : SpaceTime → ℝ := fun z => (1 / 2 : ℝ) * z.2 0
  have hc0 : ContDiff ℝ ∞ c0 :=
    contDiff_const.mul ((AxisymmetricFields.projection 1).contDiff.comp contDiff_snd)
  have hc1 : ContDiff ℝ ∞ c1 :=
    contDiff_const.mul ((AxisymmetricFields.projection 0).contDiff.comp contDiff_snd)
  have hr0 := finiteRate_bilinear (finiteRate_compact (q := q) hc0 hB hlB M) hrH
    hU hlU hq hc0.contDiffOn hH (ContinuousLinearMap.mul ℝ ℝ)
  have hr1 := finiteRate_bilinear (finiteRate_compact (q := q) hc1 hB hlB M) hrH
    hU hlU hq hc1.contDiffOn hH (ContinuousLinearMap.mul ℝ ℝ)
  simp only [zero_add] at hr0 hr1
  have ha := finiteRate_linear hr0 hU hlU (hc0.contDiffOn.mul hH) (basisInjection 0)
  have hb := finiteRate_linear hr1 hU hlU (hc1.contDiffOn.mul hH) (basisInjection 1)
  have hc := finiteRate_linear hrK hU hlU hK (basisInjection 2)
  exact finiteRate_add (finiteRate_add ha hb hU hlU
    ((hc0.contDiffOn.mul hH).smul contDiffOn_const)
    ((hc1.contDiffOn.mul hH).smul contDiffOn_const)) hc hU hlU
    (((hc0.contDiffOn.mul hH).smul contDiffOn_const).add
      ((hc1.contDiffOn.mul hH).smul contDiffOn_const)) (hK.smul contDiffOn_const)
end PotentialRates
end NavierStokes.BaseResidual
end
end

-- REPLAY NavierStokes.DiagonalResidual.JetRate.add 448 475
run_cmd IO.println "BLOCK NavierStokes.DiagonalResidual.JetRate.add"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.DiagonalResidual
open Set Filter Function
open scoped Topology BigOperators ContDiff
section Rates
variable {D V : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup V] [NormedSpace ℝ V]
#count_heartbeats in
theorem JetRate.add_R {l : Filter D} {q : D → ℝ} {f g : D → V} {m : ℕ} {r : ℝ}
    {U : Set D} (hf : Fam.F2076.JetRate' l q f m r) (hg : Fam.F2076.JetRate' l q g m r)
    (hU : IsOpen U) (hlU : ∀ᶠ x in l, x ∈ U)
    (hsf : ContDiffOn ℝ ∞ f U) (hsg : ContDiffOn ℝ ∞ g U) :
    Fam.F2076.JetRate' l q (fun x => f x + g x) m r := by
  obtain ⟨A, hA, ha⟩ := hf
  obtain ⟨B, hB, hb⟩ := hg
  refine ⟨A + B, add_nonneg hA hB, ?_⟩
  filter_upwards [hlU, ha, hb] with x hx hax hbx
  calc
    _ ≤ ‖iteratedFDeriv ℝ m f x‖ + ‖iteratedFDeriv ℝ m g x‖ :=
      ResidualStability.norm_jet_add_le hU hsf hsg hx m
    _ ≤ A * (q x) ^ r + B * (q x) ^ r := add_le_add hax hbx
    _ = (A + B) * (q x) ^ r := (add_mul _ _ _).symm
end Rates
end NavierStokes.DiagonalResidual
end
end

-- REPLAY NavierStokes.DiagonalResidual.JetRate.congr_on 479 499
run_cmd IO.println "BLOCK NavierStokes.DiagonalResidual.JetRate.congr_on"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.DiagonalResidual
open Set Filter Function
open scoped Topology BigOperators ContDiff
section Rates
variable {D V : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup V] [NormedSpace ℝ V]
#count_heartbeats in
theorem JetRate.congr_on_R {l : Filter D} {q : D → ℝ} {f g : D → V} {m : ℕ} {r : ℝ}
    {U : Set D} (hf : Fam.F2076.JetRate' l q f m r) (hU : IsOpen U)
    (hlU : ∀ᶠ x in l, x ∈ U) (hfg : EqOn f g U) : Fam.F2076.JetRate' l q g m r := by
  obtain ⟨C, hC, hb⟩ := hf
  refine ⟨C, hC, ?_⟩
  filter_upwards [hlU, hb] with x hx hbound
  rwa [← ResidualStability.iteratedFDeriv_eqOn hU hfg m hx]
end Rates
end NavierStokes.DiagonalResidual
end
end

-- REPLAY NavierStokes.DiagonalResidual.JetRate.weaken 503 524
run_cmd IO.println "BLOCK NavierStokes.DiagonalResidual.JetRate.weaken"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.DiagonalResidual
open Set Filter Function
open scoped Topology BigOperators ContDiff
section Rates
variable {D V : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup V] [NormedSpace ℝ V]
#count_heartbeats in
theorem JetRate.weaken_R {l : Filter D} {q : D → ℝ} {f : D → V} {m : ℕ} {r s : ℝ}
    (hf : Fam.F2076.JetRate' l q f m r) (hq : ∀ᶠ x in l, 0 < q x ∧ q x ≤ 1) (hsr : s ≤ r) :
    Fam.F2076.JetRate' l q f m s := by
  obtain ⟨C, hC, hb⟩ := hf
  refine ⟨C, hC, ?_⟩
  filter_upwards [hq, hb] with x hx hbound
  exact hbound.trans (mul_le_mul_of_nonneg_left
    (Real.rpow_le_rpow_of_exponent_ge hx.1 hx.2 hsr) hC)
end Rates
end NavierStokes.DiagonalResidual
end
end

-- REPLAY NavierStokes.MixedDiagonalResidual.residual_jetRate 528 576
run_cmd IO.println "BLOCK NavierStokes.MixedDiagonalResidual.residual_jetRate"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.MixedDiagonalResidual
open ProblemStatement Set Filter DiagonalResidual ResidualStability
open scoped Topology ContDiff BigOperators
#count_heartbeats in
theorem residual_jetRate_R {a : ℕ → ℝ} (ha : Tendsto a atTop atTop)
    {q : SpaceTime → ℝ} {A B : ℕ → VelocityField} {P : ℕ → PressureField}
    {g LA LB LP Lbg Lres : ℕ → ℝ} {U : Set SpaceTime} {l : Filter SpaceTime}
    (hU : IsOpen U) (hqpos : ∀ z ∈ U, 0 < q z) (hq : ContDiffOn ℝ ∞ q U)
    (hA : ∀ j, ContDiffOn ℝ ∞ (A j) U) (hB : ∀ j, ContDiffOn ℝ ∞ (B j) U)
    (hP : ∀ j, ContDiffOn ℝ ∞ (P j) U)
    (hgmono : Monotone g) (hgtop : Tendsto g atTop atTop)
    (hbA : DiagonalJetBounds.CutStageBounds a q A g LA U)
    (hbB : DiagonalJetBounds.CutStageBounds a q B g LB U)
    (hbP : DiagonalJetBounds.CutStageBounds a q P g LP U)
    (hlU : ∀ᶠ z in l, z ∈ U) (hqzero : Tendsto q l (𝓝 0))
    (hbg : ∀ J m, Fam.F2076.JetRate' l q (uncutVelocity A B J) m (-Lbg m))
    (hres : ∀ J m, Fam.F2076.JetRate' l q
      (fun z => navierStokesResidual (uncutVelocity A B J)
        (DiagonalJetBounds.uncutPrefix P (J + 1)) z.1 z.2) m (g J - Lres m))
    (m : ℕ) (r : ℝ) (hr : 0 ≤ r) :
    Fam.F2076.JetRate' l q (residual a q A B P) m r := by
  have hlq : ∀ᶠ z in l, 0 < q z ∧ q z ≤ 1 := by
    filter_upwards [hlU, hqzero.eventually (gt_mem_nhds (show (0 : ℝ) < 1 by norm_num))]
      with z hz hq1
    exact ⟨hqpos z hz, hq1.le⟩
  have hprefixP (J : ℕ) :
      ContDiffOn ℝ ∞ (DiagonalJetBounds.uncutPrefix P (J + 1)) U :=
    ContDiffOn.sum (fun j _ => hP j)
  apply DiagonalResidual.residual_jetRate_of_stages
    (uStage := uncutVelocity A B)
    (pStage := fun J => DiagonalJetBounds.uncutPrefix P (J + 1))
    (g := g) (Ltail := fun m => max (velocityLoss LA LB m) (LP m))
    hU hlU hlq (velocity_smooth ha hU hqpos hq hA hB)
    (SolenoidalDiagonal.potentialSum_contDiffOn ha hU hqpos hq hP)
    (uncutVelocity_smooth hU hA hB) hprefixP hgtop hbg ?_ ?_ hres m r hr
  · intro J m hm
    apply (velocity_tail_jetRate ha hU hqpos hq hA hB hgmono hbA hbB
      hlU hlq hqzero J m (by omega)).weaken hlq
    exact sub_le_sub (hgmono (Nat.le_succ J)) (le_max_left (velocityLoss LA LB m) (LP m))
  · intro J m hm
    apply (jetRate_diagonal_tail ha hU hq hP hgmono hbP hlU hlq hqzero J m
      (by omega)).weaken hlq
    exact sub_le_sub (hgmono (Nat.le_succ J)) (le_max_right (velocityLoss LA LB m) (LP m))
end NavierStokes.MixedDiagonalResidual
end
end

