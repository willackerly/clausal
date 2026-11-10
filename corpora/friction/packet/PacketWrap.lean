/-
Packet experiment, step 1: every theorem of the cluster (the nine frame-carrying theorems of
`Euler.FixedEndpointStrong`, selected by `bench/friction_bundles.py cluster`) restated against
`Frame`, proved FROM the original (namespace `FrictionPacket.Wrap`), and the original statement
proved back FROM the restated one (namespace `FrictionPacket.Back`).
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

namespace FrictionPacket.Wrap

variable {U E : Type*}
  [NormedAddCommGroup U] [InnerProductSpace ℝ U] [CompleteSpace U]
  [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]

variable {T : ℝ} {Q Q₁ : C(Icc (0 : ℝ) T, U →L[ℝ] E)} {c : ℝ} (F : Frame T Q Q₁ c)
  (H : C(Icc (0 : ℝ) T, E →L[ℝ] E))
  (K : ℝ) (hK : 0 ≤ K) (hH : ∀ t v, ⟪H t v, v⟫_ℝ ≤ K * ‖v‖ ^ 2)
  (hsmall : K * (T ^ 2 / 2) ≤ 1 / 2)

theorem fixedEndpointDerivative_weak
    {V : Type*} [NormedAddCommGroup V] [InnerProductSpace ℝ V]
    (L : V →L[ℝ] TimeLp T E) (Y : V)
    (v : TimeLp T U) (hv : initialTrace T F.hT v = 0) :
    let u := fixedEndpointDerivative T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall L Y
    ⟪momentum T F.hT Q u, v⟫_ℝ =
      -⟪initialMomentumForcing T F.hT Q Q₁ H u, primitiveTimeLp T F.hT v⟫_ℝ :=
  EulerFixedEndpointStrong.fixedEndpointDerivative_weak T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall L Y v hv

theorem coordinateSlope_range (ξ : U) (t : Icc (0 : ℝ) T) :
    ∃ x : U, Q t x = initialRealPrimitive T
      (fixedEndpointDerivative T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall
        (affineTrial T F.hT Q Q₁) ξ) t :=
  EulerFixedEndpointStrong.coordinateSlope_range T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall ξ t

theorem coordinateSlope_ae (hTpos : 0 < T) (ξ : U) :
    (coordinateSlope T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall ξ : ℝ → U) =ᵐ[timeMeasure T]
      coordinateVelocityPath T F.hT Q Q₁ c F.hc F.hQ H
        (fixedEndpointDerivative T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall
          (affineTrial T F.hT Q Q₁) ξ) :=
  EulerFixedEndpointStrong.coordinateSlope_ae T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall hTpos ξ

section Regularity

variable (Q₂ : C(Icc (0 : ℝ) T, U →L[ℝ] E)) (hTpos : 0 < T)
  (hd₁ : ∀ t : Icc (0 : ℝ) T,
    HasDerivWithinAt (extendPath T F.hT Q₁) (Q₂ t) (Icc (0 : ℝ) T) t)
  (hframe : ∀ t, Q₂ t = -((H t).comp (Q t)))

include hd₁ hframe hTpos in
theorem coordinate_equation (ξ : U) (t : Icc (0 : ℝ) T) :
    let u := fixedEndpointDerivative T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall
      (affineTrial T F.hT Q Q₁) ξ
    HasDerivWithinAt (initialCoordinates T F.hT Q c F.hc F.hQ u)
        (coordinateVelocityPath T F.hT Q Q₁ c F.hc F.hQ H u t) (Icc (0 : ℝ) T) t ∧
      HasDerivWithinAt (coordinateVelocityPath T F.hT Q Q₁ c F.hc F.hQ H u)
        (generator T Q Q₁ c F.hc F.hQ t (coordinateVelocityPath T F.hT Q Q₁ c F.hc F.hQ H u t))
        (Icc (0 : ℝ) T) t :=
  EulerFixedEndpointStrong.coordinate_equation T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall Q₂ hTpos hd₁ hframe ξ t

include hd₁ hframe hTpos in
theorem coordinateSlope_h1 (ξ : U) :
    let v := coordinateVelocityPath T F.hT Q Q₁ c F.hc F.hQ H
      (fixedEndpointDerivative T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall
        (affineTrial T F.hT Q Q₁) ξ)
    AbsolutelyContinuousOnInterval v 0 T ∧
      (coordinateSlope T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall ξ : ℝ → U) =ᵐ[timeMeasure T] v ∧
      ∀ᵐ t ∂timeMeasure T,
        HasDerivAt v (coordinateAcceleration T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall ξ t) t :=
  EulerFixedEndpointStrong.coordinateSlope_h1 T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall Q₂ hTpos hd₁ hframe ξ

include hd₁ hframe hTpos in
theorem continuousCoordinateVelocity_eq (ξ : U) (t : Icc (0 : ℝ) T) :
    continuousCoordinateVelocity T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall ξ t =
      coordinateVelocityPath T F.hT Q Q₁ c F.hc F.hQ H
        (fixedEndpointDerivative T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall
          (affineTrial T F.hT Q Q₁) ξ) t :=
  EulerFixedEndpointStrong.continuousCoordinateVelocity_eq T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall Q₂ hTpos hd₁ hframe ξ t

include hd₁ hframe hTpos in
theorem historyVelocity_eq (ξ : U) (t : Icc (0 : ℝ) T) :
    historyVelocity T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall ξ t =
      Q t (coordinateVelocityPath T F.hT Q Q₁ c F.hc F.hQ H
        (fixedEndpointDerivative T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall
          (affineTrial T F.hT Q Q₁) ξ) t) :=
  EulerFixedEndpointStrong.historyVelocity_eq T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall Q₂ hTpos hd₁ hframe ξ t

include hd₁ hframe hTpos in
theorem continuousCoordinateVelocity_hasDerivWithinAt_generator (ξ : U) (t : Icc (0 : ℝ) T) :
    HasDerivWithinAt
      (extendPath T F.hT (continuousCoordinateVelocity T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall ξ))
      (generator T Q Q₁ c F.hc F.hQ t
        (continuousCoordinateVelocity T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall ξ t))
      (Icc (0 : ℝ) T) t :=
  EulerFixedEndpointStrong.continuousCoordinateVelocity_hasDerivWithinAt_generator
    T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall Q₂ hTpos hd₁ hframe ξ t

include hd₁ hframe hTpos in
theorem continuousCoordinateVelocity_eq_forward
    (evolution : Evolution T F.hT (generator T Q Q₁ c F.hc F.hQ))
    (ξ : U) (t : Icc (0 : ℝ) T) :
    continuousCoordinateVelocity T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall ξ t =
      coordinates T F.hT Q Q₁ c F.hc F.hQ evolution 0
        (continuousCoordinateVelocity T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall ξ ⟨0, le_rfl, F.hT⟩) t :=
  EulerFixedEndpointStrong.continuousCoordinateVelocity_eq_forward
    T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall Q₂ hTpos hd₁ hframe evolution ξ t

end Regularity

end FrictionPacket.Wrap

/-! ### the converse: each ORIGINAL statement from the restated one -/

namespace FrictionPacket.Back

variable {U E : Type*}
  [NormedAddCommGroup U] [InnerProductSpace ℝ U] [CompleteSpace U]
  [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]

variable (T : ℝ) (hT : 0 ≤ T)
  (Q Q₁ : C(Icc (0 : ℝ) T, U →L[ℝ] E))
  (H : C(Icc (0 : ℝ) T, E →L[ℝ] E))
  (c : ℝ) (hc : 0 < c) (hQ : ∀ t v, c * ‖v‖ ^ 2 ≤ ‖Q t v‖ ^ 2)
  (hd : ∀ t : Icc (0 : ℝ) T,
    HasDerivWithinAt (extendPath T hT Q) (Q₁ t) (Icc (0 : ℝ) T) t)
  (K : ℝ) (hK : 0 ≤ K) (hH : ∀ t v, ⟪H t v, v⟫_ℝ ≤ K * ‖v‖ ^ 2)
  (hsmall : K * (T ^ 2 / 2) ≤ 1 / 2)

theorem fixedEndpointDerivative_weak
    {V : Type*} [NormedAddCommGroup V] [InnerProductSpace ℝ V]
    (L : V →L[ℝ] TimeLp T E) (Y : V)
    (v : TimeLp T U) (hv : initialTrace T hT v = 0) :
    let u := fixedEndpointDerivative T hT Q Q₁ H c hc hQ hd K hK hH hsmall L Y
    ⟪momentum T hT Q u, v⟫_ℝ =
      -⟪initialMomentumForcing T hT Q Q₁ H u, primitiveTimeLp T hT v⟫_ℝ :=
  Wrap.fixedEndpointDerivative_weak (Frame.mk hT hc hQ hd) H K hK hH hsmall L Y v hv

theorem coordinateSlope_range (ξ : U) (t : Icc (0 : ℝ) T) :
    ∃ x : U, Q t x = initialRealPrimitive T
      (fixedEndpointDerivative T hT Q Q₁ H c hc hQ hd K hK hH hsmall
        (affineTrial T hT Q Q₁) ξ) t :=
  Wrap.coordinateSlope_range (Frame.mk hT hc hQ hd) H K hK hH hsmall ξ t

theorem coordinateSlope_ae (hTpos : 0 < T) (ξ : U) :
    (coordinateSlope T hT Q Q₁ H c hc hQ hd K hK hH hsmall ξ : ℝ → U) =ᵐ[timeMeasure T]
      coordinateVelocityPath T hT Q Q₁ c hc hQ H
        (fixedEndpointDerivative T hT Q Q₁ H c hc hQ hd K hK hH hsmall
          (affineTrial T hT Q Q₁) ξ) :=
  Wrap.coordinateSlope_ae (Frame.mk hT hc hQ hd) H K hK hH hsmall hTpos ξ

section Regularity

variable (Q₂ : C(Icc (0 : ℝ) T, U →L[ℝ] E)) (hTpos : 0 < T)
  (hd₁ : ∀ t : Icc (0 : ℝ) T,
    HasDerivWithinAt (extendPath T hT Q₁) (Q₂ t) (Icc (0 : ℝ) T) t)
  (hframe : ∀ t, Q₂ t = -((H t).comp (Q t)))

include hd₁ hframe hTpos in
theorem coordinate_equation (ξ : U) (t : Icc (0 : ℝ) T) :
    let u := fixedEndpointDerivative T hT Q Q₁ H c hc hQ hd K hK hH hsmall
      (affineTrial T hT Q Q₁) ξ
    HasDerivWithinAt (initialCoordinates T hT Q c hc hQ u)
        (coordinateVelocityPath T hT Q Q₁ c hc hQ H u t) (Icc (0 : ℝ) T) t ∧
      HasDerivWithinAt (coordinateVelocityPath T hT Q Q₁ c hc hQ H u)
        (generator T Q Q₁ c hc hQ t (coordinateVelocityPath T hT Q Q₁ c hc hQ H u t))
        (Icc (0 : ℝ) T) t :=
  Wrap.coordinate_equation (Frame.mk hT hc hQ hd) H K hK hH hsmall Q₂ hTpos hd₁ hframe ξ t

include hd₁ hframe hTpos in
theorem coordinateSlope_h1 (ξ : U) :
    let v := coordinateVelocityPath T hT Q Q₁ c hc hQ H
      (fixedEndpointDerivative T hT Q Q₁ H c hc hQ hd K hK hH hsmall
        (affineTrial T hT Q Q₁) ξ)
    AbsolutelyContinuousOnInterval v 0 T ∧
      (coordinateSlope T hT Q Q₁ H c hc hQ hd K hK hH hsmall ξ : ℝ → U) =ᵐ[timeMeasure T] v ∧
      ∀ᵐ t ∂timeMeasure T,
        HasDerivAt v (coordinateAcceleration T hT Q Q₁ H c hc hQ hd K hK hH hsmall ξ t) t :=
  Wrap.coordinateSlope_h1 (Frame.mk hT hc hQ hd) H K hK hH hsmall Q₂ hTpos hd₁ hframe ξ

include hd₁ hframe hTpos in
theorem continuousCoordinateVelocity_eq (ξ : U) (t : Icc (0 : ℝ) T) :
    continuousCoordinateVelocity T hT Q Q₁ H c hc hQ hd K hK hH hsmall ξ t =
      coordinateVelocityPath T hT Q Q₁ c hc hQ H
        (fixedEndpointDerivative T hT Q Q₁ H c hc hQ hd K hK hH hsmall
          (affineTrial T hT Q Q₁) ξ) t :=
  Wrap.continuousCoordinateVelocity_eq (Frame.mk hT hc hQ hd) H K hK hH hsmall Q₂ hTpos hd₁ hframe ξ t

include hd₁ hframe hTpos in
theorem historyVelocity_eq (ξ : U) (t : Icc (0 : ℝ) T) :
    historyVelocity T hT Q Q₁ H c hc hQ hd K hK hH hsmall ξ t =
      Q t (coordinateVelocityPath T hT Q Q₁ c hc hQ H
        (fixedEndpointDerivative T hT Q Q₁ H c hc hQ hd K hK hH hsmall
          (affineTrial T hT Q Q₁) ξ) t) :=
  Wrap.historyVelocity_eq (Frame.mk hT hc hQ hd) H K hK hH hsmall Q₂ hTpos hd₁ hframe ξ t

include hd₁ hframe hTpos in
theorem continuousCoordinateVelocity_hasDerivWithinAt_generator (ξ : U) (t : Icc (0 : ℝ) T) :
    HasDerivWithinAt
      (extendPath T hT (continuousCoordinateVelocity T hT Q Q₁ H c hc hQ hd K hK hH hsmall ξ))
      (generator T Q Q₁ c hc hQ t
        (continuousCoordinateVelocity T hT Q Q₁ H c hc hQ hd K hK hH hsmall ξ t))
      (Icc (0 : ℝ) T) t :=
  Wrap.continuousCoordinateVelocity_hasDerivWithinAt_generator (Frame.mk hT hc hQ hd)
    H K hK hH hsmall Q₂ hTpos hd₁ hframe ξ t

include hd₁ hframe hTpos in
theorem continuousCoordinateVelocity_eq_forward
    (evolution : Evolution T hT (generator T Q Q₁ c hc hQ))
    (ξ : U) (t : Icc (0 : ℝ) T) :
    continuousCoordinateVelocity T hT Q Q₁ H c hc hQ hd K hK hH hsmall ξ t =
      coordinates T hT Q Q₁ c hc hQ evolution 0
        (continuousCoordinateVelocity T hT Q Q₁ H c hc hQ hd K hK hH hsmall ξ ⟨0, le_rfl, hT⟩) t :=
  Wrap.continuousCoordinateVelocity_eq_forward (Frame.mk hT hc hQ hd)
    H K hK hH hsmall Q₂ hTpos hd₁ hframe evolution ξ t

end Regularity

end FrictionPacket.Back
