//! Ordinary example-based unit tests (the "tested" evidence kind, by example).
use wallet::{transfer, Wallet, WalletError};

fn w(balance: u64) -> Wallet {
    Wallet { balance }
}

#[test]
fn deposit_adds() {
    let mut a = w(10);
    assert!(a.deposit(5).is_ok());
    assert_eq!(a.balance, 15);
}

#[test]
fn deposit_overflow_is_rejected_and_changes_nothing() {
    let mut a = w(u64::MAX);
    assert!(matches!(a.deposit(1), Err(WalletError::Overflow)));
    assert_eq!(a.balance, u64::MAX);
}

#[test]
fn withdraw_subtracts() {
    let mut a = w(10);
    assert!(a.withdraw(10).is_ok());
    assert_eq!(a.balance, 0);
}

#[test]
fn withdraw_too_much_is_rejected_and_changes_nothing() {
    let mut a = w(10);
    assert!(matches!(a.withdraw(11), Err(WalletError::InsufficientFunds)));
    assert_eq!(a.balance, 10);
}

#[test]
fn transfer_moves_money_and_conserves_total() {
    let (mut a, mut b) = (w(100), w(20));
    assert!(transfer(&mut a, &mut b, 30).is_ok());
    assert_eq!((a.balance, b.balance), (70, 50));
}

#[test]
fn transfer_insufficient_funds() {
    let (mut a, mut b) = (w(10), w(7));
    assert!(matches!(transfer(&mut a, &mut b, 11), Err(WalletError::InsufficientFunds)));
    assert_eq!((a.balance, b.balance), (10, 7));
}

#[test]
fn transfer_destination_overflow() {
    let (mut a, mut b) = (w(1), w(u64::MAX));
    assert!(matches!(transfer(&mut a, &mut b, 1), Err(WalletError::Overflow)));
    assert_eq!((a.balance, b.balance), (1, u64::MAX));
}
