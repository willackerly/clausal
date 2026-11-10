//! Ordinary unit tests of the inventory crate (outside src/, so Charon never sees them).
use inventory::{Bin, Order, Warehouse};

fn wh(bins: &[(u32, u64)]) -> Warehouse {
    Warehouse { bins: bins.iter().map(|&(product, qty)| Bin { product, qty }).collect() }
}

fn contents(w: &Warehouse) -> Vec<(u32, u64)> {
    w.bins.iter().map(|b| (b.product, b.qty)).collect()
}

fn orders(os: &[(u32, u64)]) -> Vec<Order> {
    os.iter().map(|&(product, qty)| Order { product, qty }).collect()
}

#[test]
fn stock_of_sums_the_bins_of_one_product() {
    let w = wh(&[(7, 10), (3, 5), (7, 4)]);
    assert_eq!(w.stock_of(7), Some(14));
    assert_eq!(w.stock_of(3), Some(5));
    assert_eq!(w.stock_of(9), Some(0));
    assert_eq!(wh(&[]).stock_of(1), Some(0));
}

#[test]
fn stock_of_overflow_is_none() {
    let w = wh(&[(1, u64::MAX), (2, 1), (1, 1)]);
    assert_eq!(w.stock_of(1), None);
    assert_eq!(w.stock_of(2), Some(1));
    assert_eq!(wh(&[(1, u64::MAX), (1, 0)]).stock_of(1), Some(u64::MAX));
}

#[test]
fn find_bin_returns_the_first_match() {
    let w = wh(&[(7, 2), (3, 5), (7, 6), (7, 9)]);
    assert_eq!(w.find_bin(7, 5), Some(2));
    assert_eq!(w.find_bin(7, 0), Some(0));
    assert_eq!(w.find_bin(3, 5), Some(1));
    assert_eq!(w.find_bin(3, 6), None);
    assert_eq!(w.find_bin(8, 0), None);
}

#[test]
fn restock_adds_to_every_bin_of_the_product() {
    let mut w = wh(&[(7, 2), (3, 5), (7, u64::MAX - 1)]);
    assert_eq!(w.restock(7, 3), 2);
    assert_eq!(contents(&w), vec![(7, 5), (3, 5), (7, u64::MAX)]);
    assert_eq!(w.restock(9, 3), 0);
    assert_eq!(contents(&w), vec![(7, 5), (3, 5), (7, u64::MAX)]);
}

#[test]
fn take_empties_earlier_bins_first() {
    let mut w = wh(&[(7, 4), (3, 5), (7, 6), (7, 1)]);
    assert_eq!(w.take(7, 7), 7);
    assert_eq!(contents(&w), vec![(7, 0), (3, 5), (7, 3), (7, 1)]);
    assert_eq!(w.take(7, 10), 4);
    assert_eq!(contents(&w), vec![(7, 0), (3, 5), (7, 0), (7, 0)]);
    assert_eq!(w.take(3, 0), 0);
    assert_eq!(contents(&w), vec![(7, 0), (3, 5), (7, 0), (7, 0)]);
}

#[test]
fn fill_orders_skips_what_cannot_be_filled() {
    let mut w = wh(&[(7, 4), (3, 5), (7, 6)]);
    let os = orders(&[(7, 8), (3, 6), (7, 3), (3, 5)]);
    assert_eq!(w.fill_orders(&os), 2);
    assert_eq!(contents(&w), vec![(7, 0), (3, 0), (7, 2)]);
    assert_eq!(w.fill_orders(&[]), 0);
}

#[test]
fn fill_orders_with_overflowing_stock() {
    let mut w = wh(&[(1, u64::MAX), (1, 5)]);
    assert_eq!(w.fill_orders(&orders(&[(1, u64::MAX)])), 1);
    assert_eq!(contents(&w), vec![(1, 0), (1, 5)]);
}

#[test]
fn product_count_counts_each_product_once() {
    assert_eq!(wh(&[]).product_count(), 0);
    assert_eq!(wh(&[(7, 1)]).product_count(), 1);
    assert_eq!(wh(&[(7, 1), (3, 0), (7, 2), (9, 1), (3, 3)]).product_count(), 3);
}

#[test]
fn dominant_product_needs_more_than_half() {
    assert_eq!(wh(&[]).dominant_product(), None);
    assert_eq!(wh(&[(7, 1)]).dominant_product(), Some(7));
    assert_eq!(wh(&[(7, 1), (3, 1)]).dominant_product(), None);
    assert_eq!(wh(&[(3, 1), (7, 1), (7, 1)]).dominant_product(), Some(7));
    assert_eq!(wh(&[(7, 1), (3, 1), (3, 1), (7, 1), (7, 1)]).dominant_product(), Some(7));
    assert_eq!(wh(&[(7, 1), (3, 1), (9, 1), (7, 1)]).dominant_product(), None);
    assert_eq!(wh(&[(0, 1), (0, 2)]).dominant_product(), Some(0));
}
