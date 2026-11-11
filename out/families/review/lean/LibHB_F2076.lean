/-
M9 families, F02076 (positive control: big-O duplicate): `JetRate` (one order) and `FiniteJetRate` (all orders ≤ M).
Primitive: a DEFINITION WITH ONE EXPLICIT PARAMETER, the set of orders bounded with a common constant.
-/
import Tool
import NavierStokes.BaseResidual
import Mathlib.Util.CountHeartbeats
import Mathlib.Util.CountHeartbeats
set_option Elab.async false
set_option Elab.async false

open Set Filter Function
open scoped Topology ContDiff

namespace Fam.F2076
open NavierStokes NavierStokes.DiagonalResidual

variable {D V : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D] [NormedAddCommGroup V] [NormedSpace ℝ V]

#count_heartbeats in
/-- THE PRIMITIVE: jets of the orders in `S` are bounded by a common constant times `q ^ r`, eventually along `l`. -/
def JetRateOn (S : Set ℕ) (l : Filter D) (q : D → ℝ) (f : D → V) (r : ℝ) : Prop :=
  ∃ C : ℝ, 0 ≤ C ∧ ∀ᶠ x in l, ∀ m ∈ S, ‖iteratedFDeriv ℝ m f x‖ ≤ C * (q x) ^ r

/-! ### Each member is an instance -/

#count_heartbeats in
theorem jetRate_iff {l : Filter D} {q : D → ℝ} {f : D → V} {m : ℕ} {r : ℝ} :
    JetRate l q f m r ↔ JetRateOn {m} l q f r := by
  constructor
  · rintro ⟨C, hC, h⟩
    exact ⟨C, hC, h.mono fun x hx k hk => by rw [mem_singleton_iff.mp hk]; exact hx⟩
  · rintro ⟨C, hC, h⟩
    exact ⟨C, hC, h.mono fun x hx => hx m rfl⟩

#count_heartbeats in
/-- definitional: `m ∈ Set.Iic M` unfolds to `m ≤ M` -/
theorem finiteJetRate_iff {l : Filter D} {q : D → ℝ} {f : D → V} {M : ℕ} {r : ℝ} :
    FiniteJetRate l q f M r ↔ JetRateOn (Iic M) l q f r := Iff.rfl

/-! ### The API, once -/

#count_heartbeats in
theorem JetRateOn.mono {S T : Set ℕ} {l : Filter D} {q : D → ℝ} {f : D → V} {r : ℝ}
    (hf : JetRateOn S l q f r) (hTS : T ⊆ S) : JetRateOn T l q f r := by
  obtain ⟨C, hC, hb⟩ := hf
  exact ⟨C, hC, hb.mono fun x hx m hm => hx m (hTS hm)⟩

#count_heartbeats in
theorem JetRateOn.weaken {S : Set ℕ} {l : Filter D} {q : D → ℝ} {f : D → V} {r s : ℝ}
    (hf : JetRateOn S l q f r) (hq : ∀ᶠ x in l, 0 < q x ∧ q x ≤ 1) (hsr : s ≤ r) :
    JetRateOn S l q f s := by
  obtain ⟨C, hC, hb⟩ := hf
  refine ⟨C, hC, ?_⟩
  filter_upwards [hq, hb] with x hx hbound m hm
  exact (hbound m hm).trans (mul_le_mul_of_nonneg_left
    (Real.rpow_le_rpow_of_exponent_ge hx.1 hx.2 hsr) hC)

#count_heartbeats in
theorem JetRateOn.add {S : Set ℕ} {l : Filter D} {q : D → ℝ} {f g : D → V} {r : ℝ}
    {U : Set D} (hf : JetRateOn S l q f r) (hg : JetRateOn S l q g r)
    (hU : IsOpen U) (hlU : ∀ᶠ x in l, x ∈ U)
    (hsf : ContDiffOn ℝ ∞ f U) (hsg : ContDiffOn ℝ ∞ g U) :
    JetRateOn S l q (fun x => f x + g x) r := by
  obtain ⟨A, hA, ha⟩ := hf
  obtain ⟨B, hB, hb⟩ := hg
  refine ⟨A + B, add_nonneg hA hB, ?_⟩
  filter_upwards [hlU, ha, hb] with x hx hax hbx m hm
  exact (ResidualStability.norm_jet_add_le hU hsf hsg hx m).trans
    ((add_le_add (hax m hm) (hbx m hm)).trans_eq (by ring))

#count_heartbeats in
theorem JetRateOn.congr_on {S : Set ℕ} {l : Filter D} {q : D → ℝ} {f g : D → V} {r : ℝ}
    {U : Set D} (hf : JetRateOn S l q f r) (hU : IsOpen U)
    (hlU : ∀ᶠ x in l, x ∈ U) (hfg : EqOn f g U) : JetRateOn S l q g r := by
  obtain ⟨C, hC, hb⟩ := hf
  refine ⟨C, hC, ?_⟩
  filter_upwards [hlU, hb] with x hx hbx m hm
  rw [← ResidualStability.iteratedFDeriv_eqOn hU hfg m hx]
  exact hbx m hm

/-! ### Each member's lemmas, re-derived (statements identical to the corpus) -/
namespace Re

#count_heartbeats in
theorem JetRate.weaken {l : Filter D} {q : D → ℝ} {f : D → V} {m : ℕ} {r s : ℝ}
    (hf : JetRate l q f m r) (hq : ∀ᶠ x in l, 0 < q x ∧ q x ≤ 1) (hsr : s ≤ r) :
    JetRate l q f m s :=
  jetRate_iff.2 ((jetRate_iff.1 hf).weaken hq hsr)

#count_heartbeats in
theorem JetRate.add {l : Filter D} {q : D → ℝ} {f g : D → V} {m : ℕ} {r : ℝ}
    {U : Set D} (hf : JetRate l q f m r) (hg : JetRate l q g m r)
    (hU : IsOpen U) (hlU : ∀ᶠ x in l, x ∈ U)
    (hsf : ContDiffOn ℝ ∞ f U) (hsg : ContDiffOn ℝ ∞ g U) :
    JetRate l q (fun x => f x + g x) m r :=
  jetRate_iff.2 ((jetRate_iff.1 hf).add (jetRate_iff.1 hg) hU hlU hsf hsg)

#count_heartbeats in
theorem JetRate.congr_on {l : Filter D} {q : D → ℝ} {f g : D → V} {m : ℕ} {r : ℝ}
    {U : Set D} (hf : JetRate l q f m r) (hU : IsOpen U)
    (hlU : ∀ᶠ x in l, x ∈ U) (hfg : EqOn f g U) : JetRate l q g m r :=
  jetRate_iff.2 ((jetRate_iff.1 hf).congr_on hU hlU hfg)

end Re
end Fam.F2076
namespace Fam.F2076.Re
open NavierStokes NavierStokes.DiagonalResidual
variable {D V : Type} [NormedAddCommGroup D] [NormedSpace ℝ D] [NormedAddCommGroup V] [NormedSpace ℝ V]

#count_heartbeats in
theorem finiteRate_weaken {l : Filter D} {q : D → ℝ} {f : D → V} {M : ℕ} {r s : ℝ}
    (hf : FiniteJetRate l q f M r) (hq : ∀ᶠ x in l, 0 < q x ∧ q x ≤ 1) (hsr : s ≤ r) :
    FiniteJetRate l q f M s :=
  JetRateOn.weaken hf hq hsr

#count_heartbeats in
theorem finiteRate_congr_on {l : Filter D} {q : D → ℝ} {f g : D → V} {M : ℕ} {r : ℝ}
    {U : Set D} (hf : FiniteJetRate l q f M r) (hU : IsOpen U)
    (hlU : ∀ᶠ x in l, x ∈ U) (hfg : EqOn f g U) : FiniteJetRate l q g M r :=
  JetRateOn.congr_on hf hU hlU hfg

#count_heartbeats in
theorem finiteRate_add {l : Filter D} {q : D → ℝ} {f g : D → V} {M : ℕ} {r : ℝ}
    {U : Set D} (hf : FiniteJetRate l q f M r) (hg : FiniteJetRate l q g M r)
    (hU : IsOpen U) (hlU : ∀ᶠ x in l, x ∈ U)
    (hsf : ContDiffOn ℝ ∞ f U) (hsg : ContDiffOn ℝ ∞ g U) :
    FiniteJetRate l q (fun x => f x + g x) M r :=
  JetRateOn.add hf hg hU hlU hsf hsg

/-- The corpus's bridges between the two members are instances of `mono` (extra: not in the API list). -/
theorem finiteRate_at {l : Filter D} {q : D → ℝ} {f : D → V} {M m : ℕ} {r : ℝ}
    (hf : FiniteJetRate l q f M r) (hm : m ≤ M) : JetRate l q f m r :=
  jetRate_iff.2 (JetRateOn.mono hf (by intro k hk; rw [mem_singleton_iff.mp hk]; exact hm))

end Fam.F2076.Re
namespace Fam.F2076
open NavierStokes NavierStokes.DiagonalResidual
variable {D V : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D] [NormedAddCommGroup V] [NormedSpace ℝ V]

#count_heartbeats in
/-- Members kept as reducible names for the instances (used by the downstream replay). -/
abbrev JetRate' (l : Filter D) (q : D → ℝ) (f : D → V) (m : ℕ) (r : ℝ) : Prop := JetRateOn {m} l q f r
#count_heartbeats in
abbrev FiniteJetRate' (l : Filter D) (q : D → ℝ) (f : D → V) (M : ℕ) (r : ℝ) : Prop := JetRateOn (Iic M) l q f r

#count_heartbeats in
theorem jetRate_eq : @DiagonalResidual.JetRate = @JetRate' := by
  funext D V _ _ _ _ l q f m r
  exact propext jetRate_iff

#count_heartbeats in
theorem finiteJetRate_eq : @DiagonalResidual.FiniteJetRate = @FiniteJetRate' := rfl

end Fam.F2076
