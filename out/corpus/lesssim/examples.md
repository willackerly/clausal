### Example 1 (best case, a finite sum): step 9

Original (`NavierStokes.LocalPhysicalCopyBounds`, lines 820–850):

```lean
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
    ∃ C : ℝ, 0 ≤ C ∧ ∀ z : SpaceTime,
      z ∈ preterminal → |z.1| ≤ 1 →
      ‖iteratedFDeriv ℝ m (PhysicalCopyBounds.vectorSum f a h r0) z‖ ≤
        C * physicalQ h z ^ (h * α - PhysicalClassBounds.physicalLoss h σ m) := by
  classical
  have hbnd := fun i => physical_sum_jet_bound_of_weighted hsource (hchart i) (hmap i)
    (hb i) (hr i) (hs i) hh hh1 ha hZ hr0 hP (hp i) m
  choose C hC hbound using hbnd
  refine ⟨3 * ∑ i : Fin 3, C i,
    mul_nonneg (by norm_num) (Finset.sum_nonneg (fun i _ => hC i)), ?_⟩
  intro z hz ht
  have hq := physicalQ_pos hh hh1 hz
  have hi (i : Fin 3) : C i ≤ ∑ j : Fin 3, C j :=
    Finset.single_le_sum (fun j _ => hC j) (Finset.mem_univ i)
  have he := vectorSum_jet_bound hr hs hc ha hh hh1 hz m
    (B := (∑ i : Fin 3, C i) * physicalQ h z ^ (h * α - PhysicalClassBounds.physicalLoss h σ m))
    (fun i => (hbound i z hz ht).trans
      (mul_le_mul_of_nonneg_right (hi i) (Real.rpow_pos_of_pos hq _).le))
  exact he.trans_eq (by ring)
```

Native (`corpora/lesssim/lean/Native.lean`):

```lean
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
```

### Example 2 (several uniform parameters, multiplication by a bounded factor): step 4

Original (`NavierStokes.PhysicalClassBounds`, lines 96–122):

```lean
/-- Remove the edge growth from an actual uniform coefficient class.  The
input envelope may depend on the label and band; its domination is uniform. -/
theorem UniformClass.edge_absorbed {s : StripData D} {cL cR L : ℝ} {ρ : D → ℝ}
    (hg : FlatGeometry s cL cR L ρ) {c α : ℝ} (hc : 0 < c)
    {w : ι → ℕ → D → ℝ} {f : ι → ℕ → D → E}
    (hf : UniformClass s w α f)
    (hw : ∀ l n x, x ∈ s.domain → w l n x ≤ s.zeta x ^ c) (m : ℕ) :
    ∃ A : ℝ, 0 ≤ A ∧ ∃ p : ℕ, ∀ l n x, x ∈ s.domain → ∀ j ≤ m,
      ‖iteratedFDeriv ℝ j (f l n) x‖ ≤ A * s.epsilon n ^ α * s.slow n ^ p := by
  obtain ⟨C, hC, p, hb⟩ := hf.bounds m
  obtain ⟨K, hK, hKx⟩ := hg.uniform hc p
  refine ⟨C * K, mul_nonneg hC hK, p, ?_⟩
  intro l n x hx j hj
  have he : 0 ≤ s.epsilon n ^ α := (Real.rpow_pos_of_pos (s.epsilon_pos n) α).le
  have hs : 0 ≤ s.slow n ^ p := pow_nonneg (zero_le_one.trans (s.one_le_slow n)) _
  calc
    _ ≤ majorant s (w l) α C p n x := hb l n x hx j hj
    _ ≤ C * s.epsilon n ^ α * s.growth n x ^ p * s.zeta x ^ c :=
      mul_le_mul_of_nonneg_left (hw l n x hx)
        (mul_nonneg (mul_nonneg hC he) (pow_nonneg (s.growth_nonneg n x) _))
    _ = (C * s.epsilon n ^ α * s.slow n ^ p) *
        ((max 1 (s.delta x)⁻¹) ^ p * s.zeta x ^ c) := by
      rw [StripData.growth, mul_pow]
      ring
    _ ≤ (C * s.epsilon n ^ α * s.slow n ^ p) * K :=
      mul_le_mul_of_nonneg_left (hKx x hx) (mul_nonneg (mul_nonneg hC he) hs)
    _ = _ := by ring
```

Native (`corpora/lesssim/lean/Native.lean`):

```lean
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
```

### Example 3 (a step that got larger): step 12

Original (`NavierStokes.ActualPhysicalStageBounds`, lines 202–236):

```lean
theorem potentialIncrement_bound
    (WP : PhysicalStageBounds.WaveData h DP IP KP (Fin 3))
    (WS : PhysicalStageBounds.WaveData h DS IS KS (Fin 3))
    (MT MR : MeanInput h (CoordinateAlgebra.A h - 1 / 2))
    (hh : 0 < h) (hh1 : h < 1 / 2) {qbig g dw dm : ℝ}
    (hqT : qbig ≤ ChartScales.Q MT.firstBand) (hqR : qbig ≤ ChartScales.Q MR.firstBand)
    (hWP : g ≤ h * WP.alpha + WP.shift + dw) (hWS : g ≤ h * WS.alpha + WS.shift + dw)
    (hMT : g ≤ h * MT.alpha + dm) (hMR : g ≤ h * MR.alpha + dm) (m : ℕ) :
    ∃ C : ℝ, 0 ≤ C ∧ ∀ w ∈ CutStageEstimates.physicalSublevel h qbig,
      PhysicalWaveSum.physicalQ h w ≤ 1 →
      ‖iteratedFDeriv ℝ m (potentialIncrement WP WS MT MR) w‖ ≤
        C * PhysicalWaveSum.physicalQ h w ^ (g - PhysicalStageBounds.potentialLoss h dw dm m) := by
  have hp0 := WP.vector_bound_with_gain hh hh1 hWP m
  have hs0 := WS.vector_bound_with_gain hh hh1 hWS m
  have hp := weaken_bound (qbig := qbig) (s := g - PhysicalStageBounds.potentialLoss h dw dm m) hh hh1
    (sub_le_sub_left (le_max_left _ _) g) (by
      obtain ⟨C, hC, hb⟩ := hp0
      exact ⟨C, hC, fun w hw hqw => hb w hw.1 hqw⟩)
  have hs := weaken_bound (qbig := qbig) (s := g - PhysicalStageBounds.potentialLoss h dw dm m) hh hh1
    (sub_le_sub_left (le_max_left _ _) g) (by
      obtain ⟨C, hC, hb⟩ := hs0
      exact ⟨C, hC, fun w hw hqw => hb w hw.1 hqw⟩)
  have ht := weaken_bound (s := g - PhysicalStageBounds.potentialLoss h dw dm m)
    hh hh1 (sub_le_sub_left (le_max_right _ _) g)
    (MT.angular_bound_with_gain hh hh1 hqT hMT m)
  have hr := weaken_bound (s := g - PhysicalStageBounds.potentialLoss h dw dm m)
    hh hh1 (sub_le_sub_left (le_max_right _ _) g)
    (MR.angular_bound_with_gain hh hh1 hqR hMR m)
  have sp : ContDiffOn ℝ ∞ WP.vector (CutStageEstimates.physicalSublevel h qbig) :=
    (WP.vector_smooth hh hh1).mono inter_subset_left
  have ss : ContDiffOn ℝ ∞ WS.vector (CutStageEstimates.physicalSublevel h qbig) :=
    (WS.vector_smooth hh hh1).mono inter_subset_left
  have st := MT.angular_smooth hh hh1 hqT
  exact add_bounds hh hh1 ((sp.add ss).add st) (MR.angular_smooth hh hh1 hqR)
    (add_bounds hh hh1 (sp.add ss) st (add_bounds hh hh1 sp ss hp hs) ht) hr
```

Native (`corpora/lesssim/lean/Native.lean`):

```lean
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
```

