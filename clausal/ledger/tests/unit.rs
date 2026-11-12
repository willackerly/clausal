//! Ordinary example-based unit tests (the "tested" evidence kind, by example).
use ledger::{Ledger, Transfer};

fn l(balances: &[u64]) -> Ledger {
    Ledger { balances: balances.to_vec() }
}
fn t(from: usize, to: usize, amount: u64) -> Transfer {
    Transfer { from, to, amount }
}

#[test]
fn balance_in_and_out_of_range() {
    let a = l(&[7, 9]);
    assert_eq!(a.balance(1), Some(9));
    assert_eq!(a.balance(2), None);
}

#[test]
fn total_adds_up() {
    assert_eq!(l(&[1, 2, 3]).total(), Some(6));
    assert_eq!(l(&[]).total(), Some(0));
}

#[test]
fn total_overflow_is_none() {
    assert_eq!(l(&[u64::MAX, 1]).total(), None);
}

#[test]
fn apply_moves_money() {
    let mut a = l(&[10, 0]);
    assert!(a.apply(&t(0, 1, 4)));
    assert_eq!(a.balances, vec![6, 4]);
}

#[test]
fn apply_rejects_and_changes_nothing() {
    let mut a = l(&[10, 0]);
    assert!(!a.apply(&t(0, 1, 11)));
    assert!(!a.apply(&t(0, 2, 1)));
    assert!(!a.apply(&t(1, 1, 0)));
    assert_eq!(a.balances, vec![10, 0]);
}

#[test]
fn batch_applies_in_order_and_stops() {
    let mut a = l(&[10, 0, 0]);
    let n = a.apply_batch(&[t(0, 1, 4), t(1, 2, 4), t(1, 2, 1), t(0, 1, 1)]);
    assert_eq!(n, 2);
    assert_eq!(a.balances, vec![6, 0, 4]);
}

#[test]
fn apply_all_is_all_or_nothing() {
    let mut a = l(&[10, 0, 0]);
    assert!(a.apply_all(&[t(0, 1, 4), t(1, 2, 4)]));
    assert_eq!(a.balances, vec![6, 0, 4]);
    assert!(!a.apply_all(&[t(0, 1, 6), t(1, 2, 7)]));
    assert_eq!(a.balances, vec![6, 0, 4]);
}
