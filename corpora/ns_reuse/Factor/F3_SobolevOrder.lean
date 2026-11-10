import Euler.EulerProof
import ReuseCheck

/-!
F3. The same estimate proved separately for two Sobolev orders.

`EulerSobolevDerivativeNorm.sobolevNorm_three_le_pure_derivatives` (order 3) and
`EulerSobolevProducts.sobolevNorm_six_le_pure_derivatives` (order 6) are two 39-line proofs in
`Euler/EulerProof.lean` that differ only in the numeral and in the pointwise weight inequality
they cite.  Below is ONE lemma for an arbitrary order `s : ℕ`, with that weight inequality as a
hypothesis; its proof is the order-6 proof with `6` replaced by `s`.  Both originals are then
re-derived from it.
-/

noncomputable section

namespace ReuseFactor

open MeasureTheory FourierTransform EulerSobolev EulerSobolevProducts
open scoped SchwartzMap ENNReal ContDiff LineDeriv

theorem sobolevNorm_le_pure_derivatives (d s : ℕ)
    (hw : ∀ ξ : Domain d, besselWeight d s ξ ≤ ((d : ℝ) + 1) ^ 2 * (1 + ∑ i, ‖ξ i‖ ^ s))
    (f : 𝓢(Domain d, ℂ)) :
    sobolevNorm d s f ≤ ((d : ℝ) + 1) ^ 2 *
      (‖f.toLp 2‖ + (2 * Real.pi) ^ (-(s : ℤ)) *
        ∑ i : Fin d, ‖(directional d s (EuclideanSpace.single i 1) f).toLp 2‖) := by
  let g : Option (Fin d) → 𝓢(Domain d, ℂ) := fun i => match i with
    | none => 𝓕 f
    | some i => ((2 * Real.pi) ^ (-(s : ℤ)) : ℝ) •
        𝓕 (directional d s (EuclideanSpace.single i 1) f)
  have hpoint (ξ : Domain d) :
      ‖weightedFourier d s f ξ‖ ≤ ((d : ℝ) + 1) ^ 2 * ∑ i, ‖g i ξ‖ := by
    rw [weightedFourier_apply, norm_smul, Real.norm_of_nonneg (besselWeight_pos d s ξ).le]
    have hg : ∑ i, ‖g i ξ‖ = (1 + ∑ i, ‖ξ i‖ ^ s) * ‖𝓕 f ξ‖ := by
      rw [Fintype.sum_option]
      simp only [g, smul_apply, norm_smul,
        Real.norm_of_nonneg (by positivity : 0 ≤ (2 * Real.pi) ^ (-(s : ℤ))),
        fourier_directional_norm, EuclideanSpace.inner_single_right,
        starRingEnd_apply, star_trivial]
      have hp : (2 * Real.pi) ^ (-(s : ℤ)) * (2 * Real.pi) ^ (s : ℕ) = 1 := by
        rw [zpow_neg, zpow_natCast]
        exact inv_mul_cancel₀ (by positivity)
      simp_rw [← mul_assoc, hp, one_mul]
      rw [add_mul, one_mul, Finset.sum_mul]
    rw [hg]
    nlinarith [mul_le_mul_of_nonneg_right (hw ξ) (norm_nonneg (𝓕 f ξ))]
  have h := normLp_le_sum d (weightedFourier d s f) g (((d : ℝ) + 1) ^ 2)
    (sq_nonneg _) hpoint
  have hnorm : ∑ i, ‖(g i).toLp 2‖ = ‖f.toLp 2‖ +
      (2 * Real.pi) ^ (-(s : ℤ)) * ∑ i : Fin d,
        ‖(directional d s (EuclideanSpace.single i 1) f).toLp 2‖ := by
    rw [Fintype.sum_option]
    simp only [g]
    change ‖(𝓕 f).toLp 2‖ + ∑ i,
      ‖SchwartzMap.toLpCLM ℝ ℂ 2 volume (((2 * Real.pi) ^ (-(s : ℤ))) •
        𝓕 (directional d s (EuclideanSpace.single i 1) f))‖ = _
    simp only [map_smul, norm_smul,
      Real.norm_of_nonneg (by positivity : 0 ≤ (2 * Real.pi) ^ (-(s : ℤ))),
      SchwartzMap.toLpCLM_apply, SchwartzMap.norm_fourier_toL2_eq, Finset.mul_sum]
  rw [hnorm] at h
  exact h

end ReuseFactor

#follows "sobolev" ["EulerSobolevProducts.sobolevNorm_six_le_pure_derivatives"] :=
  fun d f => by
    simpa using ReuseFactor.sobolevNorm_le_pure_derivatives d 6
      (by simpa using EulerSobolevProducts.besselWeight_six_le_pure_six d) f

#follows "sobolev" ["EulerSobolevDerivativeNorm.sobolevNorm_three_le_pure_derivatives"] :=
  fun d f => by
    simpa using ReuseFactor.sobolevNorm_le_pure_derivatives d 3
      (by simpa using EulerSobolevDerivativeNorm.besselWeight_three_le_pure_three d) f
