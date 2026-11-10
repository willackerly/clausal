/-
Packet experiment, step 2: the nine cluster theorems RE-PROVED directly against `Frame`.
Generated from corpora/ns/Euler/FixedEndpointStrong.lean by a mechanical port (see
out/corpus/friction/BUNDLES.md): calls to cluster lemmas take the packet `F`; every other lemma of
the corpus is still unbundled, so the packet is taken apart again at each such call (`F.hT`, ...).
No original cluster theorem is used: each proof below goes through the packet versions in this file.
-/
import PacketFrame

noncomputable section

open Set MeasureTheory ContinuousLinearMap InnerProductSpace
  EulerTimeLp EulerTerminalTimePrimitive EulerInitialTimePrimitive
  EulerVolterraConvolution EulerTimeH1OperatorProduct EulerTimeH1FrameTransport
  EulerTransverseGramInverse EulerTransverseGramPath EulerTransverseInitialCoordinates
  EulerTransverseInitialInverse EulerTransverseEndpointEnergy EulerTransverseFixedEndpoint
  EulerTransverseFixedSpaceInverse EulerTransverseEndpointParameter
  EulerTransverseEndpointMomentum EulerTransverseMomentumRegularity
  EulerTransverseEndpointVelocity EulerTransverseEndpointDifferentiation
  EulerTransverseEndpointEquation EulerTransverseEndpointCoordinates
  EulerTransverseForwardInverse EulerTimeH1Reconstruction EulerContinuousTimeIntegral
  EulerLinearDuhamel

namespace FrictionPacket.Direct

variable {U E : Type*}
  [NormedAddCommGroup U] [InnerProductSpace ℝ U] [CompleteSpace U]
  [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]

variable {T : ℝ} {Q Q₁ : C(Icc (0 : ℝ) T, U →L[ℝ] E)} {c : ℝ} (F : Frame T Q Q₁ c)
  (H : C(Icc (0 : ℝ) T, E →L[ℝ] E))
  (K : ℝ) (hK : 0 ≤ K) (hH : ∀ t v, ⟪H t v, v⟫_ℝ ≤ K * ‖v‖ ^ 2)
  (hsmall : K * (T ^ 2 / 2) ≤ 1 / 2)

/-- The constructed fixed-coordinate endpoint inverse obeys the literal
weak momentum identity, for every trial lift. -/
theorem fixedEndpointDerivative_weak
    {V : Type*} [NormedAddCommGroup V] [InnerProductSpace ℝ V]
    (L : V →L[ℝ] TimeLp T E) (Y : V)
    (v : TimeLp T U) (hv : initialTrace T F.hT v = 0) :
    let u := fixedEndpointDerivative T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall L Y
    ⟪momentum T F.hT Q u, v⟫_ℝ =
      -⟪initialMomentumForcing T F.hT Q Q₁ H u, primitiveTimeLp T F.hT v⟫_ℝ := by
  dsimp only
  have ht := fixedEndpointDerivative_orthogonal T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall L Y ⟨v, hv⟩
  rw [energyOperator_inner,
    initialPrimitiveTimeLp_eq_primitive_of_trace_zero T F.hT _
      (fixedFrameDerivative_trace_zero T F.hT Q Q₁ F.hd ⟨v, hv⟩)] at ht
  change ⟪fixedEndpointDerivative T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall L Y,
      productDerivative T F.hT Q Q₁ v⟫_ℝ -
    ⟪timeMultiplier T F.hT H (initialPrimitiveTimeLp T F.hT
      (fixedEndpointDerivative T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall L Y)),
      primitiveTimeLp T F.hT (productDerivative T F.hT Q Q₁ v)⟫_ℝ = 0 at ht
  rw [primitiveTimeLp_productDerivative T F.hT Q Q₁ F.hd] at ht
  simp only [productDerivative, add_apply, comp_apply, inner_add_right] at ht
  simp only [momentum, initialMomentumForcing, sub_apply, comp_apply,
    inner_sub_left, adjoint_inner_left]
  linarith only [ht]

/-- The affine fixed-coordinate solution lies in the actual frame range
at every time, including the two endpoints. -/
theorem coordinateSlope_range (ξ : U) (t : Icc (0 : ℝ) T) :
    ∃ x : U, Q t x = initialRealPrimitive T
      (fixedEndpointDerivative T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall
        (affineTrial T F.hT Q Q₁) ξ) t := by
  rw [← coordinateSlope_product T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall ξ]
  exact ⟨initialPrimitive T F.hT (coordinateSlope T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall ξ) t,
    (initialPrimitive_initialProductDerivative T F.hT Q Q₁ F.hd _ t).symm⟩

/-- The continuous momentum reconstruction represents the explicit
coordinate derivative of the fixed affine-terminal solution. -/
theorem coordinateSlope_ae (hTpos : 0 < T) (ξ : U) :
    (coordinateSlope T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall ξ : ℝ → U) =ᵐ[timeMeasure T]
      coordinateVelocityPath T F.hT Q Q₁ c F.hc F.hQ H
        (fixedEndpointDerivative T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall
          (affineTrial T F.hT Q Q₁) ξ) := by
  rw [← coordinateSlope_derivative T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall ξ]
  exact coordinateVelocityPath_ae T F.hT Q Q₁ c F.hc F.hQ H F.hd hTpos _
    (fixedEndpointDerivative_weak F H K hK hH hsmall _ ξ)
    (coordinateSlope_range F H K hK hH hsmall ξ)

section Regularity

variable (Q₂ : C(Icc (0 : ℝ) T, U →L[ℝ] E)) (hTpos : 0 < T)
  (hd₁ : ∀ t : Icc (0 : ℝ) T,
    HasDerivWithinAt (extendPath T F.hT Q₁) (Q₂ t) (Icc (0 : ℝ) T) t)
  (hframe : ∀ t, Q₂ t = -((H t).comp (Q t)))

include hd₁ hframe hTpos in
/-- Equation (10) for the constructed affine-terminal fixed-space inverse. -/
theorem coordinate_equation (ξ : U) (t : Icc (0 : ℝ) T) :
    let u := fixedEndpointDerivative T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall
      (affineTrial T F.hT Q Q₁) ξ
    HasDerivWithinAt (initialCoordinates T F.hT Q c F.hc F.hQ u)
        (coordinateVelocityPath T F.hT Q Q₁ c F.hc F.hQ H u t) (Icc (0 : ℝ) T) t ∧
      HasDerivWithinAt (coordinateVelocityPath T F.hT Q Q₁ c F.hc F.hQ H u)
        (generator T Q Q₁ c F.hc F.hQ t (coordinateVelocityPath T F.hT Q Q₁ c F.hc F.hQ H u t))
        (Icc (0 : ℝ) T) t := by
  dsimp only
  have hw := fixedEndpointDerivative_weak F H K hK hH hsmall
    (affineTrial T F.hT Q Q₁) ξ
  have hr := coordinateSlope_range F H K hK hH hsmall ξ
  exact ⟨initialCoordinates_hasDerivWithinAt T F.hT Q Q₁ c F.hc F.hQ H hTpos F.hd _ hw hr t,
    coordinateVelocityPath_hasDerivWithinAt_generator T F.hT Q Q₁ Q₂ c F.hc F.hQ H
      hTpos F.hd hd₁ hframe _ hw hr t⟩

include hd₁ hframe hTpos in
theorem coordinateSlope_h1 (ξ : U) :
    let v := coordinateVelocityPath T F.hT Q Q₁ c F.hc F.hQ H
      (fixedEndpointDerivative T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall
        (affineTrial T F.hT Q Q₁) ξ)
    AbsolutelyContinuousOnInterval v 0 T ∧
      (coordinateSlope T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall ξ : ℝ → U) =ᵐ[timeMeasure T] v ∧
      ∀ᵐ t ∂timeMeasure T,
        HasDerivAt v (coordinateAcceleration T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall ξ t) t := by
  dsimp only
  let u := fixedEndpointDerivative T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall
    (affineTrial T F.hT Q Q₁) ξ
  let v := coordinateVelocityPath T F.hT Q Q₁ c F.hc F.hQ H u
  have hv := coordinateVelocityPath_continuous T F.hT Q Q₁ c F.hc F.hQ H u
  let g : C(Icc (0 : ℝ) T, U) := ⟨fun t => generator T Q Q₁ c F.hc F.hQ t (v t),
    (generator T Q Q₁ c F.hc F.hQ).continuous.clm_apply (hv.comp continuous_subtype_val)⟩
  have hdv (t : Icc (0 : ℝ) T) : HasDerivWithinAt v (g t) (Icc (0 : ℝ) T) t :=
    (coordinate_equation F H K hK hH hsmall Q₂ hTpos hd₁ hframe ξ t).2
  have hcont : AbsolutelyContinuousOnInterval v 0 T := by
    have hl : LipschitzOnWith ‖g‖₊ v (Icc (0 : ℝ) T) := by
      apply (convex_Icc (0 : ℝ) T).lipschitzOnWith_of_nnnorm_hasDerivWithin_le
        (f' := extendPath T F.hT g)
      · intro t ht
        simpa only [extendPath, projIcc_of_mem F.hT ht] using hdv ⟨t, ht⟩
      · intro t ht
        exact g.norm_coe_le_norm (projIcc 0 T F.hT t)
    exact (show LipschitzOnWith ‖g‖₊ v (uIcc (0 : ℝ) T) by
      simpa only [uIcc_of_le F.hT] using hl).absolutelyContinuousOnInterval
  have hae := coordinateSlope_ae F H K hK hH hsmall hTpos ξ
  refine ⟨hcont, hae, ?_⟩
  have hmem : ∀ᵐ t ∂timeMeasure T, t ∈ Ioo (0 : ℝ) T := by
    change ∀ᵐ t ∂volume.restrict (Icc (0 : ℝ) T), t ∈ Ioo (0 : ℝ) T
    rw [← restrict_Ioo_eq_restrict_Icc]
    exact ae_restrict_mem measurableSet_Ioo
  filter_upwards [hmem, hae, timeMultiplier_ae T F.hT (generator T Q Q₁ c F.hc F.hQ)
    (coordinateSlope T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall ξ)] with t ht hs ha
  have hti : t ∈ Icc (0 : ℝ) T := ⟨ht.1.le, ht.2.le⟩
  change HasDerivAt v (timeMultiplier T F.hT (generator T Q Q₁ c F.hc F.hQ)
    (coordinateSlope T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall ξ) t) t
  rw [ha, hs]
  have hdt := (hdv ⟨t, hti⟩).hasDerivAt (Icc_mem_nhds ht.1 ht.2)
  change HasDerivAt v (generator T Q Q₁ c F.hc F.hQ ⟨t, hti⟩ (v t)) t at hdt
  simpa only [extendPath, projIcc_of_mem F.hT hti] using hdt

include hd₁ hframe hTpos in
/-- The existing bounded reconstruction is this actual stationary coordinate
velocity at every time. -/
theorem continuousCoordinateVelocity_eq (ξ : U) (t : Icc (0 : ℝ) T) :
    continuousCoordinateVelocity T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall ξ t =
      coordinateVelocityPath T F.hT Q Q₁ c F.hc F.hQ H
        (fixedEndpointDerivative T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall
          (affineTrial T F.hT Q Q₁) ξ) t := by
  have hreg := coordinateSlope_h1 F H K hK hH hsmall Q₂ hTpos hd₁ hframe ξ
  exact reconstruction_eq_path T hTpos _ _ _ hreg.1 hreg.2.1 hreg.2.2 t

include hd₁ hframe hTpos in
theorem historyVelocity_eq (ξ : U) (t : Icc (0 : ℝ) T) :
    historyVelocity T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall ξ t =
      Q t (coordinateVelocityPath T F.hT Q Q₁ c F.hc F.hQ H
        (fixedEndpointDerivative T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall
          (affineTrial T F.hT Q Q₁) ξ) t) := by
  change Q t (continuousCoordinateVelocity T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall ξ t) = _
  rw [continuousCoordinateVelocity_eq F H K hK hH hsmall Q₂ hTpos hd₁ hframe]

include hd₁ hframe hTpos in
theorem continuousCoordinateVelocity_hasDerivWithinAt_generator (ξ : U) (t : Icc (0 : ℝ) T) :
    HasDerivWithinAt
      (extendPath T F.hT (continuousCoordinateVelocity T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall ξ))
      (generator T Q Q₁ c F.hc F.hQ t
        (continuousCoordinateVelocity T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall ξ t))
      (Icc (0 : ℝ) T) t := by
  have hv := (coordinate_equation F H K hK hH hsmall Q₂ hTpos hd₁ hframe ξ t).2
  rw [← continuousCoordinateVelocity_eq F H K hK hH hsmall Q₂ hTpos hd₁ hframe ξ t] at hv
  apply hv.congr_of_mem _ t.property
  intro s hs
  simpa only [extendPath, projIcc_of_mem F.hT hs] using
    continuousCoordinateVelocity_eq F H K hK hH hsmall Q₂ hTpos hd₁ hframe ξ ⟨s, hs⟩

include hd₁ hframe hTpos in
/-- The affine-terminal coordinate history coincides with the actual
homogeneous forward solver with its own initial velocity. -/
theorem continuousCoordinateVelocity_eq_forward
    (evolution : Evolution T F.hT (generator T Q Q₁ c F.hc F.hQ))
    (ξ : U) (t : Icc (0 : ℝ) T) :
    continuousCoordinateVelocity T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall ξ t =
      coordinates T F.hT Q Q₁ c F.hc F.hQ evolution 0
        (continuousCoordinateVelocity T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall ξ ⟨0, le_rfl, F.hT⟩) t := by
  rw [continuousCoordinateVelocity_eq F H K hK hH hsmall Q₂ hTpos hd₁ hframe ξ t,
    continuousCoordinateVelocity_eq F H K hK hH hsmall Q₂ hTpos hd₁ hframe ξ ⟨0, le_rfl, F.hT⟩]
  exact coordinateVelocity_eq_forward T F.hT Q Q₁ Q₂ c F.hc F.hQ H hTpos F.hd hd₁ hframe _
    (fixedEndpointDerivative_weak F H K hK hH hsmall _ ξ)
    (coordinateSlope_range F H K hK hH hsmall ξ) evolution t

end Regularity


end FrictionPacket.Direct
