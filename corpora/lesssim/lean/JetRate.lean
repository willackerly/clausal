/-
Constant-threading experiment: the corpus's own predicate `DiagonalResidual.JetRate` is Mathlib's big-O.
-/
import Lib
import NavierStokes.DiagonalResidual

open Asymptotics Filter
open NavierStokes

namespace Lesssim

variable {D V : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D] [NormedAddCommGroup V] [NormedSpace ℝ V]

/-- `JetRate l q f m r` is `(jets of order m of f) =O[l] q ^ r`, for any filter `l`, as soon as `q ^ r` is
eventually nonnegative (always the case in the corpus, where `q > 0`). -/
theorem jetRate_iff_isBigO {l : Filter D} {q : D → ℝ} {f : D → V} {m : ℕ} {r : ℝ}
    (hq : ∀ᶠ x in l, 0 ≤ q x ^ r) :
    DiagonalResidual.JetRate l q f m r ↔ (fun x => iteratedFDeriv ℝ m f x) =O[l] fun x => q x ^ r := by
  constructor
  · rintro ⟨C, -, hb⟩
    exact IsBigO.of_bound |C| (hb.mono fun x hx => hx.trans ((le_abs_self _).trans (abs_mul _ _).le))
  · intro h
    obtain ⟨C, hC, hb⟩ := h.exists_nonneg
    exact ⟨C, hC, (hb.bound.and hq).mono fun x hx => by
      have := hx.1
      rwa [Real.norm_of_nonneg hx.2] at this⟩

/-- The corpus's `JetRate.weaken` is transitivity with the exponent law. -/
example {l : Filter D} {q : D → ℝ} {f : D → V} {m : ℕ} {r s : ℝ}
    (hf : (fun x => iteratedFDeriv ℝ m f x) =O[l] fun x => q x ^ r)
    (hq : ∀ᶠ x in l, 0 < q x ∧ q x ≤ 1) (hsr : s ≤ r) :
    (fun x => iteratedFDeriv ℝ m f x) =O[l] fun x => q x ^ s :=
  hf.trans (IsBigO.of_bound 1 (hq.mono fun x hx => by
    rw [Real.norm_of_nonneg (Real.rpow_nonneg hx.1.le _), Real.norm_of_nonneg (Real.rpow_nonneg hx.1.le _),
      one_mul]
    exact Real.rpow_le_rpow_of_exponent_ge hx.1 hx.2 hsr))

#print axioms jetRate_iff_isBigO

end Lesssim
