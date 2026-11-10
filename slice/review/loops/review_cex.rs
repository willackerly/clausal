//! Reviewer's independent check on the COMPILED Rust (not through cucumber, not through the glossary):
//! the two REFUTED counterexamples really fail, and the reviewer's length-3/4/5 batches give
//! the same results as the Lean model (review/loops/ReviewLoops.lean, section C).
//! Run in a scratch copy: cp review/loops/review_cex.rs <copy>/ledger/tests/ && cargo test --test review_cex
use ledger::{Ledger, Transfer};

fn t(from: usize, to: usize, amount: u64) -> Transfer { Transfer { from, to, amount } }
fn valid(bal: &[u64], x: &Transfer) -> bool {
    x.from < bal.len() && x.to < bal.len() && x.from != x.to
        && x.amount <= bal[x.from] && bal[x.to].checked_add(x.amount).is_some()
}

#[test]
fn refuted_batch_all_valid_all_applied() {
    // counterexample reported: balances [1, 0], batch [0->1:1, 0->1:1]
    let start = vec![1u64, 0];
    let batch = [t(0, 1, 1), t(0, 1, 1)];
    assert!(batch.iter().all(|x| valid(&start, x)), "Givens must hold at the counterexample");
    let mut l = Ledger { balances: start };
    let n = l.apply_batch(&batch);
    assert_eq!(n, 1, "the claim says 2 (= batch length)");
    assert_ne!(n, batch.len());
    assert_eq!(l.balances, vec![0, 1]);
}

#[test]
fn refuted_total_always_available() {
    let l = Ledger { balances: vec![u64::MAX, 1] };
    assert_eq!(l.total(), None);
}

#[test]
fn reviewer_long_batches_agree_with_lean_model() {
    let mut l = Ledger { balances: vec![100, 20, 0] };
    assert_eq!(l.apply_batch(&[t(0, 1, 30), t(1, 2, 50), t(2, 0, 10), t(0, 2, 5)]), 4);
    assert_eq!(l.balances, vec![75, 0, 45]);
    let mut l = Ledger { balances: vec![100, 20, 0] };
    assert_eq!(l.apply_batch(&[t(0, 1, 30), t(1, 2, 50), t(2, 0, 10), t(1, 0, 1), t(0, 2, 5)]), 3);
    assert_eq!(l.balances, vec![80, 0, 40]);
    // false claim also fails at length 3
    let start = vec![100u64, 20, 0];
    let b = [t(0, 1, 60), t(1, 2, 20), t(0, 2, 60)];
    assert!(b.iter().all(|x| valid(&start, x)));
    let mut l = Ledger { balances: start };
    assert_eq!(l.apply_batch(&b), 2);
    assert_eq!(l.balances, vec![40, 60, 20]);
    let mut l = Ledger { balances: vec![5, 5] };
    assert_eq!(l.apply_batch(&[t(0, 1, 6), t(1, 0, 1), t(0, 1, 2)]), 0);
    assert_eq!(l.balances, vec![5, 5]);
}
