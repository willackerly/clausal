/-
S8. `ParametricKernelBounds.profile_comp_derivative_bound`, tried with the library unchanged.
The statement fits and the proof is the chain-rule law `jet_comp` plus two imports.  With the original's
`{E : Type*}` it does NOT compile: `jet_comp` is built on the corpus lemma `composition_jet_bound_on`, which
is stated for spaces in `Type` (error kept in `out/corpus/lesssim/sample_S8_universe_error.log`).  What
is checked here is the same proof with `{E : Type}`; it is therefore not shown equivalent to the original.
-/
import Lib
import NavierStokes.ParametricKernelBounds

noncomputable section

open Asymptotics Filter Set
open scoped Topology ContDiff BigOperators
open NavierStokes NavierStokes.ParametricKernelBounds

namespace Lesssim.Sample.Native

theorem profile_comp_derivative_bound {E : Type} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {b : E × ℝ → ℝ} (hb : ContDiff ℝ ∞ b) (n : ℕ) {R : ℝ} (hR : 0 ≤ R)
    (hjets : ∀ k ≤ n, (fun z => iteratedFDeriv ℝ k b z) =O[𝓟 {z | ‖z‖ ≤ R}] fun _ => (1 : ℝ)) :
    ∃ N : ℕ, (fun q : (E × ℝ) × ℝ => iteratedFDeriv ℝ n (b ∘ transform q.2) q.1)
      =O[𝓟 {q | ‖q.1‖ ≤ R ∧ 0 ≤ q.2}] fun q => (1 + q.2) ^ N := by
  obtain ⟨A, M, -, htransform⟩ := finite_polynomial_majorant
    (fun k (y : E × ℝ) t => ‖iteratedFDeriv ℝ k (transform t) y‖) R n
    (fun k _ => transform_derivative_bound k hR)
  refine ⟨M * n, (jet_comp (T := {q : (E × ℝ) × ℝ | ‖q.1‖ ≤ R ∧ 0 ≤ q.2})
    (g := fun _ => b) (φ := fun q => transform q.2) (U := fun _ => univ) (W := fun _ => univ)
    (pt := fun q => q.1) (A := fun _ => 1) (B := fun q => (1 + q.2) ^ M)
    (fun _ _ => isOpen_univ) (fun _ _ => isOpen_univ) (fun _ _ => hb.contDiffOn)
    (fun _ hq => (transform_contDiff hq.2).contDiffOn) (fun _ _ => mapsTo_univ _ _) (fun _ _ => mem_univ _) n
    (fun _ _ => zero_le_one) (fun _ hq => one_le_pow₀ (by linarith [hq.2]))
    (fun i hi => comp_mapsTo (hjets i hi) (k := fun q : (E × ℝ) × ℝ => transform q.2 q.1)
      fun q hq => (norm_transform_le hq.2 q.1).trans hq.1)
    (fun i _ hi => isBigO_of_bound_on A fun q hq => htransform i hi q.1 q.2 hq.1 hq.2) n le_rfl).congr_right
    fun q => by rw [one_mul, ← pow_mul]⟩

end Lesssim.Sample.Native
