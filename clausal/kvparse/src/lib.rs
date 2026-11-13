//! The code under test of the fourth project (plan node K1): a toy byte-level parser, the first target of the rule
//! pack "validated input". Charon/Aeneas translate exactly this file to Lean (lean/Generated/Kvparse.lean).
//! In profile (census/PROFILE.md): one `while` directly in the function body, helpers for one field and for the loop (Aeneas takes
//! an early return inside a loop only when the loop is directly in the function body), indexing, no iterator, no `str`, no derive. Tests live in tests/ so Charon never sees them.
//!
//! THE FORMAT. A record is one or two fields separated by `;`. A field is three bytes: a key, `=`, one decimal
//! digit. The keys are `a` and `b`; each occurs at most once, and `a` comes before `b`. So the records are
//! `a=D`, `b=D` and `a=D;b=D`. Nothing may follow the last field. An input longer than the parser's limit is
//! rejected whatever it holds. Unknown keys and repeated keys are rejected, not skipped.

/// A parser with its size limit: the longest input, in bytes, it accepts.
pub struct Parser {
    pub limit: usize,
}

/// A parsed record: for each key, whether it was given and the value of its digit (0 if it was not given).
pub struct Record {
    pub has_a: bool,
    pub a: u8,
    pub has_b: bool,
    pub b: u8,
}

/// One field at position `i`: key, `=`, digit. Records it in `r` and says whether it is a field the record may have
/// here: `a` at most once and before `b`, `b` at most once, no other key.
fn field(inp: &[u8], i: usize, r: &mut Record) -> bool {
    // a field is three bytes   (i <= inp.len() at every call)
    if inp.len() - i < 3 {
        return false;
    }
    let k = inp[i];
    let d = inp[i + 2];
    if inp[i + 1] != b'=' || d < b'0' || d > b'9' {
        return false;
    }
    if k == b'a' {
        if r.has_a || r.has_b {
            return false;
        }
        r.has_a = true;
        r.a = d - b'0';
        true
    } else if k == b'b' {
        if r.has_b {
            return false;
        }
        r.has_b = true;
        r.b = d - b'0';
        true
    } else {
        false
    }
}

/// The record the whole input is, if it is one: a field, then either the end or `;` and another field.
fn record(inp: &[u8]) -> Option<Record> {
    let n = inp.len();
    let mut r = Record { has_a: false, a: 0, has_b: false, b: 0 };
    let mut i: usize = 0;
    let mut more = true;
    while more {
        if !field(inp, i, &mut r) {
            return None;
        }
        i += 3;
        if i == n {
            more = false;
        } else if inp[i] != b';' {
            return None;
        } else {
            i += 1;
        }
    }
    Some(r)
}

impl Parser {
    /// Parses one record. `None` if the input is longer than the limit or is not a record of the format.
    pub fn parse(&self, inp: &[u8]) -> Option<Record> {
        if inp.len() > self.limit {
            return None;
        }
        record(inp)
    }
}
