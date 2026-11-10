//! Probes for census/PROFILE.md.
//!
//! Naming: `<item>_before` is the idiom as people write it, `<item>_after` the rewrite the profile
//! recommends, `<item>_ok` a form expected to work as written. `tests` checks that before and after agree.
//! Whether each function translates is NOT asserted here: census/probes/run.sh measures it.
#![allow(clippy::all)]
#![allow(dead_code)]

// ------------------------------------------------------------------ loops
pub mod loops {
    /// `for` over a range, no early exit.
    pub fn for_range_before(n: u32) -> u32 {
        let mut acc: u32 = 0;
        for i in 0..n {
            acc = acc.wrapping_add(i);
        }
        acc
    }
    pub fn for_range_after(n: u32) -> u32 {
        let mut acc: u32 = 0;
        let mut i: u32 = 0;
        while i < n {
            acc = acc.wrapping_add(i);
            i += 1;
        }
        acc
    }

    /// `for` over a slice, no early exit.
    pub fn for_slice_before(v: &[u32]) -> u32 {
        let mut acc: u32 = 0;
        for x in v {
            acc = acc.wrapping_add(*x);
        }
        acc
    }
    pub fn for_slice_after(v: &[u32]) -> u32 {
        let mut acc: u32 = 0;
        let mut i = 0;
        while i < v.len() {
            acc = acc.wrapping_add(v[i]);
            i += 1;
        }
        acc
    }

    /// `return` from inside a `for` loop.
    pub fn for_return_before(v: &[u32], x: u32) -> Option<usize> {
        for i in 0..v.len() {
            if v[i] == x {
                return Some(i);
            }
        }
        None
    }
    pub fn for_return_after(v: &[u32], x: u32) -> Option<usize> {
        let mut i = 0;
        while i < v.len() {
            if v[i] == x {
                return Some(i);
            }
            i += 1;
        }
        None
    }

    /// `?` inside a `for` loop.
    pub fn for_try_before(v: &[u32]) -> Option<u32> {
        let mut acc: u32 = 0;
        for x in v {
            acc = acc.checked_add(*x)?;
        }
        Some(acc)
    }
    pub fn for_try_after(v: &[u32]) -> Option<u32> {
        let mut acc: u32 = 0;
        let mut i = 0;
        while i < v.len() {
            acc = acc.checked_add(v[i])?;
            i += 1;
        }
        Some(acc)
    }

    /// `return` inside a `while` loop that sits inside an `if` branch (the loop is not the tail of the function body).
    pub fn while_return_in_branch_before(v: &[u32], skip: bool) -> u32 {
        let mut acc: u32 = 0;
        if !skip {
            let mut i = 0;
            while i < v.len() {
                if v[i] == 0 {
                    return 0;
                }
                acc = acc.wrapping_add(v[i]);
                i += 1;
            }
        }
        acc.wrapping_mul(2)
    }
    pub fn while_return_in_branch_after(v: &[u32], skip: bool) -> u32 {
        let mut acc: u32 = 0;
        let mut hit_zero = false;
        if !skip {
            let mut i = 0;
            while i < v.len() {
                if v[i] == 0 {
                    hit_zero = true;
                    break;
                }
                acc = acc.wrapping_add(v[i]);
                i += 1;
            }
        }
        if hit_zero {
            0
        } else {
            acc.wrapping_mul(2)
        }
    }

    /// `return` from the inner of two nested loops.
    pub fn nested_return_before(m: &[[u32; 4]], x: u32) -> bool {
        let mut i = 0;
        while i < m.len() {
            let mut j = 0;
            while j < 4 {
                if m[i][j] == x {
                    return true;
                }
                j += 1;
            }
            i += 1;
        }
        false
    }
    fn row_contains(row: &[u32; 4], x: u32) -> bool {
        let mut j = 0;
        while j < 4 {
            if row[j] == x {
                return true;
            }
            j += 1;
        }
        false
    }
    pub fn nested_return_after(m: &[[u32; 4]], x: u32) -> bool {
        let mut i = 0;
        while i < m.len() {
            if row_contains(&m[i], x) {
                return true;
            }
            i += 1;
        }
        false
    }

    /// Labelled `break` out of two loops.
    pub fn labelled_break_before(m: &[[u32; 4]], x: u32) -> u32 {
        let mut count: u32 = 0;
        let mut i = 0;
        'outer: while i < m.len() {
            let mut j = 0;
            while j < 4 {
                if m[i][j] == x {
                    break 'outer;
                }
                count += 1;
                j += 1;
            }
            i += 1;
        }
        count
    }
    pub fn labelled_break_after(m: &[[u32; 4]], x: u32) -> u32 {
        let mut count: u32 = 0;
        let mut i = 0;
        let mut done = false;
        while i < m.len() && !done {
            let mut j = 0;
            while j < 4 && !done {
                if m[i][j] == x {
                    done = true;
                } else {
                    count += 1;
                    j += 1;
                }
            }
            if !done {
                i += 1;
            }
        }
        count
    }

    /// `loop` with `break value`.
    pub fn loop_break_value_ok(mut n: u32) -> u32 {
        let mut steps = 0;
        loop {
            if n <= 1 {
                break steps;
            }
            n /= 2;
            steps += 1;
        }
    }
}

// ------------------------------------------------------------------ iterators and closures
pub mod iters {
    pub fn sum_before(v: &[u32]) -> u32 {
        v.iter().sum()
    }
    pub fn map_collect_before(v: &[u32]) -> Vec<u32> {
        v.iter().map(|x| x.wrapping_add(1)).collect()
    }
    pub fn map_collect_after(v: &[u32]) -> Vec<u32> {
        let mut out = Vec::new();
        let mut i = 0;
        while i < v.len() {
            out.push(v[i].wrapping_add(1));
            i += 1;
        }
        out
    }
    pub fn any_before(v: &[u32], x: u32) -> bool {
        v.iter().any(|y| *y == x)
    }
    pub fn any_after(v: &[u32], x: u32) -> bool {
        let mut i = 0;
        while i < v.len() {
            if v[i] == x {
                return true;
            }
            i += 1;
        }
        false
    }
    pub fn copied_max_before(v: &[u32]) -> Option<u32> {
        v.iter().copied().max()
    }
    pub fn copied_max_after(v: &[u32]) -> Option<u32> {
        if v.is_empty() {
            return None;
        }
        let mut best = v[0];
        let mut i = 1;
        while i < v.len() {
            if v[i] > best {
                best = v[i];
            }
            i += 1;
        }
        Some(best)
    }
    pub fn enumerate_before(v: &[u32]) -> u32 {
        let mut acc: u32 = 0;
        for (i, x) in v.iter().enumerate() {
            acc = acc.wrapping_add((i as u32).wrapping_mul(*x));
        }
        acc
    }
    pub fn filter_count_before(v: &[u32]) -> usize {
        v.iter().filter(|x| **x > 10).count()
    }
    pub fn filter_count_after(v: &[u32]) -> usize {
        let mut n = 0;
        let mut i = 0;
        while i < v.len() {
            if v[i] > 10 {
                n += 1;
            }
            i += 1;
        }
        n
    }
    /// A closure that is called directly, not handed to an iterator.
    pub fn local_closure_ok(a: u32, b: u32) -> u32 {
        let add = |x: u32, y: u32| x.wrapping_add(y);
        add(a, b)
    }
    /// A closure parameter (`impl Fn`).
    pub fn apply_ok(f: impl Fn(u32) -> u32, x: u32) -> u32 {
        f(x)
    }
    pub fn call_apply_ok(x: u32) -> u32 {
        apply_ok(|y| y.wrapping_mul(3), x)
    }
    /// `Option` combinators with closures.
    pub fn option_map_before(o: Option<u32>) -> Option<u32> {
        o.map(|x| x.wrapping_add(1))
    }
    pub fn option_map_after(o: Option<u32>) -> Option<u32> {
        match o {
            Some(x) => Some(x.wrapping_add(1)),
            None => None,
        }
    }
    pub fn unwrap_or_ok(o: Option<u32>) -> u32 {
        o.unwrap_or(7)
    }
    pub fn ok_or_before(o: Option<u32>) -> Result<u32, u8> {
        o.ok_or(1u8)
    }
    pub fn map_err_before(r: Result<u32, u8>) -> Result<u32, u32> {
        r.map_err(|e| e as u32)
    }
    pub fn map_err_after(r: Result<u32, u8>) -> Result<u32, u32> {
        match r {
            Ok(x) => Ok(x),
            Err(e) => Err(e as u32),
        }
    }

    pub struct Pair {
        pub key: u32,
        pub val: u32,
    }
    impl Pair {
        pub fn key_ref(&self) -> &u32 {
            &self.key
        }
    }
    /// A method passed by name where a function is expected.
    pub fn fn_item_before(p: Option<&Pair>) -> Option<&u32> {
        p.map(Pair::key_ref)
    }
    pub fn fn_item_closure(p: Option<&Pair>) -> Option<&u32> {
        p.map(|q| q.key_ref())
    }
    pub fn fn_item_after(p: Option<&Pair>) -> Option<&u32> {
        match p {
            Some(q) => Some(q.key_ref()),
            None => None,
        }
    }
}

// ------------------------------------------------------------------ strings
pub mod strings {
    pub fn starts_with_before(s: &str) -> bool {
        s.starts_with("ab")
    }
    pub fn starts_with_after(s: &str) -> bool {
        let b = s.as_bytes();
        b.len() >= 2 && b[0] == b'a' && b[1] == b'b'
    }
    pub fn find_char_before(s: &str) -> Option<usize> {
        s.find(':')
    }
    pub fn find_char_after(s: &str) -> Option<usize> {
        let b = s.as_bytes();
        let mut i = 0;
        while i < b.len() {
            if b[i] == b':' {
                return Some(i);
            }
            i += 1;
        }
        None
    }
    pub fn split_count_before(s: &str) -> usize {
        s.split(',').count()
    }
    pub fn split_count_after(s: &str) -> usize {
        let b = s.as_bytes();
        let mut n = 1;
        let mut i = 0;
        while i < b.len() {
            if b[i] == b',' {
                n += 1;
            }
            i += 1;
        }
        n
    }
    pub fn len_ok(s: &str) -> usize {
        s.len()
    }
    pub fn is_empty_ok(s: &str) -> bool {
        s.is_empty()
    }
    pub fn bytes_digit_ok(s: &str) -> Option<u32> {
        let b = s.as_bytes();
        let mut acc: u32 = 0;
        let mut i = 0;
        while i < b.len() {
            let c = b[i];
            if c < b'0' || c > b'9' {
                return None;
            }
            acc = acc.checked_mul(10)?.checked_add((c - b'0') as u32)?;
            i += 1;
        }
        Some(acc)
    }
    pub fn parse_before(s: &str) -> Option<u32> {
        s.parse::<u32>().ok()
    }
    pub fn chars_count_before(s: &str) -> usize {
        s.chars().count()
    }
    pub fn string_push_before(a: &str, b: &str) -> String {
        let mut s = String::new();
        s.push_str(a);
        s.push_str(b);
        s
    }
    pub fn format_before(x: u32) -> String {
        format!("x={}", x)
    }
    pub fn to_string_before(x: u32) -> String {
        x.to_string()
    }
    pub fn str_eq_ok(a: &str, b: &str) -> bool {
        a == b
    }
    pub struct Amount(pub u64);
    impl core::fmt::Display for Amount {
        fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
            write!(f, "{}", self.0)
        }
    }
    impl core::fmt::Debug for Amount {
        fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
            f.write_str("Amount")
        }
    }
}

// ------------------------------------------------------------------ pattern matching
pub mod matching {
    pub fn match_char_before(c: char) -> u8 {
        match c {
            ' ' | '\t' | '\n' => 0,
            '#' => 1,
            _ => 2,
        }
    }
    pub fn match_char_after(c: u8) -> u8 {
        match c {
            b' ' | b'\t' | b'\n' => 0,
            b'#' => 1,
            _ => 2,
        }
    }
    pub fn match_range_before(c: u8) -> bool {
        matches!(c, b'0'..=b'9' | b'a'..=b'f')
    }
    pub fn match_range_after(c: u8) -> bool {
        (c >= b'0' && c <= b'9') || (c >= b'a' && c <= b'f')
    }
    pub enum Op {
        Add,
        Sub,
        Neg,
    }
    pub fn match_enum_ok(op: &Op, a: i32, b: i32) -> Option<i32> {
        match op {
            Op::Add => a.checked_add(b),
            Op::Sub => a.checked_sub(b),
            Op::Neg => a.checked_neg(),
        }
    }
    pub fn match_tuple_ok(a: Option<u32>, b: Option<u32>) -> u32 {
        match (a, b) {
            (Some(x), Some(y)) => x.wrapping_add(y),
            (Some(x), None) | (None, Some(x)) => x,
            (None, None) => 0,
        }
    }
    pub fn match_slice_before(v: &[u32]) -> u32 {
        match v {
            [] => 0,
            [x] => *x,
            [x, .., y] => x.wrapping_add(*y),
        }
    }
    pub fn match_slice_after(v: &[u32]) -> u32 {
        if v.is_empty() {
            0
        } else if v.len() == 1 {
            v[0]
        } else {
            v[0].wrapping_add(v[v.len() - 1])
        }
    }
    /// `match` on a signed integer with negative literal patterns.
    pub fn match_neg_before(x: i8) -> u8 {
        match x {
            -6 | 1 => 8,
            -5 | 2 => 9,
            _ => 7,
        }
    }
    pub fn match_neg_after(x: i8) -> u8 {
        if x == -6 || x == 1 {
            8
        } else if x == -5 || x == 2 {
            9
        } else {
            7
        }
    }
    pub fn match_uint_ok(x: u8) -> u8 {
        match x {
            0 => 10,
            1 | 2 => 20,
            _ => 30,
        }
    }
    pub fn if_let_ok(o: Option<u32>) -> u32 {
        if let Some(x) = o {
            x
        } else {
            0
        }
    }
    pub fn let_else_ok(o: Option<u32>) -> u32 {
        let Some(x) = o else {
            return 0;
        };
        x.wrapping_add(1)
    }
}

// ------------------------------------------------------------------ names
/// A user type with the same last name as an Aeneas builtin (`Slice`) that holds that builtin.
pub mod names {
    pub struct Slice<'a> {
        pub bytes: &'a [u8],
    }
    impl<'a> Slice<'a> {
        pub fn len_before(&self) -> usize {
            self.bytes.len()
        }
    }
}
/// The same type under another name (in its own module: a sibling named `Slice` would still capture the name).
pub mod names_after {
    pub struct ByteSlice<'a> {
        pub bytes: &'a [u8],
    }
    impl<'a> ByteSlice<'a> {
        pub fn len_after(&self) -> usize {
            self.bytes.len()
        }
    }
}

/// A module at the crate root; `shadow` has a parameter with the same name.
pub mod input {
    pub struct Input {
        pub value: u32,
    }
    impl Input {
        pub fn get(&self) -> u32 {
            self.value
        }
    }
}
pub mod shadow {
    use crate::input;
    pub fn param_like_module_before(input: input::Input) -> u32 {
        input.get()
    }
    pub fn param_like_module_after(inp: input::Input) -> u32 {
        inp.get()
    }
}

// ------------------------------------------------------------------ traits, generics, trait objects
pub mod traits {
    pub trait Shape {
        fn area(&self) -> u32;
        fn double_area(&self) -> u32 {
            self.area().wrapping_mul(2)
        }
    }
    pub struct Square(pub u32);
    pub struct Rect(pub u32, pub u32);
    impl Shape for Square {
        fn area(&self) -> u32 {
            self.0.wrapping_mul(self.0)
        }
    }
    impl Shape for Rect {
        fn area(&self) -> u32 {
            self.0.wrapping_mul(self.1)
        }
    }
    pub fn dyn_before(s: &dyn Shape) -> u32 {
        s.area()
    }
    pub fn dyn_box_before(s: Box<dyn Shape>) -> u32 {
        s.area()
    }
    pub fn generic_after<S: Shape>(s: &S) -> u32 {
        s.area()
    }
    pub enum AnyShape {
        Square(Square),
        Rect(Rect),
    }
    pub fn enum_after(s: &AnyShape) -> u32 {
        match s {
            AnyShape::Square(q) => q.area(),
            AnyShape::Rect(r) => r.area(),
        }
    }
    pub fn default_method_ok(s: &Square) -> u32 {
        s.double_area()
    }
    pub fn generic_ord_ok<T: Ord + Copy>(a: T, b: T) -> T {
        if a < b {
            b
        } else {
            a
        }
    }
    pub fn generic_clone_ok<T: Clone>(a: &T) -> (T, T) {
        (a.clone(), a.clone())
    }
    pub trait Container {
        type Item;
        fn first(&self) -> Option<Self::Item>;
    }
    pub struct Nums(pub Vec<u32>);
    impl Container for Nums {
        type Item = u32;
        fn first(&self) -> Option<u32> {
            if self.0.is_empty() {
                None
            } else {
                Some(self.0[0])
            }
        }
    }
    pub fn assoc_type_ok<C: Container>(c: &C) -> Option<C::Item> {
        c.first()
    }
    pub fn from_into_ok(x: u8) -> u32 {
        u32::from(x)
    }
    #[derive(Clone, Copy, PartialEq, Eq, Debug, Default, PartialOrd, Ord, Hash)]
    pub struct Cents(pub u64);
    pub fn derived_eq_ok(a: Cents, b: Cents) -> bool {
        a == b
    }
    pub fn derived_ord_ok(a: Cents, b: Cents) -> bool {
        a < b
    }
    pub fn derived_default_ok() -> Cents {
        Cents::default()
    }
    /// A closure parameter whose argument type carries a higher-ranked lifetime.
    pub struct Reader<'a> {
        pub data: &'a [u8],
        pub pos: usize,
    }
    pub fn hrtb_before<'a, R>(data: &'a [u8], f: impl for<'b> FnOnce(&'b mut Reader<'a>) -> R) -> R {
        let mut r = Reader { data, pos: 0 };
        f(&mut r)
    }
    pub fn hrtb_after<'a>(data: &'a [u8]) -> Reader<'a> {
        Reader { data, pos: 0 }
    }
    pub fn reader_next_ok(r: &mut Reader<'_>) -> Option<u8> {
        if r.pos < r.data.len() {
            let b = r.data[r.pos];
            r.pos += 1;
            Some(b)
        } else {
            None
        }
    }
}

// ------------------------------------------------------------------ memory, unsafe, interior mutability
pub mod memory {
    use std::cell::{Cell, RefCell};
    use std::collections::{BTreeMap, HashMap};
    use std::rc::Rc;

    pub fn raw_ptr_before(v: &[u32]) -> u32 {
        if v.is_empty() {
            return 0;
        }
        unsafe { *v.as_ptr() }
    }
    pub fn raw_ptr_after(v: &[u32]) -> u32 {
        if v.is_empty() {
            return 0;
        }
        v[0]
    }
    pub fn get_unchecked_before(v: &[u32], i: usize) -> u32 {
        if i < v.len() {
            unsafe { *v.get_unchecked(i) }
        } else {
            0
        }
    }
    pub fn get_unchecked_after(v: &[u32], i: usize) -> u32 {
        if i < v.len() {
            v[i]
        } else {
            0
        }
    }
    pub fn cell_before(c: &Cell<u32>) -> u32 {
        let x = c.get();
        c.set(x.wrapping_add(1));
        x
    }
    pub fn cell_after(c: &mut u32) -> u32 {
        let x = *c;
        *c = x.wrapping_add(1);
        x
    }
    pub fn refcell_before(c: &RefCell<Vec<u32>>) -> usize {
        c.borrow_mut().push(1);
        c.borrow().len()
    }
    pub fn refcell_after(c: &mut Vec<u32>) -> usize {
        c.push(1);
        c.len()
    }
    pub fn rc_before(x: &Rc<u32>) -> u32 {
        let y = Rc::clone(x);
        *y
    }
    pub fn box_ok(x: Box<u32>) -> u32 {
        *x
    }
    pub fn box_new_ok(x: u32) -> Box<u32> {
        Box::new(x)
    }
    pub fn mut_ref_ok(a: &mut u32, b: &mut u32) {
        let t = *a;
        *a = *b;
        *b = t;
    }
    pub fn return_mut_ref_ok(v: &mut [u32], i: usize) -> Option<&mut u32> {
        if i < v.len() {
            Some(&mut v[i])
        } else {
            None
        }
    }
    pub fn mem_swap_ok(a: &mut u32, b: &mut u32) {
        core::mem::swap(a, b)
    }
    pub fn mem_replace_ok(a: &mut u32) -> u32 {
        core::mem::replace(a, 0)
    }
    pub fn hashmap_before(m: &HashMap<u32, u32>, k: u32) -> Option<u32> {
        m.get(&k).copied()
    }
    pub fn btreemap_before(m: &mut BTreeMap<u32, u32>, k: u32, v: u32) -> Option<u32> {
        m.insert(k, v)
    }
    /// Association list in place of a map.
    pub fn assoc_get_after(m: &[(u32, u32)], k: u32) -> Option<u32> {
        let mut i = 0;
        while i < m.len() {
            if m[i].0 == k {
                return Some(m[i].1);
            }
            i += 1;
        }
        None
    }
}

// ------------------------------------------------------------------ collections
pub mod collections {
    pub fn vec_push_ok(v: &mut Vec<u32>, x: u32) {
        v.push(x)
    }
    pub fn vec_pop_before(v: &mut Vec<u32>) -> Option<u32> {
        v.pop()
    }
    pub fn vec_new_len_ok() -> usize {
        let v: Vec<u32> = Vec::new();
        v.len()
    }
    pub fn vec_with_capacity_ok(n: usize) -> Vec<u32> {
        Vec::with_capacity(n)
    }
    pub fn vec_macro_before() -> Vec<u32> {
        vec![1, 2, 3]
    }
    pub fn vec_macro_after() -> Vec<u32> {
        let mut v = Vec::new();
        v.push(1);
        v.push(2);
        v.push(3);
        v
    }
    pub fn vec_index_mut_ok(v: &mut Vec<u32>, i: usize, x: u32) {
        v[i] = x
    }
    pub fn vec_get_ok(v: &Vec<u32>, i: usize) -> Option<&u32> {
        v.get(i)
    }
    pub fn vec_clone_ok(v: &Vec<u32>) -> Vec<u32> {
        v.clone()
    }
    pub fn vec_insert_before(v: &mut Vec<u32>, x: u32) {
        v.insert(0, x)
    }
    pub fn vec_extend_before(v: &mut Vec<u32>, w: &[u32]) {
        v.extend_from_slice(w)
    }
    pub fn vec_is_empty_ok(v: &Vec<u32>) -> bool {
        v.is_empty()
    }
    pub fn vec_truncate_before(v: &mut Vec<u32>, n: usize) {
        v.truncate(n)
    }
    pub fn vec_contains_before(v: &Vec<u32>, x: u32) -> bool {
        v.contains(&x)
    }
    pub fn vec_sort_before(v: &mut Vec<u32>) {
        v.sort()
    }
    pub fn slice_range_ok(v: &[u32], a: usize, b: usize) -> &[u32] {
        &v[a..b]
    }
    pub fn slice_first_before(v: &[u32]) -> Option<&u32> {
        v.first()
    }
    pub fn slice_last_before(v: &[u32]) -> Option<&u32> {
        v.last()
    }
    pub fn slice_split_at_before(v: &[u32], i: usize) -> (&[u32], &[u32]) {
        v.split_at(i)
    }
    pub fn slice_swap_before(v: &mut [u32], i: usize, j: usize) {
        v.swap(i, j)
    }
    pub fn slice_copy_from_before(a: &mut [u32], b: &[u32]) {
        a.copy_from_slice(b)
    }
    pub fn array_ok(a: [u32; 4]) -> u32 {
        a[0].wrapping_add(a[3])
    }
    pub fn array_update_ok(mut a: [u32; 4], i: usize) -> [u32; 4] {
        a[i] = 9;
        a
    }
    pub fn array_repeat_ok() -> [u8; 16] {
        [0u8; 16]
    }
    pub fn tuple_ok(p: (u32, bool)) -> u32 {
        if p.1 {
            p.0
        } else {
            0
        }
    }
    pub fn option_take_ok(o: &mut Option<u32>) -> Option<u32> {
        o.take()
    }
    pub fn option_is_some_ok(o: &Option<u32>) -> bool {
        o.is_some()
    }
    pub fn option_unwrap_ok(o: Option<u32>) -> u32 {
        o.unwrap()
    }
    pub fn option_expect_before(o: Option<u32>) -> u32 {
        o.expect("value")
    }
    pub fn result_is_ok_before(r: &Result<u32, u8>) -> bool {
        r.is_ok()
    }
    pub fn result_unwrap_before(r: Result<u32, u8>) -> u32 {
        r.unwrap()
    }
}

// ------------------------------------------------------------------ numbers
pub mod numbers {
    pub fn checked_ok(a: u64, b: u64) -> Option<u64> {
        a.checked_add(b)?.checked_mul(2)
    }
    pub fn wrapping_ok(a: u32, b: u32) -> u32 {
        a.wrapping_sub(b).wrapping_mul(3)
    }
    pub fn saturating_ok(a: u32, b: u32) -> u32 {
        a.saturating_add(b)
    }
    pub fn overflowing_ok(a: u32, b: u32) -> (u32, bool) {
        a.overflowing_add(b)
    }
    pub fn plain_arith_ok(a: u32, b: u32) -> u32 {
        (a / 2 + b / 2) % 7
    }
    pub fn signed_ok(a: i64, b: i64) -> i64 {
        (a / 3 - b / 3).abs()
    }
    pub fn bits_ok(a: u32, s: u32) -> u32 {
        ((a << (s % 32)) | (a >> 3)) & 0xff ^ 1
    }
    pub fn casts_ok(a: u8, b: i32) -> u64 {
        (a as u64) + (b as u32 as u64)
    }
    pub fn u128_ok(a: u64, b: u64) -> u128 {
        (a as u128) * (b as u128)
    }
    pub fn pow_before(a: u32) -> Option<u32> {
        a.checked_pow(3)
    }
    pub fn leading_zeros_before(a: u32) -> u32 {
        a.leading_zeros()
    }
    pub fn rotate_ok(a: u32) -> u32 {
        a.rotate_left(5)
    }
    pub fn to_bytes_ok(a: u32) -> [u8; 4] {
        a.to_le_bytes()
    }
    pub fn from_bytes_ok(b: [u8; 4]) -> u32 {
        u32::from_le_bytes(b)
    }
    pub fn min_max_ok(a: u32, b: u32) -> u32 {
        core::cmp::max(a, b) - core::cmp::min(a, b)
    }
    pub fn cmp_ok(a: u32, b: u32) -> core::cmp::Ordering {
        a.cmp(&b)
    }
    pub fn try_from_before(a: u64) -> Option<u32> {
        u32::try_from(a).ok()
    }
    pub fn try_from_after(a: u64) -> Option<u32> {
        if a <= u32::MAX as u64 {
            Some(a as u32)
        } else {
            None
        }
    }
    pub fn float_add_before(a: f64, b: f64) -> f64 {
        a + b
    }
    pub fn float_cmp_before(a: f64, b: f64) -> bool {
        a < b
    }
    pub fn float_cast_before(a: u32) -> f64 {
        a as f64
    }
    /// Fixed point (hundredths) in place of floats.
    pub fn fixed_add_after(a_cents: u64, b_cents: u64) -> Option<u64> {
        a_cents.checked_add(b_cents)
    }
    pub const LIMIT: u32 = 1_000;
    pub static TABLE: [u8; 4] = [1, 2, 4, 8];
    pub fn const_ok(a: u32) -> bool {
        a < LIMIT
    }
    pub fn static_table_before(i: usize) -> u8 {
        TABLE[i % 4]
    }
    pub fn const_table_after(i: usize) -> u8 {
        const T: [u8; 4] = [1, 2, 4, 8];
        T[i % 4]
    }
}

// ------------------------------------------------------------------ panics
pub mod panics {
    pub fn index_panic_ok(v: &[u32], i: usize) -> u32 {
        v[i]
    }
    pub fn explicit_panic_ok(x: u32) -> u32 {
        if x == 0 {
            panic!("zero");
        }
        x
    }
    pub fn assert_ok(x: u32) -> u32 {
        assert!(x > 0);
        x - 1
    }
    pub fn assert_eq_before(x: u32, y: u32) -> u32 {
        assert_eq!(x, y);
        x
    }
    pub fn assert_eq_after(x: u32, y: u32) -> u32 {
        assert!(x == y);
        x
    }
    pub fn debug_assert_ok(x: u32) -> u32 {
        debug_assert!(x > 0);
        x
    }
    pub fn unreachable_ok(x: bool) -> u32 {
        if x {
            1
        } else if !x {
            0
        } else {
            unreachable!()
        }
    }
    pub fn overflow_panic_ok(a: u32, b: u32) -> u32 {
        a + b
    }
    pub fn div_zero_ok(a: u32, b: u32) -> u32 {
        a / b
    }
}

// ------------------------------------------------------------------ structure
pub mod structure {
    pub struct Account {
        pub id: u32,
        pub balance: u64,
    }
    #[derive(Debug, PartialEq, Eq)]
    pub enum Error {
        Insufficient,
        Overflow,
    }
    impl Account {
        pub fn new_ok(id: u32) -> Self {
            Account { id, balance: 0 }
        }
        pub fn deposit_ok(&mut self, amt: u64) -> Result<(), Error> {
            self.balance = self.balance.checked_add(amt).ok_or(Error::Overflow)?;
            Ok(())
        }
        pub fn deposit_match_ok(&mut self, amt: u64) -> Result<(), Error> {
            match self.balance.checked_add(amt) {
                Some(b) => {
                    self.balance = b;
                    Ok(())
                }
                None => Err(Error::Overflow),
            }
        }
        pub fn withdraw_ok(&mut self, amt: u64) -> Result<(), Error> {
            if self.balance < amt {
                return Err(Error::Insufficient);
            }
            self.balance -= amt;
            Ok(())
        }
    }
    pub fn recursion_ok(n: u32) -> u32 {
        if n == 0 {
            0
        } else {
            1 + recursion_ok(n - 1)
        }
    }
    pub struct Wrapper<T> {
        pub inner: T,
    }
    impl<T: Copy> Wrapper<T> {
        pub fn get_ok(&self) -> T {
            self.inner
        }
    }
    pub fn nested_fn_ok(x: u32) -> u32 {
        fn helper(y: u32) -> u32 {
            y.wrapping_add(1)
        }
        helper(helper(x))
    }
    pub fn shadow_ok(x: u32) -> u32 {
        let x = x.wrapping_add(1);
        let x = x.wrapping_mul(2);
        x
    }
    pub fn struct_update_ok(a: Account) -> Account {
        Account { balance: 0, ..a }
    }
    pub fn early_return_ok(a: u32) -> Option<u32> {
        if a == 0 {
            return None;
        }
        Some(100 / a)
    }
    pub fn question_convert_before(a: &str) -> Result<u32, Box<dyn std::error::Error>> {
        let x: u32 = a.parse()?;
        Ok(x)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn before_and_after_agree() {
        let v = [3u32, 0, 12, 40, 7];
        let m = [[1u32, 2, 3, 4], [5, 6, 7, 8]];
        for n in 0..9 {
            assert_eq!(loops::for_range_before(n), loops::for_range_after(n));
        }
        assert_eq!(loops::for_slice_before(&v), loops::for_slice_after(&v));
        for x in [3, 40, 99] {
            assert_eq!(loops::for_return_before(&v, x), loops::for_return_after(&v, x));
            assert_eq!(iters::any_before(&v, x), iters::any_after(&v, x));
        }
        assert_eq!(loops::for_try_before(&v), loops::for_try_after(&v));
        assert_eq!(loops::for_try_before(&[u32::MAX, 1]), loops::for_try_after(&[u32::MAX, 1]));
        for skip in [true, false] {
            assert_eq!(loops::while_return_in_branch_before(&v, skip), loops::while_return_in_branch_after(&v, skip));
            assert_eq!(loops::while_return_in_branch_before(&[1, 2], skip), loops::while_return_in_branch_after(&[1, 2], skip));
        }
        for x in [1, 6, 8, 9] {
            assert_eq!(loops::nested_return_before(&m, x), loops::nested_return_after(&m, x));
            assert_eq!(loops::labelled_break_before(&m, x), loops::labelled_break_after(&m, x));
        }
        assert_eq!(iters::map_collect_before(&v), iters::map_collect_after(&v));
        assert_eq!(iters::copied_max_before(&v), iters::copied_max_after(&v));
        assert_eq!(iters::copied_max_before(&[]), iters::copied_max_after(&[]));
        assert_eq!(iters::filter_count_before(&v), iters::filter_count_after(&v));
        for o in [None, Some(4)] {
            assert_eq!(iters::option_map_before(o), iters::option_map_after(o));
        }
        for r in [Ok(1), Err(2u8)] {
            assert_eq!(iters::map_err_before(r), iters::map_err_after(r));
        }
        let p = iters::Pair { key: 5, val: 6 };
        assert_eq!(iters::fn_item_before(Some(&p)), iters::fn_item_after(Some(&p)));
        assert_eq!(iters::fn_item_before(None), iters::fn_item_after(None));
        for s in ["", "a", "ab", "abc", "x:y", "a,b,,c", ":"] {
            assert_eq!(strings::starts_with_before(s), strings::starts_with_after(s));
            assert_eq!(strings::find_char_before(s), strings::find_char_after(s));
            assert_eq!(strings::split_count_before(s), strings::split_count_after(s));
        }
        for c in [b' ', b'\t', b'\n', b'#', b'x', b'0', b'9', b'a', b'f', b'g'] {
            assert_eq!(matching::match_char_before(c as char), matching::match_char_after(c));
            assert_eq!(matching::match_range_before(c), matching::match_range_after(c));
        }
        for x in [-7i8, -6, -5, 0, 1, 2, 3] {
            assert_eq!(matching::match_neg_before(x), matching::match_neg_after(x));
        }
        assert_eq!(
            shadow::param_like_module_before(input::Input { value: 3 }),
            shadow::param_like_module_after(input::Input { value: 3 })
        );
        for s in [&[][..], &[5][..], &[5, 6][..], &[5, 6, 7][..]] {
            assert_eq!(matching::match_slice_before(s), matching::match_slice_after(s));
        }
        assert_eq!(names::Slice { bytes: &[1, 2] }.len_before(), names_after::ByteSlice { bytes: &[1, 2] }.len_after());
        let sq = traits::Square(3);
        assert_eq!(traits::dyn_before(&sq), traits::generic_after(&sq));
        assert_eq!(traits::dyn_before(&sq), traits::enum_after(&traits::AnyShape::Square(traits::Square(3))));
        assert_eq!(memory::raw_ptr_before(&v), memory::raw_ptr_after(&v));
        for i in [0, 4, 5] {
            assert_eq!(memory::get_unchecked_before(&v, i), memory::get_unchecked_after(&v, i));
        }
        let c = std::cell::Cell::new(5);
        let mut d = 5;
        assert_eq!(memory::cell_before(&c), memory::cell_after(&mut d));
        assert_eq!(c.get(), d);
        assert_eq!(collections::vec_macro_before(), collections::vec_macro_after());
        for a in [0u64, 7, u32::MAX as u64, u32::MAX as u64 + 1] {
            assert_eq!(numbers::try_from_before(a), numbers::try_from_after(a));
        }
        for i in 0..6 {
            assert_eq!(numbers::static_table_before(i), numbers::const_table_after(i));
        }
        assert_eq!(panics::assert_eq_before(2, 2), panics::assert_eq_after(2, 2));
    }
}
