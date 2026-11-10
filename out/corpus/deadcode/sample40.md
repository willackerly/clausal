## 1. `NavierStokes.ClosedIntervalCk.primitiveLinear` (def) NavierStokes.ClosedIntervalCk:50-58
rule: c / c3 serves a root result (paper-form statement) twin= users=2 tags=[] status=held
```lean
def primitiveLinear (x : ℝ) : Path E →ₗ[ℝ] E where
  toFun f := ∫ t in (-1:ℝ)..x, extend f t
  map_add' f g := by
    simp only [extend_add, Pi.add_apply]
    exact intervalIntegral.integral_add ((extend_continuous f).intervalIntegrable _ _)
      ((extend_continuous g).intervalIntegrable _ _)
  map_smul' c f := by
    simp only [extend_smul, Pi.smul_apply, RingHom.id_apply]
    exact intervalIntegral.integral_smul c (extend f)
```

## 2. `NavierStokes.PhysicalParticularWave.referenceRawPressure_eq_common` (theorem) NavierStokes.PhysicalParticularWave:1267-1283
rule: b / b no twin found twin= users=2 tags=[] status=dead
```lean
theorem referenceRawPressure_eq_common (D : AssemblyData Parameter) (H : ReferenceIdentity D)
    {j : ℤ} (hj : j ≠ 0) (hfrequency : ∀ n, D.carrierBlock.frequency n ≠ 0) :
    referenceRawPressure D j = (rawCommon D j).pressure D.reference.band := by
  have hs : residualSource D.context D.state D.carrierBlock D.gaussianInput D.aliasInput j D.reference.band =
      transportSource (residualSource D.context D.state D.carrierBlock D.gaussianInput D.aliasInput j D.reference.band)
        (D.charts.parameter D.reference.band) (D.charts.gap D.reference.band)
        (D.charts.amplitude D.reference.band) := by
    rw [H.parameter, H.gap, H.amplitude]
    funext p
    simp [transportSource, coverPower]
  funext x
  have he := actualBandPressure_eq_reference D.reference D.charts D.context D.state D.carrierBlock
    D.gaussianInput D.aliasInput hj D.reference.band hfrequency hs x.1.1 x.2
  rw [H.parameter, H.gap, H.amplitude] at he
  simp only [id_eq, coverPower, ContinuousLinearEquiv.refl_apply, one_mul,
    div_self (hfrequency D.reference.band), one_smul] at he
  exact he.symm
```

## 3. `NavierStokes.ActualCorrectionModels.context_stress_smooth` (theorem) NavierStokes.ActualCorrectionModels:896-905
rule: a / a4 orphaned development twin= users=0 tags=[] status=dead
```lean
theorem context_stress_smooth (index : ℕ → ℕ) (n : ℕ) :
    ContDiffOn ℝ ∞ ((context H v upper B index).virtualTheta n) (contextDomain F.data.h) ∧
    ContDiffOn ℝ ∞ ((context H v upper B index).virtualAxial n) (contextDomain F.data.h) := by
  constructor
  · intro x hx
    exact (((virtualStress_smoothAt H v upper B n hx.1).comp x
      BaseContextAssembly.slowCoordinates.contDiff.contDiffAt).fst).contDiffWithinAt
  · intro x hx
    exact (((virtualStress_smoothAt H v upper B n hx.1).comp x
      BaseContextAssembly.slowCoordinates.contDiff.contDiffAt).snd).contDiffWithinAt
```

## 4. `NavierStokes.NilpotentVolterra.exists_regular_solution` (theorem) NavierStokes.NilpotentVolterra:898-913
rule: b / b no twin found twin= users=0 tags=[] status=dead
```lean
/-- A regular solution on any prescribed finite radial interval. Only
the parameter neighborhood is reduced; coefficient size places no upper
bound on the length of the radial interval. -/
theorem exists_regular_solution {R : ℝ} (hR : 0 ≤ R)
    {A₀ A₁ : ℂ → CoefficientPath R} {f : ℂ → Path R} {U : Set ℂ}
    (hU : IsOpen U) (hA₀ : DifferentiableOn ℂ A₀ U) (hA₁ : DifferentiableOn ℂ A₁ U)
    (hf : DifferentiableOn ℂ f U) {center : ℂ} {ρ σ : ℝ}
    (hDisk : Metric.closedBall center σ ⊆ U) (hgap : ρ < σ)
    (hshape : VolterraAnalyticBounds.DerivativeShape (rawCoefficient hR A₁)) :
    ∃ W : VolterraAnalyticBounds.Field,
      IsRegularSolution R (Metric.ball center ρ)
        (rawCoefficient hR A₀) (rawCoefficient hR A₁) (rawField hR f) W := by
  obtain ⟨holo, heq⟩ := integralSolution_spec hR hU hA₀ hA₁ hf hDisk hgap hshape
  exact ⟨liftedField hR A₀ A₁ f (integralSolution hR A₀ A₁ f),
    liftedField_isRegularSolution hR A₀ A₁ f (integralSolution hR A₀ A₁ f)
      Metric.isOpen_ball holo heq⟩
```

## 5. `NavierStokes.TorusCoverLattice.indexHom_range_index` (theorem) NavierStokes.TorusCoverLattice:59-62
rule: c / c3 serves a root result (paper-form statement) twin= users=1 tags=[] status=held
```lean
theorem indexHom_range_index : indexHom.range.index = 14 := by
  rw [indexHom_range_eq_ker, AddSubgroup.index_ker,
    residueHom.range_eq_top_of_surjective residueHom_surjective]
  simp
```

## 6. `NavierStokes.R3SpaceTime.volume_spatial_zero` (theorem) NavierStokes.R3SpaceTime:51-58
rule: a / a4 orphaned development twin= users=1 tags=[] status=dead
```lean
theorem volume_spatial_zero : volume {z : Domain | spaceProj z = 0} = 0 := by
  have he : {z : Domain | spaceProj z = 0} = WithLp.ofLp ⁻¹' (univ ×ˢ ({0} : Set Space)) := by
    ext z
    simp [spaceProj, WithLp.sndL]
  rw [he, (WithLp.volume_preserving_ofLp ℝ Space).measure_preimage (by measurability)]
  change ((volume : Measure ℝ).prod (volume : Measure Space)) (univ ×ˢ {0}) = 0
  rw [Measure.prod_prod]
  simp
```

## 7. `NavierStokes.R3WeakPressure.Represents.congr` (theorem) NavierStokes.R3SmoothPressure:22-23
rule: a / a4 orphaned development twin= users=2 tags=[] status=dead
```lean
theorem Represents.congr {T : 𝓢'(Domain, ℂ)} {f g : Domain → ℂ}
    (hT : Represents T f) (he : f = g) : Represents T g := he ▸ hT
```

## 8. `NavierStokes.InitialDyadicSource.initial_corrected_zero_germ_nonpositive` (theorem) NavierStokes.InitialDyadicSource:145-159
rule: a / a4 orphaned development twin= users=1 tags=[] status=dead
```lean
/-- At nonpositive radius the actual cut coefficient is zero on a full
neighborhood, so the same is true of the actual curl-corrected amplitude. -/
theorem initial_corrected_zero_germ_nonpositive (l : Index B N0) (n : ℕ) {x : FullPoint}
    (hT : 0 < x.1.2.1.1) (hR : x.1.1 ≤ 0) :
    (ActualInitialization.primaryPiece l).exactCoefficients.amplitude n =ᶠ[𝓝 x] fun _ => 0 := by
  have hout : x.1 ∉ ActualCoreSupport.refinedCarrier l n := by
    intro hx
    have hl := ((ActualCoreSupport.mem_refinedCarrier_iff l n hT).mp hx).2.1.1
    have hn : ActualCoreSupport.radialRatio x.1 ≤ 0 :=
      div_nonpos_of_nonpos_of_nonneg hR (Real.sqrt_nonneg _)
    exact (not_lt_of_ge hn) ((PrimaryTargetBounds.leftRadius_pos ActualPrimary.nominal).trans_le hl)
  have ha := ActualCoreSupport.cut_amplitude_zero_germ l n hT hout
  exact notMem_tsupport_iff_eventuallyEq.mp
    (fun hs => (notMem_tsupport_iff_eventuallyEq.mpr ha)
      ((ActualInitialization.primaryPiece l).exactAmplitude_tsupport_subset_tangent n hs))
```

## 9. `NavierStokes.RadialFluxResidual.divergence_coefficient` (theorem) NavierStokes.RadialFluxResidual:149-155
rule: b / b no twin found twin= users=1 tags=[] status=dead
```lean
theorem divergence_coefficient {V : Profile} (U : Profile) {p : ProfilePoint}
    (hV : DifferentiableAt ℝ V p) (hs : p.2.1 ≠ 0) :
    partialZ U p - 2 * radialB V p - 2 * p.2.1 * partialS (radialB V) p =
      partialS V p + partialZ U p := by
  rw [partialS_radialB_explicit hV hs]
  unfold radialB
  field_simp [hs] ; ring
```

## 10. `NavierStokes.PolarCharts.scalePlane` (def) NavierStokes.PolarCharts:346-347
rule: b / b no twin found twin= users=8 tags=[] status=held
```lean
noncomputable def scalePlane (Q : ℝ) : Plane →L[ℝ] Plane :=
  Q ^ (-(1 / 2 : ℝ)) • ContinuousLinearMap.id ℝ Plane
```

## 11. `NavierStokes.CorrectionStep.gaugeTemporalAliasBlock_represents` (theorem) NavierStokes.CorrectionStep:3089-3095
rule: b / b no twin found twin= users=0 tags=[] status=dead
```lean
theorem gaugeTemporalAliasBlock_represents (g : GaugeData S) (h : ℝ) (index : ℕ → ℕ)
    (c : Context (PressureStream.Lift S)) (u : State (PressureStream.Lift S))
    (b : HarmonicBlock (PressureStream.Lift S)) :
    (gaugeTemporalAliasBlock g h index c u b).oscillation = temporalAliasState g h index c u := by
  funext n x i
  rw [gaugeTemporalAliasBlock, ErrorHarmonics.zeroBlock_evaluation]
  rfl
```

## 12. `NavierStokes.ConstructedSlowBase.Modulated.velocity_eq_curl` (theorem) NavierStokes.ConstructedSlowBase:878-879
rule: b / b no twin found twin= users=0 tags=[] status=dead
```lean
theorem velocity_eq_curl (c : ℝ) (hc : 0 < c) (upper : ℝ) (B : ℕ) :
    velocity v c hc upper B = SpatialCurl.spatialCurl (vectorPotential v c hc upper B) := rfl
```

## 13. `NavierStokes.ActualCurrentCarrierJets.phase_smoothNear_controlPatch` (theorem) NavierStokes.ActualCurrentCarrierJets:182-187
rule: c / c1 same derivation up to renaming twin=NavierStokes.ActualCurrentCarrierJets.weightedPhase_smoothNear_controlPatch users=0 tags=[] status=dead
```lean
theorem phase_smoothNear_controlPatch (l : Label B N0) (n : ℕ)
    (k : TorusInverse.Frequency) {z : Native}
    (hz : z ∈ ActualParticularStageControls.controlPatch l n k) :
    LocalPhysicalCopyBounds.SmoothNear (phase l n) z :=
  phase_smoothNear (n := n) (i := (l,k)) (z := z)
    (ActualParticularStageControls.controlPatch_subset_padded l n k hz)
```

## 14. `NavierStokes.NaturalAxisData.neg_W_gt` (theorem) NavierStokes.NaturalAxisData:100-102
rule: b / b no twin found twin= users=0 tags=[] status=dead
```lean
theorem neg_W_gt {h j η : ℝ} (p : SmallParameters h j)
    (hη : η ∈ Icc (-1 : ℝ) 1) : 14 / 5 < -W h j η := by
  linarith [neg_W_lower_bound p hη]
```

## 15. `NavierStokes.CopySolveCompatibility.localizedCopy_transform` (theorem) NavierStokes.CopySolveCompatibility:135-140
rule: b / b no twin found twin= users=1 tags=[] status=dead
```lean
theorem localizedCopy_transform (d : LinearData P V E) (φ : Q → P)
    (g : Geometry) (hab : a ≤ b) (k : ℕ) (κ : Plane → ℝ) (j : Frequency) (q : Q) (Y : Plane) :
    (transformData d φ k).localizedCopy (refineGeometry g k) hab κ j (q, Y) =
      d.localizedCopy g hab κ j (φ q, coverPower k Y) := by
  unfold LinearData.localizedCopy
  rw [coordinates_refine, copySolve_transform]
```

## 16. `NavierStokes.ActualReferenceRebase.pullStrip` (def) NavierStokes.ActualReferenceRebase:181-193
rule: b / b no twin found twin= users=3 tags=[] status=dead
```lean
noncomputable def pullStrip (e : D ≃L[ℝ] E) (s : StripData E) : StripData D where
  domain := e ⁻¹' s.domain
  isOpen_domain := s.isOpen_domain.preimage e.continuous
  epsilon := s.epsilon
  epsilon_pos := s.epsilon_pos
  epsilon_le_one := s.epsilon_le_one
  slow := s.slow
  one_le_slow := s.one_le_slow
  delta x := s.delta (e x)
  delta_pos x hx := s.delta_pos (e x) hx
  zeta x := s.zeta (e x)
  zeta_smooth := s.zeta_smooth.comp e.contDiff.contDiffOn (fun _ hx => hx)
  zeta_nonneg x hx := s.zeta_nonneg (e x) hx
```

## 17. `NavierStokes.SpatialLocalization.periodicPressure_eventuallyEq` (theorem) NavierStokes.SpatialLocalization:322-325
rule: b / b no twin found twin= users=4 tags=[] status=dead
```lean
theorem periodicPressure_eventuallyEq (p : PressureField) {z : SpaceTime}
    (hz : z.2 ∈ plateau) : periodicPressure p =ᶠ[𝓝 z] p :=
  (PeriodicLocalization.periodize_eventuallyEq (cutPressure_supported p)
    (plateau_subset_innerCube hz)).trans (cutPressure_eventuallyEq p hz)
```

## 18. `NavierStokes.CorrectedPressureBounds.correctedPi_joint_contDiff` (theorem) NavierStokes.CorrectedPressureBounds:336-340
rule: b / b no twin found twin= users=0 tags=[] status=dead
```lean
theorem correctedPi_joint_contDiff {d : TailData} {K : ℝ} (w : ResetWitness d K) :
    ContDiff ℝ ∞ (fun p : ℝ × ℝ => correctedPi w p.1 p.2) := by
  convert! (cleanPi_joint_contDiff d).add (pressureChange_joint_contDiff w) using 1
  funext p
  simp [pressureChange]
```

## 19. `NavierStokes.MeanRankUpdate.normalizedStripData` (def) NavierStokes.MeanRankUpdate:962-976
rule: b / b no twin found twin= users=5 tags=[] status=dead
```lean
/-- The concrete logarithmic radial weights, restricted to one normalized
physical `q/Q` strip. The torus variables remain unrestricted. -/
noncomputable def normalizedStripData (coord qlo qhi rlo rhi cL cR : ℝ)
    (hc : 0 < coord) (hc1 : coord < 1) (hrlo : 0 < rlo) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε S : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hS : ∀ n, 1 ≤ S n) :
    WeightedClasses.StripData ChartPoint :=
  { WeightedRadialPrimitive.logStripData rlo rhi cL cR hrlo hcL hcR ε S hε hεone hS with
    domain := normalizedDomain coord qlo qhi rlo rhi
    isOpen_domain := normalizedDomain_isOpen hc hc1 qlo qhi rlo rhi
    delta_pos := fun _ hp => WeightedRadialPrimitive.delta_pos
      (WeightedRadialPrimitive.logPosition_mem hrlo hp.2.2)
    zeta_smooth := (WeightedRadialPrimitive.logStripData rlo rhi cL cR hrlo hcL hcR
      ε S hε hεone hS).zeta_smooth.mono (fun _ hp => hp.2.2)
    zeta_nonneg := fun _ hp => (WeightedRadialPrimitive.zeta_pos cL cR
      (WeightedRadialPrimitive.logPosition_mem hrlo hp.2.2)).le }
```

## 20. `NavierStokes.MeanStageContinuation.streamBeta_periodic` (theorem) NavierStokes.MeanStageContinuation:228-231
rule: a / a4 orphaned development twin= users=2 tags=[] status=dead
```lean
theorem streamBeta_periodic {U : Set Slow} (hU : IsOpen U) {f : Point → ℝ}
    (hf : PhysicalMeanDomain.PeriodicOn U f) (w : Slow × Slow) :
    PhysicalMeanDomain.PeriodicOn U (PressureStream.streamBeta w f) :=
  (Periodic.neg (Periodic.directional (f := fun _ => f) (fun _ => hf) hU (0, w))) 0
```

## 21. `NavierStokes.EndpointExtension.glue_vanishes_from` (theorem) NavierStokes.EndpointExtension:47-54
rule: b / b no twin found twin= users=0 tags=[] status=dead
```lean
/-- Gluing preserves a right-hand time-support bound. -/
theorem glue_vanishes_from {V : Type*} [Zero V] {a b : ℝ} {left right : ℝ → V}
    (hab : a ≤ b) (hvalue : left a = right a)
    (hzero : ∀ x, b ≤ x → right x = 0) :
    ∀ x, b ≤ x → glue a left right x = 0 := by
  intro x hx
  rw [glue_eqOn_right hvalue (hab.trans hx)]
  exact hzero x hx
```

## 22. `NavierStokes.MeanResidual.AngularContinuous.sub` (theorem) NavierStokes.MeanResidual:87-90
rule: b / b no twin found twin= users=3 tags=[] status=dead
```lean
omit [NormedSpace ℝ E] in
theorem AngularContinuous.sub {f g : SpaceTime → E}
    (hf : AngularContinuous f) (hg : AngularContinuous g) :
    AngularContinuous (fun q => f q - g q) := fun q => (hf q).sub (hg q)
```

## 23. `EulerTimeLpGramGevrey.inverseGramMultiplier_gevrey` (theorem) Euler.TimeLpGramGevrey:72-91
rule: b / b no twin found twin= users=0 tags=[] status=dead
```lean
/-- The same estimate applies to the explicit inverse-Gram multiplier in the strong equation. -/
theorem inverseGramMultiplier_gevrey (T : ℝ) (hT : 0 ≤ T)
    (Q : P → C(Icc (0 : ℝ) T, U →L[ℝ] E))
    (c : ℝ) (hc : 0 < c) (hLower : ∀ x t v, c*‖v‖^2 ≤ ‖Q x t v‖^2)
    (hQ : ContDiff ℝ ∞ Q)
    (Rc C : ℝ) (hRc : 0 ≤ Rc) (hC : 0 ≤ C)
    (hbQ : ∀ n x, ‖iteratedFDeriv ℝ n Q x‖ ≤ C*majorant Rc 0 n)
    (f : P → TimeLp T U) (hf : ContDiff ℝ ∞ f)
    (D R : ℝ) (hD : 0 ≤ D) (hR : 2*gramCost c C D*(Rc+1) ≤ R)
    (d : ℕ) (hbf : ∀ n x, ‖iteratedFDeriv ℝ n f x‖ ≤ D*majorant R d n)
    (n : ℕ) (x : P) :
    ‖iteratedFDeriv ℝ n
      (fun y => timeMultiplier T hT (gramInversePath T (Q y) c hc (hLower y)) (f y)) x‖ ≤
      majorant R (d+1) n := by
  have heq : (fun y => timeMultiplier T hT (gramInversePath T (Q y) c hc (hLower y)) (f y)) =
      fun y => gramSolver T hT (Q y) c hc (hLower y) (f y) := by
    funext y
    rw [gramSolver_eq_multiplier]
  rw [heq]
  exact gramSolution_gevrey T hT Q c hc hLower hQ Rc C hRc hC hbQ f hf D R hD hR d hbf n x
```

## 24. `NavierStokes.CorrectionInitializationNoOptions.MovingInitialization.LocalAverage.meanBar_fluxBalance_on` (theorem) NavierStokes.CorrectionInitializationNoOptions:2370-2405
rule: a / a1 cloned module twin=NavierStokes.CorrectionInitialization users=1 tags=[] status=dead
```lean
theorem meanBar_fluxBalance_on (hV : IsOpen V) (o : Operators (PressureStream.Lift S))
    (hradius : o.radius = Prod.fst)
    (hprofile : ∀ R s, s ∈ V → ∀ Y, o.radialProfile (R, (s, Y)) = o.radialProfile (R, (s, 0)))
    (R A T : ScalarField (PressureStream.Lift S)) (c : ℝ)
    (hR : ∀ n, ContDiffOn ℝ ∞ (R n) (slowDomain V))
    (hA : ∀ n, ContDiffOn ℝ ∞ (A n) (slowDomain V))
    (hT : ∀ n, ContDiffOn ℝ ∞ (T n) (slowDomain V))
    (hpR : ∀ n, PeriodicOn V (R n)) (hpA : ∀ n, PeriodicOn V (A n))
    (hpT : ∀ n, PeriodicOn V (T n)) :
    Agree (slowDomain V) (meanBar (o.radialDiv c R + o.dz A - o.radialDiv c T))
      (o.radialDiv c (meanBar R - meanBar T) + o.dz (meanBar A)) := by
  intro n x hx
  have hRc := continuous_radialDiv_slice hV o hradius hprofile R hR c n x hx
  have hTc := continuous_radialDiv_slice hV o hradius hprofile T hT c n x hx
  have hAc : Continuous (fun Y : PressureStream.Plane => o.dz A n (x.1, (x.2.1, Y))) := by
    exact continuous_const.mul (continuous_slice ((MeanIncrementBounds.SmoothOn.directional hA
      (slowDomain_open hV) o.eZ) n).continuousOn hx)
  have hbars := FourierAlias.torusMean_sub (hRc.fun_add hAc) hTc
  rw [FourierAlias.torusMean_add hRc hAc] at hbars
  change meanBar (o.radialDiv c R + o.dz A - o.radialDiv c T) n x =
    meanBar (o.radialDiv c R) n x + meanBar (o.dz A) n x - meanBar (o.radialDiv c T) n x at hbars
  rw [meanBar_radialDiv_on hV o hradius hprofile R hR hpR c n hx,
    meanBar_dz_on hV o A hA hpA n hx,
    meanBar_radialDiv_on hV o hradius hprofile T hT hpT c n hx] at hbars
  rw [hbars]
```

## 25. `NavierStokes.R3GaussianPressure.firstGaussian_partial` (theorem) NavierStokes.R3GaussianPressure:124-145
rule: a / a4 orphaned development twin= users=1 tags=[] status=dead
```lean
theorem firstGaussian_partial (a : ℝ) (i j : Fin 3) (x : Space) :
    fderiv ℝ (firstGaussian a i) x (coordinateVector j) = secondGaussian a i j x := by
  have hp := (EuclideanSpace.proj i : Space →L[ℝ] ℝ).hasFDerivAt (x := x)
  have h := ((hp.const_mul (-2 * a)).mul (hasFDerivAt_gaussianReal a x))
  have hc := Complex.ofRealCLM.hasFDerivAt.comp x h
  change (fderiv ℝ (Complex.ofRealCLM ∘
    ((fun y : Space => (-2 * a) * (EuclideanSpace.proj i) y) * gaussianReal a)) x)
      (coordinateVector j) = _
  rw [hc.fderiv]
  simp only [ContinuousLinearMap.comp_apply, add_apply,
    smul_apply, smul_eq_mul, Complex.ofRealCLM_apply, innerSL_apply_apply]
  have hi : ⟪x, coordinateVector j⟫_ℝ = x j := by
    simp [coordinateVector, EuclideanSpace.inner_eq_star_dotProduct, dotProduct]
  simp only [hi]
  change Complex.ofReal ((-2 * a * x i) * ((-2 * a * gaussianReal a x) * x j) +
    gaussianReal a x * ((-2 * a) * (coordinateVector j) i)) = _
  have hij : (coordinateVector j) i = if i = j then 1 else 0 := by
    simp [coordinateVector]
  rw [hij]
  unfold secondGaussian
  congr 1
  ring
```

## 26. `NavierStokes.ParametricHeatTail.physicalAngular_contDiffOn` (theorem) NavierStokes.ParametricHeatTail:742-747
rule: b / b no twin found twin= users=2 tags=[] status=dead
```lean
theorem physicalAngular_contDiffOn (d : TailData) {K : ℝ} (hK : 1 ≤ K) :
    ContDiffOn ℝ ∞ (physicalAngular d K) (Icc (-1 : ℝ) 1) := by
  have he : physicalAngular d K = fun eta => Real.sqrt 2 * etaDebt d K false (1 / 2) eta :=
    funext (physicalAngular_eq d (lt_of_lt_of_le zero_lt_one hK))
  rw [he]
  exact contDiffOn_const.mul (etaDebt_contDiffOn d hK false (angular_decay d))
```

## 27. `NavierStokes.GlobalBaseError.actual_error_joint_jetRate` (theorem) NavierStokes.GlobalBaseError:221-226
rule: b / b no twin found twin= users=0 tags=[] status=dead
```lean
theorem actual_error_joint_jetRate (upper : ℝ) (B m : ℕ) (r : ℝ) (hr : 0 ≤ r) :
    DiagonalResidual.JetRate originPast
      (fun z => (cartesianChart FinalSlowBase.actualProfile.outgoing.data.h z).1)
      (actualError upper B) m r :=
  error_joint_jetRate FinalSlowBase.actualProfile.certificate FinalSlowBase.actualProfile.modulation
    (actualUpper upper) B (le_max_right _ _) m r hr
```

## 28. `NavierStokes.RadialPrimitive.primitive` (def) NavierStokes.RadialPrimitive:25-27
rule: a / a4 orphaned development twin= users=16 tags=[] status=dead
```lean
/-- The ordinary radial primitive, with a specified lower endpoint. -/
def primitive (a : ℝ) (f : ℝ → ℝ) : ℝ → ℝ :=
  fun x => ∫ s in a..x, f s
```

## 29. `NavierStokes.EdgeWeightJets.edge_smul_iteratedFDeriv_bound` (theorem) NavierStokes.EdgeWeightJets:430-437
rule: b / b no twin found twin= users=2 tags=[] status=dead
```lean
theorem edge_smul_iteratedFDeriv_bound {c : ℝ} (hc : 0 < c) (j : ℕ)
    {B : E × ℝ → F} (hB : ContDiff ℝ ∞ B) {S : Set E} (hS : IsCompact S)
    (n : ℕ) {d : ℝ} (hd : 0 < d) :
    ∃ C : ℝ, 0 < C ∧ ∃ N : ℕ, ∀ i ≤ n, ∀ p ∈ S, ∀ x : ℝ, 0 < x → x ≤ d →
      ‖iteratedFDeriv ℝ i (fun y : E × ℝ =>
        (FlatCutoff.edge c y.2 / y.2 ^ j) • B y) (p, x)‖ ≤
          C * FlatCutoff.edge c x / x ^ N :=
  edge_smul_iteratedFDeriv_bound_on hc j isOpen_univ hB.contDiffOn hS n hd (subset_univ _)
```

## 30. `NavierStokes.StateReindex.radialDiv_pull` (theorem) NavierStokes.StateReindex:131-136
rule: b / b no twin found twin= users=4 tags=[] status=dead
```lean
theorem radialDiv_pull (e : D ≃ₗᵢ[ℝ] E) (o : MeanIncrementBounds.Operators E)
    (k : ℝ) (f : MeanIncrementBounds.Field E) :
    (operators e o).radialDiv k (field e f) = field e (o.radialDiv k f) := by
  unfold MeanIncrementBounds.Operators.radialDiv
  rw [dr_pull]
  rfl
```

## 31. `NavierStokes.RadialPrimitive.compactPrimitive_const_mul` (theorem) NavierStokes.RadialPrimitive:188-192
rule: a / a4 orphaned development twin= users=0 tags=[] status=dead
```lean
theorem compactPrimitive_const_mul (a b x c : ℝ) (ρ f : ℝ → ℝ) :
    compactPrimitive a b ρ (fun s => c * f s) x = c * compactPrimitive a b ρ f x := by
  unfold compactPrimitive primitive mass
  simp only [intervalIntegral.integral_const_mul]
  ring
```

## 32. `NavierStokes.ActualPhysicalStageBounds.initialPressureIncrement_rate` (theorem) NavierStokes.ActualPhysicalStageBounds:582-592
rule: b / b no twin found twin= users=0 tags=[] status=dead
```lean
theorem initialPressureIncrement_rate (W : PhysicalStageBounds.WaveData h D I K Unit)
    (M : MeanInput h (2 * CoordinateAlgebra.A h))
    (hh : 0 < h) (hh1 : h < 1 / 2) {qbig : ℝ} (hqbig : 0 < qbig)
    (hq : qbig ≤ ChartScales.Q M.firstBand) (m : ℕ) :
    JetRate ActualBaseVelocityBounds.endpoint (PhysicalWaveSum.physicalQ h)
      (initialPressureIncrement W M) m (-initialPressureLoss h W.alpha W.shift M.alpha m) := by
  obtain ⟨C, hC, hb⟩ := initialPressureIncrement_bound W M hh hh1 hq m
  refine ⟨C, hC, ?_⟩
  filter_upwards [InitializedPhysicalBackground.endpoint_sublevel hh hh1 hqbig,
    ActualBaseVelocityBounds.endpoint_q_small hh hh1] with w hw hqw
  exact hb w hw hqw.2
```

## 33. `NavierStokes.ActualCorrectionModels.fiberAgreement_dz` (theorem) NavierStokes.ActualCorrectionModels:949-953
rule: a / a4 orphaned development twin= users=2 tags=[] status=dead
```lean
theorem fiberAgreement_dz {U : Set TorusInverse.Plane} (hU : IsOpen U)
    (o : Operators LocalSignedRequest.Point) {F f : MeanIncrementBounds.Field LocalSignedRequest.Point}
    (h : ∀ n, FiberAgreement U (F n) (f n)) :
    ∀ n, FiberAgreement U (o.dz F n) (o.dz f n) :=
  Operators.dz_congr (PhysicalMeanDomain.slowDomain_open (hU.inter positiveSlow_open)) o h
```

## 34. `NavierStokes.NaturalExitParameterJets.exists_mixed_jets` (theorem) NavierStokes.NaturalExitParameterJets:59-75
rule: c / c3 serves a root result (paper-form statement) twin= users=3 tags=[] status=dead
```lean
/-- Coefficient norm control gives a single constant before either large parameter. -/
theorem exists_mixed_jets (k N : ℕ) : ∃ B, 1 ≤ B ∧
    ∀ Λ C, ∀ E : CoefficientProfile d Λ C, ∀ Y ∈ Icc (0 : ℝ) (41 / 10),
      ∀ n ≤ N, ∀ η ∈ parameterInterval,
        |iteratedDeriv n (fun ξ => AxisEvaluation.mixedSeries window d.coefficients.epsilon
          E.coefficients.1 k 0 (Y, ξ)) η| ≤ B ∧
        |iteratedDeriv n (fun ξ => AxisEvaluation.mixedSeries window d.coefficients.epsilon
          E.coefficients.2 k 0 (Y, ξ)) η| ≤ B := by
  obtain ⟨B, hB, hb⟩ := TransitionRamp.finite_majorant
    (ReferenceJetBounds.jetConstant d.coefficients k) N
  refine ⟨B, hB, ?_⟩
  intro Λ C E Y hY n hn η hη
  simp_rw [AxisEvaluation.iteratedDeriv_eta window d.coefficients.epsilon_pos _ k 0 n
    (radial_mem hY) hη, Nat.zero_add]
  obtain ⟨h₁, h₂⟩ := ReferenceJetBounds.coefficient_jet_bound d.coefficients E.coefficients
    E.norm_ball k n (p := (Y, η)) (radial_abs hY)
  exact ⟨h₁.trans (hb n hn), h₂.trans (hb n hn)⟩
```

## 35. `NavierStokes.PrimaryResidualClass.Inputs.initial_residual_class` (theorem) NavierStokes.PrimaryResidualClass:661-701
rule: b / b no twin found twin= users=1 tags=[] status=dead
```lean
/-- The actual extracted residual of the initial primary wave. The alias is
retained in the literal formula; its proved zero-mode property is used only
after the nonconstant coefficient is selected. -/
theorem initial_residual_class (u : CorrectionState.State D)
    (hmean : u.mean = ⟨0, 0, 0⟩) (A : HarmonicResidual.BlockCoefficients D)
    (hA : ∀ n i j, j ≠ 0 → A n i j = 0) :
    (HarmonicResidual.residualBlock c u (primaryBlock s c a ψ kp)
      (gaussianCoefficients c a ψ) A).WaveBounds s P (7 / 10) := by
  intro i j hj
  have hl := (h.linear_good_class j i).mono_exponent (show (7 / 10 : ℝ) ≤ 1 - 3 * κ by linarith [h.loss_le])
  have hc (m : ℤ) := (h.convection_class m i).mono_exponent
    (show (7 / 10 : ℝ) ≤ 1 - κ by linarith [h.loss_le])
  have hcr := HarmonicMeanInteraction.realCoefficient_class
    (fun n => HarmonicResidual.transport (HarmonicResidual.contextFrame c n)
      (a.frequency n) (fun y => a.phase n (y, 0)) (kp n)
      (HarmonicMeanInteraction.blockAmplitude (primaryBlock s c a ψ kp) n)
      (HarmonicMeanInteraction.blockAmplitude (primaryBlock s c a ψ kp) n) i)
    j (hc j) (hc (-j))
  apply LinearWaveBounds.class_congr (hl.add hcr)
  intro n x hx
  have hz : HarmonicResidual.stateMean u n = 0 := by
    funext y k
    fin_cases k <;> simp [HarmonicResidual.stateMean, hmean]
  change _ = HarmonicResidual.nonconstant
    ((HarmonicResidual.ofBlock (primaryBlock s c a ψ kp) (gaussianCoefficients c a ψ) A n).residualCoefficients
```

## 36. `NavierStokes.LinearWaveBounds.GraphDirections.Dz` (def) NavierStokes.LinearWaveBounds:118-119
rule: b / b no twin found twin= users=5 tags=[] status=dead
```lean
noncomputable def Dz (d : GraphDirections D) (s : StripData D) (f : ℕ → D → E) : ℕ → D → E :=
  fun n => along (d.axialField s n) (f n)
```

## 37. `NavierStokes.MeanResidual.temporal_direction` (theorem) NavierStokes.MeanResidual:286-293
rule: b / b no twin found twin= users=3 tags=[] status=dead
```lean
theorem temporal_direction {f : SpaceTime → E} (hf : ContDiff ℝ ∞ f)
    (t : ℝ) (x : Space) :
    fderiv ℝ (fun s => f (s, x)) t 1 = dt f (t, x) := by
  have h := (hf.differentiable (by simp) (t, x)).hasFDerivAt.comp t
    ((hasFDerivAt_id (𝕜 := ℝ) t).prodMk (hasFDerivAt_const (𝕜 := ℝ) x t))
  change (fderiv ℝ (f ∘ fun s => (id s, x)) t) 1 = _
  rw [h.fderiv]
  rfl
```

## 38. `NavierStokes.ActualParticularPhysicalData.ReferenceFamily.nativePotential_eq` (theorem) NavierStokes.ActualParticularPhysicalData:678-693
rule: a / a4 orphaned development twin= users=1 tags=[] status=dead
```lean
theorem nativePotential_eq {N : ℕ}
    (hf : ∀ L : F.Label, (F.data L).carrierBlock.frequency (F.data L).reference.band =
      ChartScales.carrier h L.val.val.1)
    (I : SourceIndex N) (n : ℕ) (x : NativePoint) :
    F.nativePotential N I n x =
      potentialMap (nativeFrequency (h := h) I n) (F.nativeNormal N I n x) (F.nativeAmplitude N I n x) := by
  unfold nativePotential nativeAmplitude nativeSource nativeNormal
  split_ifs with hL hn
  · have hK : referenceFrequency (F.data ⟨I.2.1, hL⟩) I.2.2.val = nativeFrequency (h := h) I n := by
      simp only [referenceFrequency, hf, nativeFrequency, nativeHarmonic, ite_eq_right hn.2, hn.1]
    change copyPotential (F.data ⟨I.2.1, hL⟩) _ _ _ _ = _
    unfold copyPotential
    rw [hK]
    rfl
  · exact (map_zero _).symm
  · exact (map_zero _).symm
```

## 39. `EulerTransversePacketProvider.Forcing.scalar_compact` (theorem) Euler.TransversePacketRegularity:73-74
rule: b / b no twin found twin= users=0 tags=[] status=dead
```lean
theorem scalar_compact (t θ : ℝ) : HasCompactSupport (fun x : Space => G.scalar I (t,(x,θ))) :=
  D.support_compact.of_isClosed_subset (isClosed_tsupport _) (G.scalar_support I t θ)
```

## 40. `NavierStokes.ActivationBounds.weightedPrimitive_uniform_jets` (theorem) NavierStokes.ActivationBounds:282-291
rule: b / b no twin found twin= users=0 tags=[] status=dead
```lean
theorem weightedPrimitive_uniform_jets {J K : Set ℝ} (hJ : IsOpen J) (hK : IsCompact K)
    (hKJ : K ⊆ J) {B : Field} (hB : ContDiffOn ℝ ∞ B (logDomain J hJ).carrier)
    (T0 : ℝ) (n : ℕ) :
    ∃ M : ℝ, 0 ≤ M ∧ ∀ T ∈ Ioc (0 : ℝ) T0, ∀ κ ∈ Icc (0 : ℝ) 1,
      ∀ y ∈ Icc (0 : ℝ) T, ∀ η ∈ K,
        |iteratedDeriv n (fun ξ => weightedPrimitive T κ B (y, ξ)) η| ≤
          M * y * activation T κ y := by
  apply width_uniform_jet_bound hJ hK hKJ (primitiveErrorFactor_smooth hJ hB)
  intro κ T hT u η _
  exact weightedPrimitive_scaled_factor hT.ne' κ B u η
```

