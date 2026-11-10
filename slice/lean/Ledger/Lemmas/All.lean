import Ledger.Lemmas.Batch
open Aeneas Aeneas.Std Result

/- `Ledger::apply_all`: all or nothing, by cloning the balances. -/
namespace ledger

/-- Aeneas ships no `step` lemma for `Vec<u64>::clone`; this is the missing one. -/
@[step]
theorem clone_vec_u64.spec (v : alloc.vec.Vec U64) :
    alloc.vec.CloneVec.clone core.clone.CloneU64 v ⦃ v' => v' = v ⦄ := by
  simp only [alloc.vec.CloneVec.clone]
  apply Std.WP.spec_bind (Slice.clone_spec (clone := core.clone.CloneU64.clone) (s := v.slice) (by intros; rfl))
  intro s hs
  simp [← hs]

@[step]
theorem Ledger.apply_all.spec (l0 : Ledger) (batch : Slice Transfer) :
    Ledger.apply_all l0 batch ⦃ r =>
      LVocab.total r.2 = LVocab.total l0 ∧
      (r.1 = false → r.2 = l0) ∧
      (LVocab.firstInvalid l0 batch → r.1 = false) ∧
      -- exact: accepted iff the pure model applies the whole batch, and then with its balances
      (r.1 = decide ((runN (nums l0) batch.val).1 = batch.val.length)) ∧
      (r.1 = true → nums r.2 = (runN (nums l0) batch.val).2) ⦄ := by
  unfold Ledger.apply_all
  step*
  · -- some transfer was rejected: the saved balances are put back
    subst saved_post
    have hx := congrArg Prod.fst applied_post3
    simp only at hx
    have hd : decide ((runN (nums l0) batch.val).1 = batch.val.length) = false :=
      decide_eq_false (by scalar_tac)
    exact ⟨rfl, fun _ => rfl, fun _ _ => trivial, hd.symm, fun h => absurd h (by decide)⟩
  · -- every transfer was applied; then the first one cannot have been invalid
    have hx := congrArg Prod.fst applied_post3
    have hy := congrArg Prod.snd applied_post3
    simp only at hx hy
    have hd : decide ((runN (nums l0) batch.val).1 = batch.val.length) = true :=
      decide_eq_true (by scalar_tac)
    refine ⟨applied_post, fun h => absurd h (by decide), fun h1 h2 => ?_, hd.symm, fun _ => hy⟩
    have h0 := (applied_post2 h1 h2).1
    have hlen : 0 < batch.val.length := List.length_pos_iff.mpr h1
    scalar_tac

end ledger
