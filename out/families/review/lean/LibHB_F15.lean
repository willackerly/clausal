/-
M9 families, F00015: fifteen predicates with different bodies and the same closure laws.
No parameter merges them.  THE PRIMITIVE IS MATHLIB'S `AddSubgroup`: each member, with its own `zero`, `add` and
`neg` lemmas as the three fields, is an additive subgroup of its space of fields; `sub` (and finite sums,
integer multiples) then come from the library's API and need no member lemma.
Form: a bundled structure (data = the set, facts = the three closure laws).  Not a type class: the members
are families indexed by parameters (a set, an interval, a gauge), so there is no canonical instance to search for.
-/
import Tool
import NavierStokes.ActualCyclePeriodicity
import NavierStokes.CorrectionStep
import NavierStokes.DefectIncrementBounds
import NavierStokes.GaugeDebtIncrement
import NavierStokes.GaugeMomentBalances
import NavierStokes.HarmonicFields
import NavierStokes.HarmonicResidual
import NavierStokes.HarmonicSourceSupport
import NavierStokes.LocalRankDefect
import NavierStokes.MeanIncrementBounds
import NavierStokes.MeanStateRegularity
import NavierStokes.MovingMomentBounds
import NavierStokes.PhysicalResidualNaturality
import NavierStokes.PrimaryCopyBounds
import Mathlib.Util.CountHeartbeats
set_option Elab.async false

open NavierStokes
open scoped ContDiff

noncomputable section

namespace Fam.F15

#count_heartbeats in
/-- The bridge, once: a predicate with the three closure laws is an `AddSubgroup`. -/
def ofPred {M : Type*} [AddGroup M] (P : M → Prop) (h0 : P 0)
    (hadd : ∀ {a b}, P a → P b → P (a + b)) (hneg : ∀ {a}, P a → P (-a)) : AddSubgroup M where
  carrier := {a | P a}
  add_mem' := hadd
  zero_mem' := h0
  neg_mem' := hneg

#count_heartbeats in
theorem mem_ofPred {M : Type*} [AddGroup M] {P : M → Prop} {h0 : P 0}
    {hadd : ∀ {a b}, P a → P b → P (a + b)} {hneg : ∀ {a}, P a → P (-a)} {a : M} :
    a ∈ ofPred P h0 hadd hneg ↔ P a := Iff.rfl

section
variable {D : Type}

#count_heartbeats in
def bandLimited (N : ℕ) : AddSubgroup (HarmonicResidual.Coefficients D) :=
  ofPred (fun c => HarmonicFields.BandLimited c N) (HarmonicResidual.band_zero N)
    HarmonicFields.BandLimited.add HarmonicResidual.band_neg

#count_heartbeats in
def nonzeroSupported (K : Set D) : AddSubgroup (HarmonicFields.Coefficients D) :=
  ofPred (HarmonicSourceSupport.NonzeroSupported K) HarmonicSourceSupport.NonzeroSupported.zero
    HarmonicSourceSupport.NonzeroSupported.add HarmonicSourceSupport.NonzeroSupported.neg

#count_heartbeats in
def gaugeSupported (a b : ℝ) (ell : D → ℝ) (U : Set D) :
    AddSubgroup (CorrectionStep.ScalarField (PressureStream.Lift D)) :=
  ofPred (CorrectionStep.GaugeSupported a b ell U) CorrectionStep.GaugeSupported.zero
    CorrectionStep.GaugeSupported.add CorrectionStep.GaugeSupported.neg

#count_heartbeats in
def support (a b : ℝ) (ell : D → ℝ) (U : Set D) :
    AddSubgroup (MeanIncrementBounds.Field (PressureStream.Lift D)) :=
  ofPred (MovingMomentBounds.Support a b ell U) (fun _ _ _ hn => (hn rfl).elim)
    MovingMomentBounds.Support.add MovingMomentBounds.Support.neg

#count_heartbeats in
/-- `Support` and `GaugeSupported` are the same predicate, defined twice. -/
theorem support_eq_gaugeSupported (a b : ℝ) (ell : D → ℝ) (U : Set D) :
    MovingMomentBounds.Support a b ell U = CorrectionStep.GaugeSupported a b ell U := rfl

end

section
variable {D : Type} [NormedAddCommGroup D]

#count_heartbeats in
def coefficientsTranslation (U : Set D) (v : D) : AddSubgroup (HarmonicFields.Coefficients D) :=
  ofPred (ActualCyclePeriodicity.CoefficientsTranslation U v) ActualCyclePeriodicity.CoefficientsTranslation.zero
    ActualCyclePeriodicity.CoefficientsTranslation.add ActualCyclePeriodicity.CoefficientsTranslation.neg

end

section
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]



#count_heartbeats in
def smoothCoefficients (U : Set D) : AddSubgroup (HarmonicResidual.Coefficients D) :=
  ofPred (HarmonicResidual.SmoothCoefficients U) (HarmonicResidual.smoothCoefficients_zero U)
    HarmonicResidual.SmoothCoefficients.add HarmonicResidual.SmoothCoefficients.neg


#count_heartbeats in
def smoothOn (U : Set D) : AddSubgroup (MeanIncrementBounds.Field D) :=
  ofPred (MeanIncrementBounds.SmoothOn U) (fun _ => contDiffOn_const)
    MeanIncrementBounds.SmoothOn.add MeanIncrementBounds.SmoothOn.neg




#count_heartbeats in
def shell (a b : ℝ) : AddSubgroup (DefectIncrementBounds.ScalarField (DefectIncrementBounds.Point D)) :=
  ofPred (DefectIncrementBounds.Shell a b) DefectIncrementBounds.Shell.zero
    DefectIncrementBounds.Shell.add DefectIncrementBounds.Shell.neg

#count_heartbeats in
def localShell (a b : ℝ) (U : Set D) : AddSubgroup (LocalRankDefect.ScalarField (LocalRankDefect.Point D)) :=
  ofPred (LocalRankDefect.LocalShell a b U) LocalRankDefect.LocalShell.zero
    LocalRankDefect.LocalShell.add LocalRankDefect.LocalShell.neg

end

section
variable {coord : ℝ}

#count_heartbeats in
def regular (U : LocalSignedRequest.SlowRegion coord) (a b : ℝ) : AddSubgroup GaugeDebtIncrement.Scalar :=
  ofPred (GaugeDebtIncrement.Regular U a b) GaugeDebtIncrement.Regular.zero
    GaugeDebtIncrement.Regular.add GaugeDebtIncrement.Regular.neg

#count_heartbeats in
def movingField (U : LocalSignedRequest.SlowRegion coord) (a b : ℝ) : AddSubgroup MeanStateRegularity.Scalar :=
  ofPred (GaugeMomentBalances.MovingField U a b) MeanStateRegularity.MovingField.zero
    MeanStateRegularity.MovingField.add MeanStateRegularity.MovingField.neg

#count_heartbeats in
def periodic (U : Set MeanStateRegularity.Plane) : AddSubgroup MeanStateRegularity.Scalar :=
  ofPred (MeanStateRegularity.Periodic U) MeanStateRegularity.Periodic.zero
    MeanStateRegularity.Periodic.add MeanStateRegularity.Periodic.neg

end

section
variable {D E : Type} [NormedAddCommGroup D] [NormedSpace ℝ D] [NormedAddCommGroup E] [NormedSpace ℝ E]

#count_heartbeats in
/-- a relation between two coefficient families: a subgroup of the product -/
def coefficientsOn (U : Set D) (e : D ≃L[ℝ] E) (a : ℝ) :
    AddSubgroup (HarmonicFields.Coefficients D × HarmonicFields.Coefficients E) :=
  ofPred (fun p => PhysicalResidualNaturality.CoefficientsOn U e a p.1 p.2)
    (PhysicalResidualNaturality.CoefficientsOn.zero U e a)
    (fun h₁ h₂ => PhysicalResidualNaturality.CoefficientsOn.add h₁ h₂)
    (fun h => PhysicalResidualNaturality.CoefficientsOn.neg h)

#count_heartbeats in
/-- `ScalarOn` has no `neg` lemma in the corpus; it is `smul (-1)`. -/
def scalarOn (U : Set D) (e : D ≃L[ℝ] E) (a : ℝ) : AddSubgroup ((D → ℝ) × (E → ℝ)) :=
  ofPred (fun p => PhysicalResidualNaturality.ScalarOn U e a p.1 p.2)
    (fun x _ => by simp)
    (fun h₁ h₂ => PhysicalResidualNaturality.ScalarOn.add h₁ h₂)
    (fun h => by simpa using PhysicalResidualNaturality.ScalarOn.smul h (-1))

end

section
variable {ι : Type*} {D : Type} {E : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]

#count_heartbeats in
/-- `NativeJets` bundles a fact about the WEIGHT (`nonneg`), so the zero family is a member only when the weight
is nonnegative: the subgroup exists under that hypothesis and not otherwise. -/
def nativeJets (V : PrimaryCopyBounds.JetDomain ι D) (w : ι → D → ℝ)
    (hw : ∀ i x, x ∈ V.carrier i → 0 ≤ w i x) : AddSubgroup (ι → D → E) :=
  ofPred (PrimaryCopyBounds.NativeJets V w)
    ⟨hw, fun _ => contDiffOn_const, fun m => ⟨1, le_rfl, 0, fun i x hx j _ => by
      have h0 : iteratedFDeriv ℝ j ((0 : ι → D → E) i) x = 0 := by
        show iteratedFDeriv ℝ j (fun _ : D => (0 : E)) x = 0
        simp
      rw [h0, norm_zero]
      simpa using hw i x hx⟩⟩
    (fun hf hg => PrimaryCopyBounds.NativeJets.add hf hg)
    (fun hf => PrimaryCopyBounds.NativeJets.neg hf)

#count_heartbeats in
/-- Without the hypothesis the set of members can be empty, hence not a subgroup. -/
theorem nativeJets_empty (V : PrimaryCopyBounds.JetDomain ι D) (i : ι) {x : D} (hx : x ∈ V.carrier i)
    (f : ι → D → E) : ¬ PrimaryCopyBounds.NativeJets V (fun _ _ => (-1 : ℝ)) f := fun h => by
  have := h.nonneg i x hx
  norm_num at this

end

end Fam.F15
