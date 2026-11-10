// Aeneas aborts the whole crate (no output) on the signature of `Iterator::copied`.
pub fn copied_max(v: &[u32]) -> Option<u32> {
    v.iter().copied().max()
}

// Unrelated; lost together with the rest of the crate.
pub fn add_one(x: u32) -> u32 {
    x.wrapping_add(1)
}
