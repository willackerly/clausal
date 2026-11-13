//! The code under test of the fourth project (plan node W6, trust test 1): intake of a signed message ON A TOY
//! VERIFIER. Charon/Aeneas translate exactly this file to Lean (lean/Generated/Sigintake.lean). In profile: three
//! structs, two functions, no loop, no derive. Tests live in tests/ so Charon never sees them.
//!
//! `verify` IS NOT CRYPTOGRAPHY. It is a stand-in with a body, so that it translates to a Lean definition and not
//! to an axiom: anyone who knows the key number can compute the tag. Nothing proved about this crate says anything
//! about a signature scheme.
//!
//! The state is the pair (expected key, last counter). Both are handed over `&mut` because that is the one shape
//! of signature the pipeline reads a two-part state from (lean/Bdd/Ops.lean, `opMut2`); `intake` never writes the key.

pub struct Key {
    pub id: u64,
}

pub struct Counter {
    pub last: u64,
}

/// `hint` is the unsigned part: `verify` is not given it.
pub struct Message {
    pub payload: u64,
    pub counter: u64,
    pub tag: u64,
    pub hint: u64,
}

/// TOY: the tag of (payload, counter) under a key is three hex digits, one each from the key, the payload and
/// the counter.
pub fn verify(key: &Key, payload: u64, counter: u64, tag: u64) -> bool {
    tag == (key.id % 16) * 256 + (payload % 16) * 16 + counter % 16
}

/// Accepts a message iff its tag verifies under the expected key and its counter is above the last counter
/// accepted; an accepted message's counter becomes the last counter. A rejected message changes nothing.
pub fn intake(expected_key: &mut Key, last_counter: &mut Counter, msg: Message) -> bool {
    if !verify(expected_key, msg.payload, msg.counter, msg.tag) {
        return false;
    }
    if msg.counter <= last_counter.last {
        return false;
    }
    last_counter.last = msg.counter;
    true
}
