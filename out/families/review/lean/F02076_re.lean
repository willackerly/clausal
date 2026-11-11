import Tool
import F2076
import NavierStokes.BaseResidual
import NavierStokes.DiagonalResidual
import Mathlib.Util.CountHeartbeats
set_option Elab.async false  -- so that #count_heartbeats includes the proof

-- REPLAY NavierStokes.DiagonalResidual.JetRate.weaken 9 26
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
theorem JetRate.weaken_R {l : Filter D} {q : D → ℝ} {f : D → V} {m : ℕ} {r s : ℝ}
    (hf : JetRate l q f m r) (hq : ∀ᶠ x in l, 0 < q x ∧ q x ≤ 1) (hsr : s ≤ r) :
    JetRate l q f m s :=
  Fam.F2076.jetRate_iff.2 ((Fam.F2076.jetRate_iff.1 hf).weaken hq hsr)
end Rates
end NavierStokes.DiagonalResidual
end
end

-- REPLAY NavierStokes.DiagonalResidual.JetRate.add 30 49
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
theorem JetRate.add_R {l : Filter D} {q : D → ℝ} {f g : D → V} {m : ℕ} {r : ℝ}
    {U : Set D} (hf : JetRate l q f m r) (hg : JetRate l q g m r)
    (hU : IsOpen U) (hlU : ∀ᶠ x in l, x ∈ U)
    (hsf : ContDiffOn ℝ ∞ f U) (hsg : ContDiffOn ℝ ∞ g U) :
    JetRate l q (fun x => f x + g x) m r :=
  Fam.F2076.jetRate_iff.2 ((Fam.F2076.jetRate_iff.1 hf).add (Fam.F2076.jetRate_iff.1 hg) hU hlU hsf hsg)
end Rates
end NavierStokes.DiagonalResidual
end
end

-- REPLAY NavierStokes.DiagonalResidual.JetRate.congr_on 53 70
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
theorem JetRate.congr_on_R {l : Filter D} {q : D → ℝ} {f g : D → V} {m : ℕ} {r : ℝ}
    {U : Set D} (hf : JetRate l q f m r) (hU : IsOpen U)
    (hlU : ∀ᶠ x in l, x ∈ U) (hfg : EqOn f g U) : JetRate l q g m r :=
  Fam.F2076.jetRate_iff.2 ((Fam.F2076.jetRate_iff.1 hf).congr_on hU hlU hfg)
end Rates
end NavierStokes.DiagonalResidual
end
end

-- REPLAY NavierStokes.BaseResidual.finiteRate_weaken 74 108
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
theorem finiteRate_weaken_R {l : Filter D} {q : D → ℝ} {f : D → E} {M : ℕ} {r s : ℝ}
    (hf : FiniteJetRate l q f M r) (hq : ∀ᶠ x in l, 0 < q x ∧ q x ≤ 1) (hsr : s ≤ r) :
    FiniteJetRate l q f M s :=
  Fam.F2076.JetRateOn.weaken hf hq hsr
end RateAlgebra
end NavierStokes.BaseResidual
end
end

-- REPLAY NavierStokes.BaseResidual.finiteRate_congr_on 112 146
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
theorem finiteRate_congr_on_R {l : Filter D} {q : D → ℝ} {f g : D → E} {M : ℕ} {r : ℝ}
    {U : Set D} (hf : FiniteJetRate l q f M r) (hU : IsOpen U)
    (hlU : ∀ᶠ x in l, x ∈ U) (hfg : EqOn f g U) : FiniteJetRate l q g M r :=
  Fam.F2076.JetRateOn.congr_on hf hU hlU hfg
end RateAlgebra
end NavierStokes.BaseResidual
end
end

-- REPLAY NavierStokes.BaseResidual.finiteRate_add 150 186
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
theorem finiteRate_add_R {l : Filter D} {q : D → ℝ} {f g : D → E} {M : ℕ} {r : ℝ}
    {U : Set D} (hf : FiniteJetRate l q f M r) (hg : FiniteJetRate l q g M r)
    (hU : IsOpen U) (hlU : ∀ᶠ x in l, x ∈ U)
    (hsf : ContDiffOn ℝ ∞ f U) (hsg : ContDiffOn ℝ ∞ g U) :
    FiniteJetRate l q (fun x => f x + g x) M r :=
  Fam.F2076.JetRateOn.add hf hg hU hlU hsf hsg
end RateAlgebra
end NavierStokes.BaseResidual
end
end

run_cmd Fam.reportPairs "F02076" "re" [(`NavierStokes.DiagonalResidual.JetRate.weaken, `NavierStokes.DiagonalResidual.JetRate.weaken_R), (`NavierStokes.DiagonalResidual.JetRate.add, `NavierStokes.DiagonalResidual.JetRate.add_R), (`NavierStokes.DiagonalResidual.JetRate.congr_on, `NavierStokes.DiagonalResidual.JetRate.congr_on_R), (`NavierStokes.BaseResidual.finiteRate_weaken, `NavierStokes.BaseResidual.finiteRate_weaken_R), (`NavierStokes.BaseResidual.finiteRate_congr_on, `NavierStokes.BaseResidual.finiteRate_congr_on_R), (`NavierStokes.BaseResidual.finiteRate_add, `NavierStokes.BaseResidual.finiteRate_add_R)]
