/-
Packet experiment (friction census).  Sibling file: imports the BUILT ns environment, edits nothing.

The mined bundle (out/corpus/friction/BUNDLES.md): four hypotheses about the variable group
(T, Q, Q₁, c) that co-occur verbatim in 110 theorem statements of the Euler half of the corpus:

  hT : 0 ≤ T
  hc : 0 < c
  hQ : ∀ t v, c * ‖v‖ ^ 2 ≤ ‖Q t v‖ ^ 2                               (coercivity of the frame)
  hd : ∀ t, HasDerivWithinAt (extendPath T hT Q) (Q₁ t) (Icc 0 T) t    (Q₁ is the time derivative)

`Frame` is exactly that bundle as ONE hypothesis.  Note `hd` depends on the proof `hT`.
-/
import Euler.FixedEndpointStrong

noncomputable section

namespace FrictionPacket

open Set EulerVolterraConvolution

variable {U E : Type*}
  [NormedAddCommGroup U] [InnerProductSpace ℝ U]
  [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- The frame packet: the four co-occurring hypotheses as one. -/
structure Frame (T : ℝ) (Q Q₁ : C(Icc (0 : ℝ) T, U →L[ℝ] E)) (c : ℝ) : Prop where
  hT : 0 ≤ T
  hc : 0 < c
  hQ : ∀ t v, c * ‖v‖ ^ 2 ≤ ‖Q t v‖ ^ 2
  hd : ∀ t : Icc (0 : ℝ) T, HasDerivWithinAt (extendPath T hT Q) (Q₁ t) (Icc (0 : ℝ) T) t

end FrictionPacket
