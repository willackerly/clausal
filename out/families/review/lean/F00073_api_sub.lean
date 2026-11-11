import Tool
import F73
import Euler.CylinderSpatialMean
import Euler.LpSmoothFieldJets
import Euler.LpTranslation
import Euler.MeanClassicalWordBounds
import Euler.MeanPathSpatialRepresentative
import Euler.MeanTimeTranslation
import Euler.OrdinaryMollifier
import Euler.OrdinaryWordConstraints
import Mathlib.Util.CountHeartbeats
set_option Elab.async false  -- so that #count_heartbeats includes the proof

-- REPLAY EulerCylinderSpatialMean.embedding_translate 15 41
run_cmd IO.println "BLOCK EulerCylinderSpatialMean.embedding_translate"
section
set_option linter.all false
noncomputable section
namespace EulerCylinderSpatialMean
open Set MeasureTheory ContinuousLinearMap InnerProductSpace EulerSmoothLimit EulerLiftedGradientSpace
  EulerLpCylinderTranslation EulerCylinderSpatialEmbedding EulerCylinderAngleAverage
variable (P : ℝ) [Fact (0 < P)]
  {V : Type*} [NormedAddCommGroup V] [InnerProductSpace ℝ V] [CompleteSpace V]
omit [CompleteSpace V] in
#count_heartbeats in
theorem embedding_translate_R (a : LiftTangent) (u : SpatialL2 V) :
    translate P a (embedding P u) = embedding P (EulerLpTranslation.translation a.1 u) := by
  apply Lp.ext
  filter_upwards [translate_ae P a (embedding P u),
    (measurePreserving_translation P (coveringMap P a)).quasiMeasurePreserving.ae (lift_ae P u),
    lift_ae P (EulerLpTranslation.translation a.1 u),
    (Measure.quasiMeasurePreserving_fst (μ := (volume : Measure Space))
      (ν := (volume : Measure (AddCircle P)))).ae (EulerLpTranslation.translation_ae a.1 u)]
      with z ht hu he hs
  change (translate P a (embedding P u)) z = (embedding P (EulerLpTranslation.translation a.1 u)) z
  rw [ht]
  simp only [embedding_apply]
  rw [hu, he, hs]
  rfl
end EulerCylinderSpatialMean
end
end

-- REPLAY EulerCylinderSpatialMean.spatial_translation_inner 45 63
run_cmd IO.println "BLOCK EulerCylinderSpatialMean.spatial_translation_inner"
section
set_option linter.all false
noncomputable section
namespace EulerCylinderSpatialMean
open Set MeasureTheory ContinuousLinearMap InnerProductSpace EulerSmoothLimit EulerLiftedGradientSpace
  EulerLpCylinderTranslation EulerCylinderSpatialEmbedding EulerCylinderAngleAverage
variable (P : ℝ) [Fact (0 < P)]
  {V : Type*} [NormedAddCommGroup V] [InnerProductSpace ℝ V] [CompleteSpace V]
omit [Fact (0 < P)] [CompleteSpace V] in
#count_heartbeats in
theorem spatial_translation_inner_R (a : Space) (u v : SpatialL2 V) :
    inner ℝ (EulerLpTranslation.translation a u) v =
      inner ℝ u (EulerLpTranslation.translation (-a) v) := by
  have h := (EulerLpTranslation.translation a).inner_map_map u (EulerLpTranslation.translation (-a) v)
  rw [EulerLpTranslation.translation_add, add_neg_cancel, EulerLpTranslation.translation_zero] at h
  exact h
end EulerCylinderSpatialMean
end
end

-- REPLAY EulerLpTranslation.SmoothL2Field.iteratedFDeriv_translation_eq 67 90
run_cmd IO.println "BLOCK EulerLpTranslation.SmoothL2Field.iteratedFDeriv_translation_eq"
section
set_option linter.all false
noncomputable section
namespace EulerLpTranslation.SmoothL2Field
open MeasureTheory EulerSmoothLimit EulerLpDerivative Filter
open scoped ContDiff Topology
universe u
variable {V : Type u} [NormedAddCommGroup V] [NormedSpace ℝ V]
#count_heartbeats in
theorem iteratedFDeriv_translation_eq_R (A : SmoothL2Field V) (n : ℕ) (a : Space) :
    iteratedFDeriv ℝ n (fun b : Space => EulerLpTranslation.translation b A.toLp) a =
      multilinearBundling (P := Space) (V := V) volume n (EulerLpTranslation.translation a (A.jetLp n)) := by
  apply ContinuousMultilinearMap.ext
  intro v
  apply Lp.ext
  filter_upwards [A.iteratedFDeriv_translation_ae n a v,
    multilinearBundling_ae volume n (EulerLpTranslation.translation a (A.jetLp n)) v,
    translation_ae a (A.jetLp n),
    (measurePreserving_add_right (volume : Measure Space) a).quasiMeasurePreserving.ae
      (A.jetLp_ae n)] with x hd hm ht hj
  rw [hd, hm, ht, hj]
end EulerLpTranslation.SmoothL2Field
end
end

-- REPLAY EulerLpTranslation.translation_continuous 94 110
run_cmd IO.println "BLOCK EulerLpTranslation.translation_continuous"
section
set_option linter.all false
noncomputable section
namespace EulerLpTranslation
open MeasureTheory EulerSmoothLimit Filter
open scoped Topology
variable {V : Type*} [NormedAddCommGroup V] [NormedSpace ℝ V]
#count_heartbeats in
theorem translation_continuous_R (u : L2Space V) : Continuous (fun a : Space => EulerLpTranslation.translation a u) := by
  let g : Space → C(Space, Space) := fun a => ⟨fun x => x+a, continuous_id.add continuous_const⟩
  have hg : Continuous g := ContinuousMap.continuous_of_continuous_uncurry g
    (continuous_snd.add continuous_fst)
  exact continuous_const.compMeasurePreservingLp hg
    (fun a => measurePreserving_add_right (volume : Measure Space) a) (by norm_num)
end EulerLpTranslation
end
end

-- REPLAY EulerMeanClassicalWordBounds.classicalBaseSize_eq 114 130
run_cmd IO.println "BLOCK EulerMeanClassicalWordBounds.classicalBaseSize_eq"
section
set_option linter.all false
noncomputable section
namespace EulerMeanClassicalWordBounds
open MeasureTheory Set ContinuousLinearMap Finset EulerSmoothLimit EulerMeanSolenoidal
  EulerMeanSmoothRepresentative EulerMeanTimeContinuousTranslation EulerParameterWordGevrey
  EulerGevrey
open scoped ContDiff
variable {ι : Type*}
variable [Fintype ι]
#count_heartbeats in
theorem classicalBaseSize_eq_R (directions : ι → Space) (q : ℕ) (u : L2) (hu : SmoothOrbit u) :
    classicalBaseSize directions q u hu = baseSize directions q (fun a : Space => EulerLpTranslation.translation a u) 0 := by
  simp only [classicalBaseSize, classicalWordLp_eq, ordinaryWord, baseSize, wordSum]
end EulerMeanClassicalWordBounds
end
end

-- REPLAY EulerMeanClassicalWordBounds.classicalBlockSize_eq 134 155
run_cmd IO.println "BLOCK EulerMeanClassicalWordBounds.classicalBlockSize_eq"
section
set_option linter.all false
noncomputable section
namespace EulerMeanClassicalWordBounds
open MeasureTheory Set ContinuousLinearMap Finset EulerSmoothLimit EulerMeanSolenoidal
  EulerMeanSmoothRepresentative EulerMeanTimeContinuousTranslation EulerParameterWordGevrey
  EulerGevrey
open scoped ContDiff
variable {ι : Type*}
variable [Fintype ι]
#count_heartbeats in
theorem classicalBlockSize_eq_R (directions : ι → Space) (q : ℕ) (u : L2) (hu : SmoothOrbit u) (n : ℕ) :
    classicalBlockSize directions q u hu n = block directions q (fun a : Space => EulerLpTranslation.translation a u) n 0 := by
  unfold classicalBlockSize block
  apply sum_congr rfl
  intro w _
  rw [classicalBaseSize_eq]
  exact congrArg (fun g : Space → L2 => baseSize directions q g 0)
    (funext (ordinaryWord_translation directions u hu w))
end EulerMeanClassicalWordBounds
end
end

-- REPLAY EulerMeanSmoothRepresentative.path_orbit_tensor_evaluation 159 177
run_cmd IO.println "BLOCK EulerMeanSmoothRepresentative.path_orbit_tensor_evaluation"
section
set_option linter.all false
noncomputable section
namespace EulerMeanSmoothRepresentative
open Set MeasureTheory EulerSmoothLimit EulerMeanSolenoidal EulerMeanOrdinaryLift
  EulerLiftedGradientSpace EulerCylinderSobolevSpace EulerSobolevPointEvaluation
  EulerMeanTimeContinuousTranslation
open scoped ContDiff
#count_heartbeats in
theorem path_orbit_tensor_evaluation_R (T : ℝ) (p : C(Icc (0 : ℝ) T, EulerMeanSolenoidal.L2))
    (hp : ContDiff ℝ ∞ (fun a : Space => pathTranslation T a p))
    (n : ℕ) (t : Icc (0 : ℝ) T) :
    iteratedFDeriv ℝ n (fun a : Space => EulerLpTranslation.translation a (p t)) 0 =
      (ContinuousMap.evalCLM ℝ t).compContinuousMultilinearMap
        (iteratedFDeriv ℝ n (fun a : Space => pathTranslation T a p) 0) :=
  (ContinuousMap.evalCLM ℝ t).iteratedFDeriv_comp_left hp.contDiffAt (by simp)
end EulerMeanSmoothRepresentative
end
end

-- REPLAY EulerMeanTimeTranslation.translation_continuous 181 196
run_cmd IO.println "BLOCK EulerMeanTimeTranslation.translation_continuous"
section
set_option linter.all false
noncomputable section
namespace EulerMeanTimeTranslation
open Set MeasureTheory InnerProductSpace ContinuousLinearMap EulerSmoothLimit
  EulerMeanSolenoidal EulerTimeLp EulerTerminalTimePrimitive EulerTimeLpBoundedMap
#count_heartbeats in
theorem translation_continuous_R (u : L2) : Continuous (fun a : Space => EulerLpTranslation.translation a u) := by
  let g : Space → C(Space, Space) := fun a => ⟨fun x => x+a, continuous_id.add continuous_const⟩
  have hg : Continuous g := ContinuousMap.continuous_of_continuous_uncurry g
    (continuous_snd.add continuous_fst)
  exact continuous_const.compMeasurePreservingLp hg
    (fun a => measurePreserving_add_right (volume : Measure Space) a) (by norm_num)
end EulerMeanTimeTranslation
end
end

-- REPLAY EulerOrdinaryMollifier.translation_inner_shift 200 216
run_cmd IO.println "BLOCK EulerOrdinaryMollifier.translation_inner_shift"
section
set_option linter.all false
noncomputable section
namespace EulerOrdinaryMollifier
open Set Filter MeasureTheory InnerProductSpace ContinuousLinearMap EulerSmoothLimit
  EulerMeanSolenoidal EulerNoncompactTransport EulerLpTranslation.SmoothL2Field
open scoped ContDiff Topology Convolution
#count_heartbeats in
theorem translation_inner_shift_R (a : Space) (u v : L2) :
    ⟪EulerLpTranslation.translation a u,v⟫_ℝ=⟪u,EulerLpTranslation.translation (-a) v⟫_ℝ := by
  calc
    _=⟪EulerLpTranslation.translation a u,EulerLpTranslation.translation a (EulerLpTranslation.translation (-a) v)⟫_ℝ := by
      rw [translation_add,add_neg_cancel,translation_zero]
    _=_ := (EulerLpTranslation.translation a).inner_map_map _ _
end EulerOrdinaryMollifier
end
end

-- REPLAY EulerOrdinarySobolev.projection_word 220 237
run_cmd IO.println "BLOCK EulerOrdinarySobolev.projection_word"
section
set_option linter.all false
noncomputable section
namespace EulerOrdinarySobolev
open MeasureTheory InnerProductSpace ContinuousLinearMap EulerSmoothLimit EulerLpTranslation
  EulerLpTranslation.SmoothL2Field EulerParameterWordGevrey EulerMeanSolenoidal
open scoped ContDiff
#count_heartbeats in
theorem projection_word_R (A : SmoothL2Field Space) {n : ℕ} (w : Fin n → Fin 3) :
    solenoidalProjection (wordField A w).toLp = wordDerivative axis
      (fun a : Space => EulerLpTranslation.translation a (solenoidalProjection A.toLp)) w 0 := by
  rw [word_toLp_eq_orbit,← wordDerivative_comp_clm axis solenoidalProjection _ A.translation_contDiff]
  congr 2
  funext a
  exact (solenoidalProjection_translation a A.toLp).symm
end EulerOrdinarySobolev
end
end

-- REPLAY EulerOrdinarySobolev.word_toLp_eq_orbit 241 259
run_cmd IO.println "BLOCK EulerOrdinarySobolev.word_toLp_eq_orbit"
section
set_option linter.all false
noncomputable section
namespace EulerOrdinarySobolev
open MeasureTheory InnerProductSpace ContinuousLinearMap EulerSmoothLimit EulerLpTranslation
  EulerLpTranslation.SmoothL2Field EulerParameterWordGevrey EulerMeanSolenoidal
open scoped ContDiff
#count_heartbeats in
theorem word_toLp_eq_orbit_R (A : SmoothL2Field Space) {n : ℕ} (w : Fin n → Fin 3) :
    (wordField A w).toLp = wordDerivative axis
      (fun a : Space => EulerLpTranslation.translation a A.toLp) w 0 := by
  apply Lp.ext
  filter_upwards [(wordField A w).toLp_ae,A.iteratedFDeriv_translation_ae n 0 (axis ∘ w)]
    with x ha hb
  rw [ha,wordField_field]
  simpa only [wordDerivative,Function.comp_def,add_zero] using hb.symm
end EulerOrdinarySobolev
end
end

