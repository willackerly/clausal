//! The code under test of the third project (plan node X7): a bounded counter. Charon/Aeneas translate
//! exactly this file to Lean (lean/Generated/Counter.lean). Deliberately tiny and in profile: one struct,
//! one function, no loop, no derive. Tests live in tests/ so Charon never sees them.

pub struct Counter {
    pub count: u64,
}

impl Counter {
    /// Adds `by` to the count if the result is at most 100, and says whether it did.
    /// A bump that would pass 100 is rejected and changes nothing.
    pub fn bump(&mut self, by: u64) -> bool {
        if self.count > 100 {
            return false;
        }
        if by > 100 - self.count {
            return false;
        }
        self.count += by;
        true
    }
}
