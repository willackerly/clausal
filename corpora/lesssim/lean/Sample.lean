/-
Constant-threading experiment: the seeded sample of 10 theorems outside the family
(`out/corpus/lesssim/sample.json`), tried against the library of `Lib.lean` as it stood after the family.
`Sample.Native.X` is the restatement proved against the relation, `Sample.Back.X` has exactly the original
type and is proved from it, `Sample.Fwd.X` is the converse.
-/
import Native
import Equiv
import NavierStokes.BaseStressClasses
import NavierStokes.PositiveTimeSignedData
import NavierStokes.SmoothFamilyTorusInverse
import NavierStokes.ParametricKernelBounds
import NavierStokes.SharpGraphBounds
import NavierStokes.WaveEnvelopeTransport

noncomputable section

open Asymptotics Filter Set
open scoped Topology ContDiff BigOperators
open NavierStokes

namespace Lesssim.Sample

namespace Native

/-- S3. `BaseStressClasses.correction_weighted_jets`: extend a bound from `q ≤ 1` to all `q > 0`, the
jet being zero for `q > 1`. -/
theorem correction_weighted_jets {F : OutgoingProfile.Profile} {W : NominalProfile.Witness F}
    (H : NominalConeAssembly.Certificate W) {ld : ModulatedProfileAssembly.LoopData W}
    (v : ModulatedProfileAssembly.Witness ld) (upper : ℝ) (B m : ℕ) :
    ∃ N : ℕ, (fun p => SlowBorelBase.blownJet m (BaseStressClasses.correction H v upper B) p)
      =O[𝓟 {p | 0 < p.1 ∧ p.2 ∈ FinalSlowBase.annulus W}]
      fun p => p.1 ^ F.data.h * FinalSlowBase.weight W p.2 * (FinalSlowBase.edgeDistance W p.2)⁻¹ ^ N := by
  obtain ⟨D, -, N, hb⟩ := FinalSlowBase.weighted_jets H v upper B m
  refine ⟨N, IsBigO.of_bound |D| (eventually_principal.2 ?_)⟩
  rintro ⟨q, w⟩ ⟨hq, hw⟩
  by_cases hq1 : q ≤ 1
  · exact ((hb q hq hq1 w hw).trans_eq (by simp only [mul_assoc])).trans
      ((le_abs_self _).trans (abs_mul _ _).le)
  · have hz := AllBandBaseJets.correction_blownJet_eq_zero
      (FinalSlowBase.scales_admissible H v upper B).positive F.data.h
      (BaseResidual.stressPair (FinalSlowBase.coefficients H v)) (lt_of_not_ge hq1) w m
    change SlowBorelBase.blownJet m (BaseStressClasses.correction H v upper B) (q, w) = 0 at hz
    change ‖SlowBorelBase.blownJet m (BaseStressClasses.correction H v upper B) (q, w)‖ ≤ _
    rw [hz, norm_zero]
    exact mul_nonneg (abs_nonneg _) (norm_nonneg _)

/-- S4. `PositiveTimeSignedData.potential_physical_bound`: transfer along a germ. -/
theorem potential_physical_bound {D h : ℝ}
    (sys : PartitionedCovariance.SlotSystem D h ActualSignedGeometry.radialVector ActualSignedGeometry.temporalVector)
    (hh : 0 ≤ h) {U : PhaseJetBounds.Domain ℕ PhaseCalculus.Slow} (f : ActualSignedPhysicalData.SignedFamily U)
    {a b : ℝ} {s : WeightedClasses.StripData ActualSignedPhysicalData.Native}
    (hloc : PositiveTimeSignedData.PrimitiveLocalization (h := h) f a b s)
    (G : ActualSignedPhysicalData.ReferenceGeometry sys f)
    (hh0 : 0 < h) (hh1 : h < 1 / 2) (ha : 0 < a) (hb : 0 < b) (hp : ActualSignedPhysicalData.NativeProfiles (h := h) f)
    (hn : ActualSignedPhysicalData.NativeRegular sys hh f) {P : ℝ} (hP : 1 ≤ P)
    (hf : ∀ (L : ActualSignedPhysicalData.NativeLabel f.active),
      |((f.primary L).pulse (f.column L)).phase.p L.val.1| ≤ P ∧
        |((f.primary L).pulse (f.column L)).phase.pz L.val.1| ≤ P ∧
          |((f.primary L).pulse (f.column L)).phase.x0 L.val.1| ≤ P)
    {α : ℝ} {w : ActualSignedPhysicalData.SourceIndex → ℕ → ActualSignedPhysicalData.Native → ℝ}
    (hpotential : LocalPhysicalCopyBounds.LocalSourceBounds s h α w
      (ActualSignedPhysicalData.nativePotentialSource sys hh f)) (m : ℕ) :
    (fun x => iteratedFDeriv ℝ m (PhysicalCopyBounds.vectorSum
        (ActualSignedPhysicalData.potentialFamily sys hh f) (a / 4) h sys.radius) x)
      =O[𝓟 {x | x ∈ PhysicalWaveSum.preterminal ∧ PhysicalWaveSum.physicalQ h x ≤ 1}]
      fun x => PhysicalWaveSum.physicalQ h x ^ (h * α - PhysicalClassBounds.physicalLoss h (-h) m) :=
  congr_left_on (Lesssim.Native.WaveData.vector_bound
    (PositiveTimeSignedData.potentialWaveData sys hh f hloc G hh0 hh1 ha hb hp hn hP hf hpotential) hh0 hh1 m)
    fun _ hx => PhysicalWaveSum.iteratedFDeriv_eq_of_eventuallyEq
      (PositiveTimeSignedData.potentialWaveData_vector_germ sys hh f hloc G hh0 hh1 ha hb hp hn hP hf
        hpotential hx.1) m

section Torus

open SmoothFamilyTorusInverse TorusInverse

variable {P : Type} [NormedAddCommGroup P] [NormedSpace ℝ P]

/-- S7. `SmoothFamilyTorusInverse.exists_uniform_coefficient_bound`.  ESCAPE HATCH: the Fourier lemma
outside the sample takes one explicit constant for three bounds. -/
theorem exists_uniform_coefficient_bound {f : Source P} (hf : ContDiff ℝ ∞ f)
    (hp : Periodic f) (n : ℕ) {K : Set P} (hK : IsCompact K) :
    (fun q : P × Frequency => weight q.2 ^ n * ‖coefficient f q.1 q.2‖)
      =O[𝓟 {q | q.1 ∈ K}] fun _ => (1 : ℝ) := by
  -- one continuous function on one compact set carries the three bounds
  obtain ⟨C, -, hC⟩ := exists_bound_on (((hf.continuous.norm.add (torusXJet_smooth hf n).continuous.norm).add
    (torusXJet_smooth (swapTorus_smooth hf) n).continuous.norm).continuousOn.isBigO_principal
    (hK.prod (isCompact_Icc.prod isCompact_Icc)) (c := (1 : ℝ)) (by simp)) fun _ _ => zero_le_one
  have h3 (p : P) (hp : p ∈ K) (x : ℝ) (hx : x ∈ Icc (0 : ℝ) 1) (y : ℝ) (hy : y ∈ Icc (0 : ℝ) 1) :
      ‖f (p, (x, y))‖ + ‖torusXJet n f (p, (x, y))‖ + ‖torusXJet n (swapTorus f) (p, (x, y))‖ ≤ C :=
    (le_abs_self _).trans ((hC (p, (x, y)) ⟨hp, hx, hy⟩).trans_eq (mul_one C))
  refine isBigO_of_bound_on (3 ^ n * C) fun q hq => ?_
  rw [Real.norm_of_nonneg (mul_nonneg (pow_nonneg (weight_pos _).le _) (norm_nonneg _)), mul_one]
  apply SmoothFourierData.coefficient_polynomial_bound (slice_smooth hf q.1) (hp q.1) n
  all_goals
    intro x hx y hy
    have h := h3 q.1 hq x hx y hy
    have h0 := norm_nonneg (f (q.1, (x, y)))
    have h1 := norm_nonneg (torusXJet n f (q.1, (x, y)))
    have h2 := norm_nonneg (torusXJet n (swapTorus f) (q.1, (x, y)))
  · change ‖f (q.1, (x, y))‖ ≤ C
    linarith
  · rw [← slice_torusXJet hf n q.1]
    change ‖torusXJet n f (q.1, (x, y))‖ ≤ C
    linarith
  · change ‖SmoothFourierData.xJet n (slice (swapTorus f) q.1) (x, y)‖ ≤ C
    rw [← slice_torusXJet (swapTorus_smooth hf) n q.1]
    change ‖torusXJet n (swapTorus f) (q.1, (x, y))‖ ≤ C
    linarith

/-- S9. `SmoothFamilyTorusInverse.uniform_multiplied_coeff_bound`.  ESCAPE HATCH, same reason. -/
theorem uniform_multiplied_coeff_bound {m : Frequency → ℂ} (hm : ParametricTorusInverse.PolynomialGrowth m)
    {f : Source P} (hf : ContDiff ℝ ∞ f) (hp : Periodic f) {K : Set P} (hK : IsCompact K) :
    (fun q : P × Frequency => m q.2 * coefficient f q.1 q.2)
      =O[𝓟 {q | q.1 ∈ K}] fun q => (weight q.2 ^ 4)⁻¹ := by
  obtain ⟨s, M, hM, hm⟩ := hm
  obtain ⟨B, -, hb⟩ := exists_bound_on (exists_uniform_coefficient_bound hf hp (s + 4) hK) fun _ _ => zero_le_one
  exact isBigO_of_bound_on (M * B) fun q hq => ParametricTorusInverse.multiplied_coeff_bound hM hm
    (fun k => (le_abs_self _).trans ((hb (q.1, k) hq).trans_eq (mul_one B))) q.2

end Torus

end Native

/-! ## Statement-only restatements: S5 and S10 (no native proof; see LESSSIM.md) -/

section S5

open WeightedClasses CommonCoverSolve CommonCoverClass TorusInverse WaveEnvelopeTransport

variable {P V : Type} [NormedAddCommGroup P] [NormedSpace ℝ P] [NormedAddCommGroup V] [NormedSpace ℝ V]

/-- S5. `WaveEnvelopeTransport.waveClass_sourceArgument_bound`: its conclusion and the relation's form
are equivalent. -/
theorem waveClass_sourceArgument_bound_iff (s : StripData P) (B : Plane ≃L[ℝ] Plane) {h : ℝ}
    (band gap : ℕ → ℕ) (center : ℕ → Plane) (r L : ℕ → ℝ) (W : ℕ → ℝ → ℝ) (hW : ∀ n v, 0 ≤ W n v)
    {α : ℝ} {f : ℕ → P × Plane → V} (N : ℕ) :
    (∃ d : ℕ, ∀ j ≤ N, (fun q : ℕ × Frequency × (P × Plane) × ℝ => iteratedFDeriv ℝ j
        (fun x : Joint P => f q.1 (sourceArgument (bandGeometry B h (band q.1) (gap q.1) (center q.1)) q.2.1 x))
        (q.2.2.1, q.2.2.2))
      =O[𝓟 {q | q.2.2.1.1 ∈ s.domain ∧
        ((bandGeometry B h (band q.1) (gap q.1) (center q.1)).coordinates q.2.1 q.2.2.1.2).1 ∈
          Icc (-(r q.1)) (r q.1) ∧ q.2.2.2 ∈ Icc 0 (L q.1)}]
      fun q => s.growth q.1 q.2.2.1.1 ^ d * (s.epsilon q.1 ^ α * Real.sqrt (s.zeta q.2.2.1.1)) * W q.1 q.2.2.2)
    ↔ ∃ C : ℝ, 0 ≤ C ∧ ∃ d : ℕ, ∀ n (k : Frequency) (z : P × Plane), z.1 ∈ s.domain →
      ((bandGeometry B h (band n) (gap n) (center n)).coordinates k z.2).1 ∈ Icc (-(r n)) (r n) →
      ∀ v ∈ Icc 0 (L n), ∀ j ≤ N,
      ‖iteratedFDeriv ℝ j
        (fun x : Joint P => f n (sourceArgument (bandGeometry B h (band n) (gap n) (center n)) k x))
        (z, v)‖ ≤
      C * s.growth n z.1 ^ d * (s.epsilon n ^ α * Real.sqrt (s.zeta z.1)) * W n v := by
  constructor
  · rintro ⟨d, hd⟩
    obtain ⟨C, hC, hb⟩ := exists_bound_on_le hd fun q _ => mul_nonneg (mul_nonneg
      (pow_nonneg (s.growth_nonneg _ _) _)
      (mul_nonneg (Real.rpow_nonneg (s.epsilon_pos _).le _) (Real.sqrt_nonneg _))) (hW _ _)
    exact ⟨C, hC, d, fun n k z hz hξ v hv j hj => (hb (n, k, z, v) ⟨hz, hξ, hv⟩ j hj).trans_eq (by ring)⟩
  · rintro ⟨C, -, d, hb⟩
    exact ⟨d, fun j hj => isBigO_of_bound_on C fun q hq =>
      (hb q.1 q.2.1 q.2.2.1 hq.1 hq.2.1 q.2.2.2 hq.2.2 j hj).trans_eq (by ring)⟩

end S5

section S10

open ProblemStatement PhysicalGraphBounds

/-- S10. `SharpGraphBounds.graphRestriction_jet_bound`: a bound uniform over all smooth `F`, with the
bound `B` on the jets of `F` as a second universally quantified constant.  In the relation, `F` joins the
tuple of uniform parameters and `B` becomes the sum of the jet norms. -/
theorem graphRestriction_jet_bound_iff {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {h a b : ℝ} (m : ℕ) :
    ((fun q : ℕ × SpaceTime × (LiftPoint → E) => iteratedFDeriv ℝ m (q.2.2 ∘ physicalLift h q.1) q.2.1)
      =O[𝓟 {q | 4 ≤ q.1 ∧ scaledRadial q.1 q.2.1 ∈ annulus a b ∧ |q.2.1.1| ≤ 1 ∧ ContDiff ℝ ∞ q.2.2}]
      fun q => (∑ k ∈ Finset.range (m + 1), ‖iteratedFDeriv ℝ k q.2.2 (physicalLift h q.1 q.2.1)‖) *
        ChartScales.Q q.1 ^ (-(m : ℝ) * (1 + h)))
    ↔ ∃ C : ℝ, 0 < C ∧ ∀ n : ℕ, 4 ≤ n → ∀ p : SpaceTime,
      scaledRadial n p ∈ annulus a b → |p.1| ≤ 1 →
      ∀ F : LiftPoint → E, ContDiff ℝ ∞ F → ∀ B : ℝ, 0 ≤ B →
      (∀ k ≤ m, ‖iteratedFDeriv ℝ k F (physicalLift h n p)‖ ≤ B) →
      ‖iteratedFDeriv ℝ m (F ∘ physicalLift h n) p‖ ≤
        C * B * ChartScales.Q n ^ (-(m : ℝ) * (1 + h)) := by
  constructor
  · intro hO
    obtain ⟨C, hC, hb⟩ := exists_bound_on hO fun q _ => mul_nonneg
      (Finset.sum_nonneg fun _ _ => norm_nonneg _) (Real.rpow_nonneg (ChartScales.Q_pos _).le _)
    refine ⟨C * (m + 1) + 1, by positivity, fun n hn p hp ht F hF B hB hFB => ?_⟩
    have hQ : 0 ≤ ChartScales.Q n ^ (-(m : ℝ) * (1 + h)) := Real.rpow_nonneg (ChartScales.Q_pos n).le _
    have hsum : ∑ k ∈ Finset.range (m + 1), ‖iteratedFDeriv ℝ k F (physicalLift h n p)‖ ≤ (m + 1) * B := by
      have := Finset.sum_le_card_nsmul (Finset.range (m + 1))
        (fun k => ‖iteratedFDeriv ℝ k F (physicalLift h n p)‖) B
        (fun k hk => hFB k (Nat.lt_succ_iff.1 (Finset.mem_range.1 hk)))
      simpa [Finset.card_range, nsmul_eq_mul] using this
    calc _ ≤ C * ((∑ k ∈ Finset.range (m + 1), ‖iteratedFDeriv ℝ k F (physicalLift h n p)‖) *
          ChartScales.Q n ^ (-(m : ℝ) * (1 + h))) := hb (n, p, F) ⟨hn, hp, ht, hF⟩
      _ ≤ C * (((m + 1) * B) * ChartScales.Q n ^ (-(m : ℝ) * (1 + h))) := by gcongr
      _ ≤ _ := by nlinarith [mul_nonneg hB hQ]
  · rintro ⟨C, -, hb⟩
    exact isBigO_of_bound_on C fun q hq => (hb q.1 hq.1 q.2.1 hq.2.1 hq.2.2.1 q.2.2 hq.2.2.2 _
      (Finset.sum_nonneg fun _ _ => norm_nonneg _)
      (fun k hk => Finset.single_le_sum (f := fun k => ‖iteratedFDeriv ℝ k q.2.2 (physicalLift h q.1 q.2.1)‖)
        (fun _ _ => norm_nonneg _) (Finset.mem_range.2 (Nat.lt_succ_of_le hk)))).trans_eq (mul_assoc _ _ _)

end S10

/-! ## Nothing weakened: S3, S4, S7, S9 -/

namespace Back

theorem correction_weighted_jets : type_of% @BaseStressClasses.correction_weighted_jets := by
  intro F W H ld v upper B m
  obtain ⟨N, hN⟩ := Native.correction_weighted_jets H v upper B m
  have hg : ∀ p ∈ {p : ℝ × _ | 0 < p.1 ∧ p.2 ∈ FinalSlowBase.annulus W},
      0 ≤ p.1 ^ F.data.h * FinalSlowBase.weight W p.2 * (FinalSlowBase.edgeDistance W p.2)⁻¹ ^ N := by
    intro p hp
    have hw' : p.2 ∈ BaseResidual.activeWindow (FinalSlowBase.logLeft W) (FinalSlowBase.logRight W) := by
      rw [← FinalSlowBase.annulus_eq W]; exact hp.2
    exact mul_nonneg (mul_nonneg (Real.rpow_nonneg hp.1.le _) (ActiveAnnulusWeight.radialWeight_pos hw'.1).le)
      (pow_nonneg (inv_nonneg.mpr (BaseResidual.activeDelta_bounds hw').1.le) N)
  obtain ⟨C, hC, hb⟩ := exists_bound_on hN hg
  refine ⟨C + 1, by linarith, N, fun q hq w hw => ?_⟩
  exact ((hb (q, w) ⟨hq, hw⟩).trans (mul_le_mul_of_nonneg_right (show C ≤ C + 1 by linarith) (hg (q, w) ⟨hq, hw⟩))).trans_eq
    (by ring)

theorem potential_physical_bound : type_of% @PositiveTimeSignedData.potential_physical_bound := by
  intro D h sys hh U f a b s hloc G hh0 hh1 ha hb hp hn P hP hf α w hpotential m
  exact back3 (fun z hz _ => PhysicalWaveSum.physicalQ_pos hh0 hh1 hz)
    (Native.potential_physical_bound sys hh f hloc G hh0 hh1 ha hb hp hn hP hf hpotential m)

theorem exists_uniform_coefficient_bound :
    type_of% @SmoothFamilyTorusInverse.exists_uniform_coefficient_bound := by
  intro P _ _ f hf hp n K hK
  obtain ⟨C, hC, hb⟩ := back1 (Native.exists_uniform_coefficient_bound hf hp n hK)
  exact ⟨C, hC, fun p hp k => hb (p, k) hp⟩

theorem uniform_multiplied_coeff_bound :
    type_of% @SmoothFamilyTorusInverse.uniform_multiplied_coeff_bound := by
  intro P _ _ m hm f hf hp K hK
  obtain ⟨C, hC, hb⟩ := exists_bound_on (Native.uniform_multiplied_coeff_bound hm hf hp hK)
    fun q _ => inv_nonneg.mpr (pow_nonneg (TorusInverse.weight_pos _).le _)
  exact ⟨C, hC, fun p hp k => hb (p, k) hp⟩

end Back

namespace Fwd

theorem correction_weighted_jets : type_of% @Native.correction_weighted_jets := by
  intro F W H ld v upper B m
  obtain ⟨D, -, N, hb⟩ := BaseStressClasses.correction_weighted_jets H v upper B m
  exact ⟨N, isBigO_of_bound_on D fun p hp => (hb p.1 hp.1 p.2 hp.2).trans_eq (by ring)⟩

theorem potential_physical_bound : type_of% @Native.potential_physical_bound := by
  intro D h sys hh U f a b s hloc G hh0 hh1 ha hb hp hn P hP hf α w hpotential m
  exact fwd3 (PositiveTimeSignedData.potential_physical_bound sys hh f hloc G hh0 hh1 ha hb hp hn hP hf
    hpotential m)

theorem exists_uniform_coefficient_bound : type_of% @Native.exists_uniform_coefficient_bound := by
  intro P _ _ f hf hp n K hK
  obtain ⟨C, hC, hb⟩ := SmoothFamilyTorusInverse.exists_uniform_coefficient_bound hf hp n hK
  exact fwd1 (fun q _ => mul_nonneg (pow_nonneg (TorusInverse.weight_pos _).le _) (norm_nonneg _))
    ⟨C, hC, fun q hq => hb q.1 hq q.2⟩

theorem uniform_multiplied_coeff_bound : type_of% @Native.uniform_multiplied_coeff_bound := by
  intro P _ _ m hm f hf hp K hK
  obtain ⟨C, -, hb⟩ := SmoothFamilyTorusInverse.uniform_multiplied_coeff_bound hm hf hp hK
  exact isBigO_of_bound_on C fun q hq => hb q.1 hq q.2

end Fwd

end Lesssim.Sample
