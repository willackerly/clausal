//! Ordinary example-based unit tests (the "tested" evidence kind, by example).
use kvparse::Parser;

fn parse(limit: usize, s: &str) -> Option<(bool, u8, bool, u8)> {
    Parser { limit }.parse(s.as_bytes()).map(|r| (r.has_a, r.a, r.has_b, r.b))
}

#[test]
fn the_three_shapes_of_record_are_accepted() {
    assert_eq!(parse(7, "a=1"), Some((true, 1, false, 0)));
    assert_eq!(parse(7, "b=2"), Some((false, 0, true, 2)));
    assert_eq!(parse(7, "a=9;b=0"), Some((true, 9, true, 0)));
}

#[test]
fn an_input_longer_than_the_limit_is_rejected() {
    assert_eq!(parse(3, "a=1"), Some((true, 1, false, 0)));
    assert_eq!(parse(2, "a=1"), None);
    assert_eq!(parse(6, "a=1;b=2"), None);
}

#[test]
fn what_is_not_a_record_is_rejected() {
    for s in ["", "a", "a=", "a=x", "a:1", "a=1;", ";a=1", "a=1x", "a=1;b=2x", "a=1;;b=2", "a=10"] {
        assert_eq!(parse(100, s), None, "{s:?}");
    }
}

#[test]
fn unknown_repeated_misordered_and_upper_case_keys_are_rejected() {
    for s in ["c=1", "c=1;a=2", "a=1;c=2", "a=1;a=2", "b=1;b=2", "b=2;a=1", "A=1", "a=1;B=2"] {
        assert_eq!(parse(100, s), None, "{s:?}");
    }
}
