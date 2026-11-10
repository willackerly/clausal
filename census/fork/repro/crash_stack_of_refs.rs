// Candidate reproduction of the uncaught `Failure("ty_regions shouldn't be called on erased or body regions")`
// (shape of cedar-policy-core's `CedarValueJson::height`).
pub enum V {
    Leaf(u32),
    Set(Vec<V>),
}

impl V {
    pub fn height(&self) -> usize {
        let mut stack: Vec<(&V, usize)> = vec![(self, 0)];
        let mut max_depth: usize = 0;
        while let Some((val, depth)) = stack.pop() {
            if depth > max_depth {
                max_depth = depth;
            }
            match val {
                V::Leaf(_) => {}
                V::Set(vs) => {
                    for v in vs {
                        stack.push((v, depth + 1));
                    }
                }
            }
        }
        max_depth
    }
}

// Unrelated; lost together with the rest of the crate.
pub fn add_one(x: u32) -> u32 {
    x.wrapping_add(1)
}
