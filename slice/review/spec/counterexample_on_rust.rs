use wallet::{transfer, Wallet, WalletError};
#[test]
fn refuted_counterexample_on_real_rust() {
    let (mut a, mut b) = (Wallet { balance: 1 }, Wallet { balance: u64::MAX });
    assert!(1 <= a.balance); // Given: amount is not more than Alice's balance
    let r = transfer(&mut a, &mut b, 1);
    assert!(matches!(r, Err(WalletError::Overflow)), "Then 'the operation succeeds' must FAIL");
    assert_eq!((a.balance, b.balance), (1, u64::MAX));
    assert_ne!(a.balance as u128 + 1, 1u128); // Then 'decreased by 1' fails
}
