/-
Tests for `Rosette.Candidates` and `Rosette.Lift` on real Mathlib theorems from analysis,
algebra, combinatorics and number theory. Compiling this file *is* the test: every `#rosette_lift`
adds kernel-checked theorems, and the `run_meta` blocks below throw if an invariant fails.

  lake build Rosette.Candidates Rosette.Lift && lake env lean Rosette/Tests.lean
-/
import Mathlib
import Rosette.Lift

open Lean Meta Rosette

/-! ## Candidate enumeration -/

-- analysis
#rosette_candidates image_le_of_liminf_slope_right_lt_deriv_boundary'
#rosette_candidates IsCompact.exists_isMinOn 5
-- algebra
#rosette_candidates exists_prime_orderOf_dvd_card
#rosette_candidates Polynomial.card_roots' 5
-- combinatorics
#rosette_candidates Finset.all_card_le_biUnion_card_iff_exists_injective
#rosette_candidates Finset.exists_ne_map_eq_of_card_lt_of_maps_to 5
-- number theory
#rosette_candidates Nat.sum_four_squares
#rosette_candidates legendreSym.quadratic_reciprocity 5

/-! ## Lifting: new kernel-checked lemmas + rewritten main theorem -/

#rosette_lift image_le_of_liminf_slope_right_lt_deriv_boundary' (k := 5)
#rosette_lift IsCompact.exists_isMinOn (k := 3)
#rosette_lift exists_prime_orderOf_dvd_card (k := 5)
#rosette_lift Polynomial.card_roots' (k := 3)
#rosette_lift Finset.all_card_le_biUnion_card_iff_exists_injective (k := 5)
#rosette_lift Finset.exists_ne_map_eq_of_card_lt_of_maps_to (k := 3)
#rosette_lift Nat.sum_four_squares (k := 5)
#rosette_lift legendreSym.quadratic_reciprocity (k := 5) (minProof := 60) (maxStmt := 120)

/-- The declarations lifted above. -/
def Rosette.testDecls : Array Name := #[
  ``image_le_of_liminf_slope_right_lt_deriv_boundary', ``IsCompact.exists_isMinOn,
  ``exists_prime_orderOf_dvd_card, ``Polynomial.card_roots',
  ``Finset.all_card_le_biUnion_card_iff_exists_injective,
  ``Finset.exists_ne_map_eq_of_card_lt_of_maps_to,
  ``Nat.sum_four_squares, ``legendreSym.quadratic_reciprocity]

/-! ## Invariants -/

/- For each test declaration: `X.lifted` is a theorem with *syntactically the same* statement as
`X`, it really calls at least one `X.lifted_i`, every `X.lifted_i` is a theorem, and lifting
introduced no new axioms. -/
run_meta do
  let env ← getEnv
  for n in Rosette.testDecls do
    let orig ← getConstInfo n
    let some (.thmInfo main) := env.find? (n ++ `lifted)
      | throwError "{n}.lifted is missing or not a theorem"
    unless main.type == orig.type do throwError "{n}.lifted: statement differs"
    let aux := main.value.getUsedConstants.filter fun c =>
      c.toString.startsWith (n.toString ++ ".lifted_")
    if aux.isEmpty then throwError "{n}.lifted does not call any lifted lemma"
    for a in aux do
      let some (.thmInfo _) := env.find? a | throwError "{a} is not a theorem"
    let ax0 ← collectAxioms n
    let ax1 ← collectAxioms (n ++ `lifted)
    for a in ax1 do
      unless ax0.contains a do throwError "{n}.lifted uses new axiom {a}"
    logInfo m!"ok: {n}.lifted calls {aux.size} lifted lemma(s); axioms {ax1}"

/- The kernel gate is real: a wrong proof is rejected, not silently accepted. -/
run_meta do
  let bad ← try
      addTheoremChecked `Rosette.Tests.bogus [] (mkConst ``False) (mkConst ``True.intro)
      pure false
    catch _ => pure true
  unless bad do throwError "kernel accepted a bogus theorem"
  logInfo "ok: bogus theorem rejected by the kernel"

/- ... and it stays on when the ambient options ask to skip the kernel (review finding). -/
set_option debug.skipKernelTC true in
run_meta do
  let bad ← try
      addTheoremChecked `Rosette.Tests.bogus2 [] (mkConst ``False) (mkConst ``True.intro)
      pure false
    catch _ => pure true
  unless bad do throwError "kernel check was skipped under debug.skipKernelTC"
  logInfo "ok: bogus theorem rejected even with debug.skipKernelTC"

/-! ## Regressions for the two enumeration bugs found in review -/

/-- A proof in which `⟨h hx, h' (h hx)⟩` occurs three times and every variable has type `ι` or
`Set ι`. -/
theorem Rosette.Tests.dup {ι : Type} (s t u : Set ι) (h : s ⊆ t) (h' : t ⊆ u) (x : ι) (hx : x ∈ s) :
    (x ∈ t ∧ x ∈ u) ∧ (x ∈ u ∧ x ∈ t) ∧ (x ∈ t ∧ x ∈ u) ∧ (x ∈ u ∧ x ∈ t) ∧ (x ∈ t ∧ x ∈ u) :=
  ⟨⟨h hx, h' (h hx)⟩, ⟨h' (h hx), h hx⟩, ⟨h hx, h' (h hx)⟩, ⟨h' (h hx), h hx⟩, ⟨h hx, h' (h hx)⟩⟩

run_meta do
  let r ← candidatesOfConstCore ``Rosette.Tests.dup { minProofSize := 5 }
  -- 1. no variable is listed twice in an interface (`∀ {ι : Type} {ι : Type} …` before the fix)
  for c in r.cands do
    if (c.statement.splitOn "{ι : Type} {ι : Type}").length > 1 then
      throwError "duplicated binder in: {c.statement}"
    -- 8 variables are in scope (ι s t u h h' x hx); nothing can depend on more
    if c.numDeps > 8 then throwError "{c.numDeps} dependencies, only 8 variables exist"
  -- 2. a repeated subterm is one candidate with a position count, not one candidate per position
  unless r.cands.any (·.occurrences == 3) do
    throwError "the subterm that occurs three times was not merged into one candidate"
  for c in r.cands do
    for d in r.cands do
      if c.id < d.id && c.stmtHash == d.stmtHash && c.proofSizeDag == d.proofSizeDag
          && c.proofSizeTree == d.proofSizeTree then
        throwError "candidates {c.id} and {d.id} are the same lemma"
  logInfo m!"ok: {r.cands.size} distinct candidates, no repeated binder"

-- lifting a subterm that occurs at several positions replaces every copy
#rosette_lift Rosette.Tests.dup (k := 1) (minProof := 20)
run_meta do
  let some (.thmInfo main) := (← getEnv).find? ``Rosette.Tests.dup.lifted
    | throwError "Rosette.Tests.dup.lifted missing"
  logInfo m!"ok: Rosette.Tests.dup.lifted has {dagSize main.value} nodes \
    (original {dagSize (← proofOfConst ``Rosette.Tests.dup)})"

/- Structural statement hash: invariant under binder names and universe names, sensitive to
the statement itself. -/
run_meta do
  let a ← Elab.Term.TermElabM.run' do
    Elab.Term.elabTerm (← `(∀ (n m : Nat), n + m = m + n)) none
  let b ← Elab.Term.TermElabM.run' do
    Elab.Term.elabTerm (← `(∀ (x y : Nat), x + y = y + x)) none
  let c ← Elab.Term.TermElabM.run' do
    Elab.Term.elabTerm (← `(∀ (x y : Nat), x + y = x + y)) none
  unless statementHash a == statementHash b do throwError "hash depends on binder names"
  if statementHash a == statementHash c then throwError "hash does not separate statements"
  let u := (← getConstInfo ``List.length_append).type
  let u' := u.instantiateLevelParams (← getConstInfo ``List.length_append).levelParams
    [Level.param `some_other_universe]
  unless statementHash u == statementHash u' do throwError "hash depends on universe names"
  logInfo "ok: statement hash"

/-! ## Expected non-results (reported, not hidden) -/

-- `Nat.bertrand` is an alias: its proof term is a single constant, so there is nothing to lift.
#rosette_candidates Nat.bertrand
#rosette_lift Nat.bertrand

-- Axioms have no proof term.
/-- error: rosette: 'propext' has no value (axiom, constructor, recursor, …) -/
#guard_msgs in
#rosette_candidates propext

-- Definitions are not theorems.
/-- error: rosette: 'Nat.add' is not a theorem (its type is not a proposition) -/
#guard_msgs in
#rosette_lift Nat.add

/-! ## JSON lines -/

#rosette_dump "out/rosette_tests_candidates.jsonl" image_le_of_liminf_slope_right_lt_deriv_boundary' IsCompact.exists_isMinOn exists_prime_orderOf_dvd_card Polynomial.card_roots' Finset.all_card_le_biUnion_card_iff_exists_injective Finset.exists_ne_map_eq_of_card_lt_of_maps_to Nat.sum_four_squares legendreSym.quadratic_reciprocity Nat.bertrand
