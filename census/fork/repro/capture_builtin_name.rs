// A user type whose last name component is the name of an Aeneas builtin type (`Slice`) and which holds that builtin.
// The generated Lean declares `structure names.Slice ... where bytes : Slice Std.U8`: inside the declaration `Slice`
// resolves to the structure being declared, and every function mentioning the type compiles only "using sorry".
pub mod names {
    pub struct Slice<'a> {
        pub bytes: &'a [u8],
    }
    impl<'a> Slice<'a> {
        pub fn len(&self) -> usize {
            self.bytes.len()
        }
    }
}
