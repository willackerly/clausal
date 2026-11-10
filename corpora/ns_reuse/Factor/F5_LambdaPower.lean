import NavierStokes.CorrectedPulseAmplitude
import NavierStokes.UniformAngularReset
import ReuseCheck

/-!
F5. One inequality for two exponents.

`CorrectedPulseAmplitude.power29_le_lambda : d.core.lam ^ 29 ≤ d.core.lam` and
`UniformAngularReset.power28_le_self : d.core.lam ^ 28 ≤ d.core.lam` are proved separately (and
by different routes).  One lemma for every positive exponent replaces both.
-/

namespace ReuseFactor
open NavierStokes NavierStokes.OutgoingTail

theorem lam_pow_le_self (d : TailData) {n : ℕ} (hn : n ≠ 0) : d.core.lam ^ n ≤ d.core.lam :=
  pow_le_of_le_one d.core.lam_pos.le (by linarith [d.core.lam_lt]) hn

end ReuseFactor

#follows "lam_pow" ["NavierStokes.CorrectedPulseAmplitude.power29_le_lambda",
                    "NavierStokes.UniformAngularReset.power28_le_self"] :=
  fun d => ReuseFactor.lam_pow_le_self d (by norm_num)
