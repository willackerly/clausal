import Euler.BaseFirstPacketChoice
import Euler.BaseFirstPacketChoiceNoOptions
import Euler.BaseFirstPacketEvolution
import Euler.BaseFirstPacketEvolutionNoOptions
import Euler.BaseInductionStage
import Euler.BaseInductionStageNoOptions
import Euler.GevreyGeneratingDerivatives
import Euler.GevreyGeneratingDerivativesNoOptions
import Euler.LpCylinderCoefficientTime
import Euler.LpCylinderCoefficientTimeInvestigation
import Euler.MeanPacketEnvelopeBounds
import Euler.MeanPacketEnvelopeBoundsNoOptions
import Euler.PacketShiftArithmetic
import Euler.PacketShiftArithmeticNoOptions
import Euler.ParentGeometryForwardChoice
import Euler.ParentGeometryForwardChoiceNoOptions
import Euler.ParentGeometryJoinedChoice
import Euler.ParentGeometryJoinedChoiceInvestigation
import Euler.TransversePacketCorrector
import Euler.TransversePacketCorrectorNoOptions
import NavierStokes.ActualParticularDynamics
import NavierStokes.ActualParticularDynamicsNoOptions
import NavierStokes.CorrectionInitialization
import NavierStokes.CorrectionInitializationNoOptions
import NavierStokes.DiagonalJetBounds
import NavierStokes.DiagonalJetBoundsNoOptions
import ReuseCheck

/-!
F6. Cloned modules.

Thirteen modules named `…NoOptions` / `…Investigation` are copies of a base module under a new
namespace (the largest, `NavierStokes/CorrectionInitializationNoOptions.lean`, has 5,573 lines).
For every theorem of a clone that has a twin in its base module (same statement and proof up to
renaming, key `svP`) we ask the kernel whether the ORIGINAL theorem, as a bare constant, proves
the copy.  This succeeds when the copied definitions the statement mentions unfold to the same
terms as the originals; it must fail when the statement mentions a copied structure or inductive
type, which is a different type however identical it looks.
-/

set_option maxHeartbeats 1000000

#follows_pairs "clone" "../../out/corpus/reuse/factor/clone_pairs.jsonl"
