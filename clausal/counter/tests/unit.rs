//! Ordinary example-based unit tests (the "tested" evidence kind, by example).
use counter::Counter;

#[test]
fn bump_adds() {
    let mut c = Counter { count: 10 };
    assert!(c.bump(5));
    assert_eq!(c.count, 15);
}

#[test]
fn bump_to_the_bound_is_accepted() {
    let mut c = Counter { count: 40 };
    assert!(c.bump(60));
    assert_eq!(c.count, 100);
}

#[test]
fn bump_past_the_bound_is_rejected_and_changes_nothing() {
    let mut c = Counter { count: 40 };
    assert!(!c.bump(61));
    assert_eq!(c.count, 40);
}

#[test]
fn a_count_already_past_the_bound_is_never_bumped() {
    let mut c = Counter { count: 101 };
    assert!(!c.bump(0));
    assert_eq!(c.count, 101);
}
