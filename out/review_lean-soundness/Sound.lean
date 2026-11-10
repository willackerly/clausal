import Mathlib
import Rosette.Lift
open Lean Meta Rosette

-- 1. axioms of lifted results
#rosette_lift Nat.sum_four_squares (k := 5)
#print axioms Nat.sum_four_squares
#print axioms Nat.sum_four_squares.lifted
#print axioms Nat.sum_four_squares.lifted_1
#print axioms Nat.sum_four_squares.lifted_2
#print axioms Nat.sum_four_squares.lifted_3
#check @Nat.sum_four_squares.lifted
#check @Nat.sum_four_squares
#rosette_lift exists_prime_orderOf_dvd_card (k := 5)
#print axioms exists_prime_orderOf_dvd_card.lifted
#print axioms exists_prime_orderOf_dvd_card

-- 2. kernel gate with skipKernelTC
set_option debug.skipKernelTC true in
run_meta do
  let ok ← try
      addTheoremChecked `Rev.bogus [] (mkConst ``False) (mkConst ``True.intro); pure true
    catch _ => pure false
  logInfo m!"skipKernelTC: bogus accepted = {ok}"

-- 2b. ill-typed value whose type is right "by name" only
run_meta do
  let ok ← try
      addTheoremChecked `Rev.bogus2 [] (mkConst ``False) (mkApp2 (mkConst ``sorryAx [0]) (mkConst ``False) (mkConst ``Bool.false)); pure true
    catch _ => pure false
  logInfo m!"sorryAx value accepted by addTheoremChecked = {ok}"

-- 3. duplicated binders
theorem Rev.dup {ι : Type} (s t u : Set ι) (h : s ⊆ t) (h' : t ⊆ u) (x : ι) (hx : x ∈ s) :
    (x ∈ t ∧ x ∈ u) ∧ (x ∈ u ∧ x ∈ t) ∧ (x ∈ t ∧ x ∈ u) ∧ (x ∈ u ∧ x ∈ t) ∧ (x ∈ t ∧ x ∈ u) :=
  ⟨⟨h hx, h' (h hx)⟩, ⟨h' (h hx), h hx⟩, ⟨h hx, h' (h hx)⟩, ⟨h' (h hx), h hx⟩, ⟨h hx, h' (h hx)⟩⟩

run_meta do
  let r ← candidatesOfConstCore ``Rev.dup { minProofSize := 5 }
  for c in r.cands do logInfo m!"{c.format}"

-- 4. dependent let + have
theorem Rev.letdep (n : Nat) (h : 0 < n) : ∃ m, m = n + n ∧ 0 < m ∧ m ≠ 1 := by
  let m := n + n
  have hm : 0 < m := by omega
  have hm' : m ≠ 1 := by omega
  exact ⟨m, rfl, hm, hm'⟩

run_meta do
  let r ← candidatesOfConstCore ``Rev.letdep { minProofSize := 5 }
  logInfo m!"letdep: {r.cands.size} cands errors={r.errors}"
  for c in (sortByRatio r.cands).extract 0 6 do logInfo m!"{c.format}"
  let l ← liftConst ``Rev.letdep { k := 4, minProofSize := 10, maxFraction := 0.9, enum := { minProofSize := 5, ppStatements := false } }
  logInfo m!"{l.skeleton}"
#print axioms Rev.letdep.lifted
#print Rev.letdep.lifted

-- 5. hash invariance probes
run_meta do
  let a ← Elab.Term.TermElabM.run' do Elab.Term.elabTerm (← `(∀ (n m : Nat), n + m = m + n)) none
  let b ← Elab.Term.TermElabM.run' do Elab.Term.elabTerm (← `(∀ {n m : Nat}, n + m = m + n)) none
  let c ← Elab.Term.TermElabM.run' do Elab.Term.elabTerm (← `(∀ (n m : Nat), m + n = n + m)) none
  let d ← Elab.Term.TermElabM.run' do Elab.Term.elabTerm (← `(∀ (n : Nat) (h : 0 < n) (h' : n < 5), n ≠ 7)) none
  let e ← Elab.Term.TermElabM.run' do Elab.Term.elabTerm (← `(∀ (n : Nat) (h' : n < 5) (h : 0 < n), n ≠ 7)) none
  logInfo m!"binderinfo-invariant={statementHash a == statementHash b} alpha-renamed-swap-equal={statementHash a == statementHash c} hyp-order-invariant={statementHash d == statementHash e}"
  let u1 := mkSort (.max (.param `u) (.param `v))
  let u2 := mkSort (.max (.param `v) (.param `u))
  logInfo m!"level max commut: {statementHash u1 == statementHash u2}"
