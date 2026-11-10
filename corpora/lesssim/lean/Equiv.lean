/-
Constant-threading experiment: nothing is weakened.

`Lesssim.Back.X` has EXACTLY the type of the original corpus theorem (`type_of% @Original`; also checked
structurally in `Measure.lean`) and is proved from `Lesssim.Native.X` alone.
`Lesssim.Fwd.X` has exactly the type of `Lesssim.Native.X` and is proved from the original corpus theorem:
the converse, so the two statements are interderivable.
-/
import Native

noncomputable section

open Asymptotics Filter Set
open scoped Topology ContDiff BigOperators
open NavierStokes NavierStokes.WeightedClasses NavierStokes.LabelSumBounds

namespace Lesssim

section Shapes

variable {X : Type*} {E : Type*} [SeminormedAddCommGroup E] {S : Set X}

/-- shape 1 (bounded on a set), out of the relation -/
theorem back1 {F : X → ℝ} (h : F =O[𝓟 S] fun _ => (1 : ℝ)) : ∃ K : ℝ, 0 ≤ K ∧ ∀ x ∈ S, F x ≤ K :=
  let ⟨C, hC, hb⟩ := exists_bound_on h fun _ _ => zero_le_one
  ⟨C, hC, fun x hx => (le_abs_self _).trans ((hb x hx).trans_eq (mul_one C))⟩

/-- shape 1, into the relation; needs the bounded quantity to be nonnegative -/
theorem fwd1 {F : X → ℝ} (hF : ∀ x ∈ S, 0 ≤ F x) (h : ∃ K : ℝ, 0 ≤ K ∧ ∀ x ∈ S, F x ≤ K) :
    F =O[𝓟 S] fun _ => (1 : ℝ) :=
  let ⟨K, _, hb⟩ := h
  isBigO_of_bound_on K fun x hx => by rw [Real.norm_of_nonneg (hF x hx), mul_one]; exact hb x hx

/-- shape 3 (a power of a positive quantity, on a set cut out by two conditions), out of the relation -/
theorem back3 {P : X → Prop} {F : X → E} {Q : X → ℝ} {r : ℝ} (hQ : ∀ x ∈ S, P x → 0 < Q x)
    (h : F =O[𝓟 {x | x ∈ S ∧ P x}] fun x => Q x ^ r) :
    ∃ C : ℝ, 0 ≤ C ∧ ∀ x ∈ S, P x → ‖F x‖ ≤ C * Q x ^ r :=
  let ⟨C, hC, hb⟩ := exists_bound_on h fun x hx => (Real.rpow_pos_of_pos (hQ x hx.1 hx.2) r).le
  ⟨C, hC, fun x hx hP => hb x ⟨hx, hP⟩⟩

/-- shape 3, into the relation -/
theorem fwd3 {P : X → Prop} {F : X → E} {Q : X → ℝ} {r : ℝ}
    (h : ∃ C : ℝ, 0 ≤ C ∧ ∀ x ∈ S, P x → ‖F x‖ ≤ C * Q x ^ r) :
    F =O[𝓟 {x | x ∈ S ∧ P x}] fun x => Q x ^ r :=
  let ⟨C, _, hb⟩ := h
  isBigO_of_bound_on C fun x hx => hb x hx.1 hx.2

end Shapes

/-! ## The original statements, from the native ones -/

namespace Back

theorem weight_uniform_bound : type_of% @WeightedRadialPrimitive.weight_uniform_bound := by
  intro cL cR hcL hcR L m
  exact back1 (Native.weight_uniform_bound hcL hcR L m)

theorem flat_edge_uniform : type_of% @PhysicalClassBounds.flat_edge_uniform := by
  intro cL cR c hcL hcR hc L m
  exact back1 (Native.flat_edge_uniform hcL hcR hc L m)

theorem FlatGeometry.uniform : type_of% @PhysicalClassBounds.FlatGeometry.uniform := by
  intro D _ _ s cL cR L ρ hg c hc m
  exact back1 (Native.FlatGeometry.uniform hg hc m)

theorem UniformClass.edge_absorbed : type_of% @PhysicalClassBounds.UniformClass.edge_absorbed := by
  intro D _ _ E _ _ ι s cL cR L ρ hg c α hc w f hf hw m
  obtain ⟨p, hp⟩ := Native.UniformClass.edge_absorbed hg hc hf hw m
  obtain ⟨A, hA, hb⟩ := exists_bound_on_le hp fun q _ =>
    mul_nonneg (Real.rpow_nonneg (s.epsilon_pos _).le _) (pow_nonneg (zero_le_one.trans (s.one_le_slow _)) _)
  exact ⟨A, hA, p, fun l n x hx j hj => (hb (l, n, x) hx j hj).trans_eq (mul_assoc _ _ _).symm⟩

theorem LocalSourceBounds.chart_bound :
    type_of% @LocalPhysicalCopyBounds.LocalSourceBounds.chart_bound := by
  intro h D E _ _ _ _ ι s α w source hs m
  obtain ⟨p, hp⟩ := Native.LocalSourceBounds.chart_bound hs m
  obtain ⟨A, hA, hb⟩ := exists_bound_on_le hp fun q hq =>
    mul_nonneg (Real.rpow_nonneg (ChartScales.Q_pos _).le _)
      (pow_nonneg (zero_le_one.trans (PhysicalGraphBounds.S_ge_one (n := q.2.1) (by have := hq.1; omega))) _)
  exact ⟨A, hA, p, fun l n hn x hx j hj => (hb (l, n, x) ⟨hn, hx⟩ j hj).trans_eq (mul_assoc _ _ _).symm⟩

theorem commonChart_amplitude_bound :
    type_of% @LocalPhysicalCopyBounds.commonChart_amplitude_bound := by
  intro H K f a b h r0 D _ _ ι s α σ w source hs hc hchart hmap m
  obtain ⟨p, hp⟩ := Native.commonChart_amplitude_bound hs hchart hmap m
  obtain ⟨A, hA, hb⟩ := exists_bound_on_le hp fun q _ =>
    mul_nonneg (Real.rpow_nonneg (ChartScales.Q_pos _).le _)
      (pow_nonneg (zero_le_one.trans (PhysicalGraphBounds.S_ge_one (n := q.2.1.1.val.1) (by have := q.2.1.1.property; omega))) _)
  exact ⟨A, hA, p, fun k I x hx j hj => (hb (k, I, x) hx j hj).trans_eq (mul_assoc _ _ _).symm⟩

theorem localStrippedClass_of_weighted :
    type_of% @LocalPhysicalCopyBounds.localStrippedClass_of_weighted :=
  @Native.localStrippedClass_of_weighted

theorem physical_sum_jet_bound_of_weighted :
    type_of% @LocalPhysicalCopyBounds.physical_sum_jet_bound_of_weighted := by
  intro H Δ K f a b h r0 Z D _ _ ι s α σ P w source hsource hc hchart hmap hb hr hs hh hh1 ha hZ hr0 hP hp m
  exact back3 (fun z hz _ => PhysicalWaveSum.physicalQ_pos hh hh1 hz)
    (Native.physical_sum_jet_bound_of_weighted hsource hchart hmap hb hr hs hh hh1 ha hZ hr0 hP hp m)

theorem physical_vector_sum_jet_bound_of_weighted :
    type_of% @LocalPhysicalCopyBounds.physical_vector_sum_jet_bound_of_weighted := by
  intro H Δ K a b h r0 Z D _ _ ι s α σ P w source hsource f hc hchart hmap hb hr hs hh hh1 ha hZ hr0 hP hp m
  exact back3 (fun z hz _ => PhysicalWaveSum.physicalQ_pos hh hh1 hz)
    (Native.physical_vector_sum_jet_bound_of_weighted hsource hc hchart hmap hb hr hs hh hh1 ha hZ hr0 hP hp m)

theorem WaveData.vector_bound : type_of% @PhysicalStageBounds.WaveData.vector_bound := by
  intro h D _ _ I K W hh hh1 m
  exact back3 (fun z hz _ => PhysicalWaveSum.physicalQ_pos hh hh1 hz) (Native.WaveData.vector_bound W hh hh1 m)

theorem WaveData.vector_bound_with_gain : type_of% @PhysicalStageBounds.WaveData.vector_bound_with_gain := by
  intro h g delta D _ _ I K W hh hh1 hg m
  exact back3 (fun z hz _ => PhysicalWaveSum.physicalQ_pos hh hh1 hz)
    (Native.WaveData.vector_bound_with_gain W hh hh1 hg m)

theorem potentialIncrement_bound : type_of% @ActualPhysicalStageBounds.potentialIncrement_bound := by
  intro h DP DS _ _ _ _ IP KP IS KS WP WS MT MR hh hh1 qbig g dw dm hqT hqR hWP hWS hMT hMR m
  exact back3 (fun z hz _ => PhysicalWaveSum.physicalQ_pos hh hh1 hz.1)
    (Native.potentialIncrement_bound WP WS MT MR hh hh1 hqT hqR hWP hWS hMT hMR m)

theorem CycleInputs.potential_bound : type_of% @ActualPhysicalStageBounds.CycleInputs.potential_bound := by
  intro h κ qbig DP DS _ _ _ _ IP KP IS KS D H Q hh hh1 hκ k m
  exact back3 (fun z hz _ => PhysicalWaveSum.physicalQ_pos hh hh1 hz.1)
    (Native.CycleInputs.potential_bound D H Q hh hh1 hκ k m)

end Back

/-! ## The native statements, from the original ones (converse) -/

namespace Fwd

theorem weight_uniform_bound : type_of% @Native.weight_uniform_bound := by
  intro cL cR hcL hcR L m
  exact fwd1 (fun x hx => (WeightedRadialPrimitive.weight_pos cL cR m hx).le)
    (WeightedRadialPrimitive.weight_uniform_bound hcL hcR L m)

theorem flat_edge_uniform : type_of% @Native.flat_edge_uniform := by
  intro cL cR c hcL hcR hc L m
  exact fwd1 (fun x hx => mul_nonneg (pow_nonneg (zero_le_one.trans (le_max_left _ _)) _)
    (Real.rpow_nonneg (WeightedRadialPrimitive.zeta_pos cL cR hx).le _))
    (PhysicalClassBounds.flat_edge_uniform hcL hcR hc L m)

theorem FlatGeometry.uniform : type_of% @Native.FlatGeometry.uniform := by
  intro D _ _ s cL cR L ρ hg c hc m
  exact fwd1 (fun x hx => mul_nonneg (pow_nonneg (zero_le_one.trans (le_max_left _ _)) _)
    (Real.rpow_nonneg (s.zeta_nonneg x hx) _)) (hg.uniform hc m)

theorem UniformClass.edge_absorbed : type_of% @Native.UniformClass.edge_absorbed := by
  intro D _ _ E _ _ ι s cL cR L ρ hg c α hc w f hf hw m
  obtain ⟨A, -, p, hb⟩ := PhysicalClassBounds.UniformClass.edge_absorbed hg hc hf hw m
  exact ⟨p, fun j hj => isBigO_of_bound_on A fun q hq => (hb q.1 q.2.1 q.2.2 hq j hj).trans_eq (mul_assoc _ _ _)⟩

theorem LocalSourceBounds.chart_bound : type_of% @Native.LocalSourceBounds.chart_bound := by
  intro D _ _ ι E _ _ h s α w source hs m
  obtain ⟨A, -, p, hb⟩ := hs.chart_bound m
  exact ⟨p, fun j hj => isBigO_of_bound_on A fun q hq =>
    (hb q.1 q.2.1 hq.1 q.2.2 hq.2 j hj).trans_eq (mul_assoc _ _ _)⟩

theorem commonChart_amplitude_bound : type_of% @Native.commonChart_amplitude_bound := by
  intro H K f a b h r0 D _ _ ι s α σ w source hs hc hchart hmap m
  obtain ⟨A, -, p, hb⟩ := LocalPhysicalCopyBounds.commonChart_amplitude_bound hs hchart hmap m
  exact ⟨p, fun j hj => isBigO_of_bound_on A fun q hq => (hb q.1 q.2.1 q.2.2 hq j hj).trans_eq (mul_assoc _ _ _)⟩

theorem physical_sum_jet_bound_of_weighted : type_of% @Native.physical_sum_jet_bound_of_weighted := by
  intro H Δ K f a b h r0 Z D _ _ ι s α σ P w source hsource hc hchart hmap hb hr hs hh hh1 ha hZ hr0 hP hp m
  exact fwd3 (LocalPhysicalCopyBounds.physical_sum_jet_bound_of_weighted hsource hchart hmap hb hr hs
    hh hh1 ha hZ hr0 hP hp m)

theorem physical_vector_sum_jet_bound_of_weighted :
    type_of% @Native.physical_vector_sum_jet_bound_of_weighted := by
  intro H Δ K a b h r0 Z D _ _ ι s α σ P w source hsource f hc hchart hmap hb hr hs hh hh1 ha hZ hr0 hP hp m
  exact fwd3 (LocalPhysicalCopyBounds.physical_vector_sum_jet_bound_of_weighted hsource hc hchart hmap hb
    hr hs hh hh1 ha hZ hr0 hP hp m)

theorem WaveData.vector_bound : type_of% @Native.WaveData.vector_bound := by
  intro h D _ _ I K W hh hh1 m
  exact fwd3 (W.vector_bound hh hh1 m)

theorem WaveData.vector_bound_with_gain : type_of% @Native.WaveData.vector_bound_with_gain := by
  intro h g delta D _ _ I K W hh hh1 hg m
  exact fwd3 (W.vector_bound_with_gain hh hh1 hg m)

theorem potentialIncrement_bound : type_of% @Native.potentialIncrement_bound := by
  intro h DP DS _ _ _ _ IP KP IS KS WP WS MT MR hh hh1 qbig g dw dm hqT hqR hWP hWS hMT hMR m
  exact fwd3 (ActualPhysicalStageBounds.potentialIncrement_bound WP WS MT MR hh hh1 hqT hqR hWP hWS hMT hMR m)

theorem CycleInputs.potential_bound : type_of% @Native.CycleInputs.potential_bound := by
  intro h DP DS _ _ _ _ IP KP IS KS κ qbig D H Q hh hh1 hκ k m
  exact fwd3 (D.potential_bound H Q hh hh1 hκ k m)

end Fwd

end Lesssim
