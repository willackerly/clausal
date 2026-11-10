//! The code under test for plan node P2: a warehouse of storage bins, each holding units of one
//! product, and the loops that count, find, restock and take stock and fill orders.
//! Charon/Aeneas translate exactly this file to Lean (lean/Generated/Inventory.lean).
//! No derives; tests live in tests/ so Charon never sees them.

/// One storage bin: `qty` units of product `product`.
pub struct Bin {
    pub product: u32,
    pub qty: u64,
}

/// A customer order: `qty` units of product `product`.
pub struct Order {
    pub product: u32,
    pub qty: u64,
}

/// The bins in a fixed order, bin 0 first. Several bins may hold the same product.
pub struct Warehouse {
    pub bins: Vec<Bin>,
}

impl Warehouse {
    /// How many units of `product` the warehouse holds in all bins together,
    /// or `None` if that number does not fit in a u64.
    pub fn stock_of(&self, product: u32) -> Option<u64> {
        let mut sum: u64 = 0;
        let mut i = 0;
        while i < self.bins.len() {
            if self.bins[i].product == product {
                sum = match sum.checked_add(self.bins[i].qty) {
                    Some(s) => s,
                    None => return None,
                };
            }
            i += 1;
        }
        Some(sum)
    }

    /// The position of the first bin that holds `product` and at least `at_least` units
    /// of it, or `None` if no bin does.
    pub fn find_bin(&self, product: u32, at_least: u64) -> Option<usize> {
        let mut i = 0;
        while i < self.bins.len() {
            if self.bins[i].product == product && self.bins[i].qty >= at_least {
                return Some(i);
            }
            i += 1;
        }
        None
    }

    /// Add `amount` units to every bin of `product`. A bin that would go past
    /// u64::MAX is filled to u64::MAX. Returns how many bins were restocked.
    pub fn restock(&mut self, product: u32, amount: u64) -> usize {
        let mut count = 0;
        let mut i = 0;
        while i < self.bins.len() {
            if self.bins[i].product == product {
                self.bins[i].qty = self.bins[i].qty.saturating_add(amount);
                count += 1;
            }
            i += 1;
        }
        count
    }

    /// Take up to `want` units of `product`, from the first bins first: each bin of the
    /// product gives what it holds until `want` units have been taken. Returns how many
    /// units were taken, which is less than `want` only if the warehouse runs out.
    pub fn take(&mut self, product: u32, want: u64) -> u64 {
        let mut left = want;
        let mut i = 0;
        while i < self.bins.len() && left > 0 {
            if self.bins[i].product == product {
                let q = self.bins[i].qty;
                let t = if q < left { q } else { left };
                self.bins[i].qty = q - t;
                left -= t;
            }
            i += 1;
        }
        want - left
    }

    /// Whether the warehouse holds at least `qty` units of `product` in all.
    fn can_fill(&self, product: u32, qty: u64) -> bool {
        match self.stock_of(product) {
            Some(s) => s >= qty,
            None => true, // more than u64::MAX units: enough for any order
        }
    }

    /// Fill the orders in turn. An order is filled, by taking its units with `take`, when
    /// the warehouse holds enough of its product at that point; otherwise it is skipped
    /// and nothing is taken for it. Returns how many orders were filled.
    pub fn fill_orders(&mut self, orders: &[Order]) -> usize {
        let mut filled = 0;
        let mut i = 0;
        while i < orders.len() {
            let o = &orders[i];
            if self.can_fill(o.product, o.qty) {
                self.take(o.product, o.qty);
                filled += 1;
            }
            i += 1;
        }
        filled
    }

    /// How many different products the bins hold; a product held in several bins counts once.
    pub fn product_count(&self) -> usize {
        let mut count = 0;
        let mut i = 0;
        while i < self.bins.len() {
            let mut j = 0;
            while j < i && self.bins[j].product != self.bins[i].product {
                j += 1;
            }
            if j == i {
                count += 1;
            }
            i += 1;
        }
        count
    }

    /// The product held by more than half of the bins, or `None` if no product is.
    pub fn dominant_product(&self) -> Option<u32> {
        let n = self.bins.len();
        let mut candidate: u32 = 0;
        let mut votes: usize = 0;
        let mut i = 0;
        while i < n {
            let p = self.bins[i].product;
            if votes == 0 {
                candidate = p;
                votes = 1;
            } else if p == candidate {
                votes += 1;
            } else {
                votes -= 1;
            }
            i += 1;
        }
        let mut count: usize = 0;
        let mut j = 0;
        while j < n {
            if self.bins[j].product == candidate {
                count += 1;
            }
            j += 1;
        }
        if count > n - count {
            Some(candidate)
        } else {
            None
        }
    }
}
