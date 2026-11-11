/-
Synthetic re-inventions used as controls for the M7 detector.  Never part of any corpus.
  Carries   : copy of Mathlib `Set.MapsTo` under a new name, arguments shuffled, binder made explicit
  gap       : thin wrapper around `dist` with the arguments swapped
  BddBy     : a hidden-constant predicate of the big-O kind (sign conjunct, no norm on the bound)
and three lemmas re-proved for `Carries` that copy `Set.MapsTo.comp`, `Set.MapsTo.mono_left`, `Set.mapsTo_id`.
-/
import Mathlib.Data.Set.Function
import Mathlib.Analysis.Asymptotics.Defs
import Mathlib.Topology.MetricSpace.Pseudo.Defs
import Mathlib.Order.Monotone.Defs
import Mathlib.Order.SuccPred.Basic

namespace ReinventPlanted

def Carries {α β : Type*} (t : Set β) (f : α → β) (s : Set α) : Prop :=
  ∀ a, a ∈ s → f a ∈ t

noncomputable def gap {X : Type*} [PseudoMetricSpace X] (a b : X) : ℝ := dist b a

def BddBy {α : Type*} (l : Filter α) (g : α → ℝ) (f : α → ℝ) : Prop :=
  ∃ C, 0 ≤ C ∧ ∀ᶠ x in l, |f x| ≤ C * g x

theorem Carries.comp {α β γ : Type*} {s : Set α} {t : Set β} {p : Set γ} {f : α → β} {g : β → γ}
    (h₁ : Carries p g t) (h₂ : Carries t f s) : Carries p (g ∘ f) s :=
  fun a ha => h₁ _ (h₂ a ha)

theorem Carries.mono_left {α β : Type*} {s₁ s₂ : Set α} {t : Set β} {f : α → β}
    (hf : Carries t f s₁) (hs : s₂ ⊆ s₁) : Carries t f s₂ :=
  fun a ha => hf a (hs ha)

theorem carries_id {α : Type*} (s : Set α) : Carries s id s := fun _ h => h

theorem gap_comm {X : Type*} [PseudoMetricSpace X] (a b : X) : gap a b = gap b a := dist_comm _ _

theorem gap_triangle {X : Type*} [PseudoMetricSpace X] (a b c : X) : gap a c ≤ gap a b + gap b c := by
  unfold gap; rw [add_comm]; exact dist_triangle c b a

end ReinventPlanted

/-!
Reviewer's controls (added in the reviewer's scratch copy only; written by the reviewer, not the builder).
P = should be found (equivalent to a library notion); N = must not be confirmed as a library notion.
-/
namespace ReviewControls
open Filter

/-- P1: the body of `Monotone`, specialised to ℕ → ℝ. -/
def UpHill (f : ℕ → ℝ) : Prop := ∀ a b, a ≤ b → f a ≤ f b
/-- P2: `Function.Injective`, written out. -/
def OneToOne {α β : Type*} (f : α → β) : Prop := ∀ a b, f a = f b → a = b
/-- P3: little-o, with absolute values and an explicit ε. -/
def Negligible {α : Type*} (l : Filter α) (f g : α → ℝ) : Prop :=
  ∀ ε : ℝ, 0 < ε → ∀ᶠ x in l, |f x| ≤ ε * |g x|
/-- P4: convergence of a real sequence, ε–N (library: `Tendsto u atTop (𝓝 a)`). -/
def ConvergesTo (u : ℕ → ℝ) (a : ℝ) : Prop := ∀ ε > 0, ∃ N, ∀ n ≥ N, |u n - a| < ε
/-- P5: Lipschitz on ℝ with a real constant (library: `LipschitzWith`, constant in ℝ≥0). -/
def LipBound (K : ℝ) (f : ℝ → ℝ) : Prop := ∀ x y, |f x - f y| ≤ K * |x - y|

/-- N1: a hidden constant against a bound that is never nonnegative; not big-O
(it says `|f x| ≤ C·(negative)` eventually, i.e. the filter is trivial). -/
def NegBound (l : Filter ℕ) (f : ℕ → ℝ) : Prop :=
  ∃ C, 0 ≤ C ∧ ∀ᶠ x in l, |f x| ≤ C * (-(1 + (x : ℝ) ^ 2))
/-- N2: `MapsTo` plus a strictly stronger extra conjunct. -/
def CarriesNonempty {α β : Type*} (t : Set β) (f : α → β) (s : Set α) : Prop :=
  (∀ a, a ∈ s → f a ∈ t) ∧ s.Nonempty
/-- N3: one-sided slack: not `Monotone`. -/
def AlmostUp (f : ℕ → ℝ) : Prop := ∀ a b, a ≤ b → f a ≤ f b + 1
/-- N4: a plain arithmetic formula with no shared meaning (coincidence class). -/
def stepAbove (n : ℕ) : ℕ := 80 * n + 1
/-- N5: a pair with no shared meaning (coincidence class). -/
def flipPair (p : ℕ × ℝ) : ℝ × ℕ := (p.2, p.1)

end ReviewControls
