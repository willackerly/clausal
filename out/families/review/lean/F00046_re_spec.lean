import Tool
import NavierStokes.MeanIncrementBounds
import Mathlib.Util.CountHeartbeats
set_option Elab.async false  -- so that #count_heartbeats includes the proof

-- REPLAY NavierStokes.MeanIncrementBounds.Class.neg 7 31
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
theorem neg_S {s : StripData D} {α : ℝ} {f : Field D} (hf : MeanClass s α f) :
    MeanClass s α (-f) := by
  have h := hf.map (-ContinuousLinearMap.id ℝ ℝ)
  simp only [_root_.neg_apply, ContinuousLinearMap.id_apply] at h
  exact h
end Class
end NavierStokes.MeanIncrementBounds
end
end

-- REPLAY NavierStokes.MeanIncrementBounds.Class.sub 35 59
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
theorem sub_S {s : StripData D} {α : ℝ} {f g : Field D}
    (hf : MeanClass s α f) (hg : MeanClass s α g) : MeanClass s α (f - g) := by
  have h := hf.add (neg hg)
  simp only [sub_eq_add_neg] at h ⊢
  exact h
end Class
end NavierStokes.MeanIncrementBounds
end
end

