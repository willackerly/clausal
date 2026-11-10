// Aeneas aborts the whole crate (no output) on the signature of `core::str::pattern::Pattern::into_searcher`.
pub fn find_colon(s: &str) -> Option<usize> {
    s.find(':')
}

// Unrelated; lost together with the rest of the crate.
pub fn add_one(x: u32) -> u32 {
    x.wrapping_add(1)
}
