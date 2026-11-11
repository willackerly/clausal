import Tool
import F46
import NavierStokes.MeanIncrementBounds
import Mathlib.Util.CountHeartbeats
set_option Elab.async false  -- so that #count_heartbeats includes the proof

-- REPLAY NavierStokes.MeanIncrementBounds.Class.neg 8 30
run_cmd IO.println "BLOCK NavierStokes.MeanIncrementBounds.Class.neg"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.MeanIncrementBounds
open Set Filter WeightedClasses
open scoped ContDiff Topology
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
namespace Operators
end Operators
namespace SmoothOn
variable {U : Set D} {f g : Field D}
end SmoothOn
namespace Operators
end Operators
namespace Class
#count_heartbeats in
theorem neg_R {s : StripData D} {α : ℝ} {f : Field D} (hf : MeanClass s α f) :
    MeanClass s α (-f) :=
  NavierStokes.CurlClassBounds.class_neg hf
end Class
end NavierStokes.MeanIncrementBounds
end
end

-- REPLAY NavierStokes.MeanIncrementBounds.Class.sub 34 56
run_cmd IO.println "BLOCK NavierStokes.MeanIncrementBounds.Class.sub"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.MeanIncrementBounds
open Set Filter WeightedClasses
open scoped ContDiff Topology
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
namespace Operators
end Operators
namespace SmoothOn
variable {U : Set D} {f g : Field D}
end SmoothOn
namespace Operators
end Operators
namespace Class
#count_heartbeats in
theorem sub_R {s : StripData D} {α : ℝ} {f g : Field D}
    (hf : MeanClass s α f) (hg : MeanClass s α g) : MeanClass s α (f - g) :=
  NavierStokes.CurlClassBounds.class_sub hf hg
end Class
end NavierStokes.MeanIncrementBounds
end
end

