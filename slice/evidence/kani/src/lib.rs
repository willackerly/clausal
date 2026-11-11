//! Bounded model checking of the compiled sentences (plan node E1). Nothing here is written per rule:
//! `harnesses.rs`, `checks.rs` are GENERATED from ../../build/trees.json; `typed.rs` is the typed reading of each
//! vocabulary piece, written once.
//!
//!   cargo kani --harness k9_r0 --exact        (names and sizes: ../../build/evidence_gen.json)
#![cfg(kani)]
#![allow(unused_variables, unused_mut, unused_parens, dead_code)]

#[path = "../../src/typed.rs"]
mod typed;
#[path = "../../src/checks.rs"]
mod checks;
mod harnesses;
