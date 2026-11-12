//! The code under test. Charon/Aeneas translate exactly this file to Lean
//! (lean/Generated/Wallet.lean). No derives: each derive adds generated trait
//! impls to the translated surface. Tests live in tests/ so Charon never sees them.

pub enum WalletError {
    InsufficientFunds,
    Overflow,
}

pub struct Wallet {
    pub balance: u64,
}

impl Wallet {
    pub fn deposit(&mut self, amt: u64) -> Result<(), WalletError> {
        match self.balance.checked_add(amt) {
            Some(b) => {
                self.balance = b;
                Ok(())
            }
            None => Err(WalletError::Overflow),
        }
    }

    pub fn withdraw(&mut self, amt: u64) -> Result<(), WalletError> {
        if amt > self.balance {
            return Err(WalletError::InsufficientFunds);
        }
        self.balance -= amt;
        Ok(())
    }
}

pub fn transfer(src: &mut Wallet, dst: &mut Wallet, amt: u64) -> Result<(), WalletError> {
    if src.balance < amt {
        return Err(WalletError::InsufficientFunds);
    }
    let nb = match dst.balance.checked_add(amt) {
        Some(b) => b,
        None => return Err(WalletError::Overflow),
    };
    src.balance -= amt;
    dst.balance = nb;
    Ok(())
}
