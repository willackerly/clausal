//! The second code under test: a ledger of balances with loops over collections.
//! Charon/Aeneas translate exactly this file to Lean (lean/Generated/Ledger.lean).
//! No derives; tests live in tests/ so Charon never sees them.

/// Move `amount` from account `from` to account `to` (indexes into the ledger).
pub struct Transfer {
    pub from: usize,
    pub to: usize,
    pub amount: u64,
}

pub struct Ledger {
    pub balances: Vec<u64>,
}

impl Ledger {
    /// The balance of account `i`, or `None` if there is no such account.
    pub fn balance(&self, i: usize) -> Option<u64> {
        if i < self.balances.len() {
            Some(self.balances[i])
        } else {
            None
        }
    }

    /// The sum of all balances, or `None` if it does not fit in a u64.
    pub fn total(&self) -> Option<u64> {
        let mut sum: u64 = 0;
        let mut i = 0;
        while i < self.balances.len() {
            sum = match sum.checked_add(self.balances[i]) {
                Some(s) => s,
                None => return None,
            };
            i += 1;
        }
        Some(sum)
    }

    /// Apply one transfer. Returns false, leaving the ledger as it was, if an
    /// account does not exist, sender and receiver are the same account, the
    /// sender cannot cover the amount, or the receiver's balance would overflow.
    pub fn apply(&mut self, t: &Transfer) -> bool {
        let n = self.balances.len();
        if t.from >= n || t.to >= n || t.from == t.to {
            return false;
        }
        let f = self.balances[t.from];
        if f < t.amount {
            return false;
        }
        let nb = match self.balances[t.to].checked_add(t.amount) {
            Some(b) => b,
            None => return false,
        };
        self.balances[t.from] = f - t.amount;
        self.balances[t.to] = nb;
        true
    }

    /// Apply the transfers in order, stopping at the first one that is rejected.
    /// Returns how many were applied.
    pub fn apply_batch(&mut self, batch: &[Transfer]) -> usize {
        let mut i = 0;
        while i < batch.len() {
            if !self.apply(&batch[i]) {
                break;
            }
            i += 1;
        }
        i
    }

    /// All or nothing: apply every transfer of the batch, or, if one is rejected,
    /// put every balance back as it was. Returns whether the batch was applied.
    pub fn apply_all(&mut self, batch: &[Transfer]) -> bool {
        let saved = self.balances.clone();
        let applied = self.apply_batch(batch);
        if applied < batch.len() {
            self.balances = saved;
            return false;
        }
        true
    }
}
