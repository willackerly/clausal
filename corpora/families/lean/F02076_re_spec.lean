import Tool
import NavierStokes.BaseResidual
import NavierStokes.DiagonalResidual
import Mathlib.Util.CountHeartbeats
set_option Elab.async false  -- so that #count_heartbeats includes the proof

-- REPLAY NavierStokes.DiagonalResidual.JetRate.weaken 8 29
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
theorem JetRate.weaken_S {l : Filter D} {q : D → ℝ} {f : D → V} {m : ℕ} {r s : ℝ}
    (hf : JetRate l q f m r) (hq : ∀ᶠ x in l, 0 < q x ∧ q x ≤ 1) (hsr : s ≤ r) :
    JetRate l q f m s := by
  obtain ⟨C, hC, hb⟩ := hf
  refine ⟨C, hC, ?_⟩
  filter_upwards [hq, hb] with x hx hbound
  exact hbound.trans (mul_le_mul_of_nonneg_left
    (Real.rpow_le_rpow_of_exponent_ge hx.1 hx.2 hsr) hC)
end Rates
end NavierStokes.DiagonalResidual
end
end

-- REPLAY NavierStokes.DiagonalResidual.JetRate.add 33 60
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
theorem JetRate.add_S {l : Filter D} {q : D → ℝ} {f g : D → V} {m : ℕ} {r : ℝ}
    {U : Set D} (hf : JetRate l q f m r) (hg : JetRate l q g m r)
    (hU : IsOpen U) (hlU : ∀ᶠ x in l, x ∈ U)
    (hsf : ContDiffOn ℝ ∞ f U) (hsg : ContDiffOn ℝ ∞ g U) :
    JetRate l q (fun x => f x + g x) m r := by
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

-- REPLAY NavierStokes.DiagonalResidual.JetRate.congr_on 64 84
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
theorem JetRate.congr_on_S {l : Filter D} {q : D → ℝ} {f g : D → V} {m : ℕ} {r : ℝ}
    {U : Set D} (hf : JetRate l q f m r) (hU : IsOpen U)
    (hlU : ∀ᶠ x in l, x ∈ U) (hfg : EqOn f g U) : JetRate l q g m r := by
  obtain ⟨C, hC, hb⟩ := hf
  refine ⟨C, hC, ?_⟩
  filter_upwards [hlU, hb] with x hx hbound
  rwa [← ResidualStability.iteratedFDeriv_eqOn hU hfg m hx]
end Rates
end NavierStokes.DiagonalResidual
end
end

-- REPLAY NavierStokes.BaseResidual.finiteRate_weaken 88 124
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
theorem finiteRate_weaken_S {l : Filter D} {q : D → ℝ} {f : D → E} {M : ℕ} {r s : ℝ}
    (hf : FiniteJetRate l q f M r) (hq : ∀ᶠ x in l, 0 < q x ∧ q x ≤ 1) (hsr : s ≤ r) :
    FiniteJetRate l q f M s := by
  apply finiteJetRate_of_jetRate (hq.mono (fun _ hx => hx.1))
  intro m hm
  exact (finiteRate_at hf hm).weaken hq hsr
end RateAlgebra
end NavierStokes.BaseResidual
end
end

-- REPLAY NavierStokes.BaseResidual.finiteRate_congr_on 128 167
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
theorem finiteRate_congr_on_S {l : Filter D} {q : D → ℝ} {f g : D → E} {M : ℕ} {r : ℝ}
    {U : Set D} (hf : FiniteJetRate l q f M r) (hU : IsOpen U)
    (hlU : ∀ᶠ x in l, x ∈ U) (hfg : EqOn f g U) : FiniteJetRate l q g M r := by
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

-- REPLAY NavierStokes.BaseResidual.finiteRate_add 171 213
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
theorem finiteRate_add_S {l : Filter D} {q : D → ℝ} {f g : D → E} {M : ℕ} {r : ℝ}
    {U : Set D} (hf : FiniteJetRate l q f M r) (hg : FiniteJetRate l q g M r)
    (hU : IsOpen U) (hlU : ∀ᶠ x in l, x ∈ U)
    (hsf : ContDiffOn ℝ ∞ f U) (hsg : ContDiffOn ℝ ∞ g U) :
    FiniteJetRate l q (fun x => f x + g x) M r := by
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

