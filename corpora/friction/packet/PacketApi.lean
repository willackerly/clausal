/-
Packet experiment, step 3: the best case for the packet.  The restated statements of step 1 still
take the packet apart (`F.hT`, `F.hc`, ...) at every operation, because every DEFINITION of the
corpus consumes the four facts one by one.  Here each operation that occurs in the nine statements
gets a packet-level wrapper (the "API per operation" cost: 16 definitions), and the nine theorems
are restated once more against that API and proved from step 1.
-/
import PacketWrap

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

namespace FrictionPacket

variable {U E : Type*}
  [NormedAddCommGroup U] [InnerProductSpace ℝ U] [CompleteSpace U]
  [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]

variable {T : ℝ} {Q Q₁ : C(Icc (0 : ℝ) T, U →L[ℝ] E)} {c : ℝ} (F : Frame T Q Q₁ c)
  (H : C(Icc (0 : ℝ) T, E →L[ℝ] E))
  (K : ℝ) (hK : 0 ≤ K) (hH : ∀ t v, ⟪H t v, v⟫_ℝ ≤ K * ‖v‖ ^ 2)
  (hsmall : K * (T ^ 2 / 2) ≤ 1 / 2)

/-! #### glue: one wrapper per operation used in the cluster's statements -/

abbrev Frame.initialTrace := EulerTerminalTimePrimitive.initialTrace (E := U) T F.hT
abbrev Frame.primitiveTimeLp := EulerTerminalTimePrimitive.primitiveTimeLp (E := U) T F.hT
abbrev Frame.momentum := EulerTransverseMomentumRegularity.momentum T F.hT Q
abbrev Frame.initialMomentumForcing :=
  EulerTransverseEndpointMomentum.initialMomentumForcing T F.hT Q Q₁ H
abbrev Frame.affineTrial := EulerTransverseEndpointParameter.affineTrial T F.hT Q Q₁
abbrev Frame.fixedEndpointDerivative {V : Type*} [NormedAddCommGroup V] [InnerProductSpace ℝ V]
    (L : V →L[ℝ] TimeLp T E) (Y : V) :=
  EulerTransverseFixedEndpoint.fixedEndpointDerivative T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall L Y
abbrev Frame.coordinateSlope :=
  EulerTransverseEndpointCoordinates.coordinateSlope T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall
abbrev Frame.coordinateAcceleration :=
  EulerTransverseEndpointCoordinates.coordinateAcceleration T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall
abbrev Frame.continuousCoordinateVelocity :=
  EulerTransverseEndpointCoordinates.continuousCoordinateVelocity T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall
abbrev Frame.historyVelocity :=
  EulerTransverseEndpointCoordinates.historyVelocity T F.hT Q Q₁ H c F.hc F.hQ F.hd K hK hH hsmall
abbrev Frame.coordinateVelocityPath :=
  EulerTransverseEndpointVelocity.coordinateVelocityPath T F.hT Q Q₁ c F.hc F.hQ H
abbrev Frame.initialCoordinates :=
  EulerTransverseInitialCoordinates.initialCoordinates T F.hT Q c F.hc F.hQ
abbrev Frame.generator := EulerTransverseForwardInverse.generator T Q Q₁ c F.hc F.hQ
abbrev Frame.extendPathU := EulerVolterraConvolution.extendPath (Y := U) T F.hT
abbrev Frame.Evolution := EulerLinearDuhamel.Evolution T F.hT F.generator
abbrev Frame.coordinates := EulerTransverseForwardInverse.coordinates T F.hT Q Q₁ c F.hc F.hQ
abbrev Frame.zero : Icc (0 : ℝ) T := ⟨0, le_rfl, F.hT⟩

namespace Api

theorem fixedEndpointDerivative_weak
    {V : Type*} [NormedAddCommGroup V] [InnerProductSpace ℝ V]
    (L : V →L[ℝ] TimeLp T E) (Y : V)
    (v : TimeLp T U) (hv : F.initialTrace v = 0) :
    let u := F.fixedEndpointDerivative H K hK hH hsmall L Y
    ⟪F.momentum u, v⟫_ℝ = -⟪F.initialMomentumForcing H u, F.primitiveTimeLp v⟫_ℝ :=
  Wrap.fixedEndpointDerivative_weak F H K hK hH hsmall L Y v hv

theorem coordinateSlope_range (ξ : U) (t : Icc (0 : ℝ) T) :
    ∃ x : U, Q t x = initialRealPrimitive T
      (F.fixedEndpointDerivative H K hK hH hsmall F.affineTrial ξ) t :=
  Wrap.coordinateSlope_range F H K hK hH hsmall ξ t

theorem coordinateSlope_ae (hTpos : 0 < T) (ξ : U) :
    (F.coordinateSlope H K hK hH hsmall ξ : ℝ → U) =ᵐ[timeMeasure T]
      F.coordinateVelocityPath H (F.fixedEndpointDerivative H K hK hH hsmall F.affineTrial ξ) :=
  Wrap.coordinateSlope_ae F H K hK hH hsmall hTpos ξ

section Regularity

variable (Q₂ : C(Icc (0 : ℝ) T, U →L[ℝ] E)) (hTpos : 0 < T)
  (hd₁ : ∀ t : Icc (0 : ℝ) T,
    HasDerivWithinAt (extendPath T F.hT Q₁) (Q₂ t) (Icc (0 : ℝ) T) t)
  (hframe : ∀ t, Q₂ t = -((H t).comp (Q t)))

include hd₁ hframe hTpos in
theorem coordinate_equation (ξ : U) (t : Icc (0 : ℝ) T) :
    let u := F.fixedEndpointDerivative H K hK hH hsmall F.affineTrial ξ
    HasDerivWithinAt (F.initialCoordinates u) (F.coordinateVelocityPath H u t) (Icc (0 : ℝ) T) t ∧
      HasDerivWithinAt (F.coordinateVelocityPath H u)
        (F.generator t (F.coordinateVelocityPath H u t)) (Icc (0 : ℝ) T) t :=
  Wrap.coordinate_equation F H K hK hH hsmall Q₂ hTpos hd₁ hframe ξ t

include hd₁ hframe hTpos in
theorem coordinateSlope_h1 (ξ : U) :
    let v := F.coordinateVelocityPath H (F.fixedEndpointDerivative H K hK hH hsmall F.affineTrial ξ)
    AbsolutelyContinuousOnInterval v 0 T ∧
      (F.coordinateSlope H K hK hH hsmall ξ : ℝ → U) =ᵐ[timeMeasure T] v ∧
      ∀ᵐ t ∂timeMeasure T, HasDerivAt v (F.coordinateAcceleration H K hK hH hsmall ξ t) t :=
  Wrap.coordinateSlope_h1 F H K hK hH hsmall Q₂ hTpos hd₁ hframe ξ

include hd₁ hframe hTpos in
theorem continuousCoordinateVelocity_eq (ξ : U) (t : Icc (0 : ℝ) T) :
    F.continuousCoordinateVelocity H K hK hH hsmall ξ t =
      F.coordinateVelocityPath H (F.fixedEndpointDerivative H K hK hH hsmall F.affineTrial ξ) t :=
  Wrap.continuousCoordinateVelocity_eq F H K hK hH hsmall Q₂ hTpos hd₁ hframe ξ t

include hd₁ hframe hTpos in
theorem historyVelocity_eq (ξ : U) (t : Icc (0 : ℝ) T) :
    F.historyVelocity H K hK hH hsmall ξ t =
      Q t (F.coordinateVelocityPath H (F.fixedEndpointDerivative H K hK hH hsmall F.affineTrial ξ) t) :=
  Wrap.historyVelocity_eq F H K hK hH hsmall Q₂ hTpos hd₁ hframe ξ t

include hd₁ hframe hTpos in
theorem continuousCoordinateVelocity_hasDerivWithinAt_generator (ξ : U) (t : Icc (0 : ℝ) T) :
    HasDerivWithinAt (F.extendPathU (F.continuousCoordinateVelocity H K hK hH hsmall ξ))
      (F.generator t (F.continuousCoordinateVelocity H K hK hH hsmall ξ t)) (Icc (0 : ℝ) T) t :=
  Wrap.continuousCoordinateVelocity_hasDerivWithinAt_generator F H K hK hH hsmall Q₂ hTpos hd₁ hframe ξ t

include hd₁ hframe hTpos in
theorem continuousCoordinateVelocity_eq_forward (evolution : F.Evolution) (ξ : U) (t : Icc (0 : ℝ) T) :
    F.continuousCoordinateVelocity H K hK hH hsmall ξ t =
      F.coordinates evolution 0 (F.continuousCoordinateVelocity H K hK hH hsmall ξ F.zero) t :=
  Wrap.continuousCoordinateVelocity_eq_forward F H K hK hH hsmall Q₂ hTpos hd₁ hframe evolution ξ t

end Regularity

end Api

end FrictionPacket
