//! Minimal reproduction of the "mixed declaration group" defect found on cedar-policy-core.
//!
//! `impl Display for Expr` formats a child with `write!(f, "-{}", child)`. That needs `Expr: Display` as a trait
//! instance inside `fmt`, so the impl and its method refer to each other: one declaration group holding a trait impl
//! and a function. Aeneas's function analysis stops at such a group ("Mixed declaration groups ... are not supported
//! yet") and does not analyse the functions that come after it in the declaration order.
//! `census/rerun.sh` (probes) measures which of the functions below survive.
#![allow(dead_code)]

use core::fmt;

pub enum Expr {
    Lit(u32),
    Neg(Box<Expr>),
}

pub fn unrelated_a(x: u32) -> u32 {
    x.wrapping_add(1)
}

/// BEFORE: the recursion goes through the trait (`{}` on a child of the same type).
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

pub enum Expr2 {
    Lit(u32),
    Neg(Box<Expr2>),
}

impl Expr2 {
    /// AFTER: the recursion is an inherent method calling itself ...
    pub fn write_to(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Expr2::Lit(n) => write!(f, "{}", n),
            Expr2::Neg(e) => {
                f.write_str("-")?;
                e.write_to(f)
            }
        }
    }
}

/// ... and the trait method only forwards to it.
impl fmt::Display for Expr2 {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        self.write_to(f)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn same_text() {
        let a = Expr::Neg(Box::new(Expr::Neg(Box::new(Expr::Lit(7)))));
        let b = Expr2::Neg(Box::new(Expr2::Neg(Box::new(Expr2::Lit(7)))));
        assert_eq!(a.to_string(), "--7");
        assert_eq!(a.to_string(), b.to_string());
        let t = Term::Paren(Box::new(Group { inner: Term::Num(4) }));
        assert_eq!(t.to_string(), "([4])");
    }
}
