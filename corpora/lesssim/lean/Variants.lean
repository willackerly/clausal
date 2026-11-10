/-
Constant-threading experiment: the three multi-parameter statements (4–6) written with projections
(`q.1`, `q.2.1`, `q.2.2`) in place of pattern-matching lambdas.  Same propositions up to definitional
unfolding (each is closed by the native theorem); only the statement size differs.
-/
import Native

noncomputable section

open Asymptotics Filter Set
open scoped Topology ContDiff BigOperators
open NavierStokes NavierStokes.WeightedClasses NavierStokes.LabelSumBounds

namespace Lesssim.Variant

variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
  {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] {ι : Type*}

theorem UniformClass.edge_absorbed {s : StripData D} {cL cR L : ℝ} {ρ : D → ℝ}
    (hg : PhysicalClassBounds.FlatGeometry s cL cR L ρ) {c α : ℝ} (hc : 0 < c)
    {w : ι → ℕ → D → ℝ} {f : ι → ℕ → D → E} (hf : UniformClass s w α f)
    (hw : ∀ l n x, x ∈ s.domain → w l n x ≤ s.zeta x ^ c) (m : ℕ) :
    ∃ p : ℕ, ∀ j ≤ m, (fun q : ι × ℕ × D => iteratedFDeriv ℝ j (f q.1 q.2.1) q.2.2)
      =O[𝓟 {q | q.2.2 ∈ s.domain}] fun q => s.epsilon q.2.1 ^ α * s.slow q.2.1 ^ p :=
  Native.UniformClass.edge_absorbed hg hc hf hw m

open LocalPhysicalCopyBounds PhysicalWaveSum PhysicalCopyBounds in
theorem LocalSourceBounds.chart_bound {E : Type} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {h : ℝ} {s : StripData D} {α : ℝ} {w : ι → ℕ → D → ℝ} {source : ι → ℕ → D → E}
    (hs : LocalSourceBounds s h α w source) (m : ℕ) :
    ∃ p : ℕ, ∀ j ≤ m, (fun q : ι × ℕ × D => iteratedFDeriv ℝ j (source q.1 q.2.1) q.2.2)
      =O[𝓟 {q | 4 ≤ q.2.1 ∧ q.2.2 ∈ s.domain}]
        fun q => ChartScales.Q q.2.1 ^ (h * α) * ChartScales.S q.2.1 ^ p :=
  Native.LocalSourceBounds.chart_bound hs m

open LocalPhysicalCopyBounds PhysicalWaveSum PhysicalCopyBounds in
theorem commonChart_amplitude_bound {H : ℕ} {K : Type*} {f : CopyFamily H K} {a b h r0 : ℝ}
    {s : StripData D} {α σ : ℝ} {w : ι → ℕ → D → ℝ} {source : ι → ℕ → D → ℂ}
    (hs : LocalSourceBounds s h α w source) {hc : SupportCells f}
    (hchart : CommonChart f hc a b h r0 σ source)
    (hmap : ∀ k I, MapsTo (hchart.map k I) (hchart.domain k I) s.domain) (m : ℕ) :
    ∃ p : ℕ, ∀ j ≤ m, (fun q : K × WaveIndex H × LiftPoint => iteratedFDeriv ℝ j (f.amplitude q.1 q.2.1) q.2.2)
      =O[𝓟 {q | q.2.2 ∈ hchart.domain q.1 q.2.1}]
        fun q => ChartScales.Q q.2.1.1.val.1 ^ (h * α + σ) * ChartScales.S q.2.1.1.val.1 ^ p :=
  Native.commonChart_amplitude_bound hs hchart hmap m

end Lesssim.Variant
