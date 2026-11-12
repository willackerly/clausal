//! Ordinary example-based unit tests (the "tested" evidence kind, by example).
use sigintake::{intake, verify, Counter, Key, Message};

fn msg(payload: u64, counter: u64, tag: u64, hint: u64) -> Message {
    Message { payload, counter, tag, hint }
}

#[test]
fn the_toy_tag_is_three_hex_digits() {
    assert!(verify(&Key { id: 1 }, 1, 1, 0x111));
    assert!(!verify(&Key { id: 2 }, 1, 1, 0x111));
    assert!(verify(&Key { id: u64::MAX }, 0, u64::MAX, 0xf0f));
}

#[test]
fn a_verifying_message_with_a_higher_counter_is_accepted_and_sets_the_counter() {
    let (mut k, mut c) = (Key { id: 1 }, Counter { last: 0 });
    assert!(intake(&mut k, &mut c, msg(1, 1, 273, 9)));
    assert_eq!((k.id, c.last), (1, 1));
}

#[test]
fn a_message_that_does_not_verify_is_rejected_and_changes_nothing() {
    let (mut k, mut c) = (Key { id: 2 }, Counter { last: 0 });
    assert!(!intake(&mut k, &mut c, msg(1, 1, 273, 0)));
    assert_eq!((k.id, c.last), (2, 0));
}

#[test]
fn the_same_message_again_is_rejected() {
    let (mut k, mut c) = (Key { id: 1 }, Counter { last: 0 });
    assert!(intake(&mut k, &mut c, msg(1, 1, 273, 0)));
    assert!(!intake(&mut k, &mut c, msg(1, 1, 273, 0)));
    assert_eq!(c.last, 1);
}
