// Reproduction of "one mixed declaration group makes every later function fail".
// Two types whose `Display` impls format each other (`Term`, `Group`) put trait impls and functions
// in one declaration group. Aeneas's function analysis stops at that group, and the functions
// declared after it (`unrelated_b`, `Wrapper::get`, `unrelated_c`) fail with "Internal error"
// although they have nothing to do with it.
#![allow(dead_code)]

use core::fmt;

pub enum Expr {
    Lit(u32),
    Neg(Box<Expr>),
}

pub fn unrelated_a(x: u32) -> u32 {
    x.wrapping_add(1)
}

/// The recursion goes through the trait (`{}` on a child of the same type).
impl fmt::Display for Expr {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Expr::Lit(n) => write!(f, "{}", n),
            Expr::Neg(e) => write!(f, "-{}", e),
        }
    }
}

/// Two types whose `Display` impls use each other.
pub enum Term {
    Num(u32),
    Paren(Box<Group>),
}

pub struct Group {
    pub inner: Term,
}

impl fmt::Display for Term {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Term::Num(n) => write!(f, "{}", n),
            Term::Paren(g) => write!(f, "({})", g),
        }
    }
}

impl fmt::Display for Group {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "[{}]", self.inner)
    }
}

pub fn unrelated_b(x: u32) -> u32 {
    x.wrapping_mul(3)
}

pub struct Wrapper(pub u32);

impl Wrapper {
    pub fn get(&self) -> u32 {
        self.0
    }
}

pub fn unrelated_c(w: &Wrapper) -> u32 {
    w.get().wrapping_sub(1)
}
