/-
Constant-threading experiment: the 13 theorems of the frozen family, restated with `=O[𝓟 S]` and proved
against the relation.  No theorem here uses an original family theorem; lemmas of the corpus outside the
family are used as they stand.
-/
import Lib

noncomputable section

open Asymptotics Filter Set
open scoped Topology ContDiff BigOperators
open NavierStokes NavierStokes.WeightedClasses NavierStokes.LabelSumBounds

namespace Lesssim.Native

/-! ### 1–3: the flat weight is bounded -/

/-- 1. `WeightedRadialPrimitive.weight_uniform_bound` -/
theorem weight_uniform_bound {cL cR : ℝ} (hcL : 0 < cL) (hcR : 0 < cR) (L : ℝ) (m : ℕ) :
    WeightedRadialPrimitive.weight cL cR L m =O[𝓟 (Ioo 0 L)] fun _ => (1 : ℝ) :=
  (isBigO_of_le_on fun _ hx => abs_le_abs_of_nonneg (WeightedRadialPrimitive.weight_pos cL cR m hx).le
    (WeightedRadialPrimitive.weight_le_wholeMajorant hcL.le hcR.le m hx)).trans
  (mono_set ((WeightedRadialPrimitive.wholeMajorant_continuous hcL hcR L m).continuousOn.isBigO_principal
    isCompact_Icc (by simp)) Ioo_subset_Icc_self)

/-- 2. `PhysicalClassBounds.flat_edge_uniform` -/
theorem flat_edge_uniform {cL cR c : ℝ} (hcL : 0 < cL) (hcR : 0 < cR) (hc : 0 < c) (L : ℝ) (m : ℕ) :
    (fun x => (max 1 (WeightedRadialPrimitive.delta L x)⁻¹) ^ m * WeightedRadialPrimitive.zeta cL cR L x ^ c)
      =O[𝓟 (Ioo 0 L)] fun _ => (1 : ℝ) :=
  congr_left_on (weight_uniform_bound (mul_pos hc hcL) (mul_pos hc hcR) L m) fun x hx => by
    have hd : 1 ≤ (WeightedRadialPrimitive.delta L x)⁻¹ :=
      (one_le_inv₀ (WeightedRadialPrimitive.delta_pos hx)).mpr (WeightedRadialPrimitive.delta_le_one L x)
    simp only [max_eq_right hd, PhysicalClassBounds.zeta_rpow hx, WeightedRadialPrimitive.weight,
      div_eq_mul_inv, inv_pow, mul_comm]

/-- 3. `PhysicalClassBounds.FlatGeometry.uniform` -/
theorem FlatGeometry.uniform {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
    {s : StripData D} {cL cR L : ℝ} {ρ : D → ℝ}
    (hg : PhysicalClassBounds.FlatGeometry s cL cR L ρ) {c : ℝ} (hc : 0 < c) (m : ℕ) :
    (fun x => (max 1 (s.delta x)⁻¹) ^ m * s.zeta x ^ c) =O[𝓟 s.domain] fun _ => (1 : ℝ) :=
  congr_left_on (comp_mapsTo (flat_edge_uniform hg.left_pos hg.right_pos hc L m) hg.position)
    fun x hx => by simp only [hg.delta_eq x hx, hg.zeta_eq x hx]


/-! ### 4–6: jets of the weighted source, uniform in label, band and point -/

section Weighted

variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
  {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] {ι : Type*}

/-- 4. `PhysicalClassBounds.UniformClass.edge_absorbed` -/
theorem UniformClass.edge_absorbed {s : StripData D} {cL cR L : ℝ} {ρ : D → ℝ}
    (hg : PhysicalClassBounds.FlatGeometry s cL cR L ρ) {c α : ℝ} (hc : 0 < c)
    {w : ι → ℕ → D → ℝ} {f : ι → ℕ → D → E} (hf : UniformClass s w α f)
    (hw : ∀ l n x, x ∈ s.domain → w l n x ≤ s.zeta x ^ c) (m : ℕ) :
    ∃ p : ℕ, ∀ j ≤ m, (fun ((l, n, x) : ι × ℕ × D) => iteratedFDeriv ℝ j (f l n) x)
      =O[𝓟 {q | q.2.2 ∈ s.domain}] fun (_, n, _) => s.epsilon n ^ α * s.slow n ^ p := by
  obtain ⟨p, hp⟩ := uniformClass_isBigO hf m
  refine ⟨p, fun j hj => (hp j hj).trans ?_⟩
  have hweight : (fun q : ι × ℕ × D => w q.1 q.2.1 q.2.2) =O[𝓟 {q | q.2.2 ∈ s.domain}]
      fun q => s.zeta q.2.2 ^ c :=
    isBigO_of_le_on fun q hq => abs_le_abs_of_nonneg (hf.weight_nonneg _ _ _ hq) (hw _ _ _ hq)
  have hedge := comp_mapsTo (FlatGeometry.uniform hg hc p) (k := fun q : ι × ℕ × D => q.2.2) fun _ hq => hq
  refine (((isBigO_refl (fun q : ι × ℕ × D => s.epsilon q.2.1 ^ α * s.growth q.2.1 q.2.2 ^ p) _).mul
    hweight).congr_right fun q => ?_).trans
    (((isBigO_refl (fun q : ι × ℕ × D => s.epsilon q.2.1 ^ α * s.slow q.2.1 ^ p) _).mul hedge).congr_right
      fun q => mul_one _)
  simp only [StripData.growth, mul_pow]; ring


open LocalPhysicalCopyBounds PhysicalWaveSum PhysicalCopyBounds in
/-- 5. `LocalPhysicalCopyBounds.LocalSourceBounds.chart_bound` -/
theorem LocalSourceBounds.chart_bound {E : Type} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {h : ℝ} {s : StripData D} {α : ℝ} {w : ι → ℕ → D → ℝ} {source : ι → ℕ → D → E}
    (hs : LocalSourceBounds s h α w source) (m : ℕ) :
    ∃ p : ℕ, ∀ j ≤ m, (fun ((l, n, x) : ι × ℕ × D) => iteratedFDeriv ℝ j (source l n) x)
      =O[𝓟 {q | 4 ≤ q.2.1 ∧ q.2.2 ∈ s.domain}]
        fun (_, n, _) => ChartScales.Q n ^ (h * α) * ChartScales.S n ^ p := by
  obtain ⟨cL, cR, L, ρ, hflat⟩ := hs.flat_geometry
  obtain ⟨c, hc, hw⟩ := hs.weight_le
  obtain ⟨C, -, e, hslow⟩ := hs.slow_le
  obtain ⟨p, hp⟩ := Native.UniformClass.edge_absorbed hflat hc hs.uniform hw m
  have hS : (fun q : ι × ℕ × D => s.slow q.2.1) =O[𝓟 {q | 4 ≤ q.2.1 ∧ q.2.2 ∈ s.domain}]
      fun q => ChartScales.S q.2.1 ^ e :=
    isBigO_of_bound_on C fun q hq =>
      (Real.norm_of_nonneg (zero_le_one.trans (s.one_le_slow _))).trans_le (hslow _ hq.1)
  refine ⟨e * p, fun j hj => (mono_set (hp j hj) fun _ hq => hq.2).trans ?_⟩
  refine ((isBigO_refl (fun q : ι × ℕ × D => s.epsilon q.2.1 ^ α) _).mul (hS.pow p)).congr_right fun q => ?_
  rw [hs.epsilon_eq, ChartScales.epsilon, ← Real.rpow_mul (ChartScales.Q_pos _).le, ← pow_mul]

end Weighted

section Copies

open LocalPhysicalCopyBounds PhysicalWaveSum PhysicalCopyBounds

variable {H Δ : ℕ} {K : Type*} {f : CopyFamily H K} {a b h r0 Z : ℝ}
  {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D] {ι : Type*}

/-- 6. `LocalPhysicalCopyBounds.commonChart_amplitude_bound` -/
theorem commonChart_amplitude_bound {s : StripData D} {α σ : ℝ}
    {w : ι → ℕ → D → ℝ} {source : ι → ℕ → D → ℂ}
    (hs : LocalSourceBounds s h α w source) {hc : SupportCells f}
    (hchart : CommonChart f hc a b h r0 σ source)
    (hmap : ∀ k I, MapsTo (hchart.map k I) (hchart.domain k I) s.domain) (m : ℕ) :
    ∃ p : ℕ, ∀ j ≤ m, (fun ((k, I, x) : K × WaveIndex H × LiftPoint) => iteratedFDeriv ℝ j (f.amplitude k I) x)
      =O[𝓟 {q | q.2.2 ∈ hchart.domain q.1 q.2.1}]
        fun (_, I, _) => ChartScales.Q I.1.val.1 ^ (h * α + σ) * ChartScales.S I.1.val.1 ^ p := by
  obtain ⟨p, hp⟩ := Native.LocalSourceBounds.chart_bound hs m
  obtain ⟨B, -, e, he⟩ := hchart.positive_jets m
  refine ⟨p + e * m, fun j hj => ?_⟩
  have hS (I : WaveIndex H) : 1 ≤ ChartScales.S I.1.val.1 :=
    PhysicalGraphBounds.S_ge_one (by have := I.1.property; omega)
  -- the chain rule, uniformly over the copy, the wave index and the point of the patch
  have hcomp := jet_comp (T := {q : K × WaveIndex H × LiftPoint | q.2.2 ∈ hchart.domain q.1 q.2.1})
    (g := fun q => source (hchart.sourceIndex q.1 q.2.1) q.2.1.1.val.1) (φ := fun q => hchart.map q.1 q.2.1)
    (U := fun q => hchart.domain q.1 q.2.1) (W := fun _ => s.domain) (pt := fun q => q.2.2)
    (A := fun q => ChartScales.Q q.2.1.1.val.1 ^ (h * α) * ChartScales.S q.2.1.1.val.1 ^ p)
    (B := fun q => ChartScales.S q.2.1.1.val.1 ^ e)
    (fun _ _ => hchart.open_domain _ _) (fun _ _ => s.isOpen_domain) (fun _ _ => hs.uniform.smooth _ _)
    (fun _ _ => hchart.smooth _ _) (fun _ _ => hmap _ _) (fun _ hq => hq) m
    (fun _ _ => mul_nonneg (Real.rpow_nonneg (ChartScales.Q_pos _).le _) (pow_nonneg (zero_le_one.trans (hS _)) _))
    (fun _ _ => one_le_pow₀ (hS _))
    (fun i hi => comp_mapsTo (hp i hi)
      (k := fun q : K × WaveIndex H × LiftPoint =>
        (hchart.sourceIndex q.1 q.2.1, q.2.1.1.val.1, hchart.map q.1 q.2.1 q.2.2))
      fun q hq => ⟨q.2.1.1.property, hmap _ _ hq⟩)
    (fun i h1 hi => isBigO_of_bound_on B fun q hq => he _ _ _ hq i h1 hi) j hj
  -- on its patch the amplitude is `Q ^ σ` times that composition
  refine (congr_left_on ((isBigO_refl (fun q : K × WaveIndex H × LiftPoint =>
      ChartScales.Q q.2.1.1.val.1 ^ σ) _).smul hcomp) ?_).congr_right fun q => ?_
  · rintro ⟨k, I, x⟩ hx
    have hd : ContDiffAt ℝ ∞ (source (hchart.sourceIndex k I) I.1.val.1 ∘ hchart.map k I) x :=
      ((hs.uniform.smooth _ _).contDiffAt (s.isOpen_domain.mem_nhds (hmap k I hx))).comp x
        ((hchart.smooth k I).contDiffAt ((hchart.open_domain k I).mem_nhds hx))
    have hamp : f.amplitude k I =ᶠ[𝓝 x] fun y => (ChartScales.Q I.1.val.1 ^ σ) •
        (source (hchart.sourceIndex k I) I.1.val.1 ∘ hchart.map k I) y :=
      eventuallyEq_of_mem ((hchart.open_domain k I).mem_nhds hx) (hchart.amplitude_eq k I)
    change _ = iteratedFDeriv ℝ j (f.amplitude k I) x
    rw [iteratedFDeriv_eq_of_eventuallyEq hamp j, iteratedFDeriv_const_smul_apply'
      (hd.of_le (ENat.natCast_le_of_coe_top_le_withTop le_rfl j))]
  · obtain ⟨k, I, x⟩ := q
    dsimp only
    rw [ Real.rpow_add (ChartScales.Q_pos _), pow_add, ← pow_mul]; ring


/-- 7. `LocalPhysicalCopyBounds.localStrippedClass_of_weighted`.  ESCAPE HATCH: the conclusion is the
project structure `JetData`, whose fields take the constants as arguments, so the statement is kept and
the constant of 6 is unpacked here. -/
theorem localStrippedClass_of_weighted {s : StripData D} {α σ P : ℝ}
    {w : ι → ℕ → D → ℝ} {source : ι → ℕ → D → ℂ}
    (hs : LocalSourceBounds s h α w source) {hc : SupportCells f}
    (hchart : CommonChart f hc a b h r0 σ source)
    (hmap : ∀ k I, MapsTo (hchart.map k I) (hchart.domain k I) s.domain)
    (hb : PhysicalCopyBounds.CarrierBounds f hc a b h r0)
    (hsmooth : SmoothData f a h r0)
    (hp : ∀ k L, |(f.carrier k L).angular| ≤ P ∧
      |(f.carrier k L).axial| ≤ P ∧ |(f.carrier k L).radial| ≤ P) (m : ℕ) :
    ∃ A : ℝ, 0 ≤ A ∧ ∃ B : ℝ, 1 ≤ B ∧ ∃ p q : ℕ,
      JetData f hc a b h r0 P A B (h * α + σ) p q m := by
  obtain ⟨p, hAp⟩ := Native.commonChart_amplitude_bound hs hchart hmap m
  have hS (I : WaveIndex H) : 1 ≤ ChartScales.S I.1.val.1 :=
    PhysicalGraphBounds.S_ge_one (by have := I.1.property; omega)
  obtain ⟨A, hA, hAp⟩ := exists_bound_on_le hAp (fun q _ => mul_nonneg (Real.rpow_nonneg (ChartScales.Q_pos _).le _)
      (pow_nonneg (zero_le_one.trans (hS _)) _))
  obtain ⟨B, hB, q, hBq⟩ := hb.profile_bound m
  refine ⟨A, hA, B, hB, p, q, hp, ?_⟩
  intro k I z hz hregion hann hcell hts
  constructor
  · intro j hj
    simpa only [Real.rpow_natCast, mul_assoc] using jet_bound_at_closure
      (hsmooth.amplitude k I z hz hts).contDiffAt
      (hchart.contains k I z hz hregion hann hcell hts) j
      (fun y hy => hAp (k, I, y) hy j hj)
  · intro chart hpolar
    constructor
    · intro j hj
      have he := (hBq k I.1 _ (hb.contains k I z hz hregion hann hcell chart hpolar) j hj).1
      simp only [Real.rpow_natCast]
      exact he
    · intro j hj
      have he := (hBq k I.1 _ (hb.contains k I z hz hregion hann hcell chart hpolar) j hj).2
      simp only [Real.rpow_natCast]
      exact he

/-- 8. `LocalPhysicalCopyBounds.physical_sum_jet_bound_of_weighted`.  ESCAPE HATCH: the constants of 7 are
passed by hand to `physical_sum_jet_bound` (outside the family), and its constant is wrapped again. -/
theorem physical_sum_jet_bound_of_weighted {s : StripData D} {α σ P : ℝ}
    {w : ι → ℕ → D → ℝ} {source : ι → ℕ → D → ℂ}
    (hsource : LocalSourceBounds s h α w source) {hc : SupportCells f}
    (hchart : CommonChart f hc a b h r0 σ source)
    (hmap : ∀ k I, MapsTo (hchart.map k I) (hchart.domain k I) s.domain)
    (hb : PhysicalCopyBounds.CarrierBounds f hc a b h r0)
    (hr : SupportData f a b h r0 Z Δ) (hs : SmoothData f a h r0)
    (hh : 0 < h) (hh1 : h < 1 / 2) (ha : 0 < a) (hZ : 0 ≤ Z) (hr0 : 0 ≤ r0)
    (hP : 1 ≤ P) (hp : ∀ k L, |(f.carrier k L).angular| ≤ P ∧
      |(f.carrier k L).axial| ≤ P ∧ |(f.carrier k L).radial| ≤ P) (m : ℕ) :
    (fun z => iteratedFDeriv ℝ m (f.sum a h r0) z) =O[𝓟 {z | z ∈ preterminal ∧ |z.1| ≤ 1}]
      fun z => physicalQ h z ^ (h * α - PhysicalClassBounds.physicalLoss h σ m) := by
  obtain ⟨A, hA, B, hB, p, q, hclass⟩ := Native.localStrippedClass_of_weighted hsource hchart hmap hb hs hp m
  obtain ⟨C, -, hbound⟩ := LocalPhysicalCopyBounds.physical_sum_jet_bound (K := K) (b := b) hh hh1 ha hZ hr0 hP hB
    (Nat.cast_nonneg q) H Δ m (h * α + σ) p A hA
  refine isBigO_of_bound_on C fun z hz => (hbound f hr hs hc hclass z hz.1 hz.2).trans_eq ?_
  unfold PhysicalClassBounds.physicalLoss
  congr 2; ring

/-- 9. `LocalPhysicalCopyBounds.physical_vector_sum_jet_bound_of_weighted` -/
theorem physical_vector_sum_jet_bound_of_weighted {s : StripData D} {α σ P : ℝ}
    {w : ι → ℕ → D → ℝ} {source : ι → ℕ → D → ℂ}
    (hsource : LocalSourceBounds s h α w source) {f : Fin 3 → CopyFamily H K}
    (hc : ∀ i, SupportCells (f i))
    (hchart : ∀ i, CommonChart (f i) (hc i) a b h r0 σ source)
    (hmap : ∀ i k I, MapsTo ((hchart i).map k I) ((hchart i).domain k I) s.domain)
    (hb : ∀ i, PhysicalCopyBounds.CarrierBounds (f i) (hc i) a b h r0)
    (hr : ∀ i, SupportData (f i) a b h r0 Z Δ)
    (hs : ∀ i, SmoothData (f i) a h r0)
    (hh : 0 < h) (hh1 : h < 1 / 2) (ha : 0 < a) (hZ : 0 ≤ Z) (hr0 : 0 ≤ r0)
    (hP : 1 ≤ P) (hp : ∀ i k L, |((f i).carrier k L).angular| ≤ P ∧
      |((f i).carrier k L).axial| ≤ P ∧ |((f i).carrier k L).radial| ≤ P) (m : ℕ) :
    (fun z => iteratedFDeriv ℝ m (PhysicalCopyBounds.vectorSum f a h r0) z)
      =O[𝓟 {z | z ∈ preterminal ∧ |z.1| ≤ 1}]
      fun z => physicalQ h z ^ (h * α - PhysicalClassBounds.physicalLoss h σ m) :=
  (isBigO_of_bound_on (g := fun z => ∑ i, ‖iteratedFDeriv ℝ m ((f i).sum a h r0) z‖) 3 fun z hz =>
    vectorSum_jet_bound hr hs hc ha hh hh1 hz.1 m fun i =>
      Finset.single_le_sum (f := fun i => ‖iteratedFDeriv ℝ m ((f i).sum a h r0) z‖)
        (fun _ _ => norm_nonneg _) (Finset.mem_univ i)).trans
  (IsBigO.fun_sum fun i _ => (Native.physical_sum_jet_bound_of_weighted hsource (hchart i) (hmap i)
    (hb i) (hr i) (hs i) hh hh1 ha hZ hr0 hP (hp i) m).norm_left)

end Copies

/-! ### 10–13: the physical stage -/

section Stage

open PhysicalWaveSum ActualPhysicalStageBounds

variable {h g delta : ℝ} {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D] {I K : Type*}

/-- 10. `PhysicalStageBounds.WaveData.vector_bound` -/
theorem WaveData.vector_bound (W : PhysicalStageBounds.WaveData h D I K (Fin 3))
    (hh : 0 < h) (hh1 : h < 1 / 2) (m : ℕ) :
    (fun w => iteratedFDeriv ℝ m W.vector w) =O[𝓟 {w | w ∈ preterminal ∧ physicalQ h w ≤ 1}]
      fun w => physicalQ h w ^ (h * W.alpha - PhysicalClassBounds.physicalLoss h W.shift m) :=
  mono_set (Native.physical_vector_sum_jet_bound_of_weighted W.source_bounds W.cells W.chart W.chart_maps
    W.carrier W.support W.smooth hh hh1 W.lower_pos W.slow_nonneg W.width_nonneg W.frequency_one_le
    W.frequencies m) fun _ hw => ⟨hw.1, PhysicalStageBounds.abs_time_le_one hh hh1 hw.1 hw.2⟩

/-- 11. `PhysicalStageBounds.WaveData.vector_bound_with_gain` -/
theorem WaveData.vector_bound_with_gain (W : PhysicalStageBounds.WaveData h D I K (Fin 3))
    (hh : 0 < h) (hh1 : h < 1 / 2) (hg : g ≤ h * W.alpha + W.shift + delta) (m : ℕ) :
    (fun w => iteratedFDeriv ℝ m W.vector w) =O[𝓟 {w | w ∈ preterminal ∧ physicalQ h w ≤ 1}]
      fun w => physicalQ h w ^ (g - (PhysicalGraphBounds.waveLoss h m + delta)) :=
  (Native.WaveData.vector_bound W hh hh1 m).trans
    (isBigO_rpow_of_le (fun _ hw => ⟨physicalQ_pos hh hh1 hw.1, hw.2⟩)
      (by unfold PhysicalClassBounds.physicalLoss; linarith))

end Stage

section Increments

open PhysicalWaveSum ActualPhysicalStageBounds CutStageEstimates

variable {h : ℝ} {DP DS : Type} [NormedAddCommGroup DP] [NormedSpace ℝ DP]
  [NormedAddCommGroup DS] [NormedSpace ℝ DS] {IP KP IS KS : Type*}

/-- 12. `ActualPhysicalStageBounds.potentialIncrement_bound` -/
theorem potentialIncrement_bound
    (WP : PhysicalStageBounds.WaveData h DP IP KP (Fin 3))
    (WS : PhysicalStageBounds.WaveData h DS IS KS (Fin 3))
    (MT MR : MeanInput h (CoordinateAlgebra.A h - 1 / 2))
    (hh : 0 < h) (hh1 : h < 1 / 2) {qbig g dw dm : ℝ}
    (hqT : qbig ≤ ChartScales.Q MT.firstBand) (hqR : qbig ≤ ChartScales.Q MR.firstBand)
    (hWP : g ≤ h * WP.alpha + WP.shift + dw) (hWS : g ≤ h * WS.alpha + WS.shift + dw)
    (hMT : g ≤ h * MT.alpha + dm) (hMR : g ≤ h * MR.alpha + dm) (m : ℕ) :
    (fun w => iteratedFDeriv ℝ m (potentialIncrement WP WS MT MR) w)
      =O[𝓟 {w | w ∈ physicalSublevel h qbig ∧ physicalQ h w ≤ 1}]
      fun w => physicalQ h w ^ (g - PhysicalStageBounds.potentialLoss h dw dm m) := by
  have hQ : ∀ w ∈ {w | w ∈ physicalSublevel h qbig ∧ physicalQ h w ≤ 1},
      0 < physicalQ h w ∧ physicalQ h w ≤ 1 := fun w hw => ⟨physicalQ_pos hh hh1 hw.1.1, hw.2⟩
  have hwave := isBigO_rpow_of_le hQ
    (sub_le_sub_left (le_max_left _ _) g : g - PhysicalStageBounds.potentialLoss h dw dm m ≤ _)
  have hmean := isBigO_rpow_of_le hQ
    (sub_le_sub_left (le_max_right _ _) g : g - PhysicalStageBounds.potentialLoss h dw dm m ≤ _)
  have hp := (mono_set (Native.WaveData.vector_bound_with_gain WP hh hh1 hWP m)
    fun _ hw => ⟨hw.1.1, hw.2⟩).trans hwave
  have hs := (mono_set (Native.WaveData.vector_bound_with_gain WS hh hh1 hWS m)
    fun _ hw => ⟨hw.1.1, hw.2⟩).trans hwave
  obtain ⟨CT, -, hT⟩ := MT.angular_bound_with_gain hh hh1 hqT hMT m
  obtain ⟨CR, -, hR⟩ := MR.angular_bound_with_gain hh hh1 hqR hMR m
  have ht := (isBigO_of_bound_on CT fun w hw => hT w hw.1 hw.2).trans hmean
  have hr := (isBigO_of_bound_on CR fun w hw => hR w hw.1 hw.2).trans hmean
  have sp : ContDiffOn ℝ ∞ WP.vector (physicalSublevel h qbig) :=
    (WP.vector_smooth hh hh1).mono inter_subset_left
  have ss : ContDiffOn ℝ ∞ WS.vector (physicalSublevel h qbig) :=
    (WS.vector_smooth hh hh1).mono inter_subset_left
  have st := MT.angular_smooth hh hh1 hqT
  have hU := physicalSublevel_open hh hh1 qbig
  exact jet_add hU ((sp.add ss).add st) (MR.angular_smooth hh hh1 hqR) (fun _ hw => hw.1)
    (jet_add hU (sp.add ss) st (fun _ hw => hw.1) (jet_add hU sp ss (fun _ hw => hw.1) hp hs) ht) hr

open private potential_gain mean_gain from NavierStokes.ActualPhysicalStageBounds

/-- 13. `ActualPhysicalStageBounds.CycleInputs.potential_bound` -/
theorem CycleInputs.potential_bound {κ qbig : ℝ} (D : CycleInputs h DP IP KP DS IS KS)
    (H : D.Metadata κ) (Q : D.ValidScale qbig)
    (hh : 0 < h) (hh1 : h < 1 / 2) (hκ : κ ≤ 1 / 100000) (k m : ℕ) :
    (fun w => iteratedFDeriv ℝ m (D.potential k) w)
      =O[𝓟 {w | w ∈ physicalSublevel h qbig ∧ physicalQ h w ≤ 1}]
      fun w => physicalQ h w ^
        (ActualIterationLedger.gain h (k + 1) - PhysicalStageBounds.potentialLoss h h 0 m) :=
  Native.potentialIncrement_bound (D.particularPotential k) (D.signedPotential k) (D.temporal k) (D.rank k)
    hh hh1 (Q.temporal k) (Q.rank k)
    (potential_gain hh.le hκ k (H.particularPotential k) (H.particularPotentialShift k))
    (potential_gain hh.le hκ k (H.signedPotential k) (H.signedPotentialShift k))
    (mean_gain hh.le hκ k (H.temporal k)) (mean_gain hh.le hκ k (H.rank k)) m

end Increments

end Lesssim.Native
